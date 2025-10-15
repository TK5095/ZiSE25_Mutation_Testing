sudo apt upgrade
sudo apt update

Install LLVM Toolchain:
wget https://apt.llvm.org/llvm.sh
chmod +x llvm.sh
sudo ./llvm.sh 18

PATH:
export PATH=/usr/lib/llvm-18/bin:$PATH
in etc/environment?

mull project:
https://mull.readthedocs.io/en/0.26.0/Installation.html#install-on-ubuntu
https://github.com/mull-project/mull/releases/download/0.26.1/Mull-18-0.26.1-LLVM-18.1-ubuntu-x86_64-24.04.deb

Put mull.yml where you start mull-runner-18

Twister:
1) export ZEPHYR_TOOLCHAIN_VARIANT=llvm

2) west twister --coverage --coverage-basedir . -T temp_alert/tests/test_temp_alert/ --platform native_sim

3) mull-runner-18 -allow-surviving --reporters IDE --report-name fmt twister-out/native_sim_native/llvm/temp_alert.buzzer/zephyr/zephyr.exe
-> Better, write a script where all zephyr.exe are found and invoked by mull-runner-18
