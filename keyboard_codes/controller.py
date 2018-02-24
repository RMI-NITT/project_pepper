"""
Code to detect keyboard interrupts and print the requisite velocities to the terminal
"""
from pynput import keyboard

print "Press up for forward\nPress down for reverse\nPress left for left\nPress right for right\n" \
+ "Press s for stop\nPress escape to exit\n"

ls = 0
rs = 0

def on_press(key):
    global ls, rs
    try:
        a = key.char
        if a == 's':
            ls = 0
            rs = 0
    except AttributeError:
        if key == keyboard.Key.up:
            if ls < 255:
                ls += 1
            if ls < 0:
                ls = 0
            if rs > -255:
                rs -= 1
            if rs > 0:
                rs = 0
        elif key == keyboard.Key.down:
            if ls > -255:
                ls -= 1
            if ls > 0:
                ls = 0
            if rs < 255:
                rs += 1
            if rs < 0:
                rs = 0
        elif key == keyboard.Key.left:
            ls = 0
            if rs > -255:
                rs -= 1
            if rs > 0:
                rs = 0
        elif key == keyboard.Key.right:
            rs = 0
            if ls < 255:
                ls += 1
            if ls < 0:
                ls = 0
        
        print ls, rs

def on_release(key):
    # print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
