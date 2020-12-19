import os
import argparse
import json
from datetime import datetime

from parse_session_types import session_settings


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--roster', '-r',
                        action='store',
                        metavar='FILE',
                        dest='roster_file_name',
                        required=True,
                        help='specifies the roster file for stats')
    parser.add_argument('--it', '-i',
                        action='store',
                        dest='it_stats',
                        nargs=2,
                        metavar=('HOSTID', 'TERMID'),
                        help='adds an output files to give to IT for total attendance')
    parser.add_argument('--stats', '-s',
                        action='store',
                        metavar='FILE',
                        default='stats.json',
                        dest='stats',
                        help='enable interactive prompt for stats')
    parser.add_argument('--output-dir', '-o',
                        action='store',
                        metavar='DIR',
                        default='./results',
                        dest='output_dir',
                        help='specifies the directory for output')
    parser.add_argument('file_names',
                        metavar='FILE',
                        nargs='+',
                        help='the list of files to process')

    return parser.parse_args()


# get the files from the system arguments and sort them as session files and override files
def collect_file_names(file_names):
    session_file_names = []
    override_file_names = []
    for file_name in file_names:
        if file_name.endswith(".csv"):
            session_file_names.append(file_name)
        elif file_name.endswith(".txt"):
            override_file_names.append(file_name)
    return session_file_names, override_file_names


# read in the roster information and create a dictionary that holds that information
def create_roster(roster, session_list, roster_filename):
    try:
        with open(roster_filename if roster_filename is not None else "roster.csv") as csvfile:
            csvfile.readline()
            student_info = csvfile.readline().strip().split(',')
            while len(student_info) == 4:
                if student_info[2].lower() not in roster:
                    roster[student_info[2].lower()] = {
                        "first_name": student_info[1],
                        "last_name": student_info[0],
                        "section": student_info[3],
                        "sessions": ['0'] * len(session_list)
                    }
                student_info = csvfile.readline().strip().split(',')
    except IOError:
        return IOError


def write_master_list_csv(roster, session_list, directory):
    try:
        file_name = os.path.join(directory, 'master.csv')
        with open(file_name, 'w') as master_file:
            master_file.write("First Name,Last Name,Email,Section," + ','.join(session_list) + '\n')
            for email in roster:
                master_file.write(roster[email]["first_name"] + ',' + roster[email]["last_name"] + ',' + email + ',' + roster[email]["section"] + ',' + ','.join(roster[email]["sessions"]) + '\n')
    except IOError:
        print("Master File could not be created.")


def write_stat_files(stats, roster, session_list, directory):
    for key, stat in stats.items():
        try:
            file_name = os.path.join(directory, stat['file_name'] + ".csv")
            with open(file_name, 'w') as stat_file:
                validSessions = []
                for session in session_list:
                    if len(stat['startDate']) > 0 and datetime.strptime(stat['startDate'], '%m/%d/%Y') <= datetime.strptime(session['date'], '%m/%d/%Y') <= datetime.strptime(stat['endDate'], '%m/%d/%Y'):
                        if (session['abbreviation'] == 'SI' and stat['includeSI']
                                or (session['abbreviation'] == 'OH' and stat['includeOH'])
                                or (session['abbreviation'] == 'TR' and stat['includeTR'])):
                            validSessions.append(session)
                attendance = {}
                stat_file.write('First Name,Last Name,Email,Total Attendance\n')
                for session in validSessions:
                    for email in session['attendance_records']:
                        if stat['qualifiedOnly']:
                            required_time = session_settings[session['session_type']]['required_time']
                            if (session['attendance_records'][email]['time_attended'] == 'override'
                                    or session['attendance_records'][email]['time_attended'] >= required_time):
                                if email not in attendance:
                                    attendance[email] = {
                                        "session_count": 0
                                    }
                                # add the time the the person was in the session to their previous times
                                attendance[email]["session_count"] += 1
                        else:
                            if email not in attendance:
                                attendance[email] = {
                                    "session_count": 0
                                }
                            # add the time the the person was in the session to their previous times
                            attendance[email]["session_count"] += 1
                for email in attendance:
                    if attendance[email]["session_count"] >= stat['requiredCount']:
                        stat_file.write(
                            roster[email]["first_name"] + ',' +
                            roster[email]["last_name"] + ',' +
                            email + ',' +
                            str(attendance[email]["session_count"]) + '\n')
        except IOError:
            print("Stat file '" + stat['name'] + ".csv' could not be created.")


def write_IT_file(leaderID, term, attendance_data, directory, includeOH):
    try:
        file_name = os.path.join(directory, 'IT_attendance.csv')
        with open(file_name, 'w') as it_file:
            it_file.write('Leader ID, Term ID, Baylor Email, Session Date')
            for session in attendance_data:
                if session['session_type'] != 'OH' or includeOH:
                    for person in session['attendance_records']:
                        it_file.write(str(leaderID) + ',' + str(term) + ',' + str(person) + ',' + str(session['date']) + '\n')
    except IOError:
        print("Error creating the IT file 'IT_attendance.csv'")
