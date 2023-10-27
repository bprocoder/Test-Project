from datetime import datetime, timedelta
from dateutil import parser

def modify_datetime(input_datetime):
    now = datetime.now()
    input_datetime = datetime.strptime(str(input_datetime),"%Y-%m-%d %H:%M:%S.%f%z").replace(tzinfo=None)
    input_date = input_datetime.date()
    input_time = input_datetime.time()

    if input_date < now.date():
        formatted_date = input_datetime.strftime("%d/%m/%y")
        return formatted_date
    else:
        formatted_time = input_datetime.strftime("%I:%M %p")
        return formatted_time

# Example usage:
# input_datetime = datetime.strptime("2023-06-08 13:10:11.517037+00:00", "%Y-%m-%d %H:%M:%S.%f%z")
# result = modify_datetime(input_datetime)
# print(result)
