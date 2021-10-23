from mss import *
from configparser import ConfigParser
import numpy as np
import cv2
import time
import win32gui
import os


def main():
    config_object = ConfigParser()
    try:
        config_object.read("config.ini")
        m = config_object["MINIMAPSIZE"]
        shortcut = config_object["shortcut"]
        monitor = {"left": int(m["left"]), "top": int(m["top"]), "width": int(m["width"]), "height": int(m["height"])}
    except:
        print("Couldn't find config file Creating one now ")
        print("Please go inside a game (practice mode)")
        input("press any key when ready")
        print("it will automatically alt-tab leave it for a couple seconds ")
        time.sleep(2)
        os.system("python detect_mini_map.py")
        time.sleep(1)
        main()

    with mss() as sct:
        while True:
            # uncomment these line to get fps (1/2)

            last_time = time.time()

            img = sct.grab(monitor)

            # (2/2)
            print(f"FPS:{int((1 / (time.time() - last_time)))}")

            cv2.namedWindow('Hola', cv2.WINDOW_KEEPRATIO)
            cv2.imshow('Hola', np.array(img))
            if cv2.waitKey(25) & 0xFF == ord(f'{shortcut["key"]}'):
                cv2.destroyAllWindows()
                break


if __name__ == '__main__':
    main()
