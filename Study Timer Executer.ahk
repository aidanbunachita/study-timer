#SingleInstance, Force
SendMode Input
SetWorkingDir, %A_ScriptDir%

!Esc::
if not WinExist("ahk_class TkTopLevel") {
    Run, python StudyTimer.py
} else{
    MsgBox Study Timer already on.
}
Return

!1::
if WinActive("ahk_class TkTopLevel")  {
    Send, {z}{a}
}
else if WinExist("ahk_class TkTopLevel"){
    WinActivate, ahk_class TkTopLevel
    Send, {z}{a}
    
} else {
    MsgBox The study timer isn't on yet.
}
Return

!2::
if WinActive("ahk_class TkTopLevel")  {
    Send, {z}{q}
}
else if WinExist("ahk_class TkTopLevel"){
    WinActivate, ahk_class TkTopLevel
    Send, {z}{q}
    
} else {
    MsgBox The study timer isn't on yet.
}
Return

!3::
if WinActive("ahk_class TkTopLevel")  {
    Send, {z}{x}
}
else if WinExist("ahk_class TkTopLevel"){
    WinActivate, ahk_class TkTopLevel
    Send, {z}{x}
    
} else {
    MsgBox The study timer isn't on yet.
}
Return

!4::
if WinActive("ahk_class TkTopLevel")  {
    Send, {z}{c}
}
else if WinExist("ahk_class TkTopLevel"){
    WinActivate, ahk_class TkTopLevel
    Send, {z}{c}
    
} else {
    MsgBox The study timer isn't on yet.
}
Return

!q::
if WinActive("ahk_class TkTopLevel")  {
    Send, {z}{v}
}
else if WinExist("ahk_class TkTopLevel"){
    WinActivate, ahk_class TkTopLevel
    Send, {z}{v}
    
} else {
    MsgBox The study timer isn't on yet.
}
Return


