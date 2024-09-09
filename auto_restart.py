import tkinter as tk
import psutil
import time
import subprocess
import threading

def is_process_running(process_name):
    for process in psutil.process_iter():
        try:
            if process_name.lower() in process.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def start_server():
    while a == 1:
        if not is_process_running("java.exe"):
            subprocess.Popen(['start', 'cmd', '/k', r'StartServer.bat'], shell=True)
        time.sleep(1)

def on_button_click():
    global a
    if button["text"] == "开启":
        button.config(bg="red", text="关闭")
        a = 0
    else:
        button.config(bg="green", text="开启")
        a = 1

    if a == 1:
        server_thread = threading.Thread(target=start_server)
        server_thread.daemon = True
        server_thread.start()

a = 1

root = tk.Tk()
root.title("自动重启")

button = tk.Button(root, text="开启", bg="green", command=on_button_click)
button.pack(pady=20)

root.mainloop()
