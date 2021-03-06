from itertools import islice
from re import S
import tkinter as tk
from tkinter import Listbox, ttk
from tkinter.constants import BOTH, CENTER, END, LEFT, RIGHT, Y
from typing import List, Callable, Union
from tkcalendar import *
from datetime import *
from functools import cmp_to_key

from record import Record, RecordManager
from detector import Detector

# init and start
CAM_ID = 0
detector = Detector(CAM_ID)
# detector.start()

record_manager = RecordManager('./study_history.csv')

started_time = datetime.now()
ended_time = datetime.now()

update_callback_list: List[Callable] = []

is_started = False

def update():
    for cb in update_callback_list:
        cb()

# returns records of date, by descending order (key=studied_time)
def get_records(date: date) -> List[Record]:
    global record_manager

    records = [*filter(lambda record: record.started_at.date() == date, record_manager.get_records())]

    return sorted(records, reverse=True)

def get_records_test(date: date) -> List[Record]:
    values: List[Record] = [
        Record(datetime(2021, 1, 1, 8, 0, 0), datetime(2021, 1, 1, 9, 0, 0)),
        Record(datetime(2021, 1, 1, 10, 0, 0), datetime(2021, 1, 1, 13, 0, 0)),
        Record(datetime(2021, 1, 1, 14, 0, 0), datetime(2021, 1, 1, 18, 0, 0)),
        Record(datetime(2021, 1, 1, 18, 30, 0), datetime(2021, 1, 1, 21, 32, 57)),
        Record(datetime(2021, 1, 1, 23, 10, 43), datetime(2021, 1, 1, 23, 58, 40))
    ]

    return sorted(values, reverse=True)

def get_current_studied_time() -> timedelta:
    global started_time, ended_time

    return ended_time - started_time

def start_recording():
    global started_time, ended_time, detector, record_manager, is_started

    if is_started:
        return

    started_time = datetime.now()
    ended_time = datetime.now()

    is_started = True

end_recording_cb_list: List[Callable] = []
def end_recording():
    global started_time, ended_time, detector, record_manager, is_started

    if not is_started:
        return

    ended_time = datetime.now()

    is_started = False

    for cb in end_recording_cb_list:
        cb()

dispose_callbacks_list: List[Callable] = []
def dispose():
    for cb in dispose_callbacks_list:
        cb()

def main():
    root = tk.Tk()
    root.wm_geometry('600x400')
    # set window size

    # set title name

    def left_window():
        nonlocal root

        # set left frame
        left_window_frame = tk.Frame(root, padx=10, pady=10)
        left_window_frame.pack(side=LEFT, fill=Y)

        selected_date = datetime.now().date()

        #### date picker widget

        # create datepicker frame
        date_picker_frame = tk.Frame(left_window_frame, pady=5)
        date_picker_frame.pack()

        # add label
        date_entry_label = tk.Label(date_picker_frame, text='??????')
        date_entry_label.pack(side=LEFT)

        # add datepicker widget
        date_entry_widget = DateEntry(date_picker_frame)
        date_entry_widget.pack(side=LEFT)

        # connect events and callbacks
        def cb(e):
            nonlocal selected_date, date_entry_widget
            selected_date = date_entry_widget.get_date()
            update_callback_list()

        date_entry_widget.bind('<<DateEntrySelected>>', cb)

        #### date list widget

        # create date list frame
        date_list_frame = tk.Frame(left_window_frame, pady=5)
        date_list_frame.pack(expand=True, fill=BOTH)

        # create list widget
        date_list = tk.Listbox(date_list_frame, selectmode='single', height=0)
        date_list.pack(expand=True, fill=BOTH)

        # define callback functions for list
        def update_date_list():
            nonlocal selected_date, date_list

            # clear all entries
            date_list.delete(0, END)

            # add all records from that date
            # take 5 from list, if "get_records" is short than 5, add defaults 0y 0m 0d
            for index, record in islice(enumerate(get_records(selected_date) + [None] * 5), 5):
                if record != None:
                    _, [hour, minute, second] = record.studied_time()
                    text = f'{index}. {hour}?????? {minute}??? {second}???'

                else:
                    text = f'{index}. 0?????? 0??? 0???'

                date_list.insert(index, text)

        update_date_list()

        # connect events and callbacks

        # add update function to loop list
        end_recording_cb_list.append(update_date_list)

    def right_window():
        nonlocal root

        # define right frame
        right_window_frame = tk.Frame(root, bg='purple', width=400)
        right_window_frame.pack(side=RIGHT, expand=True, fill=BOTH)

        def webcam():
            nonlocal right_window_frame
            
            # define webcam frame
            webcam_frame = tk.Frame(right_window_frame, bg='blue', width=100, height=100)
            webcam_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

            # ????????? ????????? ????????????
            webcam_label = tk.Label(webcam_frame)
            webcam_label.pack()

            # add update function to loop list
            def event_loop(): # <- ??? ?????????????????? ?????????
                # check https://cjsal95.tistory.com/32
                global detector
                nonlocal webcam_label

                nd_array_raw = detector.get_image() # opencv2 ????????? image

                # convert image for tkinter

                # set label's image

                pass

            update_callback_list.append(event_loop)

        def button_frame():
            nonlocal right_window_frame

            # define button frame
            button_frame = tk.Frame(right_window_frame, bg='red', width=300, height=70)
            button_frame.place(relx=0.5, rely=0.7, anchor='n')

            button_start = tk.Button(button_frame, text='?????? ??????')
            button_start.grid(row=0, column=0, padx=10)

            button_end = tk.Button(button_frame, text='?????? ?????????')
            button_end.grid(row=0, column=1, padx=10)

            # define button widgets and add events of it
            button_start['command'] = start_recording
            button_end['command'] = end_recording

        def timer_frame():
            nonlocal right_window_frame

            timer_frame = tk.Frame(right_window_frame, bg='orange', width=300, height=70)
            timer_frame.place(relx=0.5, rely=0.2)

            timer_label = tk.Label(timer_frame, text='00:00:00')
            timer_label.pack(expand=True, fill=BOTH)

            def update_timer_label():
                studied_time = get_current_studied_time()
                timer_label['text'] = str(studied_time)

            # add update function to loop list
            update_callback_list.append(update_timer_label)

        webcam()
        button_frame()
        timer_frame()

    left_window()
    right_window()

    try:
        while True:
            update()
            root.update()

    except:
        dispose()
        exit(0)

main()

while True:
    update()

'''
??? ??? ??????
1. ?????? ??????????????? (webcam() ??????)
2. ??????????????? ??????, ????????? ????????????
3. end() ??? ??? ??????, file??? csv ?????? ????????????
4. ???????????? padding ????????? (optional)
'''