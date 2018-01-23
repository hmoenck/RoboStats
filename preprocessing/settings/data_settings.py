from datetime import datetime
import locale
import settings.default_params as default

def handle_timestamp(timestamp, form = default.time_format, loc = 'en_US.utf8' ): 
    print(timestamp)
    locale.setlocale(locale.LC_ALL, loc)
    dt = datetime.strptime(timestamp, form)

    return dt
