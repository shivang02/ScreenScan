import pystray
from pystray import MenuItem as item
from PIL import Image
import json
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import pyscreeze
from pynput import keyboard
import pytesseract
import os
from datetime import datetime
import pyperclip
import subprocess
from basicFunc import addPathScreenshotTesseract, on_activate

keyboard_listener = None

def startProgram():
    global keyboard_listener

    locFile = "locations.json"
    if not os.path.exists(locFile):
        with open(locFile, "w") as f:
            f.write("{\"screenshots_path\": \"\", \"tesseract_path\": \"\"}")

    # if screenshots_path or tesseract_path is empty, open the setup window
    with open(locFile, "r") as f:
        locations = json.load(f)
        if locations == {"screenshots_path": "", "tesseract_path": ""}:
            addPathScreenshotTesseract(locFile)

    # import from locFile
    with open(locFile, "r") as f:
        locations = json.load(f)
        pytesseract.pytesseract.tesseract_cmd = locations["tesseract_path"]
        if "screenshots_folder" not in os.listdir(locations["screenshots_path"]):
            os.mkdir(locations["screenshots_path"] + "/screenshots_folder")

    cmb = [
        {keyboard.Key.alt_l, keyboard.KeyCode.from_char('3')},
        {keyboard.Key.alt_r, keyboard.KeyCode.from_char('3')},
        {keyboard.Key.alt_l, keyboard.KeyCode.from_char('3')},
    ]

    current = set()


    def on_pushdown(key):
        if any([key in z for z in cmb]):
            current.add(key)

            if any(all(k in current for k in z) for z in cmb):
                current.remove(key)
                on_activate(locations)
                keyboard_listener.stop()


    def on_letgo(key):
        if any([key in z for z in cmb]):
            current.remove(key)

    # Create the keyboard listener
    keyboard_listener = keyboard.Listener(on_press=on_pushdown, on_release=on_letgo)
    keyboard_listener.start()

def openSSFolder():
    locFile = "locations.json"
    with open(locFile, "r") as f:
        locations = json.load(f)
        screenshots_folder = locations["screenshots_path"] + "/screenshots_folder"
        print("Opening screenshots folder:", screenshots_folder)
        # Open the screenshots folder in the default file explorer
        subprocess.Popen(f'start "" "{screenshots_folder}"', shell=True)

# Create the system tray icon and menu
def setup_tray_icon():
    icon_path = "icon.png" 
    icon_image = Image.open(icon_path)
    menu = (
        item('Do it!', startProgram),
                item('SS folder', openSSFolder),
                item('Exit', lambda icon, item: icon.stop())
    )
    menu = tuple(menu)
    tray_icon = pystray.Icon("name", icon_image, "Title", menu)
    return tray_icon

if __name__ == '__main__':
    tray_icon = setup_tray_icon()
    tray_icon.run()
    