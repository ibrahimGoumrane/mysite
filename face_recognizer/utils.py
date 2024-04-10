from datetime import datetime, timedelta,date
import math

class Utils :
    def set_current_time(self,date:datetime=datetime.now())->dict:
        Date_Info =  date.strftime("%Y-%m-%d")
        current_day = date.strftime('%A')
        current_hour = math.floor(date.hour)
        return {
            'start_hour': current_hour,
            'end_hour': current_hour + 2,
            'week_day': current_day,
            'full_date': Date_Info,
        }
    
utils=Utils()
