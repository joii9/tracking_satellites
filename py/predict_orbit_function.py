from datetime import datetime, timezone, timedelta
from sgp4.api import WGS72, Satrec, jday # Import jday
import numpy as np
import time


def predict_orbit(tle_line1, tle_line2, year, month, day, hour):


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

        print(f"At {time_to_predict} UTC:")
        print(f"Longitud: {lon_deg:.4f} degrees")
        print(f"Latitud: {lat_deg:.4f} degrees")
        f"Altitud: {alt:.4f} km"


#TLEs
tle_line1 = "1 23168U 94038A   25205.46876539 -.00000083  00000-0  00000-0 0  9998"
tle_line2 = "2 23168  13.9258 355.0578 0007968 128.6983 238.2166  1.00162475113728"


#Increment in date
current_time_utc= datetime.now(timezone.utc)
#print(current_time)

#start_time = time.time()  # Record the start time
for hour_to_add in range(745):
    #print(hour_to_add)
    time_increment= timedelta(hours=hour_to_add)
    future_time = current_time_utc + time_increment
    #print(type(future_time))
    
    year=future_time.year
    month=future_time.month
    day=future_time.day
    hour=future_time.hour

    predict_orbit(tle_line1, tle_line2, year, month, day, hour)
    #print(f"{year}- {month}- {day}- {hour}")
#end_time = time.time()    # Record the end time
#execution_time = end_time - start_time
#print(f"Execution time: {execution_time:.4f} seconds")




# CODE TO TEST THE TIME OF EXECUTION OF A FUNCTION

#start_time = time.time()  # Record the start time
# Your code goes here



#end_time = time.time()    # Record the end time
#execution_time = end_time - start_time
#print(f"Execution time: {execution_time:.4f} seconds")
