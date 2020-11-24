import string
import sys
from datetime import *
import pprint
from file_IO import *
from parse_session import get_session_data
from parse_session_types import session_settings

sessions_data = []
roster = {}
session_list = []
attendance_total = {}  # dictionary of email (key) to # sessions attended


def add_emails(session, dictionary):
    for email in session['attendance_records']:
        if email not in dictionary:
            dictionary[email] = 0
        dictionary[email] += 1
    return dictionary


# return a list, and a separate function to parse this return to a csv
def get_stats(countOH=False, countTR=False, start_date=None, end_date=None):
    attendance_total_stats = {}
    for session in sessions_data:
        if start_date is None or (start_date <= datetime.strptime(session['date'], "%m-%d-%Y") <= end_date):
            if (session['abbreviation'] == 'SI'
                    or (session['abbreviation'] == 'OH' and countOH)
                    or (session['abbreviation'] == 'TR' and countTR)):
                attendance_total_stats = add_emails(session, attendance_total_stats)

    return attendance_total_stats


# def get_stats_required(start_date, end_date, required_count, countOH=False, countTR=False):  #TODO LOOK AT IT
#     attendance_total = get_stats(countOH, countTR, start_date, end_date)
#     qualified = {}
#     for email in attendance_total:
#         print(email, attendance_total[email])
#         if attendance_total[email] >= required_count:
#             if email not in qualified:
#                 qualified[email] = attendance_total[email]
#     return qualified  # dictionary of email (key) to # sessions attended (value)


# def stats_prompts_file_create():
#     print("Would you like to get overall stats? (Y/N)")
#     while input() in 'yY':
#         print('Would you like to include office hours? (Y/N)')
#         office_hour = input() in 'yY'
#         print('Would you like to include test reviews? (Y/N)')
#         test_review = input() in 'yY'
#
#         print('Would you like to set a date range for the stats? (Y/N)')
#         response = input()
#         if response in 'yY':
#             print('Enter the start date: (MM/DD/YYYY)')
#             date_start = datetime.strptime(input(), "%m/%d/%Y")
#             print('Enter the end date: (MM/DD/YYYY)')
#             date_end = datetime.strptime(input(), "%m/%d/%Y")
#             print('Would you like to get only students that qualified? (Y/N)')
#             if input() in 'yY':
#                 print('What is the number of attendances required?')
#                 required_attn = int(input())
#                 diction = get_stats_required(date_start, date_end, required_attn, office_hour, test_review)
#                 write_file_stats('_q' + ('_OH' if office_hour else '') + ('_TR' if test_review else '') + '_' + date_start.strftime("%Y-%m-%d") + '-' + date_end.strftime("%Y-%m-%d"), diction, roster)
#             else:
#                 diction = get_stats(office_hour, test_review, date_start, date_end)
#                 write_file_stats(('_OH' if office_hour else '') + ('_TR' if test_review else '') + '_' + date_start.strftime("%Y-%m-%d") + '-' + date_end.strftime("%Y-%m-%d"), diction, roster)
#         else:
#             diction = get_stats(office_hour, test_review)
#             write_file_stats(('_OH' if office_hour else '') + ('_TR' if test_review else ''), diction, roster)
#         print("Would you like to get more overall stats? (Y/N)")


# what this does
def add_session(attend_list, session_type, session_date):
    sessions_data.append({"abbreviation": session_settings[session_type]['abbreviation'],
                          "session_type": session_type,
                          "date": session_date.strftime("%m-%d-%Y"),
                          "total_attendance": len(attendance),
                          "attendance_records": attend_list})
    return sessions_data


if __name__ == "__main__":
    args = parse_arguments()
    print(args.file_names)

    # get a list of the file names for each session
    session_filename_list, override_filename_list = collect_file_names(args.file_names)
    # session_filename_list = [filename, filename]
    for session_file in session_filename_list:
        # for each session get get the supposed file name, and check if it exists in override_filename_list
        override_file = session_file.split('.')[0] + '.txt'
        try:
            attendance, s_type, s_date = get_session_data(args.output_dir, session_file, (override_file if override_file in override_filename_list else None))
            session_list.append(s_type + ' ' + s_date.strftime("%m/%d/%Y"))
            # add session to master list
            add_session(attendance, s_type, s_date)
        except IOError:
            # if the file does not open, print error
            print("File Error: " + session_file + (' and/or ' + override_file if override_file in override_filename_list else '') + ' could not be opened.')

    # sort the list of session names by date
    session_list.sort(key=lambda s: datetime.strptime(s[-10:], '%m/%d/%Y'))

    # load in the roster date and create it.
    try:
        create_roster(roster, session_list, args.roster_file_name)
    except IOError:
        print("Error roster.csv could not be read. No data beyond individual sessions can be created.")
        exit()

    index = 0
    for session in sessions_data:
        for email in session["attendance_records"]:
            roster[email]["sessions"][index] = '1'
        index += 1

    make_master_list_csv(roster, session_list, args.output_dir)

    if args.interactive_stats:
        print("Not yet finished.")
        # stats_prompts_file_create()



