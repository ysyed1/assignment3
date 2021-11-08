import urllib.request
import json
from pprint import pprint
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Useful URLs (you need to add the appropriate parameters for your requests)
MAPQUEST_BASE_URL = "http://www.mapquestapi.com/geocoding/v1/address"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"

# Your API KEYS (you need to use your own keys - very long random characters)
# Add Saanya Mapquest API Key here
MAPQUEST_API_KEY = ""
MBTA_API_KEY = "68b2a7ae63184c6c930c23dd6940c075"

# A little bit of scaffolding if you want to use it

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urllib.request.urlopen(url)
    response_text = f.read().decode('utf-8')
    response_data = json.loads(response_text)
    return response_data


def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.
    See https://developer.mapquest.com/documentation/geocoding-api/address/get/
    for Mapquest Geocoding  API URL formatting requirements.
    """
    place_name = str(place_name)
    place_name = place_name.replace(" ", "%20")
    place_name = f"{place_name},MA"
    url = f'http://www.mapquestapi.com/geocoding/v1/address?key={MAPQUEST_API_KEY}&location={place_name}'
    json_data = get_json(url)
    coordinates = json_data["results"][0]["locations"][0]["latLng"]
    latitude = coordinates["lat"]
    longitude = coordinates["lng"]
    return latitude, longitude


def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible)
    tuple for the nearest MBTA station to the given coordinates.
    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL
    formatting requirements for the 'GET /stops' API.
    """
    url = f"https://api-v3.mbta.com/stops?api_key={MBTA_API_KEY}&sort=distance&filter%5Blatitude%5D={latitude}&filter%5Blongitude%5D={longitude}"
    data = get_json(url)
    try:
        name = data["data"][0]["attributes"]["name"]
        wheelchair_accessible = data["data"][0]["attributes"]["wheelchair_boarding"]
    except:
        return "MBTA Not Available"
    if wheelchair_accessible == 0:
        wheelchair_accessible = "No Information"
    elif wheelchair_accessible == 1:
        wheelchair_accessible = "Accessible"
    else:
        wheelchair_accessible = "Inaccessible"
    return f"Station: {name}, Wheelchair Accessibility: {wheelchair_accessible}"


def find_stop_near(place_name):
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.
    """
    location_data = get_lat_long(place_name)
    latitude = location_data[0]
    longitude = location_data[1]
    return get_nearest_station(latitude, longitude)


def main():
    """
    You can test all the functions here
    """
    place = str(input("Please enter your location here: "))
    print(find_stop_near(place))


if __name__ == '__main__':
    main()
