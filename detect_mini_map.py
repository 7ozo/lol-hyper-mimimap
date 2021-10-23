import win32gui
import numpy as np
import cv2
import time
from PIL import ImageGrab
from configparser import ConfigParser
import ctypes

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def detect_minimap():
    # load minimap image
    minimap = cv2.imread('minimap1.png')
    # convert into grayscale
    minimap = grayscale(minimap)
    # canny edge detection
    minimap_edges_og = cv2.Canny(minimap, 25, 50)
    map_found = False
    map_position = (0, 0, 0, 0)

    # keep finding till the map is found.

    while not map_found:
        hwnd = win32gui.FindWindow(None, "League of Legends (TM) Client")
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(2)
        size_of_window = win32gui.GetWindowRect(hwnd)
        print(size_of_window)
        img = ImageGrab.grab(size_of_window)
        frame = np.array(img)
        # minimap is at the bottom of the screen, so we only detect the bottom part.
        mid_line = int(0.50 * frame.shape[0])
        bottom = frame[int(mid_line):, :, :]

        bottom = grayscale(bottom)
        edges = cv2.Canny(bottom, 25, 50)
        minimap_edges = minimap_edges_og.copy()
        temp = None
        maxres = None
        probs = dict()
        if minimap_edges.shape[0] > edges.shape[0]:
            minimap_edges = cv2.resize(minimap_edges_og, (edges.shape[0], edges.shape[0]))

        # change the minimap size untill we find its location.
        for i in range(minimap_edges.shape[0], 120, -2):
            res = cv2.matchTemplate(edges, minimap_edges, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= 0.2)
            for pt in zip(*loc[::-1]):
                temp = (
                    pt[0], pt[1] + mid_line, minimap_edges.shape[0] + pt[0], mid_line + minimap_edges.shape[1] + pt[1])
                maxres = res.max()
                cv2.rectangle(frame, temp[:2], temp[2:4], (255, 128, 255), 2)
                probs[maxres] = temp
            minimap_edges = cv2.resize(minimap_edges_og, (i, i))

        if len(probs) > 0:
            map_position = probs[maxres]
            map_found = True

        return map_position, size_of_window

def main():
    while (True):
        bbox, size = detect_minimap()
        if bbox == (0, 0, 0, 0):
            print("Map Not found")
            print("Make sure u are in a live game (practice game)")
            continue
        else:

            user32 = ctypes.windll.user32
            user32.keybd_event(0x12, 0, 0, 0)  # Alt
            time.sleep(0.25)
            user32.keybd_event(0x09, 0, 0, 0)  # Tab
            time.sleep(0.25)
            print(f"Map found {bbox}")
            break

    config_object = ConfigParser()

    config_object["WINDOWRES"] = {
        "width": size[2],
        "height": size[3]
    }
    config_object["MINIMAPSIZE"] = {
        "left": bbox[0],
        "top": bbox[1],
        "width": bbox[2] - bbox[0],
        "height": bbox[3] - bbox[1]
    }
    config_object["shortcut"] = {
        "key": "q",
    }

    with open('config.ini', 'w') as conf:
        config_object.write(conf)


if __name__ == '__main__':
    main()