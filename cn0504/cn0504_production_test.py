# Copyright (C) 2019 Analog Devices, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#     - Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#     - Neither the name of Analog Devices, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#     - The use of this software may or may not infringe the patent rights
#       of one or more patent holders.  This license does not release you
#       from the requirement that you obtain separate licenses from these
#       patent holders to use this software.
#     - Use of the software either in source or binary form, must be run
#       on or directly connected to an Analog Devices Inc. component.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, NON-INFRINGEMENT, MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED.
#
# IN NO EVENT SHALL ANALOG DEVICES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, INTELLECTUAL PROPERTY
# RIGHTS, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
import time

# Channel scale factors


def main(my_ip):
    try:
        import adi
        myswitch = adi.ksz9477@0(uri=my_ip)
        # REMEMBER TO VERIFY POWERDOWN/UP BEHAVIOR
    except:
      print("No device found")
      sys.exit(0)

    print("Setting sample rates...")
    #Set maximum sampling frequency
    myswitch.sample_rate = 9600

    # Production test code
    input("\n\nStarting Production Test! Verify nothing connected to output jacks, press enter to continue...")
    failed_tests = []
    input("Set both potentiometers to 12:00 position, then press enter to continue...")

    time.sleep(1)

    del myswitch
    del adi

    if len(failed_tests) == 0:
        print("Board PASSES!!")
    else:
        print("Board FAILED the following tests:")
        for failure in failed_tests:
            print(failure)
        print("Note failures and set aside for debug.")

if __name__ == '__main__':
    import os
    from time import sleep
    hardcoded_ip = 'ip:localhost'
    my_ip = sys.argv[1] if len(sys.argv) >= 2 else hardcoded_ip
    print("Connecting with CN0508 context at %s" % (my_ip))

    while(1):
        testdata = main(my_ip)
        x = input("Type \'s\' to shut down, \'a\' to test again, or \'q\'to quit:  ")
        if(x == 's'):
            if os.name == "posix":
                os.system("shutdown -h now")
            else:
                print("Sorry, can only shut down system when running locally on Raspberry Pi")
            break
        elif(x == 'q'):
            break
        else:
            sleep(0.5)
        # any other character tests again.