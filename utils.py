import errno
import os
import time
from math import sin, cos, acos, radians


class Utils:
    MEAN_EARTH_RADIUS_KM = 6371

    @staticmethod
    def write_to_file(filepath, content, backup=False):
        if filepath is None or len(content) == 0:
            raise ValueError('Unable to write to file, invalid parameters.')
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            if backup:
                backup_path = os.path.dirname(filepath) + "/history/" + time.strftime("%Y%m%d-%H%M%S") + "-" + \
                              filepath.split("/")[-1]
                os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                os.rename(filepath, backup_path)
            content = [line + '\n' for line in content]
            with open(filepath, "w") as f:
                f.writelines(content)
            print("Written to file: " + filepath)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise exc
        except Exception as e:
            print("Exception writing to : " + filepath)
            raise e

    @classmethod
    def great_circle_distance(cls, coords1, coords2):
        """
        Function that computes the great-circle distance between two input coords.
        Formula: https://en.wikipedia.org/wiki/Great-circle_distance
        :param coords1: First set of coordinates (latitude, longitude)
        :param coords2: Second set of coordinates (latitude, longitude)
        :return: Distance in kilometres.
        """
        if len(coords1) != 2 or len(coords2) != 2:
            raise ValueError('Unable to compute great circle distance, invalid parameters.')

        (lat_1, lon_1) = cls.coords_to_radians(coords1)

        (lat_2, lon_2) = cls.coords_to_radians(coords2)

        sin_lats = sin(lat_1) * sin(lat_2)
        cos_lats = cos(lat_1) * cos(lat_2)
        delta_lon = abs(lon_1 - lon_2)

        central_angle_rad = acos(sin_lats + cos_lats * cos(delta_lon))
        distance_km = cls.MEAN_EARTH_RADIUS_KM * central_angle_rad
        distance_km = round(distance_km, 2)

        return distance_km

    @classmethod
    def coords_to_radians(cls, coords):
        (lat, lon) = coords
        lat = radians(lat)
        lon = radians(lon)
        return lat, lon
