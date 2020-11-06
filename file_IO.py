import os
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='TODO: fix')

    parser.add_argument('--stats', '-s',
                        action='store_true',
                        dest='interactive_stats',
                        help='enable interactive prompt for stats')
    parser.add_argument('--roster', '-r',
                        action='store',
                        metavar='FILE',
                        dest='roster_file_name',
                        required=True,
                        help='specifies the roster file for stats')
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


def make_master_list_csv(roster, session_list, directory):
    try:
        file_name = os.path.join(directory, 'master.csv')
        with open(file_name, 'w') as master_file:
            master_file.write("First Name,Last Name,Email,Section," + ','.join(session_list) + '\n')
            for email in roster:
                master_file.write(roster[email]["first_name"] + ',' + roster[email]["last_name"] + ',' + email + ',' + roster[email]["section"] + ',' + ','.join(roster[email]["sessions"]) + '\n')
    except IOError:
        print("Master File could not be created.")


def write_file_stats(tag, stats, roster):
    try:
        with open("reports/" + 'stats' + tag + ".csv", 'w') as stat_file:
            print('File: stats' + tag + '.csv created.')
            stat_file.write('First Name,Last Name,Email,Section,Total Attendance\n')
            for email in stats:
                stat_file.write(roster[email]["first_name"] + ',' + roster[email]["last_name"] + ',' + email + ',' + roster[email]["section"] + ',' + str(stats[email]) + '\n')
    except IOError:
        print("Stat file 'stats" + tag + ".csv' could not be created.")
