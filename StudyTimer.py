import tkinter as tk
from tkinter import ttk
from workbenchTimerClass import timerPro

{ # GEM notation & Important sources
# GEMTest: replaced in final implementation
# GEMFinal: used in final implementation
# GEMMaybe: to consider for final implementation

# Source links:
#   [new main]                      https://www.youtube.com/watch?v=SYkmiKSq7Ls
#   [main]                          https://tkdocs.com/tutorial/concepts.html 
#   [docu]                          https://docs.python.org/3/library/tkinter.ttk.html#using-ttk 
#   [tk grid]                       https://www.pythontutorial.net/tkinter/tkinter-grid/
#   [ttk style]                     https://www.pythontutorial.net/tkinter/ttk-style/
#   [topmost vs overridedirect]     https://stackoverflow.com/questions/42141414/tkinter-topmost-and-overridedirect 
}
#---------------------------------------------------------------------------------------------------------- 

root = tk.Tk()
root.title("•••")
root.attributes('-topmost', True)
# root.resizable(False, False) GEMFinal
root.columnconfigure(0, weight = 1)
root.rowconfigure(0, weight = 1)
# root.bind('<Configure>', lambda a: root.geometry('+%s+%s' % (145,889))) GEMFinal

banners = ( ("500x500+735+315", "grey"),    # I
            ("279x140+145+849", "Green"),   # G
            ("279x375+145+614", "Orange"),  # O
            ("279x750+145+239", "Red")      # R
)
tSet_timers = { 
                (5, 5, "March")
                (3, 5, "Chunk"),
                (4, 5, 8, 2, "Pick-off"),
                (2, 4, "Meta-skim"),
                (10, 10, 10, 15, 15, "Review")
}

current_banner = banners[1]      # GEMTest
root.geometry(current_banner[0]) # GEMTest

{ # Missing:  
#   1.) ability to log which state we were in (Grn, Orng, or Rd) for stats purposes
#   2.) a QWERTYUIOP or Home-Row sequence WITH DELAY (2-3s) for your n-step initiation plan before each study session (ex. Q - display Step 2 text; W - dislay Step 3 text; etc.)
#   3.) notification for when we're terminating the program (tell user in bold caps "Check Cmd Line before closing it!", exit message in 3s)
}
#---------------------------------------------------------------------------------------------------------- 
style = ttk.Style()
style.configure('TLabel', font = ('Times New Roman', 16))
style.configure('current.TLabel', font = ('Times New Roman', 50))
style.configure('title.TLabel', font = ('Times New Roman', 22))
style.configure('phase.TLabel', font = ('Courier New', 12))

study_banner = ttk.Label(root, background = current_banner[1])
study_banner.grid(column = 0, row = 0, sticky = tk.E + tk.W + tk.N + tk.S)
#------------------------------------------------------------------------|
tSet_frame = ttk.Frame(root, padding = (30, 0, 30, 0))
tSet_frame.grid(column = 0, row = 1, sticky = tk.E + tk.W + tk.N +tk.S)
for col in range(1, 6):                                                    
    tSet_frame.columnconfigure(col, weight = 1)
tSet_frame.columnconfigure(0, weight = 2)                                  
#------------------------------------------------------------------------|
phase_frame = ttk.Frame(root, padding = (50, -20, 0, 20))
phase_frame.grid(column = 0, row = 2, sticky = tk.E + tk.W + tk.N +tk.S)
for col in range(2):
    phase_frame.columnconfigure(col, weight = 1)

tSet_name = ttk.Label(tSet_frame, text = "None", style = "title.TLabel")                      
time_current = ttk.Label(tSet_frame, text = "•", style = "current.TLabel")
time_1 = ttk.Label(tSet_frame, text = "•")
time_2 = ttk.Label(tSet_frame, text = "•")             
time_3 = ttk.Label(tSet_frame, text = "•")                   
time_4 = ttk.Label(tSet_frame, text = "•")                
time_5 = ttk.Label(tSet_frame, text = "•") 
#--|
tSet_name.grid(row = 0, column = 0)
time_1.grid(row = 0, column = 1)
time_2.grid(row = 0, column = 2)
time_3.grid(row = 0, column = 3)
time_4.grid(row = 0, column = 4)
time_5.grid(row = 0, column = 5)

time_current.grid(row = 0, column = 1)

current_phase = "None"

phase = ttk.Label(tSet_frame, text = "Phase : " + current_phase, style = "phase.TLabel")
phase.grid(row = 1, columnspan = 6)
#---------------------------------------------------------------------------------------------------------- 





#---------------------------------------------------------------------------------------------------------- 

# listener = keyboard.Listener(on_press=print('hi')) GEMMaybe
# listener.start()

root.bind('<FocusIn>', lambda _: tSet_name.configure(text = "Hi!"))
root.bind('<FocusOut>', lambda _: tSet_name.configure(text = "Boo!"))
root.bind('<p><q><v>', lambda _: main_timer.start_set([3, 4, 5, 6]))        # to AHK (as alt-1 to 4): <pqv>, <bnm>, <wsx>, and 2 more

root.bind('<q><a><z>', lambda _: main_timer.end_timer())                       # in AHK: as alt-enter 

main_timer = timerPro()                                                         # tSet declaration

root.mainloop()
main_timer.end_timer()  # Once mainloop is exited, the timer halts.
# Reminders:
#   1.) iconic() to minimize
#----------------------------------------------------------------------------------------------------------

