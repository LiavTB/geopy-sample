from geopy.distance import great_circle

from utils.poi_type_to_points_distance import get_max_distance_for_classification, get_default_distance


class GeoLocationResult:
    def __init__(self, address, x, y, locator_name, classifications=None):
        if classifications is None:
            classifications = []
        self.address = address
        self.x = x
        self.y = y
        self.classifications = classifications
        self.locator_name = locator_name
        self.__last_match_check = None

    def get_distance(self, x, y):
        point_result = (self.y, self.x)
        point_original = (y, x)
        distance = great_circle(point_original, point_result).meters
        return distance

    def match(self, x, y):
        distance = self.get_distance(x, y)
        if len(self.classifications) != 0:
            self.__last_match_check = True in list(
                map(lambda classification: distance <= get_max_distance_for_classification(classification),
                    self.classifications))
        else:
            self.__last_match_check = distance <= get_default_distance()
        return self.__last_match_check

    def get_last_match_check(self):
        return self.__last_match_check
