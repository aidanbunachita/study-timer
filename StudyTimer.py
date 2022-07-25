import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as tkmb
from TimersPro import TimerSet

class TimerWidget(): # GEMFinal: add a QWERTYUIOP or Home-Row sequence WITH DELAY (2-3s) for your n-step initiation plan before each study session (ex. Q - display Step 2 text; W - dislay Step 3 text; etc.)
    def __init__(self, banners, timer_sets):
        root = tk.Tk()
        root.title("•••")
        root.attributes('-topmost', True)
        root.resizable(False, False)
        root.columnconfigure(0, weight = 1)
        root.rowconfigure(0, weight = 1)
        root.bind('<Configure>', lambda a: root.geometry('+%s+%s' % (145,889))) 
        self.root = root
        self.banner = banners[0]    # Default Banner

        style = ttk.Style()
        style.configure('TLabel', font = ('Times New Roman', 16))
        style.configure('current.TLabel', font = ('Times New Roman', 30))
        style.configure('title.TLabel', font = ('Times New Roman', 14))
        style.configure('phase.TLabel', font = ('Courier New', 12))
        self.style = style

        banner_frame = ttk.Label(self.root, background = current_banner[1])
        banner_frame.grid(column = 0, row = 0, sticky = tk.E + tk.W + tk.N + tk.S)
        self.banner_frame = banner_frame

        tSet_frame = ttk.Frame(self.root, padding = (30, 0, 30, 0))
        tSet_frame.grid(column = 0, row = 1, sticky = tk.E + tk.W + tk.N +tk.S)
        self.tSet_frame = tSet_frame                                

        phase_frame = ttk.Frame(self.root, padding = (50, -20, 0, 20))
        phase_frame.grid(column = 0, row = 2, sticky = tk.E + tk.W + tk.N +tk.S)
        self.phase_frame = phase_frame

root = tk.Tk()
root.title("•••")
root.attributes('-topmost', True)
#   root.resizable(False, False)        
#   root.bind('<Configure>', lambda a: root.geometry('+%s+%s' % (145,889)))
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)
 
banners = ( ("500x500+735+315", "grey"),    # I
            ("279x140+145+849", "Green"),   # G
            ("279x375+145+614", "Orange"),  # O
            ("279x750+145+239", "Red")      # R
)
timer_sets = { 
                (5, 5, "March"),
                (3, 5, "Chunk"),
                (4, 5, 8, 2, "Pick-off"),
                (2, 4, "Meta-skim"),
                (10, 10, 10, 15, 15, "Review")
}

current_banner = banners[1]      # GEMTest
root.geometry(current_banner[0]) # GEMTest


##=============================[styling the widgets]======================================||
#
style = ttk.Style()
style.configure('TLabel', font = ('Times New Roman', 16))
style.configure('current.TLabel', font = ('Times New Roman', 50))
style.configure('title.TLabel', font = ('Times New Roman', 22))
style.configure('phase.TLabel', font = ('Courier New', 12))

study_banner = ttk.Label(root, background = current_banner[1])
study_banner.grid(column = 0, row = 0, sticky = tk.E + tk.W + tk.N + tk.S)

tSet_frame = ttk.Frame(root, padding = (30, 0, 30, 0))
tSet_frame.grid(column = 0, row = 1, sticky = tk.E + tk.W + tk.N +tk.S)
for col in range(1, 6):                                                    
    tSet_frame.columnconfigure(col, weight = 1)
tSet_frame.columnconfigure(0, weight = 2)                                  

phase_frame = ttk.Frame(root, padding = (50, 0, 0, ))
phase_frame.grid(column = 0, row = 2, sticky = tk.E + tk.W + tk.N +tk.S)
for col in range(2):
    phase_frame.columnconfigure(col, weight = 1)
#
##========================================================================================||


tSet_name = ttk.Label(tSet_frame, text = "[Start]", style = "title.TLabel")                      
time_past = ttk.Label(tSet_frame, text = " •  •  •")
time_current = ttk.Label(tSet_frame, text = "•", style = "current.TLabel")
time_future = ttk.Label(tSet_frame, text = "•  ")             

#--|
tSet_name.grid(row = 0, column = 0)
time_past.grid(row = 0, column = 1)
time_current.grid(row = 0, column = 2)
time_future.grid(row = 0, column = 3)

current_phase = "None"

phase = ttk.Label(tSet_frame, text = "Phase : " + current_phase, style = "phase.TLabel")
phase.grid(row = 1, columnspan = 6)

##===========================[Tkinter keybindings]========================================||
#
root.bind('<FocusIn>', lambda _: tSet_name.configure(text = "Hi!"))         
root.bind('<FocusOut>', lambda _: tSet_name.configure(text = "Boo!"))
root.bind('<z><a>', lambda _: main_timer.start_set([3, 5])) 
root.bind('<z><q>', lambda _: main_timer.start_set([3, 5, 10]))
root.bind('<z><x>', lambda _: main_timer.start_set([3, 3]))
root.bind('<z><c>', lambda _: main_timer.start_set([10, 10, 10, 15, 15]))
root.bind('<z><v>', lambda _: main_timer.terminate())     
#           
##========================================================================================||

if __name__ == "__main__":
    main_timer = TimerSet(5) 
    root.mainloop()
    main_timer.kill_timer()  # GEMDesc: Once mainloop is exited, the timer halts.