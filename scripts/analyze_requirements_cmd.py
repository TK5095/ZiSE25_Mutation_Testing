
from textwrap import dedent
from west.commands import WestCommand
import os
import shutil
from argparse import Namespace
import build_reqman_configuration as req_config

from typing import List, Optional, Dict


HERE = os.path.abspath(os.path.dirname(__file__))

DESCRIPTION="""
...
"""

class AnalyzeRequirements(WestCommand):
    def __init__(self):
        super().__init__(
            'analyze-requirements',
            'Run ECLAIR analysis for requirements coverage',
            dedent(DESCRIPTION),
        )

    def do_add_parser(self, parser_adder):
        parser = parser_adder.add_parser(self.name,
                                         help=self.help,
                                         description=self.description)

        parser.add_argument('board', type=str, help='Board name to build for (e.g., native_posix)')
        parser.add_argument('--tests', '-t', action='store_true', help='include test files in analysis')
        parser.add_argument('--config', '-c', action='store_true', help='filter requirements based on current Kconfig')

        return parser

    def do_run(self, args, unknown):
        if not shutil.which('west'):
            self.die('west not found in PATH')

        if not shutil.which('eclair'):
            self.die('eclair not found in PATH, make sure ECLAIR is installed and in PATH')

        if not self.manifest:
            self.die('No west manifest')

        if not self.manifest.repo_abspath:
            self.die('No west manifest repo_abspath')

        project_dir: str = self.manifest.repo_abspath
        os.makedirs(self._out_dir(), exist_ok=True)

        self._build_reqman_config(args)
        self._clean_build(args)
        self._run_eclair_analysis(args)

        self.inf('Removing twister output')
        for item in os.listdir(project_dir):
            if item.startswith('twister-out'):
                path = os.path.join(project_dir, item)
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)

        self._create_eclair_db()

    def _eclair_dir(self) -> str:
        return os.path.abspath(os.path.join(HERE, '../ECLAIR'))

    def _out_dir(self) -> str:
        return os.path.join(self._eclair_dir(), 'requirements_analysis_out')

    def _build_log(self) -> str:
        return os.path.join(self._out_dir(), 'build.log')

    def _eclair_out_dir(self) -> str:
        return self._out_dir()

    def _eclair_data_dir(self) -> str:
        return os.path.join(self._eclair_out_dir(), 'data')

    def _eclair_diagnostics_output(self) -> str:
        return os.path.join(self._eclair_out_dir(), 'DIAGNOSTICS.txt')

    def _eclair_db(self) -> str:
        return os.path.join(self._eclair_out_dir(), 'PROJECT.ecd')

    def _read_kconfig(self, build_dir: str) -> Dict[str, bool]:
        """Read Kconfig values from the build directory."""
        config_file = os.path.join(build_dir, 'zephyr', '.config')
        config = {}
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('CONFIG_') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key] = value == 'y'
        
        return config

    def _get_enabled_components(self, args: Namespace) -> Optional[List[str]]:
        """Get list of enabled components based on Kconfig."""
        if not args.config:
            return None

        # Get build directory
        if not self.manifest or not self.manifest.repo_abspath:
            self.die('No west manifest repo_abspath')
        build_dir = os.path.join(self.manifest.repo_abspath, 'build')

        # Config-only build
        if not os.path.exists(build_dir):
            self.inf('No build directory found, running configuration...')
            cmd = ["west", "build", "-b", args.board, "--cmake-only"]
            self.run_subprocess(cmd).check_returncode()

        # Read Kconfig values
        config = self._read_kconfig(build_dir)

        enabled_components = []
        if config.get('CONFIG_APP_DISPLAY', False):
            enabled_components.append('APP_DISPLAY')
        if config.get('CONFIG_APP_BUZZER', False):
            enabled_components.append('APP_BUZZER')
        if config.get('CONFIG_APP_LEDS', False):
            enabled_components.append('APP_LEDS')
            
        self.inf(f'Enabled components from Kconfig: {enabled_components}')
        return enabled_components

    def _build_reqman_config(self, args: Namespace) -> None:
        # Get enabled components Kconfig
        enabled_components = self._get_enabled_components(args)
        
        output = req_config.build_config(
            os.path.abspath(os.path.join(HERE, '../temp_alert.sdoc')),
            [
                ('SRS', 'SRS-.*'),
            ],
            enabled_components
        )
        config_path = os.path.join(self._eclair_dir(), 'temp_alert.sdoc.ecl')
        with open(config_path, 'w') as f:
            f.write(output)

    def _clean_build(self, args: Namespace) -> None:
        if not args.tests:
            cmd = ["west", "build", "-t", "pristine", "-b", args.board]
            self.inf(f'Cleaning build for board {args.board}')
            if self.verbosity >= 4:
                self.inf(f'  Command: {" ".join(cmd)}')
            self.run_subprocess(cmd).check_returncode()

    def _build_command(self, args: Namespace) -> List[str]:
        if args.tests:
            if args.board != "native_sim":
                raise ValueError("Invalid board for test analysis")
            return ["west", "twister", "-T", "tests", "--platform", args.board]
        else:
            return ["west", "build", "-b", args.board]

    def _run_eclair_analysis(self, args: Namespace) -> None:
        eclair_data_dir = self._eclair_data_dir()
        eclair_diagnostics = self._eclair_diagnostics_output()

        if os.path.exists(eclair_data_dir):
            shutil.rmtree(eclair_data_dir)

        if os.path.exists(eclair_diagnostics):
            os.remove(eclair_diagnostics)

        os.makedirs(eclair_data_dir, exist_ok=True)

        ecl = os.path.join(self._eclair_dir(), 'analysis_REQMAN.ecl')
        cmd = ["eclair_env",
               "-verbose",
               f"-eval_file={ecl}",
               "-enable=B.REPORT.ECB",
               f"-config=B.REPORT.ECB,output=join_paths(\"{eclair_data_dir}\",\"FRAME.@FRAME@.ecb\")",
               f"-config=B.REPORT.ECB,tags=show",
               "--"] + self._build_command(args)

        env = os.environ.copy()
        env['ECLAIR_DATA_DIR'] = eclair_data_dir
        env['ECLAIR_DIAGNOSTICS_OUTPUT'] = self._eclair_diagnostics_output()

        self.inf(f'Running eclair_env')
        build_log = self._build_log()
        if self.verbosity >= 4:
            self.inf(f'  Command: {" ".join(cmd)}')
            self.inf(f'  ECLAIR_DATA_DIR={env["ECLAIR_DATA_DIR"]}')
            self.inf(f'  ECLAIR_DIAGNOSTICS_OUTPUT={env["ECLAIR_DIAGNOSTICS_OUTPUT"]}')
            self.inf(f'  TWISTER_LOG={build_log}')
        self.inf(f'Logging to: {eclair_diagnostics}')
        with open(build_log, 'w') as log_file:
            self.run_subprocess(
                cmd,
                env=env,
                stdout=log_file,
                stderr=log_file
            ).check_returncode()

    def _create_eclair_db(self) -> None:
        eclair_data_dir = self._eclair_data_dir()
        db = self._eclair_db()

        if os.path.exists(db):
            self.wrn(f'Removing existing ECLAIR database {db}')
            os.remove(db)

        ecb_files = [os.path.join(eclair_data_dir, f) for f in os.listdir(eclair_data_dir) if f.startswith('FRAME.') and f.endswith('.ecb')]
        if not ecb_files:
            self.die('No FRAME.*.ecb files found in ECLAIR data directory')

        cmd = ["eclair_report", f"-create_db={db}"] + ecb_files + ["-load"]

        self.inf(f'Creating ECLAIR database')
        self.run_subprocess(cmd).check_returncode()
        self.inf(f'ECLAIR database created at {db}')
