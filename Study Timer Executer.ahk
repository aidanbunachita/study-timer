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

!^Enter::   ; REMEMBER to ask via msg box if it was a success or not
if else if WinActive("ahk_class TkTopLevel") {
    Send, {q}{a}{z}
} else if WinExist("ahk_class TkTopLevel") {
    WinActivate, ahk_class TkTopLevel
    Send, {q}{a}{z}
} 

else {
    MsgBox Study Timer not on.
}
Return

!1::
if WinActive("ahk_class TkTopLevel") {
    Send, {p}{q}{v}
} else if WinExist("ahk_class TkTopLevel") {
    WinActivate, ahk_class TkTopLevel
    Send, {p}{q}{v}
}
else {
    MsgBox Study Timer not on.
}
Return

!2::
if else if WinActive("ahk_class TkTopLevel") {
    Send, {b}{n}{m}
} else if WinExist("ahk_class TkTopLevel") {
    WinActivate, ahk_class TkTopLevel
    Send, {b}{n}{m}
} 

else {
    MsgBox Study Timer not on.
}
Return






; XMind hotkey; delete during implementation

!]::

Send, ^{PgDn}
return

![::

Send, ^{PgUp}
return

