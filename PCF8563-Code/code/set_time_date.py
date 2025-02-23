from datetime import datetime
import sys
import os

libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '~/PCF8563-Code/lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_PCF8563 import PCF8563

# Get the current system time
now = datetime.now()
hour = now.hour
minute = now.minute
second = now.second
year = now.year
month = now.month
day = now.day

# Initialize the PCF8563 RTC
rtc = PCF8563.PCF8563()
rtc.Init()

# Set the RTC time and date
rtc.Set_Time(hour, minute, second)
rtc.Set_Days(year, month, day)

print("RTC time and date set successfully.")
# Verify the time and date
current_time = rtc.Get_Time()
current_date = rtc.Get_Days()

print(f"Current Time: {current_time[2]:02d}:{current_time[1]:02d}:{current_time[0]:02d}")
print(f"Current Date: {current_date[0]:02d}/{current_date[1]:02d}/{current_date[3]}{current_date[2]:02d}")