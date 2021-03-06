# AttendanceReportGenerator
This is created for a friend who runs 'SI' sessions via zoom.

It uses a zoom report, and finds those that attended and the total time they were in the session.

This information can then be processed to get information needed about attendence. For example, to see if a student has attended enough sessions to qualify for the test review.

# To run this program

```
positional arguments:
  FILE                  the list of files to process

optional arguments:
  -h, --help            show this help message and exit
  --roster FILE, -r FILE
                        specifies the roster file for stats
  --it HOSTID TERMID, -i HOSTID TERMID
                        adds an output files to give to IT for total
                        attendance
  --stats, -s           enable interactive prompt for stats
  --output-dir DIR, -o DIR
                        specifies the directory for output
```

 
`FILE` (the list of files) can be listed or by piping in the names for files in a folder.

\* Note: files that are `.cvs` are sorted as session files and `.txt` are sorted as override files


# File Formats
****For safety of the students, all input and output files are not posted. An example of what the input and output files will be below.***

**File formats:**   
***input zoom report:*** 
This file is a `.csv`  
```
Meeting ID,Topic,Start Time,End Time,User Email,Duration (Minutes),Participants,
###########,session_type,mm/DD/YYYY HH:MM:SS AM/PM,mm/DD/YYYY HH:MM:SS AM/PM,hostemail@email.com,##,##,

Name (Original Name),User Email,Join Time,Leave Time,Duration (Minutes),Recording Consent
Full Name,email@email.com,mm/DD/YYYY HH:MM:SS AM/PM,mm/DD/YYYY HH:MM:SS AM/PM,##[,Y]
```

***input override report:***  
This file is a `.txt`  
```
email@email.com
email@email.com
email@email.com
...
```

***input roster:***  
This file is a `.csv`  
```
Last Name,First Name,Email,Section
last_name,first_name,email@email.com,#
```

***output session:***  
All three files will be generated for each session.
(There are 3 variations of this file)   
`-all` where all session information is printed, students that attended for long enough to qualify and did not.  
`-qualifiers` where the studends that attended for long enough to qualify, this list is the one that is used for get_stats().  
`-nonqualifiers` where the students that were removed from the `qualifiers` list are held.  

```
email,time_attended(float)
email@email.com,#.#
email@email.com,#.#
```

***output master:***  
```
First Name,Last Name,Email,Section,(Session Type and Date)...
first_name,last_name,email@email.com,#,(1 if attended or 0 if not for each)...
```

***output stats:***  
```
First Name,Last Name,Email,Total Attendance
first_name,last_name,email@email.com,1
```

***output IT stats:***  
```
hostID,termID,email@email.com,mm/DD/YYYY
hostID,termID,email@email.com,mm/DD/YYYY
```
