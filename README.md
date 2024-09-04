# Password_Inseter
This simple python skript checks a password by hashing it with sha256 + salt

First time running it, will ask you for a password.  
After that, it will ask you to repeat it.  
If it matches, it will then ask you for the programm you want to insert the password in.  
Then you will can also set the arguments to start the program (optional).  
Next it ask you for the progamm wait time.   
That is how long to wait before the progam is ready to get the input (default 2s).  
Lastly it ask you if the progam should wait for the started progam to finish (default yes)  

Now every time you start the script it asks you for the password,  
and if it is the correct one, it starts the selected programm and types the password in.  
After that it presses enter.  
If you dont type anything it wil just exit.

The input tester included can be used to check the function of the software.

This was made for the:  
SAM - Steam Account Manager  
https://github.com/rex706/SAM

In the past I got 2 error messages there, when the software got the wrong password / no password.  
This avoides this, by having its own password check mecanisim.
