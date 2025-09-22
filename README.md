[![ECLAIR coding guidelines_compliance](https://github.com/BUGSENG/ZiSE25/actions/workflows/ECLAIR_coding_guidelines_compliance.yml/badge.svg?branch=main&event=push)](https://github.com/BUGSENG/ZiSE25/actions/workflows/ECLAIR_coding_guidelines_compliance.yml)
[![temp_alert tests](https://github.com/BUGSENG/ZiSE25/actions/workflows/twister_tests.yml/badge.svg?branch=main)](https://github.com/BUGSENG/ZiSE25/actions/workflows/twister_tests.yml)
[![ECLAIR coverage and requirements](https://github.com/BUGSENG/ZiSE25/actions/workflows/ECLAIR_requirements_coverage.yml/badge.svg)](https://github.com/BUGSENG/ZiSE25/actions/workflows/ECLAIR_requirements_coverage.yml)

# Temp Alert

**temp_alert** is a Zephyr-based embedded application that monitors ambient temperature via a BME280 sensor and:

- **Displays** the current temperature (XX.YY °C) on a TM1637 4-digit 7-segment display
- **Alerts** when temperature exceeds a configurable threshold, using both:
  - A **buzzer** (Temporal-3 fire-alarm pattern)
  - An **LED** chase animation on four GPIO-driven LEDs
- **Modular feature support**, enable or disable in `prj.conf`:

    ```ini
    CONFIG_APP_LEDS=y       # Enable LED warning animation when threshold is exceeded
    CONFIG_APP_BUZZER=y     # Enable buzzer alarm when threshold is exceeded
    CONFIG_APP_DISPLAY=y    # Enable TM1637 display of the current temperature
    ```

---

## Getting Started

### Visual Studio Code & Zephyr Workbench

1. **Install VS Code** and the **Zephyr Workbench** extension (Windows, Linux and Mac).
   Follow this guide:
   https://zephyr-workbench.com/docs/documentation/installation/

2. **Install the Zephyr SDK (v0.17.2)** via this tutorial:
   [https://zephyr-workbench.com/docs/tutorials/frdm-mcxn947](https://zephyr-workbench.com/docs/tutorials/frdm-mcxn947#import-a-sdk)

3. **Import the West workspace**
   - Open the Zephyr Workbench extension.
   - Click **New West Workspace** (or **Initialize workspace**).
   - **Source location:** `https://github.com/BUGSENG/ZiSE25.git`
   - **Tag:** write `main`
   - Choose a local folder and click **Import**.

4. **Import the Application**
   - In the **Applications** panel, click **Import Zephyr Application**.
   - Select the `temp_alert` folder path from the cloned repo.
   - Point to your West workspace and SDK.
   - Choose one of these two boards: `NXP FRDM MCXN947 (CPU0)` or `STM32 ST STM32F746G Discovery`.

5. **Build**
   - Right-click on **temp_alert** -> **Build**.
   - View build output in the VS Code Terminal.

6. **Flash & Debug**
   Follow the tutorial:
   [https://zephyr-workbench.com/docs/tutorials/frdm-mcxn947](https://zephyr-workbench.com/docs/tutorials/frdm-mcxn947#flash-and-debug-project)

### Command Line

**Prerequisites**:

- OS: Ubuntu 22.04 (x86_64) or later;
- ability to issue privileged commands via `sudo`;
- (Optional) if you want to run static analysis, you should request a free
  [trial license](https://www.bugseng.com/eclair-request-trial/) for the ECLAIR Static Analysis tool.
  In the request form, indicate "Zephyr" in the "What you need" field". Once you have obtained the installer,
  follow the provided instructions to install the trial license on your machine.

  **Note** Trial licenses of the tool do not work on virtual machines or containers.

After cloning the repository run the following commands:
```bash
cd ZiSE25
sudo ./setup.sh

# Activate your Python venv
source ../.venv/bin/activate

# Build the temp_alert application for the NXP board
west build -b frdm_mcxn947/mcxn947/cpu0

# Build the temp_alert application for the STM32 board
west build -b stm32f746g_disco
```

**Note**: always perform a pristine build when switching to a different board;
to perform a pristine build, add flag `-p` to the commands above after `west build`.

**Note**: it is assumed that the virtual environment created and activated above is active
when executing the commands reported below.

## Static Analysis

If the steps above to build the application went well, you can proceed
with running static analysis, provided that you have also aquired a trial license for the static analysis tool, using the procedure described above.
The analysis is done using the [ECLAIR Software Verification
Platform](https://www.bugseng.com/eclair-static-analysis-tool), which
is supported as a Static Code Analysis (SCA) tool in the upstream
Zephyr repository (see section [ECLAIR support](https://docs.zephyrproject.org/latest/develop/sca/eclair.html)).

```bash
west build -p -b frdm_mcxn947/mcxn947/cpu0 -- -DZEPHYR_SCA_VARIANT=eclair
```

## Unit Testing

Unit tests are based on ZTest and can be discovered and run using Twister:

```bash
# One suite ID at a time
west twister -T tests -s temp_alert.display
west twister -T tests -s temp_alert.buzzer
west twister -T tests -s temp_alert.leds
```

```bash
# Or all three:
west twister -T tests
```

### Code Coverage Analysis

The following command runs the unit tests using Twister with code coverage support
enabled. It produces code coverage reports in directory `twister-out`:

```bash
# Run unit test with code coverage
west twister --coverage --coverage-basedir . -T tests --platform native_sim
```

Code coverage can also be analyzed with ECLAIR to generate coverage reports:
```bash
west analyze-coverage
```
which will produce an ECLAIR database in
`ECLAIR/coverage_analysis_out/PROJECT.ecd`.

## Requirements

The system requirements are documented using the
[StrictDoc](https://github.com/strictdoc-project/strictdoc)
Requiremements Management tool in the plain text file
[`temp_alert.sdoc`](./temp_alert.sdoc). They can also be explored interactively on a web browser
with the following command:

```bash
strictdoc server .
```

The web server can be accessed by clicking the link in the terminal output.

Requirements coverage can be analyzed with ECLAIR with the following
[custom command](./scripts/analyze_requirements_cmd.py):
```bash
west analyze-requirements -t native_sim
```
which will produce an ECLAIR database in
`ECLAIR/requirements_analysis_out/PROJECT.ecd`.

## Working on temp_alert

This sample application has been engineered to work in two main scenarios:

- As a blueprint for anyone who wants to get familiarity with the
  processes and procedures demanded by functional safety standards,
  using the Zephyr RTOS and its tooling as a base;

- As a proof of concept for people already familiar with implementing
  functional safety standards that want to use Zephyr as a base for
  their next projects.

This naturally suggests two ways of using the material available in this repository:

- clone the repository locally to build, test and optionally perform
  static code analysis on the example Zephyr application;

- fork the project on GitHub and run the CI automation scripts on your
  own premises.

## Forking the project

The Continuous Integration scripts in this repository have been
designed to be adaptable with minimal effort in a fork. To have your
own copy of the repo with CI scans running on your infrastructure,
follow these steps:

- fork the repository from the `main` branch;

- follow GitHub's documentation to set up a self-hosted runner for the forked repository ([Self-hosted runner](https://docs.github.com/en/actions/concepts/runners/self-hosted-runners), [Adding a self-hosted runner](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners) );

- edit the  GitHub workflows under `.github/workflows/*.yml` in the following manner:
  ```diff
  -runs-on: saas.eclairit.com
  -container:
  -  image: bugseng/github-runner:latest
  +runs-on: <RUNNER>
  ```
  ;

- in the machine where the self-hosted runner is installed, install
  [Docker Engine](https://docs.docker.com/engine/install/ubuntu/);

- request a free **30-day** [trial license](https://www.bugseng.com/eclair-request-trial/#request) of
  ECLAIR from BUGSENG's website (the **7-day** trial license is not
  suitable for this purpose);

- follow the instructions provided with the trial license to install
  the tool on the machine where the self-hosted runner is installed;

- add persistently to the `PATH` environment variable the path the ECLAIR installation (e.g., `/opt/bugseng/eclair-3.14.0/bin/`).

At this point, you are ready to trigger new GitHub actions runs from
your fork. To trigger one, you can make a commit to branch `main`
modifying a source file.
