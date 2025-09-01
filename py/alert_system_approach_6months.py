from web_scrapping_Perigee_Apogee_Range_appendTLEs import *
from predict_orbit_current_time import *


#### Web Scrapping 1 - 100000 satellites
for i in range(1,100000):
    print(i)
    getting_Perigee_Apogee(i)



#### PREDICTING ORBINT IN CURRENT TIME
#### To determine longitude position between -15 and -165 deg
current_time_utc= datetime.now(timezone.utc)

#print(current_time_utc)

year=current_time_utc.year
month=current_time_utc.month
day=current_time_utc.day
hour=current_time_utc.hour

#print(year)
#print(month)
#print(day)
#print(hour)

file = open("C:/Users/Joel/Documents/Python/tracking_satellites/txt/Perigee_Apogee_Range_v3.txt", "r")
#print(file.read())
str_TLEs_PAR=file.read()
#print(str_TLEs_PAR)

tle_line1= re.findall(r"1\s\d+U.+", str_TLEs_PAR)#1\s\d+U
tle_line2= re.findall(r"2\s\d+\s+\d+.\d+\s+\d+.\d+\s+\d+\s+.+", str_TLEs_PAR)

for i in range(len(tle_line1)):
    #print(tle_line1)
    #print(tle_line2)
    predict_orbit_current_time(tle_line1[i], tle_line2[i], year, month, day, hour)

