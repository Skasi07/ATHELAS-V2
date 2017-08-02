##SAURON: the core imaging and scanning module for the device
import os
import time
import glob
from shutil import copyfile
import autofocus
import RPi.GPIO as GPIO
import threading
import sys

#HELLOUPDATECHECK

os.chdir("/home/pi/device/")

#turn on the servoblaster module
os.system("sudo /home/pi/PiBits/ServoBlaster/user/servod")

LED_GPIO_CHANNEL = 20
START_POS = 100
END_POS = 200
brightness = 40

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    #GPIO 20 is for the backlight
    GPIO.setup(LED_GPIO_CHANNEL, GPIO.OUT)

### SETUP THE GPIO
setup_gpio()

living = GPIO.PWM(LED_GPIO_CHANNEL, 20000)

#TODO sends the GPIO signal to turn on the backlight
def back_light_on(brightness):
#    GPIO.output(LED_GPIO_CHANNEL, GPIO.HIGH)
	 living.start(0)
     living.ChangeDutyCycle(brightness)
     return

#TODO sends the GPIO signal to turn off the backlight
def back_light_off():
    GPIO.output(LED_GPIO_CHANNEL, GPIO.LOW)
    return

#given a pos between 100-200, sets it using the PWM pibits library-
def set_pos(pos):
    os.system("sudo /home/pi/PiBits/ServoBlaster/user/servod > /dev/null 2>&1")
    os.system("sudo echo 2=" + str(pos) + "> /dev/servoblaster")
 time.sleep(1)
    os.system("sudo echo 2=" + str(0) + "> /dev/servoblaster")
def cleanup():
    """
    Called to cleanup a run.
    """
    autofocus.move_to_top()
    set_pos(END_POS)
    autofocus.turnOFF()
    back_light_off()
#the 2-axis version of our sauron run function
def run_2():
    back_light_on()
    #time.sleep(30)
    purge()
    start = time.time()
    #turn our backlight on
    ##we are now in pos 1 focused (and know what it is), initialize the servoblaster model
    print("servoblaster initialized")
  os.system("sudo /home/pi/PiBits/ServoBlaster/user/servod")
    print("starting coarse 2")
    targetpack = autofocus.coarse_2()
    targetpos_original = targetpack[1]
    autofocus_elapsed = time.time() - start
    print("Moving to the coarse focus point")
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
    for x in xrange(0, 10):
        pos = START_POS + 5 * x
        set_pos(pos)
        ##the maximum focus reduction difference in focus we will tolerate
        #after every microstep, check if we're out of the target focus.
        #if we are, do a microcalibration to ensure we have the most focused version of the image
        #take image here, save with a proper file name to the directory 'images'
        ##this is the file we need to save, move it to images
        time.sleep(1)
        targetpack = autofocus.fine_2(pos)
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
        autofocus.turnOFF()
    for thread in move_threads:
        thread.join()

    movingelapsed = time.time() - substart
    print("full time elapsed: " + str(time.time() - start))
    print("time spent on original autofocus: " + str(autofocus_elapsed))
    print("time spent on the final image actuations: " + str(movingelapsed))
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
