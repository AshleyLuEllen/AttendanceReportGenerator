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


def add_email(session, attendance_total):
    for email in session['attendance_records']:
        if email not in attendance_total:
            attendance_total[email] = 1
        else:
            attendance_total[email] += 1
    return attendance_total


def get_stats(countOH=False, countTR=False):
    attendance_total = {}
    for session in sessions_data:
        if (session['abbreviation'] == 'SI'
                or (session['abbreviation'] == 'OH' and countOH)
                or (session['abbreviation'] == 'TR' and countTR)):
            attendance_total = add_email(session, attendance_total)
    return attendance_total


# return a list, and a separate function to parse this return to a csv
def get_stats(start_date, end_date, countOH=False, countTR=False):
    attendance_total = {}
    for session in sessions_data:
        if start_date <= datetime.strptime(session['date'], "%m-%d-%Y") <= end_date:
            if (session['abbreviation'] == 'SI'
                    or (session['abbreviation'] == 'OH' and countOH)
                    or (session['abbreviation'] == 'TR' and countTR)):
                attendance_total = add_email(session, attendance_total)
    return attendance_total  # dictionary of email (key) to # sessions attended (value)


def get_stats(start_date, end_date, required_count, countOH=False, countTR=False):
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


def get_stats_prompts():
    print("Would you like to get stats? (Y/N)")
    while input() == 'y' or 'Y':
        print('Would you like to include office hours? (Y/N)')
        office_hour = input() == 'y' or 'Y'
        print('Would you like to include test reviews? (Y/N)')
        test_review = input() == 'y' or 'Y'

        print('Would you like to set a date range for the stats? (Y/N)')
        response = input()
        if response == 'y' or 'Y':
            print('Enter the start date: (MM-DD-YYYY)')
            date_start = input()
            print('Enter the end date: (MM-DD-YYYY)')
            date_end = input()
            print('Would you like to get only students that qualified?')
            if response == 'y' or 'Y':
                print('What is the number of attendances required?')
                required_attn = int(input())
                diction = get_stats(datetime.strptime(date_start, "%m-%d-%Y"), datetime.strptime(date_end, "%m-%d-%Y"),
                                    required_attn, office_hour, test_review)
                print(get_email_from_dictionary(diction))
            diction = get_stats(datetime.strptime(date_start, "%m-%d-%Y"), datetime.strptime(date_end, "%m-%d-%Y"),
                                office_hour, test_review)
            print(get_email_from_dictionary(diction))
        elif response == 'n' or 'N':
            diction = get_stats(office_hour, False)
            print(get_email_from_dictionary(diction))


if __name__ == "__main__":
    with open('session_attendance.csv') as session_file:
        with open('override_attendance.csv') as override_file:
            session_filename = session_file.readline().strip()
            session_tags = session_filename.split('_')
            session_tags += session_tags[1].split('.')
            override_filename = override_file.readline().strip()
            override_tags = override_filename.split('_')
            override_tags += override_tags[1].split('.')
            while len(session_filename) > 1:
                if session_tags[0] == override_tags[0] and session_tags[2] == override_tags[2]:
                    a, st, sd = parse_session(session_filename, override_filename)
                    add_session(a, st, sd)

                    session_filename = session_file.readline().strip()
                    if len(session_filename) > 0:
                        session_tags = session_filename.split('_')
                        session_tags += session_tags[1].split('.')

                    override_filename = override_file.readline().strip()
                    if len(override_filename) > 0:
                        override_tags = override_filename.split('_')
                        override_tags += override_tags[1].split('.')
                else:
                    a, st, sd = parse_session(session_filename)
                    add_session(a, st, sd)

                    session_filename = session_file.readline().strip()
                    if len(session_filename) > 0:
                        session_tags = session_filename.split('_')
                        session_tags += session_tags[1].split('.')

    pprint.pprint(sessions_data)
    # get_stats_prompts()
