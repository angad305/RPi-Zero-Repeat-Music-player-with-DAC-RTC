import sys
import os

# Fix your library path
libdir = '~/PCF8563-Code/lib'
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_PCF8563 import PCF8563

# Initialize the PCF8563 RTC without reset
rtc = PCF8563.PCF8563()

# Read raw register values
second_raw = rtc.read(0x02)
minute_raw = rtc.read(0x03)
hour_raw = rtc.read(0x04)
day_raw = rtc.read(0x05)
month_raw = rtc.read(0x07)
year_raw = rtc.read(0x08)

print("Raw Register Values:")
print(f"Second: 0x{second_raw:02x}")
print(f"Minute: 0x{minute_raw:02x}")
print(f"Hour: 0x{hour_raw:02x}")
print(f"Day: 0x{day_raw:02x}")
print(f"Month: 0x{month_raw:02x}")
print(f"Year: 0x{year_raw:02x}")

# Verify the conversion methods
print("\nConverted Values:")
second = rtc.changeHexToInt(second_raw & 0x7f)
minute = rtc.changeHexToInt(minute_raw & 0x7f)
hour = rtc.changeHexToInt(hour_raw & 0x3f)
day = rtc.changeHexToInt(day_raw & 0x3f)
month = rtc.changeHexToInt(month_raw & 0x1f)
year = year_raw

print(f"Second: {second}")
print(f"Minute: {minute}")
print(f"Hour: {hour}")
print(f"Day: {day}")
print(f"Month: {month}")
print(f"Year: {year}")

# Century bit check
century_bit = (month_raw & 0x80) >> 7
print(f"\nCentury Bit: {century_bit} (0 = 20xx, 1 = 19xx)")

# Battery status
print(f"\nClock Working Bit: {(second_raw & 0x80) >> 7} (0 = working, 1 = stopped/battery issue)")