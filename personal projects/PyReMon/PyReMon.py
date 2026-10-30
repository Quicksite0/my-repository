import tkinter as tk
from tkinter import ttk
import psutil
import threading
import ctypes

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
        "bar_color": "#28a745"
    },
    "dark": {
        "bg": "#1e1e1e",
        "fg": "#ffffff",
        "header_bg": "#1e1e1e",
        "widget_bg": "#2d2d2d",
        "bar_trough": "#3c3c3c",
        "bar_color": "#4caf50"
    }
}

class ResourceMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows Resource Monitor")
        self.root.geometry("400x390")
        self.root.resizable(False, False)

        self.current_theme = "light"

        self.style = ttk.Style()
        self.style.theme_use('clam')

        # --- Top Header Frame ---
        self.header_frame = tk.Frame(root)
        self.header_frame.pack(fill="x", padx=25, pady=10)

        self.title_label = tk.Label(self.header_frame, text="System Resource Monitor", font=("Helvetica", 13, "bold"))
        self.title_label.pack(side="left")

        self.settings_btn = tk.Button(self.header_frame, text="⚙", font=("Helvetica", 14), bd=0, relief="flat", cursor="hand2", command=self.open_settings)
        self.settings_btn.pack(side="right")

        # --- CPU Usage ---
        self.cpu_label = tk.Label(root, text="CPU Usage: 0%", font=("Helvetica", 10))
        self.cpu_label.pack(anchor="w", padx=30)
        
        self.cpu_bar = ttk.Progressbar(root, orient="horizontal", length=340, mode="determinate")
        self.cpu_bar.pack(pady=5)

        # --- RAM Usage ---
        self.ram_label = tk.Label(root, text="RAM Usage: 0%", font=("Helvetica", 10))
        self.ram_label.pack(anchor="w", padx=30)
        
        self.ram_bar = ttk.Progressbar(root, orient="horizontal", length=340, mode="determinate")
        self.ram_bar.pack(pady=5)

        # --- GPU Usage ---
        self.gpu_label = tk.Label(root, text="GPU Usage: N/A", font=("Helvetica", 10))
        self.gpu_label.pack(anchor="w", padx=30)
        
        self.gpu_bar = ttk.Progressbar(root, orient="horizontal", length=340, mode="determinate")
        self.gpu_bar.pack(pady=5)

        # --- Disk Activity ---
        self.disk_label = tk.Label(root, text="Disk Activity — Read: 0 KB/s | Write: 0 KB/s", font=("Helvetica", 10))
        self.disk_label.pack(anchor="w", padx=30, pady=(10, 5))

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

        for lbl in [self.cpu_label, self.ram_label, self.gpu_label, self.disk_label]:
            lbl.configure(bg=t["bg"], fg=t["fg"])

        self.style.configure("TProgressbar", 
                             troughcolor=t["bar_trough"], 
                             background=t["bar_color"], 
                             bordercolor=t["bg"], 
                             lightcolor=t["bar_color"], 
                             darkcolor=t["bar_color"])

        set_window_dark_mode(self.root, dark=(self.current_theme == "dark"))

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
            # Properly update button colors and active states to match theme
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

            read_str = self.format_bytes(read_speed)
            write_str = self.format_bytes(write_speed)

            self.root.after(0, self.update_ui, cpu_usage, ram, gpu_usage, read_str, write_str)

    def update_ui(self, cpu_usage, ram, gpu_usage, read_str, write_str):
        self.cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
        self.cpu_bar['value'] = cpu_usage

        ram_usage = ram.percent
        used_gb = ram.used // (1024**3)
        total_gb = ram.total // (1024**3)
        self.ram_label.config(text=f"RAM Usage: {ram_usage}% ({used_gb} GB / {total_gb} GB)")
        self.ram_bar['value'] = ram_usage

        if GPU_AVAILABLE:
            self.gpu_label.config(text=f"GPU Usage: {gpu_usage}%")
            self.gpu_bar['value'] = gpu_usage
        else:
            self.gpu_label.config(text="GPU Usage: N/A")

        self.disk_label.config(text=f"Disk Activity — Read: {read_str}/s | Write: {write_str}/s")

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