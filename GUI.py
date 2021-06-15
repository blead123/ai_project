import tkinter
from tkcalendar import Calendar, DateEntry
import datetime

def raise_frame(frame):
    frame.tkraise()

root = tkinter.Tk()

# declare webcam frame
webcam_frame = tkinter.Frame(root)

# declare record frame
record_frame = tkinter.Frame(root)

# declare calender object
current_datetime = datetime.datetime.now()
calendar = Calendar(record_frame, selectmode='none', year=current_datetime.year, month=current_datetime.month, day=current_datetime.day)
calendar.pack(fill='both', expand=True)

# setup frame
for frame in webcam_frame, record_frame:
    frame.grid(row=0, column=0, sticky='news')

raise_frame(record_frame)

root.mainloop()

