import tkinter as tk
from tkinter import ttk
import psutil
import threading
import ctypes
import subprocess
import os

# force all internal subprocess calls (like GPUtil checking nvidia-smi) to stay hidden on Windows
if os.name == 'nt':
    _original_popen = subprocess.Popen
    class _HiddenPopen(_original_popen):
        def __init__(self, *args, **kwargs):
            if 'startupinfo' not in kwargs:
                suinfo = subprocess.STARTUPINFO()
                suinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                suinfo.wShowWindow = subprocess.SW_HIDE
                kwargs['startupinfo'] = suinfo
            if 'creationflags' not in kwargs:
                kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
            super().__init__(*args, **kwargs)
    subprocess.Popen = _HiddenPopen

try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

# Helper to make Windows native title bars dark
def set_window_dark_mode(window, dark=True):
    try:
        window.update()
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
        hwnd = window.winfo_id()
        value = 1 if dark else 0
        set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(ctypes.c_int(value)), ctypes.sizeof(ctypes.c_int))
    except Exception:
        pass

# Color Palettes
THEMES = {
    "light": {
        "bg": "#f0f0f0",
        "fg": "#000000",
        "header_bg": "#f0f0f0",
        "widget_bg": "#ffffff",
        "bar_trough": "#dddddd",
        "bar_color": "#28a745",
        "canvas_bg": "#ffffff",
        "line_color": "#007acc",
        "write_color": "#d9534f"
    },
    "dark": {
        "bg": "#1e1e1e",
        "fg": "#ffffff",
        "header_bg": "#1e1e1e",
        "widget_bg": "#2d2d2d",
        "bar_trough": "#3c3c3c",
        "bar_color": "#4caf50",
        "canvas_bg": "#252526",
        "line_color": "#4ec9b0",
        "write_color": "#ce9178"
    }
}

class ResourceMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows Resource Monitor")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.current_theme = "dark"

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.max_history = 30
        self.cpu_history = [0] * self.max_history
        self.ram_history = [0] * self.max_history
        self.gpu_history = [0] * self.max_history
        self.read_history = [0] * self.max_history
        self.write_history = [0] * self.max_history

        # top header frame
        self.header_frame = tk.Frame(root)
        self.header_frame.pack(fill="x", padx=25, pady=10)

        self.title_label = tk.Label(self.header_frame, text="System Resource Monitor", font=("Helvetica", 13, "bold"))
        self.title_label.pack(side="left")

        self.settings_btn = tk.Button(self.header_frame, text="⚙", font=("Helvetica", 14), bd=0, relief="flat", cursor="hand2", command=self.open_settings)
        self.settings_btn.pack(side="right")

        # cpu usage
        self.cpu_label = tk.Label(root, text="CPU Usage: 0%", font=("Helvetica", 10, "bold"))
        self.cpu_label.pack(anchor="w", padx=30)        
        self.cpu_canvas = tk.Canvas(root, width=340, height=45, highlightthickness=0)
        self.cpu_canvas.pack(pady=(2,8))
        
        # ram usage
        self.ram_label = tk.Label(root, text="RAM Usage: 0%", font=("Helvetica", 10, "bold"))
        self.ram_label.pack(anchor="w", padx=30)
        self.ram_canvas = tk.Canvas(root, width=340, height=45, highlightthickness=0)
        self.ram_canvas.pack(pady=(2,8))

        # gpu usage
        self.gpu_label = tk.Label(root, text="GPU Usage: Not available/supported", font=("Helvetica", 10, "bold"))
        self.gpu_label.pack(anchor="w", padx=30)        
        self.gpu_canvas = tk.Canvas(root, width=340, height=45, highlightthickness=0)
        self.gpu_canvas.pack(pady=(2,8))

        # disk read
        self.read_label = tk.Label(root, text="Disk Read: 0 B/s", font=("Helvetica", 9, "bold"))
        self.read_label.pack(anchor="w", padx=30)
        self.read_canvas = tk.Canvas(root, width=340, height=40, highlightthickness=0)
        self.read_canvas.pack(pady=(2, 6))

        # disk write
        self.write_label = tk.Label(root, text="Disk Write: 0 B/s", font=("Helvetica", 9, "bold"))
        self.write_label.pack(anchor="w", padx=30)
        self.write_canvas = tk.Canvas(root, width=340, height=40, highlightthickness=0)
        self.write_canvas.pack(pady=(2, 10))

        self.apply_theme()

        self.running = True
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.monitor_thread = threading.Thread(target=self.background_monitor, daemon=True)
        self.monitor_thread.start()

    def apply_theme(self):
        t = THEMES[self.current_theme]
        
        self.root.configure(bg=t["bg"])
        self.header_frame.configure(bg=t["header_bg"])
        self.title_label.configure(bg=t["header_bg"], fg=t["fg"])
        self.settings_btn.configure(bg=t["header_bg"], fg=t["fg"], activebackground=t["bg"], activeforeground=t["fg"])

        for lbl in [self.cpu_label, self.ram_label, self.gpu_label, self.read_label, self.write_label]:
            lbl.configure(bg=t["bg"], fg=t["fg"])

        for canvas in [self.cpu_canvas, self.ram_canvas, self.gpu_canvas, self.read_canvas, self.write_canvas]:
            canvas.configure(bg=t["canvas_bg"])

        set_window_dark_mode(self.root, dark=(self.current_theme == "dark"))
        self.redraw_graphs()

    def open_settings(self):
        t = THEMES[self.current_theme]
        
        settings_win = tk.Toplevel(self.root)
        settings_win.title("Settings")
        settings_win.geometry("260x200")
        settings_win.resizable(False, False)
        settings_win.configure(bg=t["bg"])
        settings_win.grab_set()

        set_window_dark_mode(settings_win, dark=(self.current_theme == "dark"))

        lbl = tk.Label(settings_win, text="Monitor Settings", font=("Helvetica", 12, "bold"), bg=t["bg"], fg=t["fg"])
        lbl.pack(pady=15)

        dark_var = tk.BooleanVar(value=(self.current_theme == "dark"))

        def toggle_theme():
            self.current_theme = "dark" if dark_var.get() else "light"
            self.apply_theme()
            
            new_t = THEMES[self.current_theme]
            settings_win.configure(bg=new_t["bg"])
            lbl.configure(bg=new_t["bg"], fg=new_t["fg"])
            chk.configure(bg=new_t["bg"], fg=new_t["fg"], selectcolor=new_t["widget_bg"], 
                          activebackground=new_t["bg"], activeforeground=new_t["fg"])
            # update button colors and active states to match theme
            close_btn.configure(bg=new_t["widget_bg"], fg=new_t["fg"], 
                                activebackground=new_t["bg"], activeforeground=new_t["fg"])
            set_window_dark_mode(settings_win, dark=(self.current_theme == "dark"))

        chk = tk.Checkbutton(settings_win, text="Dark Mode", variable=dark_var, command=toggle_theme,
                             bg=t["bg"], fg=t["fg"], selectcolor=t["widget_bg"], 
                             activebackground=t["bg"], activeforeground=t["fg"])
        chk.pack(anchor="w", padx=30, pady=10)

        close_btn = tk.Button(settings_win, text="Close", width=10, command=settings_win.destroy,
                              bg=t["widget_bg"], fg=t["fg"], activebackground=t["bg"], activeforeground=t["fg"], bd=1, relief="solid")
        close_btn.pack(pady=15)

    def background_monitor(self):
        last_disk_io = psutil.disk_io_counters()
        
        while self.running:
            cpu_usage = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory()
            
            gpu_usage = 0
            if GPU_AVAILABLE:
                try:
                    gpus = GPUtil.getGPUs()
                    if gpus:
                        gpu_usage = int(gpus[0].load * 100)
                except Exception:
                    pass

            current_disk_io = psutil.disk_io_counters()
            read_speed = current_disk_io.read_bytes - last_disk_io.read_bytes
            write_speed = current_disk_io.write_bytes - last_disk_io.write_bytes
            last_disk_io = current_disk_io

            read_kb = read_speed / 1024
            write_kb = write_speed / 1024

            read_str = self.format_bytes(read_speed)
            write_str = self.format_bytes(write_speed)

            self.cpu_history.append(cpu_usage)
            self.cpu_history.pop(0)

            self.ram_history.append(ram.percent)
            self.ram_history.pop(0)

            self.gpu_history.append(gpu_usage)
            self.gpu_history.pop(0)

            self.read_history.append(read_kb)
            self.read_history.pop(0)

            self.write_history.append(write_kb)
            self.write_history.pop(0)

            self.root.after(0, self.update_ui, cpu_usage, ram, gpu_usage, read_str, write_str)

    def update_ui(self, cpu_usage, ram, gpu_usage, read_str, write_str):
        self.cpu_label.config(text=f"CPU Usage: {cpu_usage}%")

        ram_usage = ram.percent
        used_gb = ram.used // (1024**3)
        total_gb = ram.total // (1024**3)
        self.ram_label.config(text=f"RAM Usage: {ram_usage}% ({used_gb} GB / {total_gb} GB)")

        if GPU_AVAILABLE:
            self.gpu_label.config(text=f"GPU Usage: {gpu_usage}%")
        else:
            self.gpu_label.config(text="GPU Usage: N/A")

        self.read_label.config(text=f"Disk Read: {read_str}/s")
        self.write_label.config(text=f"Disk Write: {write_str}/s")

        self.redraw_graphs()

    def redraw_graphs(self):
        t = THEMES[self.current_theme]
        line_color = t["line_color"]
        write_color = t["write_color"]

        self.draw_line_chart(self.cpu_canvas, self.cpu_history, 100, line_color, height=45)
        self.draw_line_chart(self.ram_canvas, self.ram_history, 100, line_color, height=45)
        self.draw_line_chart(self.gpu_canvas, self.gpu_history, 100, line_color, height=45)
        
        max_read = max(max(self.read_history), 1024)
        self.draw_line_chart(self.read_canvas, self.read_history, max_read, line_color, height=40)

        max_write = max(max(self.write_history), 1024)
        self.draw_line_chart(self.write_canvas, self.write_history, max_write, write_color, height=40)

    def draw_line_chart(self, canvas, data, max_val, color, height=45):
        canvas.delete("all")
        width = 340
        n = len(data)
        if n < 2 or max_val <= 0:
            return

        step_x = width / (n - 1)
        points = []

        for i, val in enumerate(data):
            x = i * step_x
            # clamp valute between 0 and max_val
            clamped_val = max(0, min(val, max_val))
            # invert y axis for drawing
            y = height - (clamped_val / max_val) * (height - 6) - 3
            points.append((x, y))

        # flatten list of tuple for create_line    
        flat_points = [coord for pt in points for coord in pt]
        canvas.create_line(flat_points, fill=color, width=2, smooth=True)

    def format_bytes(self, byte_value):
        if byte_value > 1024 * 1024:
            return f"{byte_value / (1024 * 1024):.1f} MB"
        elif byte_value > 1024:
            return f"{byte_value / 1024:.1f} KB"
        else:
            return f"{byte_value} B"

    def on_close(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ResourceMonitor(root)
    root.mainloop()