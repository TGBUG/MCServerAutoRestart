import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import psutil
import time
import subprocess
import threading
import json
import os

CONFIG_FILE = "config.bug"

def load_config():
    """加载配置文件"""
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump({"servers": []}, f, indent=4)
        log(f"配置文件 {CONFIG_FILE} 已创建，请添加服务器路径后重启程序。")
        return {"servers": []}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def is_process_running_by_cmdline(bat_path):
    """通过命令行参数检查是否有对应的 bat 进程"""
    for process in psutil.process_iter():
        try:
            if bat_path in " ".join(process.cmdline()):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def start_server(bat_path):
    """启动服务器"""
    while a == 1:
        if not is_process_running_by_cmdline(bat_path):
            log(f"未检测到 {bat_path}对应的服务器，正在尝试重新启动...")
            subprocess.Popen(
                ['start', 'cmd', '/k', bat_path],
                shell=True,
                cwd=os.path.dirname(bat_path)
            )
        time.sleep(1)

def log(message):
    """输出日志到界面（异步调用）"""
    def _write_log():
        text_box.config(state=tk.NORMAL)
        text_box.insert(tk.END, message + "\n")
        text_box.see(tk.END)
        text_box.config(state=tk.DISABLED)
    root.after(1, _write_log)

def on_button_click():
    """处理按钮点击事件"""
    global a
    if button["text"] == "开启":
        button.config(bg="red", text="关闭")
        a = 0
    else:
        button.config(bg="green", text="开启")
        a = 1

    def start_threads():
        if a == 1:
            log("监控已启动...")
            for bat_path in config["servers"]:
                server_thread = threading.Thread(target=start_server, args=(bat_path,))
                server_thread.daemon = True
                server_thread.start()
        else:
            log("监控已停止...")

    root.after(10, start_threads)

# 初始化 Tkinter 界面
a = 1
root = tk.Tk()
root.title("自动重启")

# 日志输出框
text_box = ScrolledText(root, width=80, height=20, state=tk.DISABLED)
text_box.pack(padx=10, pady=10)

# 按钮
button = tk.Button(root, text="开启", bg="green", command=on_button_click)
button.pack(pady=20)

# 加载配置文件
config = load_config()
if not config["servers"]:
    log("配置文件为空，请在 config.bug 中添加服务器启动脚本路径！")
    root.mainloop()
    exit(1)

log("程序启动完成，双击底部按钮以启动监控")
root.mainloop()
