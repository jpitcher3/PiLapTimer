from tkinter import *
import time
import RPi.GPIO as GPIO

#intialize globals
global lapstart
lapstart = time.time()

ws = Tk()
ws.geometry('600x450+1000+300')
ws.title("John's Lap Timer")
ws.config(bg='#FFFFFF')
#ws.iconbitmap('stopwatch.ico')
ws.resizable(0,0)

laptimes=()
laptime_listbox = Listbox(ws)
laptime_listbox.pack()

counter = -1
running = False
def counter_label(lbl):
    def count():
        if running:
            global counter


            #now = datetime.now()
            global lapstart
            duration = time.time() - lapstart
            

            #lbl['text']=str(timedelta(now-lapstart))   
            lbl['text'] = time.strftime("%M:%S.{}".format(str(duration % 1)[2:])[:8], time.gmtime(duration))

            lbl.after(10, count)    
            counter += 1
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
    global counter
    counter=-1
    if running==False:      
        reset_btn['state']='disabled'
        lbl['text']='00:00.000'
    else:                          
        lbl['text']=''

def MarkLapCallback(channel):
    global running
    global lapstart 
    global lastlap
    lastlap = time.time() - lapstart
    lapstart = time.time()
    laptime_listbox.insert(0,time.strftime("%M:%S.{}".format(str(lastlap % 1)[2:])[:8], time.gmtime(lastlap)))
    running=True

#bg = PhotoImage(file='stopwatch.png')
#img = Label(ws, image=bg, bg='#299617')
#img.place(x=75, y=50)

lbl = Label(
    ws, 
    text="00:00.00", 
    fg="black", 
    bg='white', 
    font="Verdana 40 bold"
    )

label_msg = Label(
    ws, text="minutes : seconds . milliseconds", 
    fg="black", 
    bg='white', 
    font="Verdana 10 bold"
    )

lbl.place(x=160, y=170)
label_msg.place(x=170, y=250)

start_btn=Button(
    ws, 
    text='Start', 
    width=15, 
    command=lambda:StartTimer(lbl)
    )

stop_btn = Button(
    ws, 
    text='Stop', 
    width=15, 
    state='disabled', 
    command=StopTimer
    )

reset_btn = Button(
    ws, 
    text='Reset', 
    width=15, 
    state='disabled', 
    command=lambda:ResetTimer(lbl)
    )

lap_btn = Button(
    ws, 
    text='Lap', 
    width=15, 
    command=lambda:MarkLapCallback(0)
    )

start_btn.place(x=30, y=390)
stop_btn.place(x=150, y=390)
reset_btn.place(x=270, y=390)
lap_btn.place(x=390, y=390)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) #pin 18 = GPIO 24
GPIO.add_event_detect(18,GPIO.FALLING,callback=MarkLapCallback, bouncetime=200)
ws.mainloop()
GPIO.cleanup(18)