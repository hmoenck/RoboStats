from datetime import datetime
import locale
import settings.default_params as default

def handle_timestamp(timestamp, time_format): 
    print(timestamp)
    if time_format == 'dt':
        t = handle_datetime(timestamp)
    elif time_format == 'ms':
        t = float(timestamp)/1000.
    elif time_format == 's': 
        t = float(timestamp)
    return t
    
def handle_datetime(timestamp, form = default.time_format, loc = 'en_US.utf8' ): 
    locale.setlocale(locale.LC_ALL, loc)
    dt = datetime.strptime(timestamp, form)
    return dt
