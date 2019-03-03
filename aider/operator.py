import urllib.request
import urllib.parse
import ssl

def getFareId(start_longitude, start_latitude, end_longitude, end_latitude):
    ssl._create_default_https_context = ssl._create_unverified_context  # dirty hack
    raw_data = {
        'Authorization Bearer': 'JA.VUNmGAAAAAAAEgASAAAABwAIAAwAAAAAAAAAEgAAAAAAAAG8AAAAFAAAAAAADgAQAAQAAAAIAAwAAAAOAAAAkAAAABwAAAAEAAAAEAAAAF4n4Ev1XX_06M7h07GUkGVsAAAAalJyiAOkLpJ4ukBu03sdRF5C3MYnotMBvYI5uJ4O8QtcfQJUdZPXuIAsI-VTNextrwkGAqegQTv2xho1JP3ctPR8q1a3ckIHrukIzJLfjStUYIxHj9eFmmMF4Sf7bZawoQ8BCaXSw54dc25fDAAAAJzyOofz3Fxt4FQ6RCQAAABiMGQ4NTgwMy0zOGEwLTQyYjMtODA2ZS03YTRjZjhlMTk2ZWU',
        'Content-Type': 'application/json',
        'product_id': '57c0ff4e-1493-4ef9-a4df-6b961525cf92',
        'start_latitude': start_latitude,
        'start_longitude': start_longitude,
        'end_latitude': end_latitude,
        'end_longitude': end_longitude,
        'seat_count': '2'
    }
    data = urllib.parse.urlencode(raw_data).encode()
    url = "https://api.uber.com/v1.2/requests/estimate"
    req = urllib.request.Request(url, data=data)  # this will make the method "POST"
    resp = urllib.request.urlopen(req)
    print(resp)

if __name__ == '__main__':
    getFareId(34.146837, -118.124278, 34.1559884, -118.1147177)
