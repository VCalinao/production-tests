# CN0504 Production Test Script

https://wiki.analog.com/resources/eval/user-guides/circuits-from-the-lab/cn0504

SD card setup:
1) Flash the latest ADI Kuiper Linux image to an SD card.
2) Put python test script into user analog's home directory.
3) Set the Raspberry Pi to boot to CLI as user analog using the Raspberry Pi Configuration utility.
4) A VERY important extra step to booting to CLI is to disable the x11vnc service:

sudo systemctl disable x11vnc.service

5) Reboot and verify that it boots to the command line, then run:

sudo python cn504_production_test.py

(This will complain if a DUT board is not connected)

Follow prompts on terminal, test results, including any failed tests, are reported at the end.

An option to shut down is given as well, which works when running the script locally.
