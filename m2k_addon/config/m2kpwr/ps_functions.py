import libm2k
import numpy as np
import time
from open_context_and_files import ain, ctx
import random
import logging
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)



R1=12# pin32
R2=24# pin18
R3=4 # pin 7
R4=2 # pin 3
GPIO.setup(R1,GPIO.OUT)
GPIO.setup(R2,GPIO.OUT)
GPIO.setup(R3,GPIO.OUT)
GPIO.setup(R4,GPIO.OUT)
GPIO.setwarnings(False)


def config_for_ps_test(ps,ain):
    """Retrieve the Power supply object and enabe the power supply channels
    Arguments:
        ps-- Power Supply object
        ain  -- AnalogIn object\n
    """
    #ctx.calibrate()
    #enable channels
    ps.enableChannel(libm2k.ANALOG_IN_CHANNEL_1, True)
    ps.enableChannel(libm2k.ANALOG_IN_CHANNEL_2,True)

    if ain.isChannelEnabled(libm2k.ANALOG_IN_CHANNEL_1)==False:
        ain.enableChannel(libm2k.ANALOG_IN_CHANNEL_1, True)
    if ain.isChannelEnabled(libm2k.ANALOG_IN_CHANNEL_2)==False:
        ain.enableChannel(libm2k.ANALOG_IN_CHANNEL_2, True)
        
    ain.setRange(libm2k.ANALOG_IN_CHANNEL_1,libm2k.PLUS_MINUS_25V)
    ain.setRange(libm2k.ANALOG_IN_CHANNEL_2,libm2k.PLUS_MINUS_25V)
    GPIO.output(R1,True)
    return

def ps_test_positive(ps,ain, file):
    """Tests the positive power supply
    Arguments:
        ps -- Power Supply object
        ain -- AnalogIn object
    Returns:
        pos_supply-- Vector that  holds 1 if the  voltage value read on the channel equals the voltage sent
    """
    

    
    
    file.write("\n\nPositive power supply test:\n")
    voltage=1


    
    t=0.2 #threshold value 
    pos_supply=[]
    
   
    while voltage<=5:
        if voltage<=3:
            GPIO.output(R2,True)
            GPIO.output(R3,True)
            GPIO.output(R4,True)
        else:
            GPIO.output(R2,True)
            GPIO.output(R3,True)
            GPIO.output(R4,False)
           
        
        ps.pushChannel(libm2k.ANALOG_IN_CHANNEL_1, voltage)
        
        time.sleep(1)

       
        read_voltage=(ain.getVoltage()[libm2k.ANALOG_IN_CHANNEL_1])
        logging.getLogger().info(read_voltage)
        
        
        file.write("Sent voltage: "+str(voltage)+"\n")
        file.write("Read voltage: "+str(read_voltage)+"\n")

        if(read_voltage>=(voltage-t) and read_voltage<=(voltage+t)):
            pos_supply=np.append(pos_supply,1)
        else:
            pos_supply=np.append(pos_supply,0)
        voltage=voltage+1
    logging.getLogger().info(pos_supply)
    
    
    GPIO.output(R2, False)
    GPIO.output(R4, False)
    GPIO.output(R4, False)
    
    ps.pushChannel(libm2k.ANALOG_IN_CHANNEL_1, 0)
    ps.enableChannel(libm2k.ANALOG_IN_CHANNEL_1, False)
    return pos_supply


def ps_test_negative(ps,ain, file):
    """Tests the negativepower supply
    Arguments:
        ps -- Power Supply object
        ain -- AnalogIn object
    Returns:
        neg_supply-- Vector that  holds 1 if the  voltage value read on the channel equals the voltage sent
    """
    
    
    file.write("\n\nNegative power supply test:\n")
    voltage=-1
    neg_supply=[]
    t=0.2 #threshold value 

    while voltage>=-5:
        if voltage>=-3:
            GPIO.output(R2,True)
            GPIO.output(R3,True)
            GPIO.output(R4,True)
        else:
            GPIO.output(R2,True)
            GPIO.output(R3,True)
            GPIO.output(R4,False)
        
        ps.pushChannel(libm2k.ANALOG_IN_CHANNEL_2, voltage)
        time.sleep(1)

        read_voltage=(ain.getVoltage()[libm2k.ANALOG_IN_CHANNEL_2])
        logging.getLogger().info(read_voltage)
        

        file.write("Sent voltage: "+str(voltage)+"\n")
        file.write("Read voltage: "+str(read_voltage)+"\n")
 
        if(read_voltage<=(voltage+t) and read_voltage>=(voltage-t)):
            neg_supply=np.append(neg_supply,1)
        else:
            neg_supply=np.append(neg_supply,0)
        voltage=voltage-1 #subtract a random value from the previous voltage value
    
    
    logging.getLogger().info(neg_supply)
    
    GPIO.output(R2,False)
    GPIO.output(R3,False)
    GPIO.output(R3,False)
    
    ps.pushChannel(libm2k.ANALOG_IN_CHANNEL_2, 0)
    ps.enableChannel(libm2k.ANALOG_IN_CHANNEL_2, False)
    return neg_supply

