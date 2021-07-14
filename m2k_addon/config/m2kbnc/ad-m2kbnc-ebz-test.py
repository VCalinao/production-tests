#! /usr/bin/python3
import libm2k
import unittest
import HtmlTestRunner
import logging
import sys
from m2k_analog_test import AnalogTests
from m2k_digital_test import DigitalTests
from m2k_powersupply_test import PowerSupplyTests

from open_context_and_files import ctx, results_dir, open_context, calibrate, create_dir


logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))




def run_test_suite():
    """ Test suite that contains all available tests.
    When run it will create a HTML report of the tests, along with plot files and csv files with results
    """
    
    
    m2k_test_suite=unittest.TestSuite()
    m2k_test_suite.addTest(PowerSupplyTests())
    m2k_test_suite.addTest(AnalogTests())
    m2k_test_suite.addTest(DigitalTests())
    result= unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output=str(results_dir), report_title="ADALM2000 libm2k test results",report_name='M2K_test_results',open_in_browser=True, combine_reports=True))
    m2k_test_suite.run(result)
    return






if __name__ =="__main__":
    """Main file where tests for all segments are called. The test classes are organized in a test suite.
    To run specific tests, comment run_test_suite() line and uncomment run_specific_tests_from...()  line(s)

    """
    ctx=libm2k.m2kOpen()
    ctx.calibrate()

    logging.getLogger().info("\n\n*** Connect the AD-M2KBNC-EBZ  to the test setup and press enter to continue the tests ***")
    input()

    run_test_suite()




libm2k.contextClose(ctx, True)