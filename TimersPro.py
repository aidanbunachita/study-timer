from threading import Event
from threading import Thread


class TimerSet():
    def __init__(self, Object = None, reactions_dict = {}):         # Missing: Timeout function & length (msg box after )
        self.ts_initialize_reactions(Object, reactions_dict)
        self.ts_initialize_values()

## Initializing Timer Set Values & Reactions
    def ts_initialize_values(self):
        self.current_time = 0               # time (in seconds) left in current timer
        self.timer = Event()                # timer wait() and set() catcher
        self.timer_thread = None            # timer thread (restricts tSet object to one thread)
        self.print_timestep = True          # optional parameter for enabling the second-by-second prints in the command line
        self.timer_thread = Thread()        # initial thread to prevent terminate() from calling is.alive() on NoneType   
    def ts_initialize_reactions(self, Object, reactions_dict):  #GEMFinal: if action is an object method: make the lambda directly call the object (IF THAT FAILS: try to make it an argument in the lambda function.)
        default_reactions = {
            "on_set_start" : lambda: print("\nStarting Timer Set...\n"),
            "on_set_end"   : lambda: print("\n\nThe timer-set's ended!\n"),
            "on_timer_end" : lambda: print("\n\nNext Timer!\n"),
            "on_terminate" : lambda: print("\n\nTimer Set Terminated! \n"),
            "on_timestep"  : lambda: print(self.current_time, end = ' ', flush = True) # flush makes print happen in real time [python.exe console]
        }
        for action in reactions_dict:
            if action in default_reactions.keys():
                default_reactions[action] = reactions_dict[action]
        
        for action in default_reactions:
            setattr(self, action, default_reactions[action])

## Timer Set Actions
    def start_set(self, timer_array):
        if self.timer_thread is None or not self.timer_thread.is_alive():
            self.timer_array = timer_array
            self.timer.clear()
            self.on_set_start()                                                         # GEMFinal []:

            self.timer_thread = Thread(target = self.start_timer)
            self.timer_thread.start()

        elif self.timer_thread.is_alive():
            print("\n\nThread is in use!\n")
    def start_timer(self):     
        timer_array_length = len(self.timer_array)                                                   
        for time in self.timer_array:
            self.current_time = time
            while not self.timer.is_set() and self.current_time > 0:
                if self.print_timestep:
                    print(self.current_time, end = ' ', flush = True)               # flush makes print happen in real time [python.exe console]
                self.timer.wait(1) 
                self.current_time -= 1                     
            if not self.timer.is_set():
                self.on_timer_end()                                                #GEMFinal [tSet_frame]: shift style of next & last ()

        if self.timer.is_set():
            self.on_terminate()                                                     # GEMFinal [banner, tSet_frame]: change highlight color of the current •
        else:
            self.on_set_end()                                                       # GEMFinal []:   
    def terminate(self):
        if self.timer_thread.is_alive():
            self.timer.set()   
            self.current_time = 0
        else:
            print("No timers are active!")  

## Future Features:
#       1. Display_timer parameter that allows the timer set to interact with a tkinter object (for real-time timer display, etc.)
#       2. TimerLap class with stopwatch-like functionality
#       3. Separate timer functionality from TimerSet class (create a TimerPro parent class and leave it there)

if __name__ == "__main__":
    import time
    testSet = TimerSet()
    testSet.start_set([80, 40, 10, 5])
    time.sleep(2)
    testSet.start_set([80, 40, 10, 5])
    time.sleep(3)
    testSet.terminate()