
import threading
import time
from pynput import keyboard

stop_event = threading.Event()
def task1():
    while not stop_event.is_set():
        print("🟢 Task 1 đang chạy...")
        time.sleep(1)

def task2():
    while not stop_event.is_set():
        print("🔵 Task 2 đang chạy...")
        time.sleep(1)

def on_release(key):
    if key == keyboard.Key.esc:
        stop_event.set()
        print("Thoát chương trình.")
        return False  # Dừng listener
    
def key_listener():
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()
      
t1 = threading.Thread(target=task1)
t2 = threading.Thread(target=task2)
t_key = threading.Thread(target=key_listener)

t1.start()
t2.start()
t_key.start()
