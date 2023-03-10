from functools import partial
from tkinter import *
from pywidgets.tk.Notebook.note_origin import Switcher_window
from datetime import datetime, timedelta,date
from .list_arranger import Achievement_widget as _Achievement_widget ,Description_title_explore
from .daysnotebook import Title_widget
from pywidgets.tk.func import bind_all_childes
import pickle
class Achievement_widget(_Achievement_widget):
    def append_item(self, widget: Description_title_explore,menu=True):
        super().append_item(widget)
        def destroy():
            widget.destroy()
            self.remove(widget)
        def popemenu():
            add_menu_pope.tk_popup(self.winfo_pointerx(),self.winfo_pointery())
        add_menu_pope=Menu(self.winfo_toplevel(),tearoff=False)
        add_menu_pope.add_command(label="remove",command=destroy)
        bind_all_childes(widget.title_frame,lambda e:popemenu(),"<Button-3>","")
        return widget
class Dayswidget(Switcher_window):
    def __init__(self, app=None ,data: dict = {}, **kwargs):
        super().__init__(app, **kwargs)
        self.title_widget=Label(self,anchor=W)
        self.title_frame=Title_widget(self)
        self.data=data
        self.container_frame=Frame(self)
        self.title_frame.forward=self.forward
        self.columnconfigure(0,weight=1)
        self.rowconfigure(2,weight=1)

        self.title_frame.grid(row=0,column=0,sticky=EW)
        self.title_widget.grid(row=1,column=0,sticky=EW)
        
        self.container_frame.grid(row=2,column=0,sticky=NSEW)
        today=date.today()
        the_day_data=data[today] if today in data else []
        self.add(today,the_day_data)
        
        #this is for when moving from side to another side
        self._current_active_week=0
        self.active_week_day={0:today.weekday()}
        self.forward(0)

    def forward(self,forward):
        days=self.title_frame.__class__.forward(self.title_frame,forward)
        for i,day in enumerate(days):
            the_day_data=self.data[day] if day in self.data else []
            widget=self.add(day,the_day_data)
            for label in self.title_frame.container.grid_slaves(column=i):
                label.bind("<Button-1>",partial(self._active,widget))
        self._current_active_week+=forward
        #get hte current active day value,activeday as a short name
        self.active_week_day[self._current_active_week]=\
            self.active_week_day[self._current_active_week] if self._current_active_week in self.active_week_day else 0
        #caluclate diffeence days to add to the timedelta
        difference_days=self.active_week_day[self._current_active_week]-datetime.today().weekday()
        current_day=datetime.today()+timedelta(days=difference_days,weeks=self._current_active_week)
        #print(str(current_day),timedelta(days=active_day,weeks=self._current_active_week-forward))
        self.active_by_day(current_day.date())
    def is_in(self,day:date):
        assert(type(day)==date)
        for widget in self:
            if  widget.day==day:
                return widget
    def getitem(self,addedday:date=date.today(),data:list=[]):
        assert(type(addedday)==date)
        
        widget=Achievement_widget(self.container_frame,addedday)

        
        if widget.day>=date.today():
            Button(widget.interior,text="add task",command=widget.add_item).grid(row=widget.interior.grid_size()[1],column=0)
        #we do this fo the button add as a first column
        #we shouldn't do this
        for val in data:
            widget.add_item(**val)
        return widget
    def add(self,day:date,data):
        assert(type(day)==date)
        return self.is_in(day) if self.is_in(day)!=None else self.append_item(self.getitem(day,data))
    def _active(self, widget: Achievement_widget,_=None):
        assert (widget!=None)
        self.title_widget["text"]=widget.day.strftime("%b %a")
        if widget.day== date.today():
            self.title_widget["text"]+=" today..."
        for child in self.container_frame.pack_slaves():
            child.pack_forget()
        widget.pack(fill=BOTH,expand=YES)
        widget._configure_canvas()
        widget._configure_interior()
    def active_by_day(self,day:date):
        assert(type(day)==date)
        widget=self.is_in(day)
        self._active(widget if widget!=None else self.add(
            day,(self.data[day]if day in self.data else []),
            )
        )
    def get_keys(self,covert_json=False):
        the_dict={}
        #return widgets in the switcher
        #return achievements days
        for day in self:
            the_value=list(day.get_keys())
            if covert_json:
                for i,val in enumerate(the_value):
                    for key,item in val.items():
                        the_value[i][key]=str(item)
            key=day.day if not covert_json else str(day.day)
            the_dict.update({key:the_value})
        return the_dict
    @staticmethod
    def load_file(file,mode="rb"):
        """FILE as pickle"""
        with open(file,mode) as  f:
            return pickle.load(f)
    def save_file(self,file:str,mode="wb"):
        with open(file,mode) as  f:
            pickle.dump(self.get_keys(),f)
    def pause_all(self,state):
        for widget in self:
            widget.pause_all(state)
def main():
    root=Tk()
    data=Dayswidget.load_file("save.pkl","rb")
    days_widget=Dayswidget(root,data)
    days_widget.forward(0)

    days_widget.active_by_day(datetime.now().date())
    days_widget.pack(fill=BOTH,expand=YES)
    Button(text="get keys",command=lambda:print(days_widget.get_keys())).pack()
    Button(text="Save",command=lambda:days_widget.save_file("D:\Projects\Focusing\\save.pkl")).pack()
    root.mainloop()
if __name__=="__main__":
    
    main() 