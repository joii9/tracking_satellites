import re
from datetime import datetime, timezone, timedelta
from sgp4.api import WGS72, Satrec, jday # Import jday
import numpy as np


def predict_orbit_current_time(tle_line1, tle_line2, year, month, day, hour):


    # Create a Satrec object from the TLE
    satellite = Satrec.twoline2rv(tle_line1, tle_line2)

    # Define the time for prediction (UTC)
    time_to_predict = datetime(year, month, day, hour, 0, 0) #, tzinfo=timezone.utc)

    # Convert the datetime object to Julian Date (jday) and fractional day (fr)
    # This is the crucial step for your sgp4 library version
    jd, fr = jday(time_to_predict.year, time_to_predict.month,
                  time_to_predict.day, time_to_predict.hour,
                  time_to_predict.minute, time_to_predict.second + time_to_predict.microsecond / 1e6)

    # Propagate the satellite using the two Julian Date arguments
    error, r, v = satellite.sgp4(jd, fr) # <-- This is the corrected change!

    if error:
        print(f"Error propagating satellite: {error}")
    else:
        # --- ECI to ECEF Conversion ---
        # We already have jd and fr, which represent the time,
        # so we can use them for GMST calculation, or use the datetime object.
        # The previous GMST calculation based on datetime is perfectly fine.

        # Calculate Julian Date (JD) and then Greenwich Mean Sidereal Time (GMST)
        # This is a simplified GMST calculation. For high precision, use a dedicated astropy function.
        # Reference: https://en.wikipedia.org/wiki/Sidereal_time#Formulas
        JD_for_GMST = (time_to_predict.toordinal() + 1721424.5 +
                       time_to_predict.hour / 24.0 +
                       time_to_predict.minute / (24.0 * 60.0) +
                       time_to_predict.second / (24.0 * 3600.0) +
                       time_to_predict.microsecond / (24.0 * 3600.0 * 1e6))

        # J2000 epoch (January 1, 2000, 12:00:00 TT) in JD
        JD_2000 = 2451545.0
        T_UT1 = (JD_for_GMST - JD_2000) / 36525.0

        GMST_deg = (280.46061837 + 360.98564736629 * (JD_for_GMST - JD_2000) +
                    0.000387933 * T_UT1**2 - T_UT1**3 / 38710000) % 360

        GMST_rad = np.deg2rad(GMST_deg)

        # Rotate ECI vector (r) by GMST to get ECEF vector (r_ecef)
        r_ecef_x = r[0] * np.cos(GMST_rad) + r[1] * np.sin(GMST_rad)
        r_ecef_y = -r[0] * np.sin(GMST_rad) + r[1] * np.cos(GMST_rad)
        r_ecef_z = r[2]
        r_ecef = np.array([r_ecef_x, r_ecef_y, r_ecef_z])

        # --- ECEF to Geodetic (Lat, Lon, Alt) Conversion ---
        a = 6378.137  # WGS84 Earth semi-major axis (km)
        f = 1 / 298.257223563  # WGS84 Earth flattening
        e2 = 2 * f - f**2  # Eccentricity squared

        p = np.sqrt(r_ecef[0]**2 + r_ecef[1]**2)
        lon = np.arctan2(r_ecef[1], r_ecef[0])

        # Initial guess for latitude
        lat = np.arctan2(r_ecef[2], p * (1 - e2))

        # Iterative solution for accurate latitude and altitude
        N = a / np.sqrt(1 - e2 * np.sin(lat)**2)
        alt = p / np.cos(lat) - N

        for _ in range(5):  # Iterate a few times for convergence
            lat_old = lat
            N = a / np.sqrt(1 - e2 * np.sin(lat)**2)
            lat = np.arctan2(r_ecef[2] + N * e2 * np.sin(lat), p)
            if abs(lat - lat_old) < 1e-10:
                break
            alt = p / np.cos(lat) - N

        lon_deg = np.degrees(lon)
        lat_deg = np.degrees(lat)

        # Ensure longitude is in the range [-180, 180]
        if lon_deg > 180:
            lon_deg -= 360
        elif lon_deg < -180:
            lon_deg += 360

        #print(f"At {time_to_predict} UTC:")
        #print(f"Longitud: {lon_deg:.4f} degrees")
        #print(f"Latitud: {lat_deg:.4f} degrees")
        #f"Altitud: {alt:.4f} km"

        # CONDICION PARA APENDEAR 
        if lon_deg < -15 and lon_deg > -165:
            write= tle_line1[2:-62]+"\n"+tle_line1+"\n"+tle_line2+"\nLongitud: "+str(lon_deg)+"\nLatitud: "+str(lat_deg)+"\nAltitud: "+str(alt)+"\nAt: "+str(time_to_predict)+"\n\n"
            #print(write)
            textfile= open("C:\\Users\\Joel\\Documents\\Python\\tracking_satellites\\txt\\Long_Lat_Alt_Range.txt", "a")
            textfile.write(write)
            textfile.close()


#current_time_utc= datetime.now(timezone.utc)
#
##print(current_time_utc)
#
#year=current_time_utc.year
#month=current_time_utc.month
#day=current_time_utc.day
#hour=current_time_utc.hour
#
##print(year)
##print(month)
##print(day)
##print(hour)
#
#
#
#file = open("C:/Users/Joel/Documents/Python/tracking_satellites/txt/Perigee_Apogee_Range_v3.txt", "r")
##print(file.read())
#str_TLEs_PAR=file.read()
##print(str_TLEs_PAR)
#
#tle_line1= re.findall(r"1\s\d+U.+", str_TLEs_PAR)#1\s\d+U
#tle_line2= re.findall(r"2\s\d+\s+\d+.\d+\s+\d+.\d+\s+\d+\s+.+", str_TLEs_PAR)
#
#for i in range(len(tle_line1)):
#    #print(tle_line1)
#    #print(tle_line2)
#    predict_orbit_current_time(tle_line1[i], tle_line2[i], year, month, day, hour)
#
##predict_orbit_current_time(tle_line1[0], tle_line2[0], year, month, day, hour)

