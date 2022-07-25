from tkinter import *
from main_widget import Dayswidget
from tkinter import messagebox
from datetime import datetime
import os
SAVING_PATH=os.path.join(os.path.dirname(__file__),"saving.pkl")
AUTO_TIME_SAVING=100
class APP(Tk):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        data=Dayswidget.load_file(SAVING_PATH,"rb") if os.path.exists(SAVING_PATH) else {}
        self.days_widget=Dayswidget(self,data)
        self.days_widget.forward(0)
        self.days_widget.active_by_day(datetime.now().date())
        self.days_widget.pack(fill=BOTH,expand=YES)

        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._auto_save()
    def _auto_save(self):
        self.days_widget.save_file(SAVING_PATH)
        self.after(AUTO_TIME_SAVING,self._auto_save)
    def _on_closing(self):
        for widget in self.days_widget:
            for achievment in widget:
                if not achievment.pausing_state and \
                    not achievment.failing and not achievment.end_target_state:
                    ansewer=messagebox.askyesnocancel("Quit", "Do you want to Pause all misions?")
                    if ansewer:
                        self.days_widget.pause_all(True)
                        self.days_widget.save_file(SAVING_PATH)
                        self.destroy()
                    elif ansewer==False:
                        self.destroy()
                    break       
            else:
                continue
            break
        else:
            self.destroy()
        
        
