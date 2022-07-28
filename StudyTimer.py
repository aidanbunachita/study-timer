from TimerGui import TimerGui
from TimersPro import TimerSequence

default_banners = {     # GEMNote: geometry is: width x height + x-coord + y-coord
    "Dormant"   : {'geometry' : "500x500+735+355", 'color' : "Grey"},
    "Idle"      : {'geometry' : "378x140+145+887", 'color' : "Green"}, 
    "Active"    : {'geometry' : "378x425+145+602", 'color' : "Blue"},
    "Halted"    : {'geometry' : "378x793+145+234", 'color' : "Red"}
}

default_timer_seqs = {  # GEMNote: times are in seconds. Also, don't forget to 
                        # leave a comma after sequences with only one timer in them, like in "Idle" or "March"
    "Idle"      : (300, ),
    "March"     : (300, ),
    "Chunk"     : (180, 300),
    "Pick-Off"  : (240, 300, 480, 120),
    "Meta-Skim" : (120, 240),
    "Review"    : (600, 600, 600, 900, 900)
}

testGui = TimerGui(default_banners, default_timer_seqs)
testTimerSeq = TimerSequence(3, 1)  # GEMNote: 1st int: duration (in s) of your 'idle' [Green-Banner timer] (default: 300) [dont do 1]
                                     #        : 2nd int: # of times "Idling..." is printed in the terminal (default: 10)

testGui.set_prompter(testTimerSeq)
testTimerSeq.set_signaller(testGui)
testGui.root.mainloop()

# GEMGuide:
#   <z + a> - Start Timer-Sequence (Chunk)
#   <z + q> - Start Timer-Sequence (Pick-Off)
#   <z + x> - Start Timer-Sequence (Meta-Skim)
#   <z + c> - Start Timer-Sequence (Review)
#   <z + v> - End Timer-Sequence 
#   <z+n+i> - Kill Timer 
#   <z+n+m> - Revive Killed Timer


# GEMFuture: Planned Changes
# 0.) TOP Priority:
#      a.1.) TRANSFER timer-seqs to TimersPro, fix messages [make the PROMPTS send the timer-seq name to TimerGUI, etc.]
#      a.2.) Create an "Idle" shortcut, which only fires when you're in the "March" timer-sequence. 
#      b.) Easier geometry, color, & shortcuts configurability, centralized in one place and streamlined (i.e. one width-value for all non-dormant banners, etc.)
#      c.) Set-Config/Presets functions (i.e. PDFXchange-with-comments-pane-hidden, etc.) that have shortcuts
#      d.) More localized functions (minimize direct edits to attributes, etc.)
#
# 1.) A TimerPro parent class that contains the basic timer functionality
#      a.) more modular function implementations, i.e. timer() is called by timer_set() n times, etc.
#      b.) An on_kill method decorator to check self.timer_kill
#
# 2.) Display_timer paramter that allows the widget to listen to the Prompter (TimerSequence, etc.)
#
# 3.) A TimerPro method that allows users to easily add timer sets/timer laps/etc.
#
# 4.) A centralized TimerPro-TimerSequence integration scheme (one class/module/file/etc.)
#      a.) An intuitive way of asking for the available 'reactions' or commands in a TimerPro object
#      b.) An intuitive way of syncing TimerPro object 'reactions' or commands with the messaging system of the interface object (i.e., a TimerGui)
#      c.) A default TimerPro interface object, in case the user doesn't want to integrate TimerPro into some object of theirs   
#      d.) A way of **adding signal : action** statement to signals_scheme [**Remember** to add 
#          their message-processing as well, if they come with kwargs] signal/prompt to the concerned signals_list or prompts_list]
#
# 5.) Cleaner code (i.e. the prompts that update the GUI all simply call one function which accepts inputs for banner, seq_title, etc.)
#
# 6.) TimerLap class with stopwatch-like functionality

# GEMFuture: Questions/To-Explore
# 1.) Why does StudyTimer hang up when you don't create a new Thread instance once the previous thread has 'stopped'?
#      a.) Is this an infinite loop?                    
# 2.) If I create a new thread each time, am I making a thread-in-a-thread? If not, then when does the previous thread terminate/stop?
# 3.) BUG-ish: March start_timer.thread doesn't detect timer.set(), UNLESS:
#       a.) print("is timer set? ", self.timer.is_set()) is done RIGHT AFTER timer.set(), then timer.clear() right after
#       b.) OR if .clear() was done after a while
#     Why? Is it because: 
#       a.) start_timer checks ONLY after 1 second? So that without the print statement, timer.clear() happens too quickly for start_timer to detect the .set()?