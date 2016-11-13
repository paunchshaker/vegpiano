import sys
import time
import json
import argparse
import pygame

import Adafruit_MPR121.MPR121 as MPR121

class Piano(object):

    def __init__(self, kit):
        self.cap = MPR121.MPR121()
        if not self.cap.begin():
            print('Error initializing MPR121')
            sys.exit(1)

        pygame.mixer.pre_init(44100, -16, 24, 1024)
        pygame.init()

        self.load_kit(kit)
        self.begin()

    def load_kit(self, json_file):
        sys.stderr.write('Loading sounds defined in {0}\n'.format(json_file))
        self.sounds = [0] * 12
        with open(json_file) as kit_spec:
            mapping = json.load(kit_spec)
            for key, soundfile in mapping.iteritems():
                self.sounds[int(key)] = pygame.mixer.Sound(soundfile)
                self.sounds[int(key)].set_volume(1)
    
    def begin(self):

        last_touched = self.cap.touched()
        while True:
            current_touched = self.cap.touched()
            for i in range(12):
                pin_bit = 1 << i
                if current_touched & pin_bit and not last_touched & pin_bit:
                    if (self.sounds[i]):
                        self.sounds[i].play()
            last_touched = current_touched
            time.sleep(0.01)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Use RaspberryPi Capacitance Touch HAT as a Piano')
    parser.add_argument('kit_json', help='json file containing association of each sensor (0-11) to a .wav file')
    args = parser.parse_args()

    sys.stderr.write("Violet and Ginger's Veggie Piano\n")
    sys.stderr.write('Hit Ctrl-C to quit...\n')
    Piano(args.kit_json)


    
