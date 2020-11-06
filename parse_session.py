import csv
import os
from datetime import *
from parse_session_types import session_settings


def parse_session_file(filename):
    # open the file
    with open(filename, 'r') as csvfile:
        attendance = {}
        readCSV = csv.reader(csvfile, delimiter=',')
        count = 0
        # for each row process the data in the file
        for row in readCSV:
            count += 1
            if count == 2:  # get the file metadata held in the second row of the file
                session_type = row[1]
                session_date = datetime.strptime(row[2], '%m/%d/%Y %I:%M:%S %p').date()
                host = row[4].lower()

                # the start time of the session from session_settings
                session_start_time = session_settings[session_type]['start_time']
            if count > 4:  # the data begins on line 4
                # parse times
                # the time from that the user joined the session
                start = datetime.strptime(row[2], '%m/%d/%Y %I:%M:%S %p')
                # the time from that the user left the session
                end = datetime.strptime(row[3], '%m/%d/%Y %I:%M:%S %p')

                # calculate the time in the session, checking that the time they joined is after the start time
                time = end - max(start, datetime.combine(session_date, session_start_time.time()))

                # set email and names
                email = row[1].lower()
                # print(row[0])
                first_name, last_name = row[0].split(' ', 1)

                # if the email is not in attendance, add the email, name, and set time_attended to 0
                if email not in attendance:
                    attendance[email] = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "time_attended": 0
                    }
                # add the time the the person was in the session to their previous times
                attendance[email]["time_attended"] += time.total_seconds() / 60
        # remove host from the attendance list
        del attendance[host.lower()]
    return attendance, session_type, session_date


def add_attendance_override(filename, attendance):
    with open(filename, 'r') as override:
        email = override.readline().strip().lower()
        while email:
            if email not in attendance:
                attendance[email] = {
                    "first_name": '',
                    "last_name": '',
                    "time_attended": 'override'
                }
            email = override.readline().strip().lower()
        return attendance


def remove_nonqualifiers(output_dir, session, session_type, session_date):
    csv_filename = os.path.join(output_dir, session_date.strftime("%Y-%m-%d") + '_' + session_settings[session_type]['abbreviation'] + "-nonqualifiers.csv")
    key_delete = []
    try:
        with open(csv_filename, 'w') as csvfile:
            csvfile.write("email,first_name,last_name,time_attended\n")
            for key in session.keys():
                if session[key]['time_attended'] < session_settings[session_type]['required_time']:
                    csvfile.write(key + ',' + session[key]['first_name'] + ',' + session[key]['last_name'] + ',' + str(
                        session[key]['time_attended']) + '\n')
                    key_delete.append(key)
            for key in key_delete:
                del session[key]
            csvfile.close()
    except IOError:
        print("I/O error: Unable to open file " + csv_filename)


def write_session_csv(output_dir, attendance, session_type, session_date, suffix=''):
    # get the filename in the format of YYYY-MM-DD_ABV[-suffix].csv
    csv_filename = os.path.join(output_dir, session_date.strftime("%Y-%m-%d") + '_' + session_settings[session_type]['abbreviation'] + suffix + '.csv')
    # get the titles of the columns
    csv_columns = ['email']
    for email in attendance.keys():
        for value in attendance[email]:
            csv_columns.append(value)
        break

    try:
        with open(csv_filename, 'w') as csvfile:
            # write the column times to the file
            csvfile.write(','.join(csv_columns) + '\n')
            # for each email in attendance
            for email in sorted(attendance.keys()):
                csvfile.write(email)
                # get the value of each part and write to the file
                for value in attendance[email]:
                    csvfile.write(',' + str(attendance[email][value]))
                csvfile.write('\n')
    except IOError:
        print("I/O error: Unable to open file " + csv_filename)


def get_session_data(output_dir, session_file_name, override_file_name=None):
    print(f"file: {session_file_name}, dir: {output_dir}")
    session_atten, stype, sdate = parse_session_file(session_file_name)
    # write the file all people that attended the session
    write_session_csv(output_dir, session_atten, stype, sdate, '-all')
    # remove from the list those that did not qualify for the time minimum
    remove_nonqualifiers(output_dir, session_atten, stype, sdate)
    # add in the people that are on the override list
    if override_file_name is not None:
        session_atten = add_attendance_override(override_file_name, session_atten)
    # write the file of those that qualified including overrides
    write_session_csv(output_dir, session_atten, stype, sdate, '-qualifiers')
    return session_atten, stype, sdate
