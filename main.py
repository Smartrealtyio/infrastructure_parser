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
            for radius_value in radius_values:
                params = {
                    'q': object_type,
                    'in': 'circle:{lat},{lon};r={radius}'.format(lat=building['latitude'], lon=building['longitude'],
                                                                 radius=radius_value),
                    'limit': 100
                }
                print(params)
                response = requests.get(self.query, params=params)
                print(json.loads(response.content.decode())['items'])
                object_count = len(json.loads(response.content.decode())['items'])
                objects_counts.append(object_count)

        return objects_counts

    def start(self):
        iter_count = 0
        while iter_count < api_limit:
            buildings = self.db.get_flats()
            parsed_info = []
            for building in buildings:
                objects_counts = self.parse(building)
                parsed_info.append({building['id']: objects_counts})
                print(parsed_info)
                iter_count += len(self.objects) * len(radius_values)
            self.db.save_flats(parsed_info)
            print(parsed_info)


if __name__ == '__main__':
    worker_instance = InfrastructureParser()
    worker_instance.start()
