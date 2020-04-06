     MD5( ByRef V, L=0 ) {
     VarSetCapacity( MD5_CTX,104,0 ), DllCall( "advapi32\MD5Init", Str,MD5_CTX )
     DllCall( "advapi32\MD5Update", Str,MD5_CTX, Str,V, UInt,L ? L : VarSetCapacity(V) )
     DllCall( "advapi32\MD5Final", Str,MD5_CTX )
     Loop % StrLen( Hex:="123456789ABCDEF0" )
      N := NumGet( MD5_CTX,87+A_Index,"Char"), MD5 .= SubStr(Hex,N>>4,1) . SubStr(Hex,N&15,1)
    Return MD5
    }
While !FileExist("samco.ini")
{
Repeat := 1
InputBox, OutputVar1 , SamBox, Set Pass, HIDE, 300, 140
InputBox, OutputVar2 , SamBox, Repeat Pass, HIDE, 300, 140
if (OutputVar1 = OutputVar2)
	if(OutputVar1 = "") {
		MsgBox , 0, Wrong, Empty Pass Try Again, 4
		Repeat := 2
		}
	else {
	Repeat := 0
	}
else if (Repeat = 1) {
	MsgBox , 0, Wrong, Pass Don't Match Try Again, 4
	Repeat := 2
	}
if (Repeat = "0") {
	OutputVar2 := ""
	While (OutputVar2 = "") {
		FileSelectFile, OutputVar2, 3, , Select Program, Applications (*.*)
		if (OutputVar2 = "")
			MsgBox , 0, Wrong, No Selection Please Select A File, 4
	}
	FileDelete, samco.ini
	FileAppend ,% MD5(OutputVar1,StrLen(OutputVar1)) , samco.ini
	FileAppend ,`n%OutputVar2%, samco.ini
}
}
Loop
{
	InputBox, OutputVar1 , SamBox, Give The Pass, HIDE, 300, 140
	OutputVar3 := MD5(OutputVar1,StrLen(OutputVar1))
	FileReadLine, OutputVar2 ,samco.ini, 1
	FileReadLine, OutputVar4 ,samco.ini, 2
	SplitPath, OutputVar4, OutputVar5, OutputVar6, , ,
	if (OutputVar3 = OutputVar2)
	{
		Run, %OutputVar4%, %OutputVar6%
		sleep, 1000
		WinActivate, ahk_exe %OutputVar5%
		Send, %OutputVar1%
		Send, {Enter}
		ExitApp
	}
	else if (OutputVar1 = "")
		ExitApp
	else
		MsgBox , 0, Wrong, Wrong Pass Try Again, 4
}