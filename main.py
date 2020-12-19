import sys
import json
from file_IO import *
from parse_session import get_session_data
from parse_session_types import session_settings

sessions_data = []
roster = {}
session_list = []
attendance_total = {}  # dictionary of email (key) to # sessions attended

term = 202030
hostID = 892472193

includeOH = True
includeNonQ = True


def add_emails(session, dictionary):
    for email in session['attendance_records']:
        if email not in dictionary:
            dictionary[email] = 0
        dictionary[email] += 1
    return dictionary


def add_session(attend_list, session_type, session_date):
    sessions_data.append({"abbreviation": session_settings[session_type]['abbreviation'],
                          "session_type": session_type,
                          "date": session_date.strftime("%m/%d/%Y"),
                          "total_attendance": len(attendance),
                          "attendance_records": attend_list})
    return sessions_data


if __name__ == "__main__":
    args = parse_arguments()

    # get a list of the file names for each session
    session_filename_list, override_filename_list = collect_file_names(args.file_names)
    # session_filename_list = [filename, filename]
    for session_file in session_filename_list:
        # for each session get get the supposed file name, and check if it exists in override_filename_list
        override_file = session_file.split('.')[0] + '.txt'
        try:
            attendance, s_type, s_date = get_session_data(args.output_dir, includeNonQ, session_file, (override_file if override_file in override_filename_list else None))
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

    write_master_list_csv(roster, session_list, args.output_dir)

    if args.stats:
        try:
            with open(args.stats) as json_file:
                stats = json.load(json_file)
                write_stat_files(stats, roster, sessions_data, args.output_dir)
        except FileNotFoundError:
            print('I/O error: Unable to open file', args.stats)

    if len(args.it_stats) == 2:
        write_IT_file(args.it_stats[0], args.it_stats[1], sessions_data, args.output_dir, includeOH)



