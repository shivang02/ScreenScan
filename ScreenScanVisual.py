import json
from pystray import MenuItem as item
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import pyscreeze
from pynput import keyboard
import pytesseract
import os
from datetime import datetime
import pyperclip

# check if locations.json exists
locFile = "locations.json"
if not os.path.exists(locFile):

    with open(locFile, "w") as f:
        f.write("{\"screenshots_path\": \"\", \"tesseract_path\": \"\"}")


# if screenshots_path or tesseract_path is empty, open the setup window
with open(locFile, "r") as f:
    locations = json.load(f)
    if locations == {"screenshots_path": "", "tesseract_path": ""}:
        win = tk.Tk()
        win.title("ScreenScan Setup")
        win.geometry("500x500")

        # Function to handle closing of the window
        def on_closing():
            win.destroy()

        win.protocol("WM_DELETE_WINDOW", on_closing)

        # Function to save the path to the screenshots folder in locations.json
        def save_path():
            global screenshots_path, tesseract_path
            # open locations.json
            with open(locFile, "r") as f:
                locations = json.load(f)
            # save the path to the screenshots folder
            locations["screenshots_path"] = screenshots_path.get(
                "1.0", "end-1c")
            # save the path to the tesseract executable
            locations["tesseract_path"] = tesseract_path.get("1.0", "end-1c")
            # save the locations in locations.json
            with open(locFile, "w") as f:
                json.dump(locations, f, indent=4)
            # close the window
            win.destroy()

        screenshots_path_label = tk.Label(
            win, text="Enter the path to the screenshots folder")
        screenshots_path_label.pack()

        # Add a text box to the path of the screenshots folder
        screenshots_path = tk.Text(win, height=1, width=20)
        screenshots_path.pack()
        screenshots_path_entry = ""

        # Function to get the path to the screenshots folder
        def get_screenshots_folder():
            global screenshots_path_entry
            screenshots_path_entry = filedialog.askdirectory()
            # display the path inputted by the user
            screenshots_path.insert(tk.END, screenshots_path_entry)

        # button to open the file explorer
        open_file_explorer_button = tk.Button(
            win, text="Open File Explorer", command=get_screenshots_folder)
        open_file_explorer_button.pack(pady=10)

        tesseract_path_label = tk.Label(
            win, text="Enter the path to the tesseract executable")
        tesseract_path_label.pack()

        # display the path to the tesseract executable
        tesseract_path = tk.Text(win, height=1, width=20)
        tesseract_path.pack()
        tesseract_path_entry = ""

        # Function to get the path to the tesseract executable
        def get_tesseract_path():
            global tesseract_path_entry
            tesseract_path_entry = filedialog.askopenfilename(
                filetypes=[("Executable Files", "*.exe")])
            # display the path inputted by the user
            tesseract_path.insert(tk.END, tesseract_path_entry)

        # button to open the file explorer
        open_file_explorer_button = tk.Button(
            win, text="Open File Explorer", command=get_tesseract_path)
        open_file_explorer_button.pack(pady=10)

        # button to save the path to the tesseract executable
        save_path_button = tk.Button(win, text="Save", command=save_path)
        save_path_button.pack(pady=10)

        win.mainloop()

# import from locFile
with open(locFile, "r") as f:
    locations = json.load(f)
    pytesseract.pytesseract.tesseract_cmd = locations["tesseract_path"]
    if "screenshots_folder" not in os.listdir(locations["screenshots_path"]):
        os.mkdir(locations["screenshots_path"] + "/screenshots_folder")

# Function to perform OCR on the cropped image


def perform_ocr(image):
    text = pytesseract.image_to_string(image)
    return text

# Function to handle the hotkey activation


