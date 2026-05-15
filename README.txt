HIT137 Assignment 3 - Spot the Difference Game

Group:
DANEXT_36

Group Members:
- S395373 - Deepjan Thapaliya
- S395743 - Sehajpreet Singh
- S393520 - Manjil Sahani Chhetri
- S393984 - Kavya Sethi

Project Description:
This project is a Python desktop application that creates a Spot the Difference game. The user loads an image, and the program automatically creates a modified copy with five random non-overlapping differences. The player must identify the differences by clicking on the modified image.

Contribution Summary:

- Deepjan Thapaliya:
  Primary developer responsible for overall software architecture, object-oriented design, GUI implementation, OpenCV image processing, gameplay logic, defensive validation, testing, debugging, GitHub integration, evidence preparation, and final project integration.

- Sehajpreet Singh:
  Assisted with gameplay testing, feature feedback, and interface evaluation.

- Manjil Sahani Chhetri:
  Assisted with testing different image inputs and reviewing gameplay behaviour.

- Kavya Sethi:
  Assisted with documentation review, usability feedback, and verification testing.
  
Main Technologies:
- Python
- Tkinter for GUI
- OpenCV for image processing
- Pillow for displaying images in Tkinter
- NumPy for image calculations
- GitHub for version control

Main Features:
- Loads JPG, JPEG, PNG, and BMP image files.
- Displays original and modified images side by side.
- Creates exactly five random differences.
- Ensures difference regions do not overlap.
- Avoids selecting very dark image regions for generated differences.
- Uses soft blended elliptical/circular colour modifications instead of harsh rectangle edits.
- Uses brightness alteration with controlled visibility.
- Uses Gaussian blur to create subtle image differences.
- Uses randomised colour tint styles for more natural gameplay.
- Preserves image aspect ratio during resizing.
- Correctly maps resized image click coordinates back to original image coordinates.
- Uses object-oriented programming with multiple classes.
- Demonstrates inheritance and polymorphism through image alteration classes.
- Separates application logic into models, image processing, controller, GUI, and main launcher files.
- Tracks correct clicks and incorrect clicks.
- Prevents duplicate scoring for already found differences.
- Displays red circles for correctly identified differences.
- Displays blue circles when remaining differences are revealed.
- Displays dark purple X markers for incorrect clicks.
- Allows only three incorrect attempts before game lockout.
- Displays game status updates and remaining attempts.
- Fully resets score, markers, and game state when a new image is loaded.
- Handles invalid or unsupported image files safely without crashing.
- Prevents crashes from clicking before loading an image.
- Prevents out-of-bound click coordinates from breaking game logic.
- Includes defensive validation for image loading and image size.
- Includes evidence screenshots demonstrating functionality and testing.

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
- Tested image loading using JPG and PNG images.
- Tested invalid image handling by renaming document files as image files.
- Tested clicking before loading an image.
- Tested correct difference clicks.
- Tested duplicate clicks on the same difference.
- Tested incorrect clicks and visual wrong-click markers.
- Tested three incorrect attempts and game lockout.
- Tested reveal differences functionality.
- Tested loading a new image after game over.
- Tested image resizing and scaling behaviour.
- Tested subtle blended image alterations on brighter image regions.
- Tested that the application does not crash on invalid input.

GitHub Repository:
https://github.com/DeepjanS395373/hit137-assignment-3