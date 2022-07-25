import os
from pywidgets.tk.func import bind_all_childes
import os,sys
from achievments_widget.widget import *
from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
import datetime
os.path.abspath
FILE_PATH=os.path.dirname(__file__)
RIGHTARROW=Image.open(os.path.join(FILE_PATH,"icons\\go_right.png"))
DOWNARROW=Image.open(os.path.join(FILE_PATH,"icons\\down-arrow2.png"))
CATEGRIES={0:None}
CONTAINER_FRAME_STYLE=dict(padx=14,pady=2)
class Title_Explorebar(Acivment_label):
    def __init__(self, app=None,defultstate=True, defult_text="", start_time: datetime.datetime = datetime.datetime.now(),last_paused_time: datetime.datetime = datetime.datetime.now(), time=0, every_time=20, end_target_state=False, failing=False, pausing_time=0, pausing_state=True, starting_state=False, **kwargs):
        super().__init__(app, defult_text, start_time,last_paused_time, time, every_time, end_target_state, failing, pausing_time, pausing_state, starting_state, **kwargs)

        #parent title to disable other unselected images in the scene 

        self.resized=RIGHTARROW.resize((20,20),Image.ANTIALIAS)
        self.rightarrow = ImageTk.PhotoImage(self.resized)
        
        self.downarrow=DOWNARROW.resize((20,20),Image.ANTIALIAS)
        self.downarrow = ImageTk.PhotoImage(self.downarrow)
        #getting wedget swished out with frame
        self.state_hiding=defultstate
    def get_item(self,parent:Widget):
        parent.rowconfigure(1,weight=1)
        parent.columnconfigure(0,weight=1)

        self.title_frame=Frame(parent)
        self.containerframe=Frame(parent,**CONTAINER_FRAME_STYLE)

        self.title_frame.columnconfigure(1,weight=1)
        #getting child container frame expand by clicking Frame
        self.iconframe=Label(self.title_frame,compound=LEFT)
        self.information_frame=Frame(self.title_frame)
        
        bind_all_childes(self.iconframe,lambda e:self._hide(),"<Button-1>")
        
        super().get_item(self.information_frame)
    def append_item(self):
        self.title_frame.grid(row=0,column=0,sticky=NSEW)
        self.iconframe.grid(row=0,column=0,sticky=NE)
        self.information_frame.grid(row=0,column=1,sticky=NSEW)
        self._hide()
        return super().append_item()
        
    def _hide(self):
        self.state_hiding = not self.state_hiding
        if self.state_hiding:
            self.containerframe.grid(row=1,column=0,sticky=NSEW)
            self.iconframe.config(image=self.downarrow)
        else:
            self.iconframe.config(image=self.rightarrow)
            self.containerframe.grid_forget()  
class  Description_title_explore(Title_Explorebar):
    def __init__(self, app=None,added_time=datetime.datetime.now(),  defultstate=True, defult_text="", start_time: datetime.datetime = datetime.datetime.now(), last_paused_time: datetime.datetime = datetime.datetime.now(), time=0, every_time=20, end_target_state=False, failing=False, pausing_time=0, pausing_state=True, starting_state=False,
                description="",categoreid:int=0,**kwargs):
        self._progress_bar=IntVar()
        super().__init__(app, defultstate, defult_text, start_time, last_paused_time, time, every_time, end_target_state, failing, pausing_time, pausing_state, starting_state, **kwargs) 
        self._description=StringVar()
        self._description.set(description)
        self.categoreid=IntVar()
        self.categoreid.set(categoreid)

        #in the arrangment of the list
        self.added_time=added_time
    
    def get_keys(self):
        the_dict=super().get_keys()
        the_dict["added_time"]=self.added_time
        the_dict["description"]=self._description.get()
        
        return the_dict
    def get_item(self, parent: Widget): 
        super().get_item(parent)
        def _track():
            self._description.set(self.text_widget.get(0.0,END))
        #for details frame
        self.containerframe.columnconfigure(0,weight=1)
        self.containerframe.rowconfigure(1,weight=1)

        self.progress_bar=ttk.Progressbar(self.containerframe,orient=HORIZONTAL,variable=self._progress_bar)
        self.time_widget=Label(self.containerframe)
        self.text_widget=Text(self.containerframe,height=10)

        self.text_widget.insert(INSERT,self._description.get())
        self.text_widget.bind("<Key>",lambda e:_track())
    def append_item(self):
        self.progress_bar.grid(row=0,column=0,sticky=EW)
        self.time_widget.grid(row=0,column=1,sticky=NSEW)
        self.text_widget.grid(row=1,column=0,columnspan=2,sticky=NSEW)
        return super().append_item()
    def _trace_time(self):
        var=super()._trace_time()
        dead_line,current_time=var if var!=None  else (self._float(self._time.get()),\
            ((datetime.datetime.now()-self.start_time).seconds-self.pausing_time)/60)
        
        if hasattr(self,"time_widget"):
            string=str(datetime.time(*self._time2hours(current_time)))
            self.time_widget["text"]=string
        try:
            self._progress_bar.set((current_time/dead_line)*100)
        except ZeroDivisionError:
            self._progress_bar.set(0)
    def __gt__(self,other):
        return self.added_time>other.added_time
def main():
    root=Tk()
    time=Description_title_explore(root)
    time.get_item(time)
    time.append_item()
    time.pack(fill=BOTH,expand=YES)
    
    root.mainloop()
if __name__=="__main__":
    main()
    
    
