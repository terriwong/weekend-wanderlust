"""Geocoding and preparing data to load in db."""

from mapbox import Geocoder

def get_coordinates_by_address(address):

    geocoder = Geocoder()
    response = geocoder.forward(address)
    coordinates = response.geojson()['features'][0]['geometry']['coordinates']

    return coordinates  # [x, y]
