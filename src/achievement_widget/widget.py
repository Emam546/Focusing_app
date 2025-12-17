import datetime
from tkinter import *
import datetime
from .voice import say


def _validation_digits_number(input: str):
    if input.isnumeric() or input == "":
        return True
    else:
        return False


STYLE_ENTRY_ACHIEVEMENT = dict(
    font=20,
)

VOICE_ASSISTANT_SAYING = dict(
    START_MISSION="mission started",
    FINISHING_TIME="the target time has finished ,the Mission {} of failed",
    HALFTIME_PASSED="Half the time passed,{1}",
    MINUTE_PASSED="{0} passed",
    REAMING_TIME_PASSED_TIME="the remaining time is {1}",
)
TRACKING_TIME = 1000


class Achievement_label(Frame):
    def __init__(
        self,
        app=NONE,
        default_text="",
        start_time: datetime.datetime = datetime.datetime.now(),
        last_paused_time: datetime.datetime = datetime.datetime.now(),
        time=0,
        every_time=20,
        end_target_state=False,
        failing=False,
        pausing_time=0,
        pausing_state=True,
        starting_state=False,
        **kwargs,
    ):
        """
        @parameters
        @default_text: default text of first entry
        @start_time: time in datetime type of starting mission passed
        @last_paused_time: last time of the pausing time ,it is used for calculating the time
        @time:time of the mission was token
        @every_time:time of reminding time of the mission,repeated time of reminding the time of the mission
        @end_target_state:state of the mission if it is completed or not
        @failing: the state of falling of the mission if it is completed or not
        """
        super().__init__(app, **kwargs)
        self.start_time = start_time
        self._reach_halftime = False
        self._last_check = datetime.datetime.now()
        self.starting_state = starting_state

        # used for calculate the pausing time
        # it is avoided duo to emergency dropping of the program
        self.last_paused_time = last_paused_time

        self.end_target_state = end_target_state
        self.failing = failing

        self.pausing_time = pausing_time
        self.pausing_state = pausing_state

        self._missionVar = StringVar()
        self._missionVar.set(default_text)
        self._time = StringVar()
        self._time.set(time)
        self._every_time = StringVar()
        self._every_time.set(every_time)

    # create for sub
    def get_item(self, parent: Widget):
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(0, weight=4)
        reg = self.winfo_toplevel().register(_validation_digits_number)
        self.missionEntry = Entry(
            parent,
            text=self._missionVar.get(),
            textvariable=self._missionVar,
            **STYLE_ENTRY_ACHIEVEMENT,
        )

        self.time_entry = Entry(
            parent,
            text=str(self._time.get()),
            textvariable=self._time,
            validatecommand=(reg, "%S"),
            width=10,
            **STYLE_ENTRY_ACHIEVEMENT,
        )

        self.every_time_entry = Entry(
            parent,
            text=str(self._every_time.get()),
            textvariable=self._every_time,
            validatecommand=(reg, "%S"),
            width=10,
            **STYLE_ENTRY_ACHIEVEMENT,
        )

        self._target_end_state = IntVar()
        state = DISABLED if self.failing else ACTIVE
        # putting tracking command to track if any time hte user change the button
        self.target_check_box = Checkbutton(
            parent,
            variable=self._target_end_state,
            command=lambda: self.end_target(self._target_end_state.get() == 1),
            onvalue=1,
            offvalue=0,
            state=state,
        )
        self._target_end_state.set((ON if self.end_target_state else OFF))

        self._paused_var = IntVar()

        def define_variable():
            self.pausing_state = self._paused_var.get() == ON

        state = DISABLED if self.failing or self.end_target_state else NORMAL

        self.pausing_button = Checkbutton(
            parent,
            text="pause",
            variable=self._paused_var,
            command=define_variable,
            onvalue=1,
            offvalue=0,
            state=state,
        )
        self._paused_var.set((ON if self.pausing_state else OFF))
        # we don't activated by default due to if ending target is true the music will be activated
        if not self.end_target_state:
            self._trace_time()

    def append_item(self):
        # self.rowconfigure(0,weight=1)
        self.missionEntry.grid(row=0, column=0, sticky=NSEW)
        self.time_entry.grid(row=0, column=1)
        self.every_time_entry.grid(row=0, column=2)
        self.pausing_button.grid(row=0, column=3)
        self.target_check_box.grid(row=0, column=4, sticky="nsew", padx=20)

    def get_keys(self):
        return dict(
            default_text=self._missionVar.get(),
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

    def pause_state(self, state):
        self.pausing_state = state
        self._paused_var.set((1 if state else 0))

    def end_target(self, state):
        """state of ending target"""
        if state:
            self.target_check_box.select()
            self.pausing_button.select()
            self.pausing_button.configure(state=DISABLED)
            self._target_end_state.set(TRUE)
            # putting some music achievements
            # ----->music
        else:
            # if the end target is false
            self.pausing_button.config(state=NORMAL)
            self._trace_time()

    @staticmethod
    def _float(str):
        try:
            return float(str)
        except:
            return 0

    def _time2hours(self, time: int):
        """TIME in minutes"""
        time = time / 60
        hours = int(time)
        minutes = int((time * 60) % 60)
        seconds = int((time * 3600) % 60)
        return hours, minutes, seconds

    def _time2string(self, time):
        hours, minutes, seconds = self._time2hours(time)
        the_str = ""
        if int(hours) >= 1:
            the_str += "{} hours and".format(hours)
        if float(minutes) >= 1:
            the_str += "{:2.0f} minutes ".format(minutes)
        if not the_str and float(seconds) > 1:
            the_str += "{:2.0f} seconds ".format(seconds)
        return the_str

    def _trace_time(self):
        # check if the target has been finished or not
        if self._target_end_state.get() == FALSE:
            # putting end line in the top
            dead_line_time = self._float(self._time.get())
            # due to return back
            # check if the mission is paused or not
            if not self.pausing_state and self.starting_state:
                self.last_paused_time = datetime.datetime.now()
                current_time = (
                    (datetime.datetime.now() - self.start_time).seconds
                    - self.pausing_time
                ) / 60
                # setting it if disabled
                remaining_time = dead_line_time - current_time
                # check if there a dead line or not or reach on failing on achieving it
                if dead_line_time > 0 and not self.failing:
                    # check if the deadline has been reached or not
                    if current_time >= dead_line_time:
                        say(
                            VOICE_ASSISTANT_SAYING["FINISHING_TIME"].format(
                                self._missionVar.get()
                            )
                        )
                        self.failing = True
                        self.target_check_box.configure(state=DISABLED)
                        self.pausing_button.configure(state=DISABLED)
                        # break the loop
                        return
                    # check if the half time has been reached or not
                    elif (
                        not self._reach_halftime and current_time >= dead_line_time / 2
                    ):
                        remaining_time_sting = self._time2string(remaining_time)
                        remaining_phase = VOICE_ASSISTANT_SAYING[
                            "REAMING_TIME_PASSED_TIME"
                        ].format(self._missionVar.get(), remaining_time_sting)
                        say(
                            VOICE_ASSISTANT_SAYING["HALFTIME_PASSED"].format(
                                self._missionVar.get(), remaining_phase
                            )
                        )
                        self._reach_halftime = True
                passed_time = (datetime.datetime.now() - self._last_check).seconds / 60
                if (
                    self._float(self._every_time.get()) > 0
                    and passed_time >= self._float(self._every_time.get())
                    and not self.failing
                ):
                    self._last_check = datetime.datetime.now()
                    say(
                        VOICE_ASSISTANT_SAYING["MINUTE_PASSED"].format(
                            self._time2string(passed_time)
                        )
                    )
                    if dead_line_time > 0:
                        string_time = self._time2string(remaining_time)
                        if string_time != "":
                            say(
                                VOICE_ASSISTANT_SAYING[
                                    "REAMING_TIME_PASSED_TIME"
                                ].format(self._missionVar.get(), string_time)
                            )

                self.after(TRACKING_TIME, self._trace_time)
                return dead_line_time, current_time

            elif self.pausing_state and self.starting_state:
                # calculate the pausing time
                self.pausing_time += (
                    datetime.datetime.now() - self.last_paused_time
                ).seconds
                self.last_paused_time = datetime.datetime.now()
                current_time = (
                    (datetime.datetime.now() - self.start_time).seconds
                    - self.pausing_time
                ) / 60
                self.after(TRACKING_TIME, self._trace_time)
                return dead_line_time, current_time
            elif not self.starting_state:
                self.start_time = datetime.datetime.now()
                self._last_check = datetime.datetime.now()
                self.last_paused_time = datetime.datetime.now()
                if not self.pausing_state:
                    say(VOICE_ASSISTANT_SAYING["START_MISSION"])
                    self.starting_state = True
                self.after(TRACKING_TIME, self._trace_time)
                return dead_line_time, 0
