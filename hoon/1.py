import requests

API_KEY = 'AIzaSyDB8Le7mss6eq1Wc2xTZK-4O2CN_mCuk9A'

def get_geolocation():
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={API_KEY}"

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

def reverse_geolocation(lat, lng):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&language=ko&key={API_KEY}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            address = data['results'][0]['formatted_address']
            print(f"주소: {address}")
            return address
        else:
            print(f"Error! 주소 정보 찾을 수 없음")
            return None
    else:
        print(f"Error! {response.status_code}")
        print(response.text)
        return None

reverse_geolocation(37.55315, 126.97253)