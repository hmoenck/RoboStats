from datetime import datetime
import locale

def handle_timestamp(timestamp, form = '%a %b %d %H:%M:%S %Y', loc = 'en_US.utf8' ): 

    locale.setlocale(locale.LC_ALL, loc)
    dt = datetime.strptime(timestamp, form)

    return dt
