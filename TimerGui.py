import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class TimerGui(): 
    def __init__(self, banners = dict(), timer_seqs = dict()):  # GEMNote: GUI's have prompters; Timers have signallers.
        self._init_tg_timer_seqs(timer_seqs)
        self._init_tg_banners(banners)              # GEMDesc: 
        self._init_tg_root()                        #        :
        self._init_tg_bindings()                    #        :
#--|       
        self._init_tg_styles()                      #        :
        self._init_tg_frames()                      #        :
        self._init_tg_tseq_labels()                 #        :
        self._init_tg_phase_labels()                #        :
#--|
        self.reactions =        {"on_seq_start"  : lambda _           : self._default_seq_start(), 
                                 "on_seq_end"    : lambda _           : self._default_seq_end(),
                                 "on_timer_start": lambda seq_is_ended: self._default_timer_start(seq_is_ended),  
                                 "on_idle_start" : lambda _           : self._default_idle_start(),  
                                 "on_idle_end"   : lambda _           : self._default_idle_end(),
                                 "on_timestep"   : lambda current_time: self._default_timestep(current_time),
                                 "on_idlestep"   : lambda _           : self._default_idlestep(),       
                                 "on_timer_kill" : lambda _           : self._default_timer_kill(),
                                 "on_timer_revive":lambda _           : self._default_timer_revive()
                                }

## Initializing TimerGui Values
    def _init_tg_timer_seqs(self, timer_seqs):
        default_timer_seqs = {
        "Idle"      : (300, ),  # GEMNote: In Seconds. If timer_seq has 1 timer, add comma afterwards [like in "Idle" or "March"]
        "March"     : (300, ),        
        "Chunk"     : (180, 300),
        "Pick-Off"  : (240, 300, 480, 120),
        "Meta-Skim" : (120, 240),
        "Review"    : (600, 600, 600, 900, 900)
        }
        if not timer_seqs == {}:
            for timer_seq in default_timer_seqs:
                default_timer_seqs[timer_seq] = timer_seqs[timer_seq]
        self.timer_seqs = default_timer_seqs   
    def _init_tg_banners(self, banners):
        default_banners = { 
            "Dormant"   : {'geometry' : "500x500+735+355", 'color' : "Grey"},   # GEMNote: geometry is: width x height + x-coord + y-coord
            "Idle"      : {'geometry' : "378x140+145+887", 'color' : "Green"},  
            "Active"    : {'geometry' : "378x425+145+602", 'color' : "Blue"},
            "Halted"    : {'geometry' : "378x793+145+234", 'color' : "Red"}
        }
        if not banners == {}:
            for banner in default_banners:
                default_banners[banner] = banners[banner]
        self.banners = default_banners
        self.current_banner = "Dormant" # GEMNote: These three initializations mirror self.update_window()'s behavior
        self.current_timer_seq = "None"
        self.current_timer_count = "" 
#--|    
    def _init_tg_root(self):
        root = tk.Tk()
        root.title("•••")
        root.attributes('-topmost', True)
        root.columnconfigure(0, weight = 1)
        root.rowconfigure(0, weight = 1)
        root.geometry(self.banners[self.current_banner]['geometry'])
        root.overrideredirect(True)
        self.root = root
    def _init_tg_bindings(self):  
        self.root.bind('<z><a>', lambda _: self.signal("start_seq", "Chunk")) 
        self.root.bind('<z><q>', lambda _: self.signal("start_seq", "Pick-Off"))
        self.root.bind('<z><x>', lambda _: self.signal("start_seq", "Meta-Skim"))
        self.root.bind('<z><c>', lambda _: self.signal("start_seq", "Review"))
        self.root.bind('<z><v>', lambda _: self.signal("end_seq"))
        self.root.bind('<z><space>', lambda _: self.signal("start_idle", True))
        self.root.bind('<z><n><i>', lambda _: self.signal("kill_timer"))
        self.root.bind('<z><n><m>', lambda _: self.signal("revive_timer"))   
