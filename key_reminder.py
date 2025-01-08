import tkinter as tk
from tkinter import ttk
import keyboard
import threading
import time
import winsound
import json
import os

class KeyReminderApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("키 알리미")
        self.root.geometry("300x200")
        
        # 설정 저장 파일 경로
        self.config_file = "key_reminder_config.json"
        
        # 설정값 초기화
        self.target_key = ""
        self.delay_time = 0
        self.is_running = False
        self.monitor_thread = None
        
        self.load_config()
        self.create_gui()
        
        # 설정이 있으면 자동으로 모니터링 시작
        if self.target_key and self.delay_time > 0:
            self.start_monitoring()
            self.status_label.config(text="모니터링 중...")
    
    def create_gui(self):
        # 키 입력 프레임
        key_frame = ttk.LabelFrame(self.root, text="키 설정")
        key_frame.pack(padx=10, pady=5, fill="x")
        
        self.key_entry = ttk.Entry(key_frame, state='readonly')
        self.key_entry.pack(padx=5, pady=5, fill="x")
        
        key_button = ttk.Button(key_frame, text="키 입력 받기", command=self.get_key)
        key_button.pack(padx=5, pady=5)
        
        # 시간 설정 프레임
        time_frame = ttk.LabelFrame(self.root, text="알림 시간 설정(초)")
        time_frame.pack(padx=10, pady=5, fill="x")
        
        self.time_entry = ttk.Entry(time_frame)
        self.time_entry.insert(0, str(self.delay_time))
        self.time_entry.pack(padx=5, pady=5, fill="x")
        
        # 저장 버튼
        save_button = ttk.Button(self.root, text="설정 저장", command=self.save_settings)
        save_button.pack(padx=10, pady=5)
        
        # 상태 표시 레이블
        self.status_label = ttk.Label(self.root, text="대기 중")
        self.status_label.pack(padx=10, pady=5)
        
        # 저장된 ��가 있으면 표시
        if self.target_key:
            self.key_entry.config(state='normal')
            self.key_entry.delete(0, tk.END)
            self.key_entry.insert(0, self.target_key)
            self.key_entry.config(state='readonly')
    
    def get_key(self):
        key_window = tk.Toplevel(self.root)
        key_window.title("키 입력")
        key_window.geometry("200x100")
        
        label = ttk.Label(key_window, text="아무 키나 누르세요...")
        label.pack(pady=20)
        
        def on_key(event):
            self.target_key = event.keysym.lower()  # 소문자로 변환
            self.key_entry.config(state='normal')
            self.key_entry.delete(0, tk.END)
            self.key_entry.insert(0, self.target_key)
            self.key_entry.config(state='readonly')
            key_window.destroy()
            
        key_window.bind('<Key>', on_key)
        key_window.focus_force()
        
    def save_settings(self):
        try:
            self.delay_time = float(self.time_entry.get())
            config = {
                "target_key": self.target_key,
                "delay_time": self.delay_time
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
            
            self.start_monitoring()
            self.status_label.config(text="모니터링 중...")
            
        except ValueError:
            self.status_label.config(text="올바른 시간을 입력하세요")
    
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.target_key = config.get("target_key", "").lower()  # 소문자로 변환
                    self.delay_time = config.get("delay_time", 0)
            except Exception as e:
                print(f"설정 파일 로드 중 오류: {e}")
                self.target_key = ""
                self.delay_time = 0
    
    def key_monitor(self):
        def on_key_event():
            winsound.Beep(2500, 300)
        
        keyboard.on_press_key(self.target_key, lambda _: threading.Timer(self.delay_time, on_key_event).start())
        
        while self.is_running:
            time.sleep(1)
    
    def start_monitoring(self):
        if self.monitor_thread is not None:
            self.is_running = False
            self.monitor_thread.join()
        
        self.is_running = True
        self.monitor_thread = threading.Thread(target=self.key_monitor)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = KeyReminderApp()
    app.run() 