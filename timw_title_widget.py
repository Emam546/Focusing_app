import datetime
from tkinter import Frame
from tkinter import ttk
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
today=datetime.datetime.now()+ datetime.timedelta(days=2)
dates = [today + datetime.timedelta(days=i) for i in range(0 - today.weekday(), 7 - today.weekday())]
#print([ for day in dates])

def time_of_day(time:datetime.datetime=datetime.datetime.now()):
    return days[time.weekday()]

class Time_widget(ttk.Notebook):
    def __init__(self,app=None,**kwargs):
        super().__init__(app,**kwargs)
        s = ttk.Style()
        s.theme_create( themename="yummy", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] ,"tabposition":"n"} },
        "TNotebook.Tab": {
            "configure": {"anchor":"center","padding": 20 ,"borderwidth":0,"font":30,"background":"red"},
            "map":       {"background": [("selected", "blue")],"foreground":[("selected", "white")],
                          "expand": [("selected", [1, 1, 1, 0])] } 
        },
        "Fri.TNotebook.Tab":{
            "configure":dict(),
            }
        })
        #s.configure('TNotebook', tabposition='n')
        # Style().configure("TNotebook", background=myTabBarColor);
        # Style().map("TNotebook.Tab", background=[("selected", myActiveTabBackgroundColor)], foreground=[("selected", myActiveTabForegroundColor)]);
        # Style().configure("TNotebook.Tab", background=myTabBackgroundColor, foreground=myTabForegroundColor);
        self.frames=[]
        # s.configure("TNotebook", background="blue", borderwidth=0)
        # s.configure("TNotebook.Tab", background="red", borderwidth=0)
        date=datetime.datetime.now()
        
        #str(data.strftime("%a"))

        #s.configure()
        s.theme_use("yummy")
        for day in dates:
            frame=Frame(self,)
            self.frames.append(frame)
            day_text=day.strftime("%a")

            self.add(frame,text='{}\n {}'.format(day_text,day.day))
            if  date.strftime("%a")==day_text:
                self.select(frame)

def main():
    from tkinter import Tk,BOTH,YES
    root=Tk()
    
    time=Time_widget(root)
    time.pack(fill=BOTH,expand=YES)
    
    root.mainloop()
if __name__=="__main__":
    main()