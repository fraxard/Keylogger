# Keylogger
# Keylogger Technical Documentation
- Ayush
- [Use all this for educational purposes only, I do not encourage any type of illegal and fraudulent activity. I will not be responsible of any incident if it includes my code, The user will solely be responsible, this is an open source platform and I'm putting my code here, so , see ya.]

## **Introduction**

The Keylogger project is a Python-based monitoring tool designed to collect various types of system and user activity data. This tool demonstrates the integration of multiple functionalities such as keystroke logging, clipboard monitoring, active window tracking, browser history access, and system information retrieval. Additionally, the project incorporates remote data transmission using a Telegram Bot for centralized logging.

This document provides an expansive technical overview of the keylogger’s design, implementation, features, and future development goals. It serves as a comprehensive reference for understanding the project’s architecture and functionality.

---

## **Key Features**

The keylogger includes the following functionalities:

1. **Keystroke Logging**:

   - Records every keystroke entered by the user.
   - Tracks both regular characters and special keys (e.g., Enter, Backspace).
   - Associates each keystroke with a timestamp and the currently active window.

2. **User Details Retrieval**:

   - Collects detailed system and user information, including:
     - Username.
     - Machine name.
     - Operating system and version.
     - System architecture (32-bit or 64-bit).
     - CPU usage percentage.
     - Memory usage percentage.
     - Local IP address.

3. **Clipboard Monitoring**:

   - Periodically retrieves clipboard content.
   - Logs clipboard data along with timestamps.

4. **Active Window Tracking**:

   - Detects and logs the title of the currently active window.
   - Records window changes to track user activity context.

5. **Browser History Access**:

   - Retrieves browsing history from Google Chrome and Mozilla Firefox.
   - Extracts URLs, page titles, and last visit timestamps.
   - Supports both Windows and Linux environments with platform-specific file paths.

6. **Remote Log Transmission**:

   - Sends collected data (keystrokes, clipboard content, user details, and browser history) to a Telegram Bot.
   - Supports periodic file transfers to ensure timely updates.

---

## **Project Architecture**

### **Core Components**

1. **Keyboard Listener**:

   - Built using the `pynput` library.
   - Listens for keypress events and logs them in real-time.

2. **Mouse Event Tracker (Planned)**:

   - Future implementation will track mouse clicks and scroll events using `pynput.mouse.Listener`.

3. **Clipboard Monitor**:

   - Utilizes the `pyperclip` library to access clipboard content.
   - Logs clipboard data at regular intervals.

4. **System Information Collector**:

   - Gathers user and system details using libraries like `os`, `platform`, `socket`, and `psutil`.

5. **Browser History Retriever**:

   - Reads SQLite databases (`History` for Chrome and `places.sqlite` for Firefox).
   - Supports platform-specific file paths for cross-compatibility.

6. **Telegram Bot Integration**:

   - Uses the `requests` library to send logs and files to a Telegram Bot.
   - Communicates with the Telegram Bot API using HTTPS requests.

7. **Persistence Mechanism (Planned)**:

   - Will implement platform-specific persistence:
     - Windows: Registry modification to run the script on startup.
     - Linux: Cron job creation for automatic execution on reboot.

### **Data Flow**

1. The script initializes and sets up keyboard and clipboard listeners.
2. Keystrokes, clipboard content, and active window data are logged in `systemlogs.txt`.
3. Browser history is accessed and saved in `chrome_history.txt` and `firefox_history.txt`.
4. Logs are periodically sent to the Telegram Bot.
5. (Planned) Persistence ensures the script starts automatically on system boot.

---

## **Code Structure**

### **File Structure**

- `keyboardAdapter.py`: The main script containing all functionality.
- `systemlogs.txt`: File for logging keystrokes, clipboard content, and active window data.
- `chrome_history.txt`: File for storing Chrome browsing history.
- `firefox_history.txt`: File for storing Firefox browsing history.

### **Key Functions**

1. **`log_key(key)`**:
   - Logs keystrokes with timestamps and active window titles.
2. **`get_user_details()`**:
   - Retrieves and formats user and system information.
3. **`get_clipboard_content()`**:
   - Fetches current clipboard content.
4. **`log_clipboard()`**:
   - Logs clipboard content at regular intervals.
5. **`get_chrome_history()`**** / ****`get_firefox_history()`**:
   - Retrieves browsing history from Chrome and Firefox databases.
6. **`send_file(log_file)`**:
   - Sends specified log files to the Telegram Bot.
7. **`add_to_persistence()`**** (Planned)**:
   - Implements platform-specific persistence.

---

## **Platform Compatibility**

- **Windows**:
  - Supports keystroke logging, clipboard monitoring, and browser history retrieval.
  - Uses the Windows Registry for persistence (planned).
- **Linux**:
  - Fully compatible with keystroke logging, clipboard monitoring, and browser history retrieval.
  - Utilizes cron jobs for persistence (planned).

---

## **Dependencies**

The project relies on the following Python libraries:

- `pynput`: For keyboard and mouse event tracking.
- `pyperclip`: For clipboard access.
- `psutil`: For system information retrieval.
- `requests`: For communicating with the Telegram Bot API.
- `sqlite3`: For accessing browser history databases.
- `os`, `platform`, `socket`: For system-specific operations.

Install dependencies using:

```bash
pip install pynput pyperclip psutil requests
```

---

## **Future Enhancements**

1. **Mouse Event Tracking**:
   - Capture mouse clicks (left, right, and middle) and scroll events.
   - Log events with timestamps and coordinates.
2. **Persistence**:
   - Ensure the keylogger starts automatically upon system boot.
   - Use registry entries for Windows and cron jobs for Linux.
3. **Enhanced Stealth**:
   - Obfuscate the script using `Cython`.
   - Compile the script into standalone executables for Windows and Linux.

---

## **Limitations**

1. Requires Python and dependencies installed on the target system (can be resolved by packaging the script).
2. May be flagged by antivirus or intrusion detection systems.
3. Limited browser support (currently only Chrome and Firefox).
4. Clipboard monitoring depends on platform-specific tools (e.g., `xclip` for Linux).

---

## **Ethical Considerations**

This keylogger is designed for educational purposes and must only be used with explicit permission from the system owner. Unauthorized use of keylogging software is illegal and unethical.

---

## **Conclusion**

The Keylogger project demonstrates a wide range of system monitoring capabilities, integrating multiple Python libraries and techniques to create a robust and extensible tool. With planned enhancements for mouse tracking and persistence, the project can serve as a foundation for further research and learning in system monitoring and automation. This documentation provides a comprehensive overview of the tool's functionality, implementation, and future goals.

