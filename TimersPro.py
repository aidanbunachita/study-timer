from threading import Event
from threading import Thread

# GEMGuide:
#   1.) Changing the Actions it does in response to a Signal: _init_ts_comms(self) [Signal = str : Action = lambda fucntion]
#   2.) Changing Idle Duration: call TimerSequence with a value argument, i.e. test = TimerSequence(40)

class TimerSequence():
    def __init__(self, idle_duration = 300, idle_steps = 10):  # GEMNote: GUI's have prompters; Timers have signallers.        
        self._init_ts_values(idle_duration, idle_steps)                        
        self.actions       = { "start_seq"     : lambda seq : self.start_seq(seq),     
                                "end_seq"       : lambda _  : self.end_seq(),
                                "start_idle"    : lambda direct: self.start_idle(direct),
                                "kill_timer"    : lambda _  : self.kill_timer(),
                                "revive_timer"  : lambda _  : self.revive_timer(),
                                "start_timer"   : lambda _  : self.start_timer(),   # GEMNote: TimerGui doesn't access this by default
                              }

## Initializing Values for TimerSequence
    def _init_ts_values(self, idle_duration, idle_steps):   
        self.current_time = 0                                           # GEMDesc: time (in seconds) left in current timer
        self.timer = Event()                                            #   ''   : timer wait() and set() catcher
        #self.idle_timer = Event()                                      #   ''   : same thing, but for the idle timer [GEMFinal: potentially deprecated]
        self.is_idle = True                                             #   ''   :
        self.timer_kill = False                                         #   ''   :

        self.idle_duration = idle_duration
        self.idle_steps = idle_steps
        self.timer_thread = None

## TimerSequence's actions
    def start_seq(self, timer_sequence = None): 
        if self.timer_kill:
            return None
        else:
            if timer_sequence is None:
                print("\nHey! You need to give me the timer-seq SOME-how...")
                return None     
            self.timer_sequence = timer_sequence
            self.current_time = 0
            self.is_idle = False
            self.timer.clear()
            self.prompt("on_seq_start")

            self.timer_thread = Thread(daemon = True, target = self.start_timer)    # GEMFinal: see if daemon is necessary
            self.timer_thread.start()                                                
    def end_seq(self):                                       
        if self.timer_kill:
            return None
        if self.timer_thread is None:
            print("No timer threads are active!")
            return None
        if self.is_idle:
            print("You're in Idle!")
            return
        self.timer.set()
        self.is_idle = True
        self.prompt("on_seq_end")   
    def kill_timer(self):
        self.prompt("on_timer_kill")
        self.timer.set()
        self.timer_kill = True
        print("\nTimer Pro has been killed. Have a good day!")
    def revive_timer(self):
        if self.timer_kill:
            self.timer_kill = False
            self.prompt("on_timer_revive")
            print("Timer revived successfully!")
        else:
            print("Timer hasn't been killed yet!")
#--|
    def start_timer(self, idle = False):                                                 
        if idle:    # GEMNote: This happens when start_timer is used for Idle
            idle_duration = self.idle_duration
            idle_step = self.idle_duration / self.idle_steps                        
            self.timer.clear()
            while self.is_idle and idle_duration > 0:       
                self.prompt("on_idlestep", idle_duration)
                idle_duration -= idle_step
                self.timer.wait(idle_step)
            if self.is_idle and idle_duration == 0:
                self.prompt("on_idle_end")                                                                                     
        else:
            for time in self.timer_sequence:
                self.prompt("on_timer_start", self.timer.is_set())
                self.current_time = time
                while not self.timer.is_set() and self.current_time > 0:
                    if self.timer_kill:     # GEMFinal: possibly allow exit ONLY when on Idle
                        return None
                    self.prompt("on_timestep", self.current_time)
                    self.timer.wait(1) 
                    self.current_time -= 1                                             
            if not self.is_idle:    # GEMTest
                self._receive_signal("end_seq")
    def start_idle(self, direct = False):               # GEMFinal: In the line below, FINALIZE AS: if self.curent_timer_seq = March or timer_seq has ended:
        if direct and self.is_idle:
            print("You're already Idle!")
            return None
        elif not self.is_idle and not self.signaller.current_timer_seq == "March":
            print("Finish the timer-sequence first.")   
            return None
        else:
            self.is_idle = True
            self.timer.set()
            self.idle_thread = Thread(daemon = True, target = self.start_timer, args = (True,))
            self.prompt("on_idle_start")                            # GEMFinal edit
            self.idle_thread.start()

## Comms methods for TimerSequence
    def set_signaller(self, signaller):
        if hasattr(signaller, "reactions"):
            self.signaller = signaller
            print("Signaller set! Remember, your available prompts are: ", self.signaller.reactions.keys())
        else:
            "Your signaller has no signals!"
    def prompt(self, message, reaction_arg = None):           
        if self.signaller is None:
            print("Set a signaller first using the set_signaller(signaller) method!")
        elif message not in self.signaller.reactions:
            print("Invalid prompt: ", message, "! Remember, your available prompts are: ", self.signaller.reactions.keys())
        else:
            self.signaller._receive_prompt(message, reaction_arg)
    def _receive_signal(self, message, action_arg = None):    # GEMDesc: TimerPro's signal-to-action hub
        if message in self.actions:
            self.actions[message](action_arg)
        else:
            print("[Error] Was sent an invalid message: ", message)


