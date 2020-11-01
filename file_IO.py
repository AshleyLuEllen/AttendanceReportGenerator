# get the files from the system arguments and sort them as session files and override files
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


# read in the roster information and create a dictionary that holds that information
def create_roster(roster, session_list):
    try:
        with open("roster.csv") as csvfile:
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


def make_master_list_csv(roster, session_list):
    try:
        with open("reports/master.csv", 'w') as master_file:
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
