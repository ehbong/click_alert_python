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
        self.root.geometry("300x300")
        
        # 설정 저장 파일 경로
        self.config_file = "key_reminder_config.json"
        
        # 설정값 초기화
        self.target_key = ""
        self.delay_time = 0
        self.is_running = False
        self.monitor_thread = None
        self.keyboard_handler = None  # 키보드 핸들러 추적을 위한 변수 추가
        self.current_immediate_sound = True  # 현재 적용된 설정 저장
        self.immediate_sound = tk.BooleanVar(value=True)  # GUI 표시용 설정
        
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
        
        # 즉시 알림음 설정 체크박스 추가
        sound_frame = ttk.LabelFrame(self.root, text="알림음 설정")
        sound_frame.pack(padx=10, pady=5, fill="x")
        
        self.sound_check = ttk.Checkbutton(
            sound_frame, 
            text="키 입력 시 알림음",
            variable=self.immediate_sound
        )
        self.sound_check.pack(padx=5, pady=5)
        
        # 저장 버튼
        save_button = ttk.Button(self.root, text="설정 적용 및 저장", command=self.save_settings)
        save_button.pack(padx=10, pady=5)
        
        # 상태 표시 레이블
        self.status_label = ttk.Label(self.root, text="대기 중")
        self.status_label.pack(padx=10, pady=5)
        
        # 저장된 키가 있으면 표시
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
            # 현재 설정 업데이트
            self.current_immediate_sound = self.immediate_sound.get()
            
            config = {
                "target_key": self.target_key,
                "delay_time": self.delay_time,
                "immediate_sound": self.current_immediate_sound
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
                    self.target_key = config.get("target_key", "").lower()
                    self.delay_time = config.get("delay_time", 0)
                    # 두 설정 모두 업데이트
                    self.current_immediate_sound = config.get("immediate_sound", True)
                    self.immediate_sound.set(self.current_immediate_sound)
            except Exception as e:
                print(f"설정 파일 로드 중 오류: {e}")
                self.target_key = ""
                self.delay_time = 0
                self.current_immediate_sound = True
                self.immediate_sound.set(True)
    
    def key_monitor(self):
        def on_key_event(e):
            # 저장된 설정값 사용
            if self.current_immediate_sound:
                winsound.Beep(1000, 200)
            threading.Timer(self.delay_time, lambda: winsound.Beep(2500, 300)).start()
        
        try:
            # 이전 핸들러가 있다면 제거
            if self.keyboard_handler:
                keyboard.unhook_key(self.target_key)
                self.keyboard_handler = None
            
            # 새로운 핸들러 등록 및 저장
            self.keyboard_handler = on_key_event  # 직접 이벤트 핸들러 함수 사용
            keyboard.on_press_key(self.target_key, self.keyboard_handler)
            
            while self.is_running:
                time.sleep(1)
                
        except Exception as e:
            print(f"키 모니터링 중 오류 발생: {e}")
            self.status_label.config(text="모니터링 오류")
    
    def start_monitoring(self):
        # 이전 모니터링 중지
        if self.monitor_thread is not None:
            self.is_running = False
            if self.keyboard_handler:
                keyboard.unhook_key(self.target_key)
                self.keyboard_handler = None  # 핸들러 초기화
            self.monitor_thread.join()
        
        # 약간의 지연 추가
        time.sleep(0.1)
        
        # 새로운 모니터링 시작
        self.is_running = True
        self.monitor_thread = threading.Thread(target=self.key_monitor)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = KeyReminderApp()
    app.run() 