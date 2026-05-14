HIT137 Assignment 3 - Spot the Difference Game

Student:
Deepjan Thapaliya

Project Description:
This project is a Python desktop application that creates a Spot the Difference game. The user loads an image, and the program automatically creates a modified copy with five random non-overlapping differences. The player must identify the differences by clicking on the modified image.

Main Technologies:
- Python
- Tkinter for GUI
- OpenCV for image processing
- Pillow for displaying images in Tkinter
- GitHub for version control

Main Features:
- Loads JPG, JPEG, PNG, and BMP image files
- Displays original and modified images side by side
- Creates exactly five random differences
- Ensures difference regions do not overlap
- Uses multiple image alteration techniques:
  1. Brightness alteration
  2. Blur alteration
  3. Colour shift alteration
- Uses OOP with multiple classes
- Demonstrates inheritance and polymorphism through image alteration classes
- Tracks correct clicks and incorrect clicks
- Shows red circles for found differences
- Allows only three incorrect attempts
- Locks the game after three mistakes
- Reveals remaining differences using blue circles
- Resets game state when a new image is loaded
- Handles invalid or unsupported image files safely

How to Run:
1. Open the project folder in VS Code or terminal.
2. Activate the virtual environment.

PowerShell:
.\.venv\Scripts\Activate.ps1

If activation is blocked, run:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

3. Install required packages:
pip install -r requirements.txt

4. Run the application:
python main.py

Testing Completed:
- Tested image loading with JPG/PNG images
- Tested invalid image handling by renaming a document file as an image
- Tested clicking before loading an image
- Tested correct difference clicks
- Tested duplicate clicks on the same difference
- Tested three incorrect attempts and game lockout
- Tested reveal differences button
- Tested loading a new image after game over
- Tested image display scaling for better usability

GitHub Repository:
https://github.com/DeepjanS395373/hit137-assignment-3