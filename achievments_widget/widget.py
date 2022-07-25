import datetime
from tkinter import *
import datetime
import  achievments_widget.voice as voice



def _vaildiation_digits_number(input:str):
    if input.isnumeric() or input == "":return True                  
    else:return False
STYLE_ENTRY_ACIVEMNT=dict(font=20,)

VOICE_ASSISTANT_SAYING=dict(
    START_MISSION="mission started",
    FINISHING_TIME="the target time has finshed ,the Mission {} of failed",
    HALFTIME_PASSED="Half the time passed,{1}",
    MINNUTE_PASSED="{} passed",
    REMAING_TIME_PASSED_TIME="the remaining time is {1}",
)
TRAKCING_TIME=1000

class Acivment_label(Frame):
    def __init__(self,app=NONE,defult_text="",start_time:datetime.datetime=datetime.datetime.now(),last_paused_time:datetime.datetime=datetime.datetime.now(),time=0,every_time=20,end_target_state=False,failing=False,pausing_time=0,pausing_state=True,starting_state=False,**kwargs):
        """
        @parameters
        @defult_text: dufult text of frist entry
        @start_time: time in datetime type of starting missinon passed
        @last_paused_time: last time of the pausing time ,it is used for calculating the time
        @time:time of the mission was token
        @every_time:time of reminding time of the mission,repeated time of reminding the time of the mission
        @end_target_state:state of the mision if it is completed or not
        @failing: the state of failling of the mission if it is completed or not
        """
        super().__init__(app,**kwargs)
        self.start_time=start_time
        self._reach_halftime=False
        self._last_check=datetime.datetime.now()
        self.starting_state=starting_state

        
        #used for calculate the pausing time
        #it is aved duo to emergency droping of the programe
        self.last_paused_time=last_paused_time
    
        self.end_target_state=end_target_state
        self.failing=failing

        self.pausing_time=pausing_time
        self.pausing_state=pausing_state

        self._misionvar=StringVar()
        self._misionvar.set(defult_text)
        self._time=StringVar()
        self._time.set(time)
        self._every_time=StringVar()
        self._every_time.set(every_time)       
    #create for sub
    def get_item(self,parent:Widget):
        parent.columnconfigure(0,weight=1)   
        parent.columnconfigure(0,weight=4)
        reg=self.winfo_toplevel().register(_vaildiation_digits_number)
        self.misionentry=Entry(parent,text=self._misionvar.get(),textvariable=self._misionvar,**STYLE_ENTRY_ACIVEMNT)
        
        self.time_entry=Entry(parent,text=str(self._time.get()),textvariable=self._time,validatecommand =(reg, '%S'),width=10,**STYLE_ENTRY_ACIVEMNT)
        
        
        self.every_time_entry=Entry(parent,text=str(self._every_time.get()),textvariable=self._every_time,validatecommand =(reg, '%S'),width=10,**STYLE_ENTRY_ACIVEMNT)
        
        self._target_end_state=IntVar()
        state=DISABLED if  self.failing else ACTIVE
        #puttin tracking commadn to track if any time hte user change the button
        self.target_check_box=Checkbutton(parent,variable=self._target_end_state,command=lambda:self.end_target(self._target_end_state.get()==1),onvalue=1,offvalue=0,state=state)
        self._target_end_state.set((ON if self.end_target_state else OFF))


        self._paused_var=IntVar()
        def define_variable():
            self.pausing_state=(self._paused_var.get()==ON)

        state=DISABLED if self.failing or  self.end_target_state else  NORMAL

        
        self.pausing_button=Checkbutton(parent,text="pause",variable=self._paused_var,command=define_variable,onvalue=1,offvalue=0,state=state)
        self._paused_var.set((ON if self.pausing_state else OFF))
        #we don't actiavted by defult due to if ending target is true the music will be activated
        if not self.end_target_state:
            self._trace_time()
    def append_item(self):
        #self.rowconfigure(0,weight=1)   
        self.misionentry.grid(row=0,column=0,sticky=NSEW)
        self.time_entry.grid(row=0,column=1)
        self.every_time_entry.grid(row=0,column=2)
        self.pausing_button.grid(row=0,column=3)
        self.target_check_box.grid(row=0,column=4,sticky="nsew",padx=20)
    def get_keys(self):
        return dict(
            defult_text=self._misionvar.get(),
            start_time=self.start_time,
            last_paused_time=self.last_paused_time,
            time=self._float(self._time.get()),
            every_time=self._float(self._every_time.get()),
            end_target_state=self.end_target_state,
            failing=self.failing,
            pausing_time=self.pausing_time,
            pausing_state=self.pausing_state,
            starting_state=self.starting_state,
            )
    def pause_state(self,state):
        self.pausing_state=state
        self._paused_var.set((1 if state else 0))
    def end_target(self,state):
        """state of ending target"""
        if state:
            self.target_check_box.select()
            self.pausing_button.select()
            self.pausing_button.configure(state=DISABLED)
            self._target_end_state.set(TRUE)
            #putting some music achivement
            #----->music
        else:
            #if the end target is false
            self.pausing_button.config(state=NORMAL)
            self._trace_time()
    @staticmethod
    def _float(str):
        try:
            return float(str)
        except:
            return 0
    def _time2hours(self,time: int):
        """TIME in minutes"""
        time=time/60
        hours=int(time)
        minutes=int((time*60)%60)
        seconds=int((time*3600)%60)
        return hours,minutes,seconds
    def _time2string(self,time):
        hours,minutes=self._time2hours(time)[:2]
        the_str=""
        if int(hours)>=1:
            the_str+="{} hours and".format(hours)
        if float(minutes)>=1:
            the_str+="{:2.0f} minutes ".format(minutes)

        return the_str
    def _trace_time(self):
        #check if the target has been finihed or not
        if self._target_end_state.get()==FALSE:
            #putting ded line in the top
            dead_line_time=self._float(self._time.get()) 
            #due to return back
           
            #check if the mission is paused or not
            if not self.pausing_state and self.starting_state:
                self.last_paused_time=datetime.datetime.now()
                current_time=((datetime.datetime.now()-self.start_time).seconds-self.pausing_time)/60
                #settin it if disabled
                remaining_time=dead_line_time-current_time
                #check if there a dead line or not or reachec on failing on achiveng it
                if dead_line_time>0 and not self.failing:
                    #check if the dead line has been reached or not
                    if current_time>=dead_line_time:
                        voice.say(VOICE_ASSISTANT_SAYING["FINISHING_TIME"].format(self._misionvar.get()))
                        self.failing=True
                        self.target_check_box.configure(state=DISABLED)
                        self.pausing_button.configure(state=DISABLED)
                        #break the loob
                        return
                    #check if the half time has been reached or not
                    elif not self._reach_halftime and \
                        current_time>=dead_line_time/2:
                        remaining_time_sting=self._time2string(remaining_time)
                        remaining_phase=VOICE_ASSISTANT_SAYING["REMAING_TIME_PASSED_TIME"].format(self._misionvar.get(),remaining_time_sting)
                        voice.say(VOICE_ASSISTANT_SAYING["HALFTIME_PASSED"].format(self._misionvar.get(),remaining_phase))
                        self._reach_halftime=True
                passed_time=(datetime.datetime.now()-self._last_check).seconds/60             
                if self._float(self._every_time.get())>0 and \
                    passed_time>=self._float(self._every_time.get()):
                    self._last_check=datetime.datetime.now()
                    voice.say(VOICE_ASSISTANT_SAYING["MINNUTE_PASSED"].format(self._time2string(passed_time)))
                    if dead_line_time>0:
                        string_time=self._time2string(remaining_time)
                        if string_time!="":  
                            voice.say(VOICE_ASSISTANT_SAYING["REMAING_TIME_PASSED_TIME"].format(self._misionvar.get(),string_time))
                
                self.after(TRAKCING_TIME,self._trace_time)
                return dead_line_time,current_time
            
            elif self.pausing_state and self.starting_state:
                #calculate the pausing time
                self.pausing_time+=(datetime.datetime.now()-self.last_paused_time).seconds
                self.last_paused_time=datetime.datetime.now()
                current_time=((datetime.datetime.now()-self.start_time).seconds-self.pausing_time)/60
                self.after(TRAKCING_TIME,self._trace_time)
                return dead_line_time,current_time
            elif not self.starting_state:
                self.start_time=datetime.datetime.now()
                self._last_check=datetime.datetime.now()
                self.last_paused_time=datetime.datetime.now()
                if not self.pausing_state:
                    voice.say(VOICE_ASSISTANT_SAYING["START_MISSION"])
                    self.starting_state=True
                self.after(TRAKCING_TIME,self._trace_time)
                return dead_line_time,0
        

def main():
    root=Tk()
    
    time=Acivment_label(root)
    time.get_item(time)
    time.append_item()
    time.pack(fill=BOTH,expand=YES)
    Button(text="get keys",command=lambda:print(time.get_keys())).pack()
    
    root.mainloop()
if __name__=="__main__":
    from __init__ import main as main2
    main()
    #main2()