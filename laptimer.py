from tkinter import *
from tkinter import ttk
import time
import RPi.GPIO as GPIO

#intialize globals
global lapstart
global prevlap
lapstart = time.time()
prevlap = lapstart-lapstart

ws = Tk()
ws.attributes('-zoomed', True)
ws.title("John's Lap Timer")
ws.config(bg='black')

#Determine ideal font size based on screen size:
global font_size

width = ws.winfo_screenwidth()
height = ws.winfo_screenheight()

a = int(height / 2)
buff = len('00:00.00')
b = int(width / (buff if buff >= 7 else 7))
font_size = min(a, b)

#Setup Frames
f_current = Frame(ws, bg="black") #top half - current lap
f_buttons = Frame(ws,bg="darkgray") #button frame
f_results = Frame(ws, bg="black") #bottom half - laptimes
f_results_left = Frame(f_results, bg="black") #bottom half - laptimes
f_results_right = Frame(f_results, bg="black") #bottom half - laptimes

laptime_listbox = Listbox(f_results_right
                          , bg="black"
                          , fg="white"
                          , width=15
                          , font=("Verdana",int(font_size/4),"bold"))
laptime_listbox.insert(0,"Previous Laps:")
difftime_listbox = Listbox(f_results_right
                          , bg="grey"
                          , fg="white"
                          , width=10
                          , font=("Verdana",int(font_size/4),"bold"))

lbl_lastLap = Label(f_results_left,text="Last Lap:",fg="white",bg="black",font=("Veranda",int(font_size/4),"bold"),anchor="w",justify="left")
lbl_lastLaptime = Label(f_results_left,text="00:00.000",fg="white",bg="black",font=("Veranda",int(font_size/2),"bold"),anchor="w",justify="left")
lbl_lastLapdiff = Label(f_results_left,text="+ 00:00.000",fg="white",bg="black",font=("Veranda",int(font_size/2),"bold"),anchor="w",justify="right")

counter = -1
running = False
def counter_label(lbl):
    def count():
        if running:
            global lapstart
            duration = time.time() - lapstart
            lbl['text'] = time.strftime("%M:%S.{}".format(str(duration % 1)[2:])[:8], time.gmtime(duration))
            lbl.after(60, count)    
    count()     

def StartTimer(lbl):
    global running
    global lapstart 
    lapstart = time.time()
    running=True
    counter_label(lbl)
    start_btn['state']='disabled'
    stop_btn['state']='normal'
    reset_btn['state']='normal'

def StopTimer():
    global running
    start_btn['state']='normal'
    stop_btn['state']='disabled'
    reset_btn['state']='normal'
    running = False

def ResetTimer(lbl):
    if running==False:      
        reset_btn['state']='disabled'
        lbl['text']='00:00.00'
    else:                          
        lbl['text']=''

def MarkLapCallback(channel):
    global running
    if running==False:
        StartTimer(lbl)
        return
    global lapstart 
    global lastlap
    global prevlap
    lastlap = time.time() - lapstart
    lapstart = time.time()
    
    laptime_listbox.insert(1,time.strftime("%M:%S.{}".format(str(lastlap % 1)[2:])[:9], time.gmtime(lastlap)))
    diff=lastlap-prevlap
    diffstr=time.strftime("%M:%S.{}".format(str(abs(diff) % 1)[2:])[:9], time.gmtime(abs(diff)))
    if diff<0:
        diffstr = ["-",diffstr]
        lbl_lastLaptime['fg']="green"
        lbl_lastLapdiff['fg']="green"
    else:
        diffstr = ["+",diffstr]
        lbl_lastLaptime['fg']="red"
        lbl_lastLapdiff['fg']="red"
    difftime_listbox.insert(0, diffstr)
    lbl_lastLaptime['text']=time.strftime("%M:%S.{}".format(str(lastlap % 1)[2:])[:9], time.gmtime(lastlap))
    lbl_lastLapdiff['text']=diffstr
    prevlap = lastlap


lbl_curlab = Label(f_current,text="Current Lap:",fg="white",bg="black",font=("Veranda",int(font_size/4),"bold"),anchor="w",justify="left")
lbl = Label(
    f_current, 
    text="00:00.00", 
    fg="white", 
    bg='black', 
    font=("Verdana",font_size,"bold")
    )

start_btn=Button(
    f_buttons, 
    text='Start', 
    width=15, 
    command=lambda:StartTimer(lbl)
    )

stop_btn = Button(
    f_buttons, 
    text='Stop', 
    width=15, 
    state='disabled', 
    command=StopTimer
    )

reset_btn = Button(
    f_buttons, 
    text='Reset', 
    width=15, 
    state='disabled', 
    command=lambda:ResetTimer(lbl)
    )

lap_btn = Button(
    f_buttons, 
    text='Lap', 
    width=15, 
    command=lambda:MarkLapCallback(0)
    )



#do layout
f_current.pack(fill=X)
f_buttons.pack(fill=X)
f_results.pack(fill=BOTH, expand=True)
f_results_left.pack(side=LEFT,fill=X)
f_results_right.pack(side=LEFT,fill=X)

lbl_curlab.pack(fill=X)
lbl.pack(fill=X)
#buttons
start_btn.pack(side=LEFT)
stop_btn.pack(side=LEFT)
reset_btn.pack(side=LEFT)
lap_btn.pack(side=LEFT)

#Results
lbl_lastLap.pack(fill=X,side=TOP)
lbl_lastLaptime.pack(fill=X,side=TOP)
lbl_lastLapdiff.pack(fill=X,side=TOP)
laptime_listbox.pack(fill=BOTH)
#difftime_listbox.pack(side=LEFT,fill=BOTH)



GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) #pin 18 = GPIO 24
GPIO.add_event_detect(18,GPIO.FALLING,callback=MarkLapCallback, bouncetime=200)
ws.mainloop()
GPIO.cleanup(18)