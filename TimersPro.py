from threading import Event
from threading import Thread

class TimerSet():
    def __init__(self, idle_duration = 300, reactions_dict = {}):       # GEMCurrent: Recheck if you still need to pass the object or if passing the methods is fine once the object exists
        self.ts_initialize_reactions(reactions_dict)
        self.ts_initialize_values(idle_duration)

    def ts_initialize_values(self, idle_duration):                      # GEMCurrent: check the code for redundant value initializations
        self.current_time = 0                                           # GEMDesc: time (in seconds) left in current timer
        self.timer = Event()                                            #        : timer wait() and set() catcher
        self.idle_timer = Event()                                       #        : same thing, but for the idle timer
        self.timer_thread = None                                        #        : timer thread (restricts tSet object to one thread)
        self.print_timestep = True                                      #        : optional parameter for enabling the second-by-second prints in the command line
        self.is_idle = True
        self.idle_duration = idle_duration
        self.timer_kill = False

    def ts_initialize_reactions(self, reactions_dict):                  #GEMCurrent: if action is an object method: make the lambda directly call the object (IF THAT FAILS: try to make it an argument in the lambda function.)
        default_reactions = {
            "on_set_start" : lambda: print("\nStarting Timer Set...\n"),
            "on_set_end"   : lambda: print("\n\nThe timer-set's ended!\n"),
            "on_timer_end" : lambda: print("\n\nNext Timer!\n"),
            "on_terminate" : lambda: print("\n\nTimer Set Terminated! \n"),
            "on_idle"      : lambda: print("\n\nIdling... \n"),
            "on_timestep"  : lambda: print(self.current_time, end = ' ', flush = True) # GEMNote: flush makes print happen in real time [python.exe console]
        }
        for action in default_reactions:
            if action in reactions_dict:
                setattr(self, action, reactions_dict[action])
            else:
                setattr(self, action, default_reactions[action])

## Timer Set Actions
    def start_set(self, timer_array): 
        if self.timer_kill:
            return None
        if self.is_idle is not False:                                   # GEMNote: If user forgets to return something with their reaction functions, it still gets triggered
            self.current_time = 0
            self.is_idle = False
            self.idle_timer.set()
            self.timer_array = timer_array
            self.timer.clear()
            self.on_set_start() # GEMFinal []:
               
            self.timer_thread = Thread(target = self.start_timer)
            self.timer_thread.start()                                   # GEMCurrent: Check when this thread dies
        else:
            print("\n\nThread is in use!\n")       
    def start_timer(self):    
        timer_queue_length = len(self.timer_array)                      # GEMFinal: make use of this for on_timer_end                                                
        for time in self.timer_array:
            self.current_time = time
            while not self.timer.is_set() and self.current_time > 0:
                if self.timer_kill:
                    return None
                if self.print_timestep:
                    print(self.current_time, end = ' ', flush = True)   # GEMFinal: remove this and incorporate on_timestep
                self.timer.wait(1) 
                self.current_time -= 1                     
            if not self.timer.is_set():
                self.on_timer_end() #GEMFinal [tSet_frame]: shift style of next & last ()
        if self.timer_kill:
            return None
        if not self.timer.is_set():                            
            self.is_idle = self.on_set_end()   # GEMFinal []: Function must return True if 1st option (proceed to idle) is selected
            self.idle_or_proceed()
        elif self.timer.is_set():
            self.is_idle = self.on_terminate()    # GEMFinal [banner, tSet_frame]: change highlight color of the current • AND offer two options: go to idle OR redo timer-array
            self.idle_or_proceed()
        
    def terminate(self):                                       
        if self.timer_thread is None:
            print("No timer threads are active!")
            return None    
        self.timer.set()
        
    def idle_or_proceed(self):
        if self.timer_kill:
            return None
        if self.is_idle is not False:
            self.idle_timer.clear()
            self.on_idle()
            self.idle_timer.wait(self.idle_duration)
            if not self.idle_timer.is_set():
                self.start_set([self.idle_duration])
            else:
                pass
        else:
            self.start_set(self.timer_array)
    
    def kill_timer(self):
        self.timer.set()
        self.idle_timer.wait(3)
        self.idle_timer.set()
        self.timer_kill = True
        print("\nTimer Pro has been killed. Have a good day!")



if __name__ == "__main__":
    import time
    testSet = TimerSet(10)
    testSet.start_set([80, 40, 10, 5])
    time.sleep(2)
    testSet.start_set([80, 40, 10, 5])
    time.sleep(3)
    testSet.terminate()
    time.sleep(40)
    testSet.kill_timer()