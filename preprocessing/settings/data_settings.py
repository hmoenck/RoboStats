from datetime import datetime
import locale
import json
#import settings.default_params as default
#date_format_file = '/date_formats.json'


def handle_timestamp(timestamp, time_format, date_format_file): 
    print(timestamp)
    if time_format == 'dt':
        t = handle_datetime(timestamp, date_format_file)
    elif time_format == 'ms':
        t = float(timestamp)/1000.
    elif time_format == 's': 
        t = float(timestamp)
    return t
    
def handle_datetime(timestamp, date_format_file): 
    
    date_formats = json.load(open(date_format_file))

    for loc, form in date_formats.items(): 
        try: 
            locale.setlocale(locale.LC_ALL, loc)
            dt = datetime.strptime(timestamp, form)
        except ValueError:
            pass
        
    return dt
