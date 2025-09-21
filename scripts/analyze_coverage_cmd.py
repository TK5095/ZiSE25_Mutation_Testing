
from textwrap import dedent
from pyparsing import Dict
from west.commands import WestCommand
import os
import shutil
import subprocess
from argparse import Namespace
import re

from typing import Dict, Generator, List


HERE = os.path.abspath(os.path.dirname(__file__))

DESCRIPTION="""
This command automates the process of running twister to collect gcov files and
then runs ECLAIR analysis on them.
"""

class AnalyzeCoverage(WestCommand):
    def __init__(self):
        super().__init__(
            'analyze-coverage',
            'Run ECLAIR analysis on test coverage data',
            dedent(DESCRIPTION),
        )

    def do_add_parser(self, parser_adder):
        parser = parser_adder.add_parser(self.name,
                                         help=self.help,
                                         description=self.description)

        parser.add_argument('--no-run', action='store_true', help='do not run twister')
        parser.add_argument('-k', '--keep-gcov-files', action='store_true', help='keep gcov files after analysis')
        parser.add_argument('--include-zephyr', action='store_true', help='include Zephyr gcov files')

        return parser

    def do_run(self, args, unknown):
        if not shutil.which('west'):
            self.die('west not found in PATH')

        if not shutil.which('gcovr'):
            self.die('gcovr not found in PATH')

        if not shutil.which('eclair'):
            self.die('eclair not found in PATH, make sure ECLAIR is installed and in PATH')

        if not self.manifest:
            self.die('No west manifest')

        if not self.manifest.repo_abspath:
            self.die('No west manifest repo_abspath')

        project_dir: str = self.manifest.repo_abspath
        os.makedirs(self._out_dir(), exist_ok=True)

        if not args.no_run:
            self._run_twister(project_dir)

        all_gcov_files = list(self._gcov_files(project_dir))
        gcov_files = self._selected_gcov_files(args, project_dir, all_gcov_files)
        if not gcov_files:
            self.die('No gcov files found')
        self.inf(f'Found {len(gcov_files)} gcov files')
        if self.verbosity >= 4:
            for f in gcov_files:
                self.inf(f'  {f}')

        self._run_eclair_analysis(gcov_files)

        if not args.keep_gcov_files:
            self.inf('Removing gcov files')
            for gcov_file in all_gcov_files:
                os.remove(gcov_file)
            for item in os.listdir(project_dir):
                if item.startswith('twister-out'):
                    path = os.path.join(project_dir, item)
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.remove(path)

        self._create_eclair_db()

    def _out_dir(self) -> str:
        return os.path.abspath(os.path.join(HERE, '../ECLAIR/coverage_analysis_out'))

    def _twister_log(self) -> str:
        return os.path.join(self._out_dir(), 'twister.log')

    def _eclair_out_dir(self) -> str:
        return self._out_dir()

    def _eclair_data_dir(self) -> str:
        return os.path.join(self._eclair_out_dir(), 'data')

    def _eclair_diagnostics_output(self) -> str:
        return os.path.join(self._eclair_out_dir(), 'DIAGNOSTICS.txt')

    def _eclair_db(self) -> str:
        return os.path.join(self._eclair_out_dir(), 'PROJECT.ecd')

    def _gcov_files(self, project_dir: str) -> Generator[str, None, None]:
        for root, _, files in os.walk(project_dir):
            for file in files:
                if file.endswith('.gcov'):
                    yield os.path.join(root, file)

    def _selected_gcov_files(self, args: Namespace, project_dir: str, files: List[str]) -> List[str]:
        selected_files = []
        for gcov_file in files:
            if not self._gcov_file_is_selected(args, project_dir, gcov_file):
                continue
            selected_files.append(gcov_file)
        return selected_files

    def _gcov_file_is_selected(self, args: Namespace, project_dir: str, gcov_file: str) -> bool:
        rel_source = os.path.relpath(self._gcov_file_source(gcov_file), project_dir)
        if not os.path.exists(os.path.join(project_dir, rel_source)):
            self.wrn(f'Source file {rel_source} for gcov file {gcov_file} does not exist, skipping')
            return False
        if rel_source.startswith('src/') or rel_source.startswith('inc/'):
            return True
        if args.include_zephyr and ('/zephyr/' in rel_source):
            return True
        return False

    def _gcov_file_source(self, gcov_file: str) -> str:
        with open(gcov_file, 'r') as f:
            first_line = f.readline()
            match = re.match(r'\s*-\s*:\s*0\s*:\s*Source:(.*)', first_line)
            if match:
                source_file = match.group(1)
                return source_file.strip()
            else:
                self.die(f'Could not find source file in gcov file {gcov_file}')

    def _run_twister(self, project_dir: str) -> None:
        twister_log = self._twister_log()
        with open(twister_log, 'w') as log_file:
            cmd = ["west", "twister", "--coverage", "--coverage-basedir", project_dir, "-T", "tests", "--platform", "native_sim"]
            self.inf(f'Running: {" ".join(cmd)}')
            self.inf(f'Logging to: {twister_log}')
            self.run_subprocess(
                cmd,
                env=self._twister_env(),
                stdout=log_file,
                stderr=log_file,
                stdin=subprocess.DEVNULL,
                cwd=project_dir,
            ).check_returncode()

    def _twister_env(self) -> Dict[str, str]:
        coverage_exec_env = os.environ.copy()

        gcovr_exe = shutil.which('gcovr')
        if not gcovr_exe:
            self.die('gcovr not found in PATH')
        coverage_exec_env['GCOVR_EXE'] = gcovr_exe

        traps_path = os.path.abspath(os.path.join(HERE, '../ECLAIR/traps'))
        coverage_exec_env['PATH'] = f"{traps_path}:{coverage_exec_env['PATH']}"

        return coverage_exec_env

    def _run_eclair_analysis(self, gcov_files: List[str]) -> None:
        eclair_data_dir = self._eclair_data_dir()
        eclair_diagnostics = self._eclair_diagnostics_output()

        if os.path.exists(eclair_data_dir):
            shutil.rmtree(eclair_data_dir)

        if os.path.exists(eclair_diagnostics):
            os.remove(eclair_diagnostics)

        os.makedirs(eclair_data_dir, exist_ok=True)

        files = ','.join([f"'{f.replace("'", "\\'")}'" for f in gcov_files])
        ecl = os.path.abspath(os.path.join(HERE, '../ECLAIR/analysis_gcov.ecl'))
        cmd = ["eclair_env", f"-eval_file={ecl}", f"-config=B.GCOV,input_files={files}", "--", "echo"]

        env = os.environ.copy()
        env['ECLAIR_DATA_DIR'] = eclair_data_dir
        env['ECLAIR_DIAGNOSTICS_OUTPUT'] = self._eclair_diagnostics_output()

        self.inf(f'Running eclair_env')
        if self.verbosity >= 4:
            self.inf(f'  Command: {" ".join(cmd)}')
            self.inf(f'  ECLAIR_DATA_DIR={env["ECLAIR_DATA_DIR"]}')
            self.inf(f'  ECLAIR_DIAGNOSTICS_OUTPUT={env["ECLAIR_DIAGNOSTICS_OUTPUT"]}')
        self.inf(f'Logging to: {eclair_diagnostics}')
        self.run_subprocess(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
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
