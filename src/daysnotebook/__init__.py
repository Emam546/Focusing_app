import tkinter as tk
from tkinter import *
from pywidgets.tk.Notebook.note_origin import Switcher_window
import datetime
import calendar


def week_days(time:datetime.date=datetime.date.today()):
    week_index=calendar.weekday(time.year,time.month,time.day)
    weekdays=[]
    for day in range(1,7-week_index):
        weekdays.append(time+datetime.timedelta(day))

    for day in range(0,week_index+1):
        weekdays.append(time-datetime.timedelta(day))
    weekdays=list(set(weekdays))
    weekdays.sort(key=datetime.datetime.weekday)
    return weekdays

class Dayswidget(Switcher_window):
    def __init__(self, app=None, data: dict = {}, **kwargs):
        super().__init__(app, **kwargs)


class circle_label(Canvas):
    def _create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

    def findXCenter(self, item):
        coords = self.bbox(item)
        xOffset = (self.winfo_width() / 2) - ((coords[2] - coords[0]) / 2)
        return xOffset

    def text_on_canvas(self, infoText):
        self.textID = self.create_text(
            0, 0, text=infoText, anchor="nw", fill="yellow")
        self.textID
        xOffset = self.findXCenter(self.textID)
        self.move(self.textID, xOffset, 0)

class Updated_weekdays_frame(Frame):
    def __init__(self,app=None,**kwargs):
        super().__init__(app,**kwargs)
        day=datetime.date.today()
        weekdays = week_days(day)
        for column,day in enumerate(weekdays):
            Label(self,text=day.strftime("%a")).grid(row=0,column=column,sticky=NSEW)
            self.columnconfigure(column,weight=1)
    def time(self,day:datetime.date):
        assert(type(day)==datetime.date)
        for child in self.grid_slaves(row=1):
            child.destroy()
        weekdays = week_days(day)
        for column,day in enumerate(weekdays):
            Label(self,text=str(day.day)).grid(row=1,column=column,sticky=NSEW)
        return weekdays
            
        
class Title_widget(Frame):
    def __init__(self, app=None, **kwargs):
        super().__init__(app, **kwargs)
        self.back_button=Button(self,text="<<",command=lambda:self.forward(-1))
        self.container = Updated_weekdays_frame(self)
        self.forward_button=Button(self,text=">>",command=lambda:self.forward(1))
        self.current_time=datetime.date.today()

        self.columnconfigure(1,weight=1)
        self.rowconfigure(0,weight=1)

        self.back_button.grid(row=0,column=0,sticky=NS)
        self.container.grid(row=0,column=1,sticky=NSEW)
        self.forward_button.grid(row=0,column=2,sticky=NS)
    def forward(self,forward):
        self.current_time+=datetime.timedelta(weeks=1)*forward
        return self.container.time(self.current_time)
def main():
    root=Tk()
    text_widget=Title_widget(root)
    text_widget.forward(0)
    text_widget.pack(fill=BOTH,expand=YES)
    root.mainloop()
if __name__=="__main__":
    main()
