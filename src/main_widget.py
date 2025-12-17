from functools import partial
import pprint
from tkinter import *
from pywidgets.tk.Notebook.note_origin import Switcher_window
from datetime import datetime, timedelta, date
from .list_arranger import (
    Achievement_widget as _Achievement_widget,
    Description_title_explore,
)
from .daysnotebook import Title_widget
from pywidgets.tk.func import bind_all_childes
import json
from typing import List


class Achievement_widget(_Achievement_widget):
    def append_item(self, widget: Description_title_explore):
        super().append_item(widget)

        def destroy():
            widget.destroy()
            self.remove(widget)

        def popemenu():
            add_menu_pope.tk_popup(self.winfo_pointerx(), self.winfo_pointery())

        add_menu_pope = Menu(self.winfo_toplevel(), tearoff=False)
        add_menu_pope.add_command(label="remove", command=destroy)
        bind_all_childes(widget.title_frame, lambda e: popemenu(), "<Button-3>", "")
        return widget


class DaysWidget(Switcher_window):
    def __init__(self, app=None, data: dict = {}, **kwargs):
        super().__init__(app, **kwargs)
        self.title_widget = Label(self, anchor=W)
        self.title_frame = Title_widget(self)
        self.data = data
        self.container_frame = Frame(self, padx=5)
        self.footerFrame = Frame(self, pady=5)
        self.title_frame.forward = self.forward
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.title_frame.grid(row=0, column=0, sticky=EW)
        self.title_widget.grid(row=1, column=0, sticky=EW)
        self.container_frame.grid(row=2, column=0, sticky=NSEW)
        self.footerFrame.grid(row=3, column=0, sticky=EW)
        today = date.today()

        # this is for when moving from side to another side
        self._current_active_week = 0
        self.active_week_day = {0: today.weekday()}

        self.addButton = Button(
            self.footerFrame,
            text="Add task",
            command=lambda: self.currentDay.add_item(),
        )
        self.addButton.anchor("center")

        self.forward(0)

    def forward(self, forward):
        days = self.title_frame.__class__.forward(self.title_frame, forward)
        for i, day in enumerate(days):
            the_day_data = (
                self.data[day.__str__()] if day.__str__() in self.data else list()
            )
            widget = self.add(day, the_day_data)
            for label in self.title_frame.container.grid_slaves(column=i):
                label.bind("<Button-1>", partial(self._active, widget))
        self._current_active_week += forward
        # get hte current active day value,activeday as a short name
        self.active_week_day[self._current_active_week] = (
            self.active_week_day[self._current_active_week]
            if self._current_active_week in self.active_week_day
            else 0
        )
        # caluclate diffeence days to add to the timedelta
        difference_days = (
            self.active_week_day[self._current_active_week] - datetime.today().weekday()
        )
        current_day = datetime.today() + timedelta(
            days=difference_days, weeks=self._current_active_week
        )
        # print(str(current_day),timedelta(days=active_day,weeks=self._current_active_week-forward))
        self.active_by_day(current_day.date())

    def is_in(self, day: date):
        assert type(day) == date
        for widget in self:
            if widget.date == day:
                return widget

    def getitem(self, addedDay: date = date.today(), data: list = []):
        assert type(addedDay) == date
        widget = Achievement_widget(self.container_frame, addedDay)
        # we do this fo the button add as a first column
        # we shouldn't do this
        for val in data:
            widget.add_item(**val)
        return widget

    def add(self, day: date, data):
        assert type(day) == date
        return (
            self.is_in(day)
            if self.is_in(day) != None
            else self.append_item(self.getitem(day, data))
        )

    def _active(self, widget: Achievement_widget, _=None):
        assert widget != None
        self.title_widget["text"] = widget.date.strftime("%b %a")
        if widget.date == date.today():
            self.title_widget["text"] += " today..."
        for child in self.container_frame.pack_slaves():
            child.pack_forget()
        widget.pack(fill=BOTH, expand=YES)
        if widget.date >= date.today():
            self.addButton.pack(expand=True)
        else:
            self.addButton.pack_forget()

        # widget._configure_canvas()
        # widget._configure_interior()
        self.currentDay = widget
        return widget

    def active_by_day(self, day: date):
        assert type(day) == date
        widget = self.is_in(day)
        return self._active(
            widget
            if widget != None
            else self.add(
                day,
                (self.data[day] if day in self.data else []),
            )
        )

    def get_keys(self):
        the_dict = {}
        # return widgets in the switcher
        # return achievements days
        widgets: List[Achievement_widget] = self
        for widget in widgets:
            the_dict.update({widget.date.isoformat(): widget.get_keys()})
        return the_dict

    @staticmethod
    def load_file(file, mode="r"):
        """Load JSON file safely"""
        try:

            def json_object_hook(obj):
                # Convert key if it's ISO datetime

                for k, v in obj.items():
                    if isinstance(v, str):
                        try:
                            obj[k] = datetime.fromisoformat(v)
                        except ValueError:
                            pass
                return obj

            with open(file, mode, encoding="utf-8") as f:
                return json.load(f, object_hook=json_object_hook)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(e)
            return {}

    def save_file(self, file: str):
        """Save keys to JSON file"""
        with open(file, "w", encoding="utf-8") as f:
            json.dump(self.get_keys(), f, ensure_ascii=False, cls=Encoder)

    def pause_all(self, state):
        for widget in self:
            widget.pause_all(state)


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
