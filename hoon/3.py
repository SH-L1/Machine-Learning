import requests
import math

G_API_KEY = 'AIzaSyDB8Le7mss6eq1Wc2xTZK-4O2CN_mCuk9A'
W_API_KEY = 'nxLYi2YzPZd9BY7KvL0qv9xzsJMyRDnYMo1f7HvitPu5%2B3rbFK82CDjMCIQmFiodgJcZiRfyvxrExC1IZNQesw%3D%3D'

def weather_by_geo():
    geo = get_geolocation()
    if geo is None:
        print("Error!")
        return None

    lat, lng = geo
    nx, ny = convert_to_grid(lat, lng)
    get_raw_data(nx, ny)

def get_geolocation():
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={G_API_KEY}"

    response = requests.post(url, json={})

    if response.status_code == 200:
        data = response.json()
        lat = data['location']['lat']
        lng = data['location']['lng']
        accuracy = data.get('accuracy', 'unknown')
        print(f"위도: {lat}, 경도: {lng}, 정확도: {accuracy}")
        return lat, lng
    else:
        print(f"Error! {response.status_code}")
        print(response.text)
        return None

def convert_to_grid(lat, lon):
    RE = 6371.00877
    GRID = 5.0
    SLAT1 = 30.0
    SLAT2 = 60.0
    OLON = 126.0
    OLAT = 38.0
    XO = 43
    YO = 136

    DEGRAD = math.pi / 180.0

    re = RE / GRID
    slat1 = SLAT1 * DEGRAD
    slat2 = SLAT2 * DEGRAD
    olon = OLON * DEGRAD
    olat = OLAT * DEGRAD

    sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(math.pi * 0.25 + slat1 * 0.5)
    sf = (sf ** sn * math.cos(slat1)) / sn
    ro = math.tan(math.pi * 0.25 + olat * 0.5)
    ro = re * sf / (ro ** sn)

    ra = math.tan(math.pi * 0.25 + lat * DEGRAD * 0.5)
    ra = re * sf / (ra ** sn)
    theta = lon * DEGRAD - olon
    if theta > math.pi:
        theta -= 2.0 * math.pi
    if theta < -math.pi:
        theta += 2.0 * math.pi
    theta *= sn

    x = ra * math.sin(theta) + XO + 0.5
    y = ro - ra * math.cos(theta) + YO + 0.5
    return int(x), int(y)

def get_raw_data(nx, ny):
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
    params = {
        'serviceKey': W_API_KEY,
        'pageNo': '1',
        'numOfRows': '1000',
        'dataType': 'XML',
        'base_date': '20250508',
        'base_time': '0600',
        'nx': str(nx),
        'ny': str(ny)
    }

    res = requests.get(url, params=params)
    print("Status Code:", res.status_code)
    print("Content-Type:", res.headers.get("Content-Type"))
    if res.status_code == 200:
        print(res.text)
    else:
        print(f"Error! {res.status_code}")
