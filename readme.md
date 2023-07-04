<!-- center the title and add a line below the title -->
<h1 align="center">ScreenScan: Capture. Extract. Simplify!</h1>

<!-- These are the badges for the project. You can add more badges by copying the code below and changing the links to the appropriate ones for your project from https://shields.io/ -->
<p align="center">
  <img src="https://img.shields.io/github/license/shivang02/whizgroup?style=flat-square" alt="License" />
  <img src="https://img.shields.io/github/languages/code-size/shivang02/whizgroup?style=flat-square" alt="Code Size" />
  <img src="https://img.shields.io/github/last-commit/shivang02/whizgroup?style=flat-square" alt="Last Commit" />
  <img src="https://img.shields.io/github/issues/shivang02/whizgroup?style=flat-square" alt="Issues" />
  <img src="https://img.shields.io/github/forks/shivang02/whizgroup?style=flat-square" alt="Forks" />
  <img src="https://img.shields.io/github/stars/shivang02/whizgroup?style=flat-square" alt="Stars" />
</p>

ScreenScan is a Python application that allows you to capture screenshots, perform Optical Character Recognition (OCR) on them, and extract text from the captured images. It utilizes the Tkinter library for GUI, the PyScreeze library for capturing screenshots, the PyTesseract library for OCR, and the Pyperclip library for copying the extracted text to the clipboard.

## Pre-Requisites

- [Python 3](https://www.python.org/downloads/)
- [Tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/shivang02/screenscan.git
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python screenscan.py
   ```

## Usage

1. On the initial setup, you will be prompted to provide the path to the screenshots folder and the path to the Tesseract executable. These paths will be stored in the `locations.json` file for future use.

2. Press the specified hotkey combination (Alt + 3 by default) to activate ScreenScan.

3. ScreenScan will capture a screenshot of the entire screen and display it in a Tkinter window.

4. To select a specific region of the screenshot, click and drag the mouse to create a bounding box around the desired area. The selected region will be cropped and displayed in a new Tkinter window.

5. In the cropped image window, you can perform the following actions:
   - Copy the extracted text to the clipboard.
   - Save the cropped image.
   - View the extracted text in a separate text box.

## Customization

You can customize the following aspects of ScreenScan:

- Hotkey Combination: Modify the `cmb` list in the code to change the hotkey combination for activating ScreenScan.

- File Paths: The paths to the screenshots folder and the Tesseract executable are stored in the `locations.json` file. You can manually edit this file if you need to update the paths.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- ScreenScan utilizes the following libraries:
  - [Tkinter](https://docs.python.org/3/library/tkinter.html)
  - [PyScreeze](https://pypi.org/project/PyScreeze/)
  - [PyTesseract](https://pypi.org/project/pytesseract/)
  - [Pyperclip](https://pypi.org/project/pyperclip/)

Feel free to contribute to this project by submitting bug reports, feature requests, or pull requests.