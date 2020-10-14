import csv
from datetime import *
import ast
import pprint
from parse_session import parse_session
from parse_session_types import session_settings

# TODO A list of sessions every one attended ever (firstName, lastName, email, number of sessions)
# TODO A list of sessions and office hours combined that everyone has attended ever (firstName, lastName, email, number of sessions)
# TODO A list of sessions and office hours combined that everyone has attended between specific dates (firstName, lastName, email, number of sessions)
# TODO A csv file that holds firstName, lastName, email, column for every session
# A list of emails that qualified for the test

sessions_data = []


def get_stats(countOH=False, countTR=False):
    attendance_total = {}
    for session in sessions_data:
        if (session['abbreviation'] == 'SI'
                or (session['abbreviation'] == 'OH' and countOH)
                or (session['abbreviation'] == 'TR' and countTR)):
            for email in session['attendance_records']:
                if email not in attendance_total:
                    attendance_total[email] = 1
                else:
                    attendance_total[email] += 1
    return attendance_total


# return a list, and a separate function to parse this return to a csv
def get_stats(start_date, end_date, countOH=False, countTR=False):
    attendance_total = {}
    for session in sessions_data:
        if start_date <= datetime.strptime(session['date'], "%m-%d-%Y") <= end_date:
            if (session['abbreviation'] == 'SI'
                    or (session['abbreviation'] == 'OH' and countOH)
                    or (session['abbreviation'] == 'TR' and countTR)):
                for email in session['attendance_records']:
                    if email not in attendance_total:
                        attendance_total[email] = 1
                    else:
                        attendance_total[email] += 1
    return attendance_total  # dictionary of email (key) to # sessions attended (value)


def get_stats_qualified(start_date, end_date, required_count, countOH=False, countTR=False):
    qualified = {}
    attendance_total = get_stats(start_date, end_date, countOH, countTR)
    for email in attendance_total:
        if attendance_total[email] >= required_count:
            if email not in qualified:
                qualified[email] = attendance_total[email]
    return qualified  # dictionary of email (key) to # sessions attended (value)


def get_email_from_dictionary(dictionary):
    email_list = []
    for email in dictionary:
        if email not in email_list:
            email_list.append(email)
    return email_list

# data := array of objects like this:
# {
#  "session_type": ["SI Session", "Online ...],
#  "date": date,
#  "attendance_records": dict from csv parser thingy
# }


# what this does
def add_session(attendance, session_type, session_date):
    sessions_data.append({"abbreviation": session_settings[session_type]['abbreviation'],
                          "session_type": session_type,
                          "date": session_date.strftime("%m-%d-%Y"),
                          "total_attendance": len(attendance),
                          "attendance_records": attendance})
    return sessions_data


a, st, sd = parse_session('2020-09-16_OH.csv')
add_session(a, st, sd)
a, st, sd = parse_session('2020-09-16_TR.csv')
add_session(a, st, sd)
a, st, sd = parse_session('2020-09-30_OH.csv', '2020-09-30_OH.txt')
add_session(a, st, sd)
a, st, sd = parse_session('2020-10-07_SI.csv', '2020-10-07_SI.txt')
add_session(a, st, sd)
a, st, sd = parse_session('2020-10-12_SI.csv', '2020-10-12_SI.txt')
add_session(a, st, sd)

# pprint.pprint(sessions_data)
date = '09-30-2020'
diction = get_stats(datetime.strptime(date, "%m-%d-%Y"), datetime.strptime(date, "%m-%d-%Y"), True, False)
print(get_email_from_dictionary(diction))