def  switch_to_pot_control(ps):
    
    ps.enableChannel(libm2k.ANALOG_IN_CHANNEL_1,False)
    ps.enableChannel(libm2k.ANALOG_IN_CHANNEL_2,False)
    logging.getLogger().info("\n\n*** Switch jumper P6 from M2k+ position to POT+ position ***")
    logging.getLogger().info("\n\n*** Switch jumper P7 from M2k- position to POT- position ***")
    logging.getLogger().info("\n After switching the jumpers, press ENTER to continue the test\n")
    input()
    return
def ps_test_positive_with_potentiometer(ps, ain, file):
    
    GPIO.output(R2,True)
    GPIO.output(R3,True)
    GPIO.output(R4,True)
    
    file.write("\n\nPositive power supply - potentiometer test:\n")
    pot_pos_supply=[]
    voltage=0
    logging.getLogger().info("\n\n*** For this test will use POT+ (R20) ***")
    logging.getLogger().info("Make sure the arrow is pointing to 1.5V and press enter")
    input()


        
    voltage=ain.getVoltage()[libm2k.ANALOG_IN_CHANNEL_1]
    logging.getLogger().info(voltage)
        
    file.write("Read voltage: "+str(voltage)+"\n")
    if (voltage>1) and (voltage <2):
        pot_pos_supply=np.append(pot_pos_supply,1)
    else:
        pot_pos_supply=np.append(pot_pos_supply,0)
        
    
    GPIO.output(R3,False)
    GPIO.output(R4,False)
 
    logging.getLogger().info("\nMake sure the arrow is pointing to 15V and press enter")

    input()
   
        
    voltage=ain.getVoltage()[libm2k.ANALOG_IN_CHANNEL_1]
    
    logging.getLogger().info(voltage)

    file.write("Read voltage: "+str(voltage)+"\n")
    if (voltage>13) and (voltage <15):
        pot_pos_supply=np.append(pot_pos_supply,1)
    else:
        pot_pos_supply=np.append(pot_pos_supply,0)
    
    
    
    GPIO.output(R2,False)
    GPIO.output(R3,False)
    GPIO.output(R4,False)
    
    
    logging.getLogger().info(pot_pos_supply)
    return pot_pos_supply


def ps_test_negative_with_potentiometer(ps, ain, file):
    
    
    GPIO.output(R2,True)
    GPIO.output(R3,True)
    GPIO.output(R4,True)
    
    file.write("\n\nNegative power supply - potentiometer test:\n")
    pot_neg_supply=[]
    voltage=0
    
    logging.getLogger().info("\n\n *** For this test will use POT- (R19) ***")
    logging.getLogger().info("Make sure the arrow is pointing to -1.5V and press enter")
    
    input()


        
    voltage=ain.getVoltage()[libm2k.ANALOG_IN_CHANNEL_2]
    logging.getLogger().info(voltage)

    file.write("Read voltage: "+str(voltage)+"\n")
    if (voltage<-1) and (voltage>-2):
        pot_neg_supply=np.append(pot_neg_supply,1)
    else:
        pot_neg_supply=np.append(pot_neg_supply,0)
    
    GPIO.output(R3,False)
    GPIO.output(R4,False)

    logging.getLogger().info("\nMake sure the arrow is pointing to -15V and press enter")
  
    
    
   
    input()


    voltage=ain.getVoltage()[libm2k.ANALOG_IN_CHANNEL_2]
    logging.getLogger().info(voltage)
    
    file.write("Read voltage: "+str(voltage)+"\n")
    if (voltage<-13) and (voltage>-15):
        pot_neg_supply=np.append(pot_neg_supply,1)
    else:
        pot_neg_supply=np.append(pot_neg_supply,0)
        
        
    GPIO.output(R1,False)
    GPIO.output(R2,False)
    GPIO.output(R3,False)
    GPIO.output(R4,False)
    
    logging.getLogger().info(pot_neg_supply)
    return pot_neg_supply
   


def test_external_connector():
    logging.getLogger().info("\n\n\n Connect a voltage source 4.5-18V to the 2 terminal screw connector")
    logging.getLogger().info("If LED DS3 is ON,  press 1 ")
    logging.getLogger().info("Press Enter to continue")
    ext_pwr=input()
    return ext_pwr

    
def test_usbTypeC_connector():
    #logging.getLogger().info("\n\n\n***! Disconnect the external power !***")
    logging.getLogger().info("\nPlug in the USB-TypeC ")
    logging.getLogger().info("\nIf LED DS3 is ON, press 1 ")
    logging.getLogger().info("Press Enter to continue")
    usb_pwr=input()
    return usb_pwr