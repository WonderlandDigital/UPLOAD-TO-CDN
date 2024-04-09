import tkinter as tk
from tkinter import filedialog
from ftplib import FTP
import pyperclip
from PIL import Image, ImageTk
import requests
from io import BytesIO
import ctypes
import os
import urllib.parse
import pygame

pygame.init()

# Handling file upload
def upload_to_cdn():
    
    # Open file dialog to select a file
    file_path = filedialog.askopenfilename()
    
    # Check if a file is selected
    if file_path:
        try:
            
            # Connect to BunnyCDN FTP server
            ftp = FTP()
            ftp.connect(HOSTNAME, PORT)
            ftp.login(USERNAME, PASSWORD)
            ftp.set_pasv(True)  # Set passive mode
            
            # Open and read the file
            with open(file_path, 'rb') as file:
                
                # Define remote file path including folder name
                file_name = os.path.basename(file_path)
                
                remote_file_path = f'/Discord Clips/{file_name}'
                
                # Upload the file
                ftp.storbinary(f'STOR {remote_file_path}', file)
            
            # Close FTP connection
            ftp.quit()
            
            # Encode the file name for URL
            encoded_file_name = urllib.parse.quote(file_name)
            
            # I am using BunnyCDN, with a folder called 'Discord Clips' Change accordingly.
            link = f'https://{STORAGE_ZONE}.b-cdn.net/Discord%20Clips/{encoded_file_name}'
            show_success_popup(link)
            
        except Exception as e:
            show_error_popup(str(e))




def show_success_popup(link):
    pyperclip.copy(link)
    
    try:
        # Download the Sound file from your CDN.
        sound_url = ''
        response = requests.get(sound_url)
        sound_file_path = 'success_sound.mp3'
        with open(sound_file_path, 'wb') as sound_file:
            sound_file.write(response.content)
        
        # Load the cached sound file
        success_sound = pygame.mixer.Sound(sound_file_path)
        
        # Play the sound file if it was a successful upload.
        success_sound.play()
        
        # Delete the cached sound file after playing
        os.remove(sound_file_path)
        ctypes.windll.user32.MessageBoxW(0, f"Uploaded File to CDN! \nLink: {link}", "Success", 0)
    
    except Exception as e:
        print(f"Error playing sound: {e}")

# Function to show error pop-up
def show_error_popup(error_msg):
    ctypes.windll.user32.MessageBoxW(0, f"Error: {error_msg}", "Error", 0)

# Function to fetch image from CDN and set it as background
def set_background_from_cdn():
    try:
        response = requests.get(BACKGROUND_IMAGE_URL)
        image_data = BytesIO(response.content)
        background_image = Image.open(image_data)
        background_photo = ImageTk.PhotoImage(background_image)
        background_label.config(image=background_photo)
        background_label.image = background_photo  # Keep a reference

        # Resize main window based on image size
        root.geometry(f"{background_image.width}x{background_image.height}")

    except Exception as e:
        print(f'Error setting background: {str(e)}')

def remove_console_icon():
    root.iconbitmap(default="")


# Initialize Tkinter
root = tk.Tk()
root.title('CDN UPLOAD')

# Disable window resizing (fullscreen)
root.resizable(False, False)

# FTP / API SETTINGS
HOSTNAME = '' 
PORT = 21
USERNAME = ''
PASSWORD = ''
STORAGE_ZONE = ''

# For TKINTER
BACKGROUND_IMAGE_URL = ''
CONSOLE_ICON_URL = ''

# Set console window icon
remove_console_icon()

# Create background label
background_label = tk.Label(root)
background_label.pack(fill="both", expand=True)

# Set initial background (optional)
set_background_from_cdn()

# Create GUI components
upload_button = tk.Button(root, text="Upload File to CDN", command=upload_to_cdn, bg='#800080', fg='white', font=('Arial', 12, 'bold'), relief=tk.RAISED, borderwidth=3)
upload_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Run the Tkinter event loop
root.mainloop()
