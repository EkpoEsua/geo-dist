"""Contains utility functions to support calculate view."""
from calculate import data
import json
from shapely.geometry import Point, Polygon
from geopy import distance as d


def clean_boundary_data(boundary: str) -> list:
    """Return cleaned boundary data as a list of coordinate pair.

    :params boundary: string containing boundary data.
    """
    boundary = json.loads(boundary)
    cleaned_boundary_data = list()

    for row in boundary:
        # -> longitude : latitude
        cleaned_boundary_data.append([row[1],row[2]])
    return cleaned_boundary_data

cleaned_mkad_data = clean_boundary_data(data.mkad)

mkad_boundary = Polygon(cleaned_mkad_data)

#find the centre point of Moscow Ring Road by calculating the centre of the mkad boundary
boundary_centre = mkad_boundary.centroid

moscow_ring_road_centre = (boundary_centre.y, boundary_centre.x)


def calculate_distance(latitude: float, longitude: float) -> float:
    """Return the computed  geodesic distance between the given longitude and latitude, 
    and Moscow Ring Road centre point.

    arguments:
    latitude -- a float 
    longitude -- a float
    """
    distance = -1
    point = Point(longitude, latitude)

    if mkad_boundary.contains(point):
        pass
    else:
        distance = d.distance((latitude, longitude), moscow_ring_road_centre)
        distance = distance.km
        distance = round(distance, 2)

    return distance

# #inside
# calculate_distance(55.830661, 37.533097)

# #edge
# calculate_distance(55.821072, 37.837148)

# #outside_edge
# calculate_distance(55.821072, 37.837153)

# #inside_edge
# calculate_distance(55.821071, 37.837110)

# #extreme
# calculate_distance(28.495632, -179.125429)

# #mid
# calculate_distance(0, 180)

# calculate_distance(55.75571349188569, 37.61924743652343)