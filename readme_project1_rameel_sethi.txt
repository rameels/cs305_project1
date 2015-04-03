*******************
SimpleWebBrowser.py
*******************

A simple web client.

Enter host (can only do so once in program runtime,
please no http:// or www. prefixes), followed by object name
(please enter full path with slashes before each
directory, no slash after filename)

Note: To clear cache, please delete all subdirectories in directory
where SimpleWebBrowser.py is located.

Shortcuts:

b: Get previous page
f: Get next page
r: Refresh current page
q: Quit the web client

Example:

rameel@rameel-Satellite-C55-A:~/Dropbox/CS305/project1$ python SimpleWebBrowser.py
Enter host name: cs.lafayette.edu
Enter object name: /~sadovnia/courses/s15/cs305/labs/index1.html
Retrieved object:
Congratulations! You have successfully downloaded index1.html
Enter object name: /~sadovnia/courses/s15/cs305/labs/index2.html
Retrieved object:
Congratulations! You have successfully downloaded index2.html
Enter object name: b
Cached copy:
Congratulations! You have successfully downloaded index1.html
Enter object name: f
Cached copy:
Congratulations! You have successfully downloaded index2.html
Enter object name: r
Cached copy:
Congratulations! You have successfully downloaded index2.html
Enter object name: q
Goodbye...

*******************
SimpleMailClient.py
*******************

A simple SMTP email client.
Enter SMTP server (lafayette.edu only please), sender address (lafayette.edu only please), 
recipient addresses (separated by comma only, please) and message (please end with blank line) 
to send email! For students, you must ssh into one of the compute machines.

Example:

rameel@rameel-Satellite-C55-A:~/Dropbox/CS305/project1$ ssh -Y sethir@compute212.cs.lafayette.edu
sethir@compute212.cs.lafayette.edu's password: 
Last login: Tue Feb 24 19:49:07 2015 from 139.147.28.94
-bash-4.2$ ls
attachments.zip  cs205    Documents  Public       tmp
babySkypeDB      cs305    Downloads  public_html  Videos
BS               cs320    ECE 425    results.txt  
CS104            DB       Music      save         
CS 150           Desktop  Pictures   Templates
-bash-4.2$ cd cs305
-bash-4.2$ ls
SimpleMailClient.py  SimpleMailClient.py~
-bash-4.2$ python SimpleMailClient.py
Enter SMTP server name: outgoing.lafayette.edu
Enter sender email address: sethir@lafayette.edu
Enter receiver email addresses, comma separated: sethir@lafayette.edu,rameel.sethi@gmail.com,rameel92@hotmail.com
Enter message, empty line for end:
Hi!
This is a simple mail client.
It was written in Python for my Computer Networks class.
Bye!

Sent!