#--|
    def _init_tg_styles(self):
        style = ttk.Style()
        style.configure('TLabel', font = ('Calibri', 7))
        style.configure('title.TLabel', font = ('Courier New', 18))
        style.configure('phase.TLabel', font = ('Courier New', 8))
        self.style = style
    def _init_tg_frames(self):
        banner_frame = ttk.Label(self.root, background = self.banners[self.current_banner]['color'])
        banner_frame.grid(column = 0, row = 0, sticky = tk.E + tk.W + tk.N + tk.S)
        self.banner_frame = banner_frame

        timer_seq_frame = ttk.Frame(self.root, padding = (0, 10, 0, 5))
        timer_seq_frame.grid(column = 0, row = 1)
        self.timer_seq_frame = timer_seq_frame                                

        phase_frame = ttk.Frame(self.root, padding = (0, 0, 0, 0))
        phase_frame.grid(column = 0, row = 2)
        self.phase_frame = phase_frame
    def _init_tg_tseq_labels(self):
        self.timer_seq_name = ttk.Label(self.timer_seq_frame, text = self.current_timer_seq, style = "title.TLabel")                      
        self.timer_count = ttk.Label(self.timer_seq_frame, text ="( ͡° ͜ʖ ͡°)")             
        self.timer_seq_name.grid(row = 0, column = 0)
        self.timer_count.grid(row = 0, column = 1)
    def _init_tg_phase_labels(self):
        self.current_phase = "None"
        self.phase = ttk.Label(self.phase_frame, text = "Phase : " + self.current_phase, style = "phase.TLabel")
        self.phase.grid()

## TimerGui's default reactions
    def _default_seq_start(self):   
        self.current_banner = "Active"
        self.current_timer_count = ""
        print("Beginning the", self.current_timer_seq, "Timer-Set...")
        self._update_window() 
    def _default_seq_end(self):             
        self.current_banner = "Halted"     
        self._update_window()
        idle_or_not = messagebox.askokcancel('Idle or Repeat?', '[[Meta-Breakdown Format]] & Mark w/ "Copper". \nOK to Idle, Cancel to Repeat')
        if idle_or_not:
            self.signal("start_idle")
        else:
            self.signal("start_seq", self.current_timer_seq)
#--|
    def _default_timer_start(self, seq_is_ended):  
        if  not self.prompter.timer_kill: # GEMFuture: band-aid solution
            if seq_is_ended:   
                self.current_timer_count += "✖️    "
            else:
                self.current_timer_count += "⚫    "
            self._update_window()
    def _default_idle_start(self):
        self.current_banner = "Idle"
        self.current_timer_seq = ""
        self.current_timer_count = ""
        self._update_window("")
    def _default_idle_end(self):        # GEMFinal: make sure all indirect prompts (not from user input) take timer_kill into account
        if not self.prompter.timer_kill:    # GEMFuture: band-aid solution
            print("Idle Over!")
            self.signal("start_seq", "March")
#--|
    def _default_timestep(self, current_time):
        print(current_time, end = ' ', flush = True)   #GEMFuture: change to GUI-related functionality
    def _default_idlestep(self):
        if not self.prompter.timer_kill:    # GEMFuture: band-aid solution
            print("\nIdling...", end = ' ', flush = True)
            self.current_timer_count += "⚫    "
            self._update_window("")
    def _default_timer_kill(self):
        self.current_banner = "Dormant"
        self.current_timer_seq = "- - -"
        self.current_timer_count = ""
        self._update_window("")
    def _default_timer_revive(self):
        self.current_timer_seq = "Do Something!"
        self.current_timer_count = ""
        self._update_window("")
#--|    
    def _update_window(self, title_seq_barrier = "|"):
        self.root.geometry(self.banners[self.current_banner]['geometry'])
        self.banner_frame.configure(background = self.banners[self.current_banner]['color'])
        self.timer_seq_name.configure(text = self.current_timer_seq + title_seq_barrier)
        self.timer_count.configure(text = self.current_timer_count)

## Comms methods for TimerGui
    def set_prompter(self, prompter):
        if hasattr(prompter, "actions"):
            self.prompter = prompter
            print("Prompter set! Remember, your available signals are: ", self.prompter.actions.keys())
        else:
            "Your prompter has no prompts!"
    def signal(self, message, action_arg = None):             # GEMNote: this processes the kwargs before calling on its prompter to receive the signal
        if self.prompter is None:
            print("Set a prompter first using the set_prompter(prompter) method!")
        elif message not in self.prompter.actions:
            print("Invalid signal: ", message, "! Remember, your available signals are: ", self.prompter.actions.keys())
        else:
            if message == "start_seq":                    # GEMNote: unpolished way of handling the start_seq line of action 
                if not self.prompter.is_idle: 
                    print("Finish the current sequence first!", flush = True)
                else:
                    self.current_timer_seq = action_arg
                    self.prompter._receive_signal(message, self.timer_seqs[self.current_timer_seq])
            else:
                self.prompter._receive_signal(message, action_arg)
    def _receive_prompt(self, message, reaction_arg = None):  # GEMDesc: TimerSequence's prompt-to-reaction hub      
        if message in self.reactions:
            self.reactions[message](reaction_arg)
        else:
            print("[Error] Was sent an invalid message: ", message)

