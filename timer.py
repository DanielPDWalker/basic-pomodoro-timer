import tkinter as tk
import datetime

import settings as settings
import save as save
    
from string import Template

import winsound


class Timer():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pom-athingy-o Timer")
        self.root.configure(background=settings.background_color)

        self.pom_cycles = save.total_pom_cycles
        self.first_run = True
        self.timer_running = True

        self.time_label = tk.Label(text="", font=('Helvetica', settings.default_font_size), background=settings.button_color, foreground=settings.text_color)
        self.time_label.pack()

        self.start_button = tk.Button(text="Start Timer", command=self.started_timer, font=(None, settings.button_font_size), background=settings.button_color, foreground=settings.text_color)
        self.start_button.pack()
        self.restart_button = tk.Button(text="Reset", command=self.stop_after, font=(None, settings.button_font_size), background=settings.button_color, foreground=settings.text_color)
        self.restart_button.pack()
        self.change_timer_button = tk.Button(text="Change Timer", command=self.switch_timer_action, font=(None, settings.button_font_size), background=settings.button_color, foreground=settings.text_color)
        self.change_timer_button.pack()

        self.pc_label = tk.Label(text="Total Pomodoro Cycles: ", font=('Helvetica', settings.button_font_size), background=settings.button_color, foreground=settings.text_color)
        self.pc_label.pack()
        self.pc_count = tk.Label(text="", font=('Helvetica', settings.button_font_size), background=settings.button_color, foreground=settings.text_color)
        self.pc_count.pack()
        self.pc_count.configure(text=self.pom_cycles)

        self.root_id = None
        self.set_time()

        self.root.mainloop()


    def calculate_new_times(self):
        self.time_now = datetime.datetime.now()
        self.time_delta = self.time_end - self.time_now
        self.time_label.configure(text=strfdelta(self.time_delta, '%M:%S'))


    def set_time(self):
        if self.timer_running:
            self.time_now = datetime.datetime.now()
            self.pom_time_amount = settings.work_time * 60
            self.time_delta = datetime.timedelta(0, self.pom_time_amount)
            self.time_end = self.time_now + self.time_delta
            self.break_time = settings.break_time * 60

            self.time_label.configure(text=strfdelta(self.time_delta, '%M:%S'))
        else:
            self.time_now = datetime.datetime.now()
            self.break_time = settings.break_time * 60
            self.time_delta = datetime.timedelta(0, self.break_time)
            self.time_end = self.time_now + self.time_delta

            self.time_label.configure(text=strfdelta(self.time_delta, '%M:%S'))


    def stop_after(self):
        try:
            self.root.after_cancel(self.root_id)
            self.set_time()
            self.start_button.config(state="normal")
            self.first_run = True
        except:
            self.set_time()
            self.first_run = True


    def switch_timer_action(self):
        try:
            self.stop_after()
        except:
            pass
        if self.timer_running:
            self.first_run = True
            self.timer_running = False
            self.set_time()
            self.start_button.config(text="Start Break")
        else:
            self.first_run = True
            self.timer_running = True
            self.set_time()
            self.start_button.config(text="Start Timer")


    def started_timer(self):
        if self.timer_running:
            if self.first_run:
                self.set_time()
                self.first_run = False
            self.start_button.config(state="disabled")
            if datetime.datetime.now() < self.time_end:
                self.calculate_new_times()
                self.root_id = self.root.after(50, self.started_timer)
            else:
                self.stop_after()
                self.pom_cycles += 1
                self.save_file_count_total_poms()
                self.pc_count.configure(text=self.pom_cycles)
                for i in range(5):
                    winsound.Beep((i*30+200), 200)
                self.first_run = False

                self.timer_running = False
                self.set_time()
                self.start_button.config(text="Start Break")
        else:
            if self.first_run:
                self.set_time()
            self.first_run = False
            self.start_button.config(state="disabled")
            if datetime.datetime.now() < self.time_end:
                self.calculate_new_times()
                self.root_id = self.root.after(50, self.started_timer)
            else:
                self.stop_after()
                for i in range(5):
                    winsound.Beep((800-(i*100)), 200)
                self.first_run = False

                self.timer_running = False
                self.start_button.config(text="Start Timer")


    def save_file_count_total_poms(self):
        f = open('save.py', 'w')
        f.write("total_pom_cycles = "+str(self.pom_cycles))
        f.close



""" This class and the below srtfdelta class and function were found on stackoverflow : 
https://stackoverflow.com/questions/8906926/formatting-timedelta-objects """

class DeltaTemplate(Template):
    delimiter = "%"


def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    hours, rem = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    d["H"] = '{:02d}'.format(hours)
    d["M"] = '{:02d}'.format(minutes)
    d["S"] = '{:02d}'.format(seconds)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)


app=Timer()