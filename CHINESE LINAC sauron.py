##SAURON: the core imaging and scanning module for the device
import os
import time
import glob
import threading
import logging
import sys
import autofocus
import RPi.GPIO as GPIO #pylint: disable=import-error
import wiringpi

logging.basicConfig(stream=sys.stdout, format='%(asctime)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

os.chdir("/home/pi/device/")

#turn on the servoblaster module
os.system("sudo /home/pi/PiBits/ServoBlaster/user/servod")

LED_GPIO_CHANNEL = 20
START_POS = 85
END_POS = 215

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    #GPIO 20 is for the backlight
    GPIO.setup(LED_GPIO_CHANNEL, GPIO.OUT)

### SETUP THE GPIO
setup_gpio()


#TODO sends the GPIO signal to turn on the backlight
def back_light_on():
    GPIO.output(LED_GPIO_CHANNEL, GPIO.HIGH)
    return

#TODO sends the GPIO signal to turn off the backlight
def back_light_off():
    GPIO.output(LED_GPIO_CHANNEL, GPIO.LOW)
    return

#given a pos between 100-200, sets it using the PWM pibits library-
def set_pos(pos):
    #os.system("sudo /home/pi/PiBits/ServoBlaster/user/servod > /dev/null 2>&1")
    #os.system("sudo echo 2=" + str(pos) + "> /dev/servoblaster")
    #time.sleep(1)
    #os.system("sudo echo 2=" + str(0) + "> /dev/servoblaster")
    wiringpi.wiringPiSetupGpio()

    wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)

    wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

    wiringpi.pwmSetClock(180)
 
    wiringpi.pwmSetRange(1960)

    wiringpi.pwmWrite(18, pos)

    time.sleep(1)

    wiringpi.pwmWrite(18, 0)

def cleanup():
    """
    Called to cleanup a run.
    """

    autofocus.move_to_top()
    set_pos(END_POS)
    autofocus.turnOFF()
    back_light_off()

def targeted_run(xpos, ypos):
    back_light_on()
    purge()
    set_pos(xpos)
    cam = autofocus.get_camera()
    autofocus.start_camera(cam)
    autofocus.setpos(
        autofocus.getpos(),
        ypos
    )
    autofocus.fine_2(cam, xpos)

#the 2-axis version of our sauron run function
def run_2():
    back_light_on()
    #time.sleep(30)
    purge()
    start = time.time()
    #turn our backlight on

    ##we are now in pos 1 focused (and know what it is), initialize the servoblaster model
    logger.info("servoblaster initialized")

    os.system("sudo /home/pi/PiBits/ServoBlaster/user/servod")

    logger.info("starting coarse 2")

    set_pos(START_POS + 20)

    camera = autofocus.get_camera()
    autofocus.start_camera(camera)
    targetpack = autofocus.coarse_2(camera)
    targetpos_original = targetpack[1]

    set_pos(START_POS)

    autofocus_elapsed = time.time() - start

    logger.info("Moving to the coarse focus point")

    autofocus.setpos(
        autofocus.getpos(),
        targetpos_original
    )

    ##main runner for the images with micro-calibrations to ensure the 
    ##images stay in focus
    #DELTA = 0.005
    ##we are now at target pos
    substart = time.time()


    move_threads = []

    for x in xrange(0, 13): # pylint: disable=undefined-variable
        pos = START_POS + 10 * x
        set_pos(pos)

        ##the maximum focus reduction difference in focus we will tolerate
        #after every microstep, check if we're out of the target focus.
        #if we are, do a microcalibration to ensure we have the most focused version of the image
        #take image here, save with a proper file name to the directory 'images'

        ##this is the file we need to save, move it to images
        time.sleep(1)

        targetpack = autofocus.fine_2(camera, x_pos=pos)

        target_image = targetpack[0]
        targetpos = targetpack[1]
        autofocus.setpos(autofocus.getpos(), targetpos_original)

        def move_images():
            return target_image.save(
                "/home/pi/device/images/{}_{}.jpg".format(
                    str(pos),
                    str(targetpos)
                )
            )

        thread = threading.Thread(target=move_images)
        thread.start()
        move_threads.append(thread)

    camera.stop()
    autofocus.turnOFF()

    for thread in move_threads:
        thread.join()

    movingelapsed = time.time() - substart

    logger.info("full time elapsed: " + str(time.time() - start))
    logger.info("time spent on original autofocus: " + str(autofocus_elapsed))
    logger.info("time spent on the final image actuations: " + str(movingelapsed))

    return glob.glob("/home/pi/device/images/*.jpg")

#get rid of all the old images because we have already uploaded
def purge():
    for fname in os.listdir('/home/pi/device/images/'):
        if fname.endswith('.jpg'):
            os.remove('/home/pi/device/images/' + fname)

    fine_images = glob.glob("/home/pi/device/fine*/*.jpg")
    coarse_images = glob.glob("/home/pi/device/coarse*/*.jpg")
    for image in (fine_images + coarse_images):
        os.remove(image)

    return
