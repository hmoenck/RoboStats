from datetime import datetime
import locale
import json
import numpy as np



def handle_timestamp(timestamp, time_format, date_format_file, rounding = False): 
    ''' This function takes a string value from the selected time column of the original file 
    and tries to convert it to either datetime format or a float value. If this is not possible
    None is returned which then triggers an error message in the window'''
     
    if time_format == 'dt':
        t = handle_datetime(timestamp, date_format_file)
        if t == None: 
            return None
            
    elif time_format == 'ms':
        try:
            t = float(timestamp)
        except ValueError: 
            return None
        if rounding: t = np.round(t, 2)
        
    elif time_format == 's': 
        try: 
            t = float(timestamp)
        except ValueError: 
            return None
        if rounding: t = np.round(t, 2)
        
    return t
    
def handle_datetime(timestamp, date_format_file): 
    ''' this function tries to convert a given string to datetime format using default formats 
    specified in the settings file'''
    
    # Format of old BioTracker data
    if isinstance(timestamp, str) and timestamp[0] == "'" and timestamp[-1] == "'":
        timestamp = timestamp[1:-1]

    date_formats = json.load(open(date_format_file))
    dt = None
    
    for key in date_formats: 
        form = date_formats[key][0]
        loc = date_formats[key][1]
        try: 
            locale.setlocale(locale.LC_ALL, loc)
            dt = datetime.strptime(timestamp, form)
        except (ValueError, TypeError) as error:
            pass    

    return dt
