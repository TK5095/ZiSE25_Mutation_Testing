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
   https://zephyr-workbench.com/docs/tutorials/frdm-mcxn947#import-a-sdk

3. **Import the West workspace**  
   - Open the Zephyr Workbench extension.  
   - Click **New West Workspace** (or **Initialize workspace**).  
   - **Source location:** `https://github.com/BUGSENG/ZiSe25.git`  
   - **Tag:** write `main`  
   - Choose a local folder and click **Import**.

4. **Import the Application**  
   - In the **Applications** panel, click **Import Zephyr Application**.  
   - Select the `temp_alert` folder path from the cloned repo.  
   - Point to your West workspace and SDK.  
   - Choose one of these two boards: `NXP FRDM MCXN947 (CPU0)` or `STM32 ST STM32F746G Discovery`.

5. **Build**  
   - Right-click on **temp_alert** → **Build**.  
   - View build output in the VS Code Terminal.

6. **Flash & Debug**  
   Follow the tutorial:  
   https://zephyr-workbench.com/docs/tutorials/frdm-mcxn947#flash-and-debug-project

---

### Command-Line
Make sure that [zephyr prerequisites](https://docs.zephyrproject.org/latest/develop/getting_started/index.html) already installed
```bash
# Activate your Python venv
source <path-to-venv>/bin/activate

# Clone & initialize workspace
mkdir ZiSe25
cd ZiSe25
west init -m https://github.com/BUGSENG/ZiSe25.git .
west update

# Install Zephyr Python dependencies
pip install -r deps/zephyr/scripts/requirements.txt

# Build the temp_alert application
cd temp_alert
west build -b frdm_mcxn947/mcxn947/cpu0
```

## Static Analysis

If the steps above to build the application went well, you can proceed with
running static analysis. It is assumed that the Python venv is already activated
and the starting directory is the top project directory (the one containing prj.conf).

# TODO: finish analysis instructions

```bash
cd temp_alert
west build -p -b frdm_mcxn947/mcxn947/cpu0 -- -DZEPHYR_SCA_VARIANT=eclair
```

## Testing

```bash
west twister -T tests --platform native_sim
```