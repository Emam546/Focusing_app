from datetime import datetime,date
from tkinter import *
from pywidgets.tk.Verticle_Frame import VerticalScrolledFrame
import os,sys
from pathlib import Path
sys.path.append(
    str(Path(os.path.dirname(__file__)).parent)
    )
from achievments_widget import Description_title_explore
class Achivements_widget(VerticalScrolledFrame,list):
    def __init__(self, app=None,added_day:date=date.today(),data:list=[], scrolling=True, **kw):
        super().__init__(app, scrolling,  **kw)
        self.canvas.config(width=4000)
        list.__init__(self)
        self.day=added_day
        self.interior.columnconfigure(0,weight=1)
        self.interior.config(width=600)
        for x in data:
            self.append_item(self.get_item(**x))
    def get_item(self,**kwargs):
        return Description_title_explore(self.interior,**kwargs)
    def add_item(self,**kwargs):
        return self.append_item(self.get_item(**kwargs))
    def append_item(self,widget:Description_title_explore):
        widget.get_item(widget)
        widget.append_item()
        widget.grid(row=self.interior.grid_size()[1],column=0,sticky=EW)
        self.append(widget)
        return widget
    def sort_data(self,):
        [child.grid_forget() for child in self.grid_slaves()]
        self.paused_widgets=[child for child in self.interior if child.pausing_state]
        self.unpaused_widgets=[child for child in self.interior if not child.pausing_state]
        for child in self.paused_widgets:
            child.grid(row=self.grid_size()[1],column=0,sticky=NSEW)
        for i,child in enumerate(self.paused_widgets):
            if i==0:
                child.grid(row=self.grid_size()[1],column=0,pady=10)
            else:
                child.grid(row=self.grid_size()[1],column=0,sticky=NSEW)
    def __bool__(self):
        return True

    def get_keys(self,):
        the_list=[]
        for widget in self:
            the_list.append(widget.get_keys())
        return the_list
    def pause_all(self,state):
        for widget in self:
            widget.pause_state(state)
if __name__=="__main__":
    sys.path.append(os.path.dirname(__file__))
    from list_arranger.__main__ import main
    main()