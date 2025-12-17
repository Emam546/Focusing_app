from pathlib import Path
from tkinter import *
from src.main_widget import DaysWidget
from tkinter import messagebox
from datetime import datetime
import os
import threading
import sys
import pystray
from PIL import Image, ImageTk

from src.utils import resource_path


def get_app_data_dir(app_name="Focusing"):
    base = Path(os.getenv("APPDATA", Path.home()))
    app_dir = base / app_name
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir


SAVE_DIR = get_app_data_dir("Focusing")
SAVING_PATH = SAVE_DIR / "saving.json"
AUTO_TIME_SAVING = 1000
ICON_IMAGE = resource_path("public/icon.ico")


class APP(Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        data = DaysWidget.load_file(SAVING_PATH, "r")
        self.days_widget = DaysWidget(self, data)
        self.days_widget.active_by_day(datetime.now().date())
        self.days_widget.pack(fill=BOTH, expand=YES)
        # self.iconbitmap(default=ICON_IMAGE)
        self.iconbitmap(ICON_IMAGE)
        tk_img = ImageTk.PhotoImage(Image.open(ICON_IMAGE))
        self.iconphoto(True, tk_img)

        self.protocol("WM_DELETE_WINDOW", self._on_window_closing)
        self._auto_save()
        threading.Thread(target=self.create_tray, daemon=True).start()

    def _on_window_closing(self):
        self.days_widget.save_file(SAVING_PATH)
        self.withdraw()

    def _auto_save(self):
        self.days_widget.save_file(SAVING_PATH)
        self.after(AUTO_TIME_SAVING, self._auto_save)

    def create_tray(self):
        def on_quit(icon, item):
            icon.stop()
            self._on_closing()
            sys.exit()

        def on_show(icon, item):
            self.deiconify()  # show window
            self.after(0, self.lift)  # bring to front

        def on_double_click(icon, item=None):
            self.deiconify()
            self.after(0, self.lift)

        tray_icon_image = Image.open(ICON_IMAGE)
        icon = pystray.Icon(
            "Focusing App",
            tray_icon_image,
            "Focusing App",
            menu=pystray.Menu(
                pystray.MenuItem("Show App", on_show), pystray.MenuItem("Quit", on_quit)
            ),
        )
        icon.run_detached(on_double_click)
        icon.run()
        return icon

    def _on_closing(self):
        for widget in self.days_widget:
            for achievment in widget:
                if (
                    not achievment.pausing_state
                    and not achievment.failing
                    and not achievment.end_target_state
                ):
                    answer = messagebox.askyesnocancel(
                        "Quit", "Do you want to Pause all missions?"
                    )
                    if answer:
                        self.days_widget.pause_all(True)
                        self.days_widget.save_file(SAVING_PATH)
                        self.destroy()
                    elif answer == False:
                        self.destroy()
                    break
            else:
                continue
            break
        else:
            self.destroy()
