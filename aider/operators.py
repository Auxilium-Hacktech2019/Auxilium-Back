import subprocess

def get_fare_id(start_longitude, start_latitude, end_longitude, end_latitude):

    shell = 'curl -X POST -H "Authorization: Bearer JA.VUNmGAAAAAAAEgASAAAABwAIAAwAAAAAAAAAEgAAAAAAAAG8AAAAFAAAAAAADgAQAAQAAAAIAAwAAAAOAAAAkAAAABwAAAAEAAAAEAAAAF4n4Ev1XX_06M7h07GUkGVsAAAAalJyiAOkLpJ4ukBu03sdRF5C3MYnotMBvYI5uJ4O8QtcfQJUdZPXuIAsI-VTNextrwkGAqegQTv2xho1JP3ctPR8q1a3ckIHrukIzJLfjStUYIxHj9eFmmMF4Sf7bZawoQ8BCaXSw54dc25fDAAAAJzyOofz3Fxt4FQ6RCQAAABiMGQ4NTgwMy0zOGEwLTQyYjMtODA2ZS03YTRjZjhlMTk2ZWU" \
     -H "Content-Type: application/json" -d \
     \'{"product_id": "57c0ff4e-1493-4ef9-a4df-6b961525cf92", "start_latitude":"37.775232", "start_longitude": "-122.4197513", "end_latitude":"37.7899886", "end_longitude": "-122.4021253","seat_count": "2"}\' \
      https://api.uber.com/v1.2/requests/estimate'
    child = subprocess.Popen(shell, shell=True, stdout=subprocess.PIPE)
    res_raw = child.communicate()[0]
    res_raw = json.loads(res_raw)
    fare_id = res_raw.get('fare').get('fare_id')
    return fare_id


def request_ride(fare_id):
    shell = 'curl -X POST \'https://sandbox-api.uber.com/v1.2/requests\' \
     -H \'Content-Type: application/json\' \
     -H \'Authorization: Bearer JA.VUNmGAAAAAAAEgASAAAABwAIAAwAAAAAAAAAEgAAAAAAAAG8AAAAFAAAAAAADgAQAAQAAAAIAAwAAAAOAAAAkAAAABwAAAAEAAAAEAAAAF4n4Ev1XX_06M7h07GUkGVsAAAAalJyiAOkLpJ4ukBu03sdRF5C3MYnotMBvYI5uJ4O8QtcfQJUdZPXuIAsI-VTNextrwkGAqegQTv2xho1JP3ctPR8q1a3ckIHrukIzJLfjStUYIxHj9eFmmMF4Sf7bZawoQ8BCaXSw54dc25fDAAAAJzyOofz3Fxt4FQ6RCQAAABiMGQ4NTgwMy0zOGEwLTQyYjMtODA2ZS03YTRjZjhlMTk2ZWU\' \
     -d \'{ "fare_id": "' + fare_id + '", "product_id": "57c0ff4e-1493-4ef9-a4df-6b961525cf92", "start_latitude": 37.761492, "start_longitude": -122.423941, "end_latitude": 37.775393, "end_longitude": -122.417546 }\''
    child = subprocess.Popen(shell, shell=True, stdout=subprocess.PIPE)
    res_raw = child.communicate()[0]
    print(res_raw)



import urllib.request
import ssl
import json

class FindHospital:
    def __init__(self, locationString):
        self.localLocationString = locationString

    def find_hospital(self):
        googleKey = 'AIzaSyBqPCGw7u3KY1ycZ8MpB7o5rCXIltzF7r8'
        ssl._create_default_https_context = ssl._create_unverified_context # dirty hack
        url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?key=' \
            + googleKey \
            + '&input=hospital&inputtype=textquery&locationbias=point:' \
            + self.localLocationString
        with urllib.request.urlopen(url) as response:
            obj = json.loads(response.read())
            hospitalId = obj['candidates'][0]['place_id']
        url = 'https://maps.googleapis.com/maps/api/place/details/json?key='\
            + googleKey \
            + '&placeid=' \
            + hospitalId
        with urllib.request.urlopen(url) as response:
            obj = json.loads(response.read())
            lat = obj['result']['geometry']['location']['lat']
            lng = obj['result']['geometry']['location']['lng']
        return lat, lng


if __name__ == '__main__':
    fare_id = get_fare_id(-118.124278, 34.146837,  -118.1147177, 34.1559884)
    request_ride(fare_id)

