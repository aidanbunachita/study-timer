# study-timer
Simple study timer program in python using the threading and Tkinter modules.

# Reminders:
#   1.) iconic() to minimize
#   2.) in case of catastrophic keybinding failure in tkinter:
#       - listener = keyboard.Listener(on_press=print('hi')) GEMMaybe
#       - listener.start()

A. For Users:
    1. GEMDesc: description of the code line
    2. GEMNote: explanation/tip regarding some decision I made when writing the code line   
   
B For Contributors:
    1. GEMTest: dummy code for testing purposes (Delete when done)
    2. GEMCurrent: what I'm (or you're, although you'd have to leave self-identification) currently working on
    3. GEMFinal: what the final iteration of the current version should implement/look like
    4. GEMFuture: notes on future plans


C. TimersPro Future Plans
    1.  Features
        i.   A TimerPro parent class that contains the basic timer functionality
                a.) more modular function implementations, i.e. timer() is called by timer_set() n times, etc.
                b.) An on_kill method decorator to check self.timer_kill

        ii.  Display_timer paramter that allows a Timer object to interact with a clock-like tkinter widget
        iii. TimerLap class with stopwatch-like functionality

    2.  Questions/To-Explore
        i.   Why does StudyTimer hang up when you don't create a new Thread instance once the previous thread has 'stopped'?
                a.) Is this an infinite loop?                    
        ii.  If I create a new thread each time, am I making a thread-in-a-thread? If not, then when does the previous thread terminate/stop?

D. References
    1. [new main]   https://www.youtube.com/watch?v=JjBr1eOo4PU
    2. [main]       https://tkdocs.com/tutorial/concepts.html 
    3. [ttk docs]   https://docs.python.org/3/library/tkinter.ttk.html#using-ttk 
    4. [SO 1]       https://stackoverflow.com/questions/42141414/tkinter-topmost-and-overridedirect     # topmost vs overridedirect