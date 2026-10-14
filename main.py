import requests
from datetime import datetime
import smtplib
import os
from dotenv import load_dotenv



# Find iss and return position  @lng and @lat
def find_iss():
    iss_response = requests.get(url='http://api.open-notify.org/iss-now.json')
    print(iss_response.json())
    lng = float(iss_response.json()['iss_position']['longitude'])
    lat = float(iss_response.json()['iss_position']['latitude'])
    location =(lat,lng)
    return location


# Find if the sun is up or not
def is_dark():
    sunset_response = requests.get(url=f'https://api.sunrise-sunset.org/json',params=parameters)
    sunset_response.raise_for_status()
    data = sunset_response.json()
    sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])
    print("Data:", data)
    print("Sunrise: ", sunrise)
    print("Sunset: ", sunset)
    print("Time now: ", time_now)
    if sunrise < time_now < sunset:
        return True
    else:
        return False
load_dotenv()
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")
LATITUDE = float(os.environ.get("LATITUDE","0.0"))
LONGITUDE = float(os.environ.get("LONGITUDE","0.0"))
MY_LOCATION = (LATITUDE,LONGITUDE)
parameters = {'lat':MY_LOCATION[0],
              'lng': MY_LOCATION[1],
              'formatted': 0,
              'tzid':'America/New_York'}
time_now = datetime.now().hour
iss_location = find_iss()

if MY_LOCATION[0]-5 < iss_location[0] < MY_LOCATION[0] +5:
    if is_dark():

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,to_addrs='gedeonfikru@gmail.com',
                            msg="Subject:ISS overhead\n\nLook up, the International space station is overhead")
    if not is_dark():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs='gedeonfikru@gmail.com',
                            msg="Subject:Too bad you can't see it\n\nTest complete")
else:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs='gedeonfikru@gmail.com',
                            msg="Subject: Test 2\n\nTest done")

