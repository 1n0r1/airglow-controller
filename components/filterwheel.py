# A collection of Python classes to run the SSL filter wheel.
# This code handles interfacing with the motor, the home sensor, and I/O with the FPI/Observatory.
# It is intended to be run on a raspberry Pi with an Adafruit Motor Bonnet.
# Brian J. Harding Feb 2021


####### PARAMETERS ########
# Specify MODE = 'active' or 0, 1, 2, or 3. If 'active', the filterwheel will listen for inputs and move the wheel
# accordingly. If an int, it will go to that filter position and stay there, regardless of
# inputs, and output READY. (This latter mode is intended as a stopgap measure. If single-filter
# mode is desired for a long period of time, the pi/motor should be shut off and the filter wheel
# should be mechanically parked, so as to avoid motor wear and tear).
MODE = 'active'
# MODE = 1 # 1 = green
# MODE = 2 # 2 = red
VERBOSE = True # If True, print a bunch of debugging information.

###########################



# TODO: Change to Odyssey gpio
# import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper # Allows for defined constants
import time
import numpy as np



######## Home sensor definition #######
class HallEffectSensor():
    '''
    A class to interface to a 3-wire Hall effect sensor. It was intended for this model, but will likely
    work with other 3-wire interfaces:
    https://www.digikey.com/en/products/detail/littelfuse-inc/59140-3-S-02-F/4780005
    '''
    def __init__(self, pin0 = 23, pin1 = 24):
        '''
        * pin0 = which GPIO pin on the raspberry pi the blue wire is connected to.
        * pin1 = which GPIO pin on the raspberry pi the black wire is connected to.
                 These use the GPIO ## numbering, not the raw sequential numbering.
                 The white wire should be connected to ground.
        '''
        if VERBOSE:
            print('    Initializing hall effect sensor...')

        # TODO: Change to Odyssey gpio
        GPIO.setmode(GPIO.BCM) # This lets us use the GPIO## notation, not the physical pin number
        # Set for inputs and pull ups
        
        self.pin0 = pin0
        self.pin1 = pin1
        
        # TODO: Change to Odyssey gpio
        GPIO.setup(pin0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        if VERBOSE:
            print('    ... Complete.')
        
    def read(self):
        '''
        Read the state of the sensor, either:
         * True  (sensors are near each other)
         * False (sensors are far from each other)
        The 3-wire interface allows to check for faults. One pin should always be high and the other 
        low. If this isn't the case, an Exception will be thrown as there's likely a fatal problem.
        '''
        
        # TODO: Change to Odyssey gpio
        p0, p1 = GPIO.input(self.pin0), GPIO.input(self.pin1)
        #if VERBOSE:
        #    print('    Read hall effect sensor  p0=%i  p1=%i' % (p0, p1))
        
        # If there is a problem (i.e., if both are low or both are high), try again a few times
        Ntries = 0
        while ((p0 == p1) & (Ntries < 10)):
            p0, p1 = GPIO.input(self.pin0), GPIO.input(self.pin1)
            Ntries += 1
            #if VERBOSE:
            #    print('    Re-read hall effect sensor due to error  p0=%i  p1=%i' % (p0, p1))
        
        if Ntries > 10:
            raise Exception("Both Hall Effect sensor pins are %s. This probably indicates an electrical or software problem." % p0)
        
        return bool(p0)
        


######## Motor definition #######

class Motor():
    ''' 
    A class to interface to the adafruit motor toolkit
    and specialize the use for the SSL filter selector. It is intended to be
    used with the Adafruit Stepper Motor Hat or Motor Bonnet:
    https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/using-stepper-motors
    '''
    
    def __init__(self, pause_between_steps = 0.008, step_style = stepper.DOUBLE):
        '''
        * pause_between steps: [ms], the delay between each step. 
                0 = fastest, but might miss steps.
                0.02 = about as slow as you'd reasonably want to go
        * step_style: stepper.SINGLE, stepper.DOUBLE, stepper.MICROSTEP. 
                      DOUBLE is the default since it seems smoothest, although it needs more power and runs hot.
        '''
        
        if VERBOSE:
            print('    Initializing motor')
            
        self.pause_between_steps = pause_between_steps
        self.step_style = step_style
        
        kit = MotorKit()
        self.motor = kit.stepper1 # This assumes you have plugged the motor into M1 and M2 on the motor bonnet.
                                  # stepper2 is also a possibility (M3 and M4)
        self.motor.release() # Start out not driving
        
        
    def go(self, steps):
        '''
        Move the motor by the specified number of steps. If positive it is defined as 'forwards' and if negative it is
        defined as 'backwards'.
        'forward' = clockwise if the driveshaft is pointed to you with the motor behind it (and if
                    you plugged in the wires black, green, red, blue as in the notes).
        
        For the OMC StepperOnline 17HS13-0404S-PG5 motor, 1 complete revolution is 1036.36 steps
        '''
        
        #if VERBOSE:
        #    print('    Motor moving %i steps...' % (steps))
            
        if steps >= 0:
            direction = stepper.FORWARD
        else:
            direction = stepper.BACKWARD
        
        for n in range(abs(steps)):
            self.motor.onestep(direction=direction, style=self.step_style)
            time.sleep(self.pause_between_steps)
        #if VERBOSE:
        #    print('    ...Complete.')
        
        
    def shutdown(self):
        '''
        Release the motor so it isn't using power. It can freely rotate.
        '''
        self.motor.release()
        if VERBOSE:
            print('    Motor shut down')
    
        
    def back_and_forth_test(self):
        '''
        Go 100 steps forwards and return backwards
        '''
        self.go(100)
        time.sleep(0.2)
        self.go(-100)
        

    

########## Combine the two above to make a filter wheel object #########


class FilterWheel():
    ''' 
    A class to control an SSL filter wheel. Interfaces with:
        * The stepper motor
        * The hall effect sensor
        * The FPI/Observatory via 3 IO pins
    '''
    
    def __init__(self):
        if VERBOSE:
            print('Begin FilterWheel initialization.')
        
        ######## Parameters #########
        self.pin_in0 = 27 # Which GPIO pin is bit 0 of the "desired filter" input from FPI/Observatory
        self.pin_in1 = 22 # Which GPIO pin is bit 1 of the "desired filter" input from FPI/Observatory
        self.pin_out = 10 # Which GPIO pin is the "acknowledge" signal back to FPI/Observatory (0=moving, 1=stable)
        sens_pin0    = 23 # Which GPIO pin on the raspberry pi the sensor's blue wire is connected to.
        sens_pin1    = 24 # Which GPIO pin on the raspberry pi the sensor's black wire is connected to.
        pause_between_steps = 0.008  # [ms], the delay between each step. 
                                     # 0 = fastest, but might miss steps.
                                     # 0.008 = a reasonable choice
                                     # 0.02 = about as slow as you'd reasonably want to go
        self.counts_per_rev = 1037 # counts per revolution (this is actually fractional)
        self.filter0_pos    = 6    # Position of filter 0 (i.e., pin_in0, pin_in1 = 0, 0) relative to home
        self.filter1_pos    = 265  # Position of filter 1 (i.e., pin_in0, pin_in1 = 0, 1) relative to home
        self.filter2_pos    = 524  # Position of filter 2 (i.e., pin_in0, pin_in1 = 1, 0) relative to home
        self.filter3_pos    = 784  # Position of filter 3 (i.e., pin_in0, pin_in1 = 1, 1) relative to home
        
        
        ######### Initialization #######
        self.raw_pos = 0 #  This is set to 0 on startup and never re-zeroed
        self.pos = np.nan  # This will be initialized after the homing routine and is
                           # always maintained such that the home sensor is the 0 position 
                           # (Specifically, 0 is the location where the home sensor first goes "high" along the
                           # forwards direction)
        self.total_steps = 0 # This counts the total number of steps (forward and backward)
        
        # This is what the FPI/Observatory system wants as the "acknowledge" signal
        self.BUSY   = GPIO.LOW 
        self.STABLE = GPIO.HIGH
        
        # This assumes the FPI Datalogger doesn't need us to pull up/down on the RPi side.
        # I'm not sure if that's the case.
        GPIO.setup(self.pin_in0, GPIO.IN,  pull_up_down=GPIO.PUD_OFF) 
        GPIO.setup(self.pin_in1, GPIO.IN,  pull_up_down=GPIO.PUD_OFF)
        GPIO.setup(self.pin_out, GPIO.OUT, pull_up_down=GPIO.PUD_OFF)
        GPIO.output(self.pin_out, self.BUSY) # Set to BUSY while we're initializing
        
        # Initialize motor
        self.motor = Motor(pause_between_steps = pause_between_steps)
    
        # Initialize hall effect sensor
        self.sensor = HallEffectSensor(pin0 = sens_pin0, pin1 = sens_pin1)
        self.sensor.read() # Just a sanity check. This will throw an error if both pins are high or both low.
    
        # Done and ready
        GPIO.output(self.pin_out, self.STABLE)
        
        if VERBOSE:
            print('End FilterWheel initialization.')
    
    def go(self, steps):
        '''
        Move the motor by the specified number of steps. If positive it is defined as 'forwards' and if negative it is
        defined as 'backwards'.
        'forward' = clockwise if the driveshaft is pointed to you with the motor behind it (and if
                    you plugged in the wires black, green, red, blue as in the notes).
                    
        This does not issue STABLE/BUSY outputs. That needs to be handled by the caller.
        '''
        #if VERBOSE:
        #    print('Request to move motor %i steps' % steps)
        # Move
        self.motor.go(steps)
        
        # Bookkeeping
        self.raw_pos += steps
        self.pos += steps
        self.total_steps += abs(steps)
        
    
    def home(self):
        '''
        Perform the homing routine to set the 0-position. This issues STABLE/BUSY outputs.
        '''
        
        if VERBOSE:
            print('Begin homing ...')
        
        # Label as busy
        GPIO.output(self.pin_out, self.BUSY)
        
        N = 0 # A counter just for this homing manuever. If it gets way too large, throw an error.
        
        # If the sensor is on the home switch, move it off:
        while(self.sensor.read()):
            self.go(1)
            N += 1
            if N > 3*self.counts_per_rev:
                raise Exception('Home sensor always returning HIGH. Home not found')
                            
        # Keep moving forward until you just hit the switch. Call this "home"
        while(not self.sensor.read()):
            self.go(1)
            N += 1
            if N > 3*self.counts_per_rev:
                raise Exception('Home sensor always returning LOW. Home not found')
            
        self.pos = 0
        
        # Label as ready
        GPIO.output(self.pin_out, self.STABLE)
        if VERBOSE:
            print('... Homing complete.')
    
    
    def goto(self, pos):
        '''
        Move the filter wheel to the commanded position. This issues STABLE/BUSY outputs.
        '''
        if VERBOSE:
            print('Request to goto position %i' % pos)
        
        assert np.isfinite(self.pos), "Need to home first"
                
        # Label as busy
        GPIO.output(self.pin_out, self.BUSY)
        
        # Move
        dpos = pos - self.pos
        self.go(dpos)
        
        # Label as ready
        GPIO.output(self.pin_out, self.STABLE)

        if VERBOSE:
            print('At position %i' % pos)
        
        
    def read_commanded_filter(self):
        '''
        Read the input pins from FPI/Observatory and return the desired filter position (0, 1, 2, 3)
        '''
        p0, p1 = GPIO.input(self.pin_in0), GPIO.input(self.pin_in1)
        filt = 2*p1 + 1*p0 # convert from binary
        #if VERBOSE:
        #    print('Read filter request: filter %i ' % filt)
        
        return filt
        
    
    def shutdown(self):
        self.motor.shutdown()
        # Drop output pins to low just to be safe
        GPIO.output(self.pin_out, GPIO.LOW)
        
        
    def run(self, mode='active'):
        '''
        An infinite loop that implements the operation of the filter wheel. Listen for inputs from
        FPI/Observatory and move the filter wheel accordingly.
        mode: 'active' or int. If 'active', the filterwheel will listen for inputs and move the wheel
              accordingly. If an int, it will go to that filter position and stay there, regardless of
              inputs, and output READY. (This latter mode is intended as a stopgap measure. If single-filter
              mode is desired for a long period of time, the pi/motor should be shut off and the filter wheel
              should be mechanically parked, so as to avoid motor wear and tear).
        '''

        #################################################
        if mode == 'active':
            
            if VERBOSE:
                print('Beginning active mode loop')
            while(True):

                # Read the input pins
                filt = self.read_commanded_filter()

                # Determine the desired position (in steps)
                desired_pos = [self.filter0_pos,
                               self.filter1_pos,
                               self.filter2_pos,
                               self.filter3_pos][filt]

                # If the desired position is far from the actual position, initiate a move
                if abs(desired_pos - self.pos) > 5:
                    # However, we want to wait a little bit to give the user a chance to change both pins,
                    # since they might not happen exactly simultaneously
                    
                    # Label as busy while we're giving time
                    GPIO.output(self.pin_out, self.BUSY)
                    
                    time.sleep(0.5)
                    
                    # Read again
                    filt = self.read_commanded_filter()

                    if VERBOSE:
                        print('Detected request to move to filter %i' % filt)

                    # Determine the desired position (in steps)
                    desired_pos = [self.filter0_pos,
                                   self.filter1_pos,
                                   self.filter2_pos,
                                   self.filter3_pos][filt]
                    
                    self.goto(desired_pos)
                    
                time.sleep(0.05)
                
        #################################################
        else: # mode is presumably an int
            
            if VERBOSE:
                print('Beginning parked mode script')
                
            # No infinite loop. Run once and terminate.
                        
            desired_pos = [self.filter0_pos,
                           self.filter1_pos,
                           self.filter2_pos,
                           self.filter3_pos][mode]
            
            self.goto(desired_pos)
            
            # Label as permanently ready
            GPIO.output(self.pin_out, self.STABLE)
            
            if VERBOSE:
                print('Ending parked mode script')
                
            
            
# The main script   
if __name__ == '__main__':
    fw = FilterWheel()

    try:
        fw.home()  
        print('Running main program...')
        fw.run(mode=MODE)    

    except Exception as e:
        
        if VERBOSE:
            print('FATAL ERROR: Terminating...\n\t%s' % e)

        # Fatal error. Label as busy until the system is restarted. 
        # We don't want FPI/Observatory to think everything is ok when it's not.
        GPIO.output(fw.pin_out, fw.BUSY)

        raise    
    
    