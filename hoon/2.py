import requests

API_KEY = 'nxLYi2YzPZd9BY7KvL0qv9xzsJMyRDnYMo1f7HvitPu5%2B3rbFK82CDjMCIQmFiodgJcZiRfyvxrExC1IZNQesw%3D%3D'

def get_raw_data(nx, ny):
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
    params = {
        'serviceKey': API_KEY,
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

get_raw_data(60, 127)