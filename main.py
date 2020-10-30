import csv
import sys
from datetime import *
import ast
import pprint
from parse_session import get_session_data
from parse_session_types import session_settings

# TODO A list of sessions every one attended ever (firstName, lastName, email, number of sessions)
# TODO A list of sessions and office hours combined that everyone has attended ever (firstName, lastName, email, number of sessions)
# TODO A list of sessions and office hours combined that everyone has attended between specific dates (firstName, lastName, email, number of sessions)
# TODO A csv file that holds firstName, lastName, email, column for every session
# A list of emails that qualified for the test

sessions_data = []
roster = {}
session_list = []
attendance_total = {}  # dictionary of email (key) to # sessions attended
attendance_total_SI = {}
attendance_total_SI_OH = {}
attendance_total_SI_OH_TR = {}


def add_emails(session):
    for email in session['attendance_records']:
        if email not in attendance_total:
            attendance_total[email] = 1
        else:
            attendance_total[email] += 1
    return attendance_total


# def get_stats(countOH=False, countTR=False):
#     attendance_total = {}
#     for session in sessions_data:
#         if (session['abbreviation'] == 'SI'
#                 or (session['abbreviation'] == 'OH' and countOH)
#                 or (session['abbreviation'] == 'TR' and countTR)):
#             attendance_total = add_emails(session, attendance_total)
#     return attendance_total
#
#
# # return a list, and a separate function to parse this return to a csv
# def get_stats(start_date, end_date, countOH=False, countTR=False):
#     for session in sessions_data:
#         if start_date <= datetime.strptime(session['date'], "%m-%d-%Y") <= end_date:
#             if (session['abbreviation'] == 'SI'
#                     or (session['abbreviation'] == 'OH' and countOH)
#                     or (session['abbreviation'] == 'TR' and countTR)):
#                 add_emails(session)
#
#
# def get_stats(start_date, end_date, required_count, countOH=False, countTR=False):  #TODO LOOK AT IT
#     qualified = {}
#     for email in attendance_total:
#         print(email, attendance_total[email])
#         if attendance_total[email] >= required_count:
#             if email not in qualified:
#                 qualified[email] = attendance_total[email]
#     return qualified  # dictionary of email (key) to # sessions attended (value)


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


# def get_stats_prompts():
#     print("Would you like to get stats? (Y/N)")
#     while input() == 'y' or 'Y':
#         print('Would you like to include office hours? (Y/N)')
#         office_hour = input() == 'y' or 'Y'
#         print('Would you like to include test reviews? (Y/N)')
#         test_review = input() == 'y' or 'Y'
#
#         print('Would you like to set a date range for the stats? (Y/N)')
#         response = input()
#         if response == 'y' or 'Y':
#             print('Enter the start date: (MM-DD-YYYY)')
#             date_start = input()
#             print('Enter the end date: (MM-DD-YYYY)')
#             date_end = input()
#             print('Would you like to get only students that qualified?')
#             if input() == 'y' or 'Y':
#                 print('What is the number of attendances required?')
#                 required_attn = int(input())
#                 diction = get_stats(datetime.strptime(date_start, "%m-%d-%Y"), datetime.strptime(date_end, "%m-%d-%Y"), required_attn, office_hour, test_review)
#                 print(get_email_from_dictionary(diction))
#             else:
#                 diction = get_stats(datetime.strptime(date_start, "%m-%d-%Y"), datetime.strptime(date_end, "%m-%d-%Y"), office_hour, test_review)
#                 print(get_email_from_dictionary(diction))
#         elif response == 'n' or 'N':
#             diction = get_stats(office_hour, False)
#             print(get_email_from_dictionary(diction))


def get_list_files(arg_list):
    session_filenames = []
    override_filenames = []
    for filename in arg_list:
        if filename == "roster.csv":
            pass
        elif filename.endswith(".csv"):
            session_filenames.append(filename)
        elif filename.endswith(".txt"):
            override_filenames.append(filename)
    return session_filenames, override_filenames


def create_roster():
    try:
        with open("roster.csv") as csvfile:
            csvfile.readline()
            student_info = csvfile.readline().strip().split(',')
            while len(student_info) == 4:
                if student_info[2].lower() not in roster:
                    roster[student_info[2].lower()] = {
                        "first_name": student_info[1],
                        "last_name": student_info[0],
                        "section": student_info[3]
                    }
                student_info = csvfile.readline().strip().split(',')
    except IOError:
        return IOError


if __name__ == "__main__":
    # get a list of the file names for each session and
    session_filename_list, override_filename_list = get_list_files(list(sys.argv))
    # session_filename_list = [filename, filename]
    for session_file in session_filename_list:
        # for each session get get the supposed file name, and check if it exists in override_filename_list
        override_file = session_file.split('.')[0] + '.txt'
        try:
            attendance, s_type, s_date = get_session_data(session_file, override_file if override_file in override_filename_list else None)
        except IOError:
            # if the file does not open, print error
            print("File Error: " + session_file + (' and/or ' + override_file if override_file in override_filename_list else '') + ' could not be opened. Check if exists.')
        session_list.append(s_type + ' ' + s_date.strftime("%m/%d/%Y"))
        # add session to master list
        add_session(attendance, s_type, s_date)

    session_list.sort(key=lambda s: datetime.strptime(s[-10:], '%m/%d/%Y'))
    print(session_list)
    try:
        create_roster()
        # pprint.pprint(roster)
    except IOError:
        print("error")

    for session in sessions_data:
        if session['abbreviation'] == 'SI' or session['abbreviation'] == 'OH':
            add_emails(session)
    # pprint.pprint(attendance_total)

    # pprint.pprint(get_email_from_dictionary(attendance_total))
    #
    # qualified = {}
    # for email in attendance_total:
    #     print(email, attendance_total[email])
    #     if attendance_total[email] >= 3:
    #         if email not in qualified:
    #             qualified[email] = attendance_total[email]
    # pprint.pprint(qualified)
    # pprint.pprint(get_email_from_dictionary(qualified))
