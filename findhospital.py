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
    fh = FindHospital("37.775232,-122.4197513")
    print(fh.find_hospital())