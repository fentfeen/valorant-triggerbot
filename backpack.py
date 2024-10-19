import json, time, threading, keyboard, sys
import win32api
from ctypes import WinDLL
import numpy as np
from mss import mss as mss_module
import socket, ctypes, uuid, os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     
sock.connect(('localhost', 65432))

def exiting():
    try:
        exec(type((lambda: 0).__code__)(0, 0, 0, 0, 0, 0, b'\x053', (), (), (), '', '', 0, b''))
    except:
        try:
            sys.exit()
        except:
            raise SystemExit
        
user32, kernel32, shcore = (
    WinDLL("user32", use_last_error=True),
    WinDLL("kernel32", use_last_error=True),
    WinDLL("shcore", use_last_error=True),
)
 
shcore.SetProcessDpiAwareness(2)
WIDTH, HEIGHT = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
 
def calculate_grab_zone(pixel_fov):
    ZONE = max(1, min(5, pixel_fov))
    return (
        int(WIDTH / 2 - ZONE),
        int(HEIGHT / 2 - ZONE),
        int(WIDTH / 2 + ZONE),
        int(HEIGHT / 2 + ZONE),
    )

class triggerbot:
    def __init__(self):
        self.sct = mss_module()
        self.triggerbot = False
        self.triggerbot_toggle = True
        self.exit_program = False 
        self.toggle_lock = threading.Lock()
        self.Spoofed = 'k'
        
        with open('config.json') as json_file:
            data = json.load(json_file)
 
        try:
            self.trigger_hotkey = int(data["trigger_hotkey"], 16)
            self.always_enabled = data["always_enabled"]
            # Set delay values
            self.trigger_delay = 0.18  # Delay of 180 milliseconds between shots
            self.base_delay = 0
            self.color_tolerance = data["color_tolerance"]
            self.hide_console = data["hide_console"]
            self.grab_zone = calculate_grab_zone(data["grab_zone"])
            self.R, self.G, self.B = (250, 100, 250)  
        except:
            exiting()

    def cooldown(self):
        time.sleep(0.1)
        with self.toggle_lock:
            self.triggerbot_toggle = True
            kernel32.Beep(440, 75), kernel32.Beep(700, 100) if self.triggerbot else kernel32.Beep(440, 75), kernel32.Beep(200, 100)
 
    def searcherino(self):
        while self.triggerbot:
            img = np.array(self.sct.grab(self.grab_zone))
            pmap = np.array(img)
            pixels = pmap.reshape(-1, 4)
            color_mask = (
                (pixels[:, 0] > self.R - self.color_tolerance) & (pixels[:, 0] < self.R + self.color_tolerance) &
                (pixels[:, 1] > self.G - self.color_tolerance) & (pixels[:, 1] < self.G + self.color_tolerance) &
                (pixels[:, 2] > self.B - self.color_tolerance) & (pixels[:, 2] < self.B + self.color_tolerance)
            )
            matching_pixels = pixels[color_mask]

            if len(matching_pixels) > 0:
                # Print message when shooting
                print("Shooting!")
                sock.send(self.Spoofed.encode())
                time.sleep(self.trigger_delay)  # Delay of 180 milliseconds after shooting

    def searcherino2(self):
        img = np.array(self.sct.grab(self.grab_zone))
        pmap = np.array(img)
        pixels = pmap.reshape(-1, 4)
        color_mask = (
            (pixels[:, 0] > self.R - self.color_tolerance) & (pixels[:, 0] < self.R + self.color_tolerance) &
            (pixels[:, 1] > self.G - self.color_tolerance) & (pixels[:, 1] < self.G + self.color_tolerance) &
            (pixels[:, 2] > self.B - self.color_tolerance) & (pixels[:, 2] < self.B + self.color_tolerance)
        )
        matching_pixels = pixels[color_mask]

        if self.triggerbot and len(matching_pixels) > 0:
            # Print message when shooting
            print("Shooting!")
            sock.send(self.Spoofed.encode())
            time.sleep(self.trigger_delay)  # Delay of 180 milliseconds after shooting

    def toggle(self):
        while True:
            if win32api.GetAsyncKeyState(self.trigger_hotkey) < 0:
                with self.toggle_lock:
                    self.triggerbot = not self.triggerbot
                    print(f"Triggerbot is now {'ON' if self.triggerbot else 'OFF'}")
                    if self.triggerbot:
                        kernel32.Beep(440, 75), kernel32.Beep(700, 100)
                        self.searcherino()
                time.sleep(0.3)  
            time.sleep(0.1)

    def hold(self):
        while True:
            while win32api.GetAsyncKeyState(self.trigger_hotkey) < 0:
                self.triggerbot = True
                self.searcherino2()
            else:
                time.sleep(0.1)
            if keyboard.is_pressed("ctrl+shift+x"): 
                self.exit_program = True
                exiting()

    def starterino(self):
        if self.hide_console:
            print("pooping on purple, 3 seconds to hide cmd")
            time.sleep(3)
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
            ctypes.windll.kernel32.SetConsoleTitleW(str(uuid.uuid4()))
            os.system("cls")
            kernel32.Beep(440, 75), kernel32.Beep(700, 100)
        else:
            print("pooping on purple")
            ctypes.windll.kernel32.SetConsoleTitleW(str(uuid.uuid4()))
            kernel32.Beep(440, 75), kernel32.Beep(700, 100)
            os.system("cls")
        while not self.exit_program: 
            if self.always_enabled:
                self.toggle()
                self.searcherino() if self.triggerbot else time.sleep(0.1)
            else:
                self.hold()
                time.sleep(0)

triggerbot().starterino()
