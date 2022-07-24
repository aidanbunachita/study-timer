#   Future Features:
#       1. Display_timer parameter that allows the timer set to interact with a tkinter object (for real-time timer display, etc.)
#

from threading import Event
from threading import Thread

class TimerSet():
    def __init__(self, on_set_start = None, on_terminate = None, on_timer_end = None, on_set_end = None):
        
        self.current_time = 0               # time (in seconds) left in current timer
        # timer_array (currently None)      # list of timers you'll cycle through during start_setσ

        self.timer = Event()                # timer wait() and set() catcher
        self.timer_thread = None            # timer thread (restricts tSet object to one thread)

        self.on_set_start =  on_set_start           # function when timer_set is started
        self.on_terminate = on_terminate    # function when timer is terminated
        self.on_timer_end = on_timer_end    # function when timer ends
        self.on_set_end = on_set_end        # function when timer_set ends

    def start_set(self, timer_array):
        if self.timer_thread is None or not self.timer_thread.is_alive():
            self.on_set_start()
            self.timer_thread = Thread(target = self.start_timer)
            self.timer_array = timer_array
            self.timer_thread.start()
            
        elif self.timer_thread.is_alive():
            print("\n\nThread is in use!\n")

    def start_timer(self):
        if self.current_time:
                print("The timer's running! Terminate it first before proceeding.")
        else:
            for time in self.timer_array:
                self.current_time = time 
                while self.current_time > 0 and not self.timer.is_set():
                    print(self.current_time, end = ' ', flush = True)               # flush makes print happen in real time [python.exe console]
                    self.timer.wait(1) 
                    self.current_time -= 1                     
                if self.current_time == 0:
                    print("\n\nTimer's up! \n")
                    self.on_timer_end()
            if self.timer.is_set():
                pass
            else:
                self.on_set_end()
                print("\n\nThe timer-set's ended!")

    def end_timer(self):
        self.timer.set()
        print("\n\nYou terminated it!\n")
        self.on_terminate()   
        self.current_time = 0
    




if __name__ == "__main__":
    import time
    testSet = TimerSet()
    testSet.start_set([80, 40, 10, 5])
    time.sleep(2)
    testSet.start_set([80, 40, 10, 5])
    time.sleep(3)
    testSet.end_timer()