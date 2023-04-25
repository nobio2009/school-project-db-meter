# Library imports
import time, pyaudio, pygame.mixer
from math import log10
from machine import Pin, PWM
from utime import sleep
import pyaudio
import time
from math import log10
import audioop

try:
    p = pyaudio.PyAudio()
    WIDTH = 2
    RATE = int(p.get_default_input_device_info()['defaultSampleRate'])
    DEVICE = p.get_default_input_device_info()['index']
    rms = 1
    print(p.get_default_input_device_info())

    def callback(in_data, frame_count, time_info, status):
        global rms
        rms = audioop.rms(in_data, WIDTH) / 32767
        return in_data, pyaudio.paContinue


    stream = p.open(format=p.get_format_from_width(WIDTH),
                    input_device_index=DEVICE,
                    channels=1,
                    rate=RATE,
                    input=True,
                    output=False,
                    stream_callback=callback)

    stream.stop_stream()
    stream.close()

    p.terminate()
    # Set up our button name and GPIO pin number
    # Also set the pin as an input and use a pull down
    button1 = Pin(3, Pin.IN, Pin.PULL_DOWN)
    
    # Set GPIO pin for audio output
    buzzer = PWM(Pin(15))

    def play_tone(frequency):
        # Set maximum volume
        buzzer.duty_u16(10000)
        # Play tone
        buzzer.freq(frequency)

    def be_quiet():
        # Set minimum volume
        buzzer.duty_u16(0)

    ## Infinite loop
    stream.start_stream()

    while stream.is_active():
        db = 20 * log10(rms)
        print(f"RMS: {rms} DB: {db}") 
        # refresh every 0.3 seconds 
        time.sleep(0.3)

        if db >= -15:
            pass

        time.sleep(0.2) # Short delay
    
        while button1.value() == 1: #If button 1 is pressed
            play_tone(1000)
            sleep(0.75)
            be_quiet()
            sleep(0.75)
        
except KeyboardInterrupt:
    buzzer.duty_u16(0)