def on_activate():

    # Function to create a screenshot
    def take_screenshot():
        screenshot = pyscreeze.screenshot()
        return screenshot

    # Function to crop the screenshot based on coordinates
    def crop_image():

        nonlocal x1, y1, x2, y2, screenshot
        # Compare X1 X2 and Y1 and Y2 and swap them if necessary
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        # Crop the image
        cropped_image = screenshot.crop((x1, y1, x2, y2))

        return cropped_image

    # Take a screenshot
    screenshot = take_screenshot()

    # Create a Tkinter window
    window = tk.Tk()
    window.attributes('-fullscreen', True)

    # Display the screenshot in the Tkinter window
    screenshot_tk = ImageTk.PhotoImage(screenshot)
    canvas = tk.Canvas(window, cursor='tcross', bd=0)
    canvas.create_image(0, 0, image=screenshot_tk, anchor="nw")
    canvas.pack(fill="both", expand=True)

    # Create a list to store the images of the bounding boxes
    images = []

    # Variables to store the coordinates of the bounding box
    '''
    x1: x-coordinate of the top left corner of the bounding box
    y1: y-coordinate of the top left corner of the bounding box
    x2: x-coordinate of the bottom right corner of the bounding box
    y2: y-coordinate of the bottom right corner of the bounding box
    move_toggle: boolean variable to check if the bounding box is being moved
    '''
    x1, y1, x2, y2 = 0, 0, 0, 0
    move_toggle = False

    # Variables to store the bounding boxes
    b_box1 = None
    b_box2 = None

    # store the color of the bounding box
    box_color = "red"

    # store the alpha value of the bounding box
    alpha = .3

    # Function to select the bounding box
    def create_rect(x, y):
        nonlocal x1, y1, x2, y2, b_box1, b_box2, images, box_color, alpha, canvas, window
        box_color2 = window.winfo_rgb(box_color) + (int(alpha*255),)
        rect_im = Image.new('RGBA', (abs(x-x1), abs(y-y1)), box_color2)

        # Create four cases to set the value of lx and ly based on the position of the mouse
        if x >= x1 and y >= y1:
            lx, ly = x1, y1
        elif x >= x1 and y < y1:
            lx, ly = x1, y
        elif x < x1 and y >= y1:
            lx, ly = x, y1
        elif x < x1 and y < y1:
            lx, ly = x, y

        # prevent the Image from being garbage-collected
        # append the image to the list
        images.append(ImageTk.PhotoImage(rect_im))
        images = images[-2:]  # keep only the last two images
        b_box1 = canvas.create_image(
            lx, ly, image=images[-1], anchor="nw")  # Create a red overlay
        b_box2 = canvas.create_rectangle(x1, y1, x, y, fill=None, outline=None)

    # Function to handle mouse button press event
    def on_press(event):
        nonlocal move_toggle, x1, y1, x2, y2, b_box1, b_box2
        move_toggle = True
        x1, y1 = event.x, event.y
        x2, y2 = event.x, event.y
        create_rect(x2, y2)

    # Function to handle mouse button release event
    def on_release(event):
        nonlocal move_toggle, x1, y1, x2, y2, b_box1, b_box2
        move_toggle = False
        x2, y2 = event.x, event.y
        # create_rect(x2, y2)

        cropped_image = crop_image()

        window.destroy()
        show_cropped_image(cropped_image)

    # Function to handle mouse move event
    def on_move(event):
        nonlocal move_toggle, b_box1, b_box2
        if move_toggle:
            canvas.delete(b_box1)
            canvas.delete(b_box2)
            create_rect(event.x, event.y)

    # Function to display the cropped image

    def show_cropped_image(cropped_image):
        # Create a new Tkinter window
        cropped_window = tk.Tk()
        cropped_window.title("Cropped Image")

        # Resize the image if necessary
        max_size = 1000
        if cropped_image.width > max_size or cropped_image.height > max_size:
            cropped_image.thumbnail((max_size, max_size), Image.ANTIALIAS)

        # Display the cropped image in the Tkinter window
        cropped_tk = ImageTk.PhotoImage(cropped_image)
        canvas = tk.Canvas(
            cropped_window, width=cropped_image.width, height=cropped_image.height)
        canvas.create_image(0, 0, image=cropped_tk, anchor="nw")
        canvas.pack()

        # Function to save the cropped image
        def save_cropped_image():
            nonlocal cropped_image
            # Add timestamp to the image filename
            timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

            # Generate the filename for the cropped image
            image_filename = f"ss_{timestamp}.png"

            # Save the cropped image
            image_path = os.path.join(
                locations["screenshots_path"]+r'\screenshots_folder', image_filename)
            cropped_image.save(image_path)

        # Function to copy text to clipboard
        def copy_to_clipboard():

            text = perform_ocr(cropped_image)

            pyperclip.copy(text)

        # Function to show text in a seperate text box
        def show_text():
            nonlocal cropped_image, cropped_window, box_color, alpha, canvas

            # Create bounding boxes around recognized text
            text = perform_ocr(cropped_image)

            # if the text is empty, display a message "No text found"
            if text in ["", " ", None, r"^\s*$"]:
                text = "No text found"

            # Check if a text box already exists in the window
            existing_text_box = cropped_window.children.get(tk.Text)

            if existing_text_box > 0:
                # Update the content of the existing text box
                existing_text_box.delete("1.0", tk.END)
                existing_text_box.insert(tk.END, text)
            else:
                # Create a new text box in the existing Tkinter window to display the recognized text
                text_box = tk.Text(cropped_window, height=10, width=cropped_window.winfo_width()//9, font=("Helvetica", 10))
                text_box.pack(side=tk.LEFT, fill=tk.BOTH)
                text_box.insert(tk.END, text)

                # Create a Scrollbar widget
                scrollbar = tk.Scrollbar(cropped_window)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

                # Configure the Scrollbar to control the Text widget
                text_box.configure(yscrollcommand=scrollbar.set)
                scrollbar.configure(command=text_box.yview)


        def close_window():
            cropped_window.destroy()

        # Create buttons for options
        copy_button = tk.Button(
            cropped_window, text="Copy Text to Clipboard", command=copy_to_clipboard)
        copy_button.pack(pady=10)

        show_text_button = tk.Button(
            cropped_window, text="Show Text", command=show_text)
        show_text_button.pack(pady=10)

        save_image_button = tk.Button(
            cropped_window, text="Save Image", command=save_cropped_image)
        save_image_button.pack(pady=10)

        cropped_window.protocol("WM_DELETE_WINDOW", close_window)

        # Start the Tkinter event loop for the cropped window i
        cropped_window.mainloop()

    # Bind mouse events to their respective functions
    canvas.bind('<ButtonPress-1>', on_press)
    canvas.bind('<ButtonRelease-1>', on_release)
    canvas.bind('<Motion>', on_move)

    window.attributes('-topmost', True)

    # Start the Tkinter event loop
    window.mainloop()


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
            on_activate()


def on_letgo(key):
    if any([key in z for z in cmb]):
        current.remove(key)


# Create the keyboard listener
with keyboard.Listener(on_press=on_pushdown, on_release=on_letgo) as listener:
    listener.join()
