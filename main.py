import requests
import json

from settings_local import *
from queries import QueryMaker


class InfrastructureParser:

    def __init__(self):
        self.db = QueryMaker()
        self.query = query_url
        self.objects = objects

    def parse(self, building):
        print(building)
        objects_counts = []
        for object_type in self.objects:
            for radius_value in rad_intervals:
                response = requests.get(self.query, params={
                    'text': object_type,
                    'll': '{lon},{lat}'.format(lon=building['longitude'], lat=building['latitude']),
                    'spn': '{lon_rad},{lat_rad}'.format(
                        lon_rad=longitude_rad * radius_value,
                        lat_rad=latitude_rad * latitude_rad)
                })
                object_count = len(json.loads(response.content.decode())['features'])
                objects_counts.append(object_count)

    def start(self):
        iter_count = 0
        while iter_count < api_limit:
            buildings = self.db.get_flats()
            parsed_info = []
            for building in buildings:
                objects_counts = self.parse(building)
                parsed_info.append(objects_counts)
                print(parsed_info)
                iter_count += len(self.objects) * len(rad_intervals)
            self.db.save_flats(parsed_info)


if __name__ == '__main__':
    worker_instance = InfrastructureParser()
    worker_instance.start()
