from datetime import datetime
from pprint import pprint


def parse_session_types():
    ss = {}
    try:
        with open('session_types.csv', 'r') as settings:
            line_length = len(settings.readline().strip().split(','))
            line = settings.readline().strip().split(',')
            while len(line) == line_length:
                session_name = line[0]
                start_time = datetime.strptime(line[1], '%I:%M:%S %p')
                end_time = datetime.strptime(line[2], '%I:%M:%S %p')
                required_time = float(line[3])
                abbreviation = line[4]
                if session_name not in ss:
                    ss[session_name] = {
                        "start_time": start_time,
                        "end_time": end_time,
                        "required_time": required_time,
                        "abbreviation": abbreviation
                    }
                line = settings.readline().strip().split(',')
    except IOError:
        print("I/O error")
    return ss


session_settings = parse_session_types()
