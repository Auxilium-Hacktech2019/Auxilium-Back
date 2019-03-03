# from uber_rides.session import Session
# from uber_rides.client import UberRidesClient
# from uber_rides.auth import AuthorizationCodeGrant
#
# def getFareId(start_longitude, start_latitude, end_longitude, end_latitude):
#     # session = Session(server_token=KFbcEFDXPPKO0dw8Q8li2JV - Eh0bCaXnFEGediYn)
#
#     auth_flow = AuthorizationCodeGrant(
#         'VXsQntCvlmfiTFw9dNhRA81jXDCO_yNU',
#         'profile delivery history places ride_widgets all_trips request_receipt request',
#         'x_yctuQtvsEo1IMTnDotNdBazZM_gR_WYZMjHYYx',
#         'https://hacktech-2019-lifesavor.github.io'
#     )
#     auth_url = auth_flow.get_authorization_url()
#     print(auth_url)
#     return
#
#     session = auth_flow.get_session(redirect_url)
#     client = UberRidesClient(session, sandbox_mode=True)
#     credentials = session.oauth2credential
#
#     # Get products for a location
#     # response = client.get_products(start_latitude, start_longitude)
#     # products = response.json.get('products')
#
#     product_id = '57c0ff4e-1493-4ef9-a4df-6b961525cf92'
#
#     # Get upfront fare and start/end locations
#     estimate = client.estimate_ride(
#         product_id=product_id,
#         start_latitude=start_latitude,
#         start_longitude=start_longitude,
#         end_latitude=end_latitude,
#         end_longitude=end_longitude,
#         seat_count=2
#     )
#     fare = estimate.json.get('fare')
#
#     # Request a ride with upfront fare and start/end locations
#     response = client.request_ride(
#         product_id=product_id,
#         start_latitude=start_latitude,
#         start_longitude=start_longitude,
#         end_latitude=end_latitude,
#         end_longitude=end_longitude,
#         seat_count=2,
#         fare_id=fare['fare_id']
#     )
#
#     request = response.json
#     request_id = request.get('request_id')
#
#     # Request ride details using `request_id`
#     response = client.get_ride_details(request_id)
#     ride = response.json
#
#
# if __name__ == '__main__':
#     getFareId(34.146837, -118.124278, 34.1559884, -118.1147177)
