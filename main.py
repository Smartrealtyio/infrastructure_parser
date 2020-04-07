import requests
import json
import traceback
import sys

from settings_local import *
from queries import QueryMaker


class InfrastructureParser:

    def __init__(self):
        self.db = QueryMaker()
        self.query = query_url
        self.objects = objects

    def parse(self, building):
        print(building, flush=True)
        objects_counts = []
        for object_type in self.objects:
            for radius_value in radius_values:
                params = {
                    'q': object_type,
                    'in': 'circle:{lat},{lon};r={radius}'.format(lat=building['latitude'], lon=building['longitude'],
                                                                 radius=radius_value),
                    'limit': 100
                }
                # print(params)
                try:
                    response = requests.get(self.query, params=params)
                    #print(json.loads(response.content.decode()))
                    object_count = len(json.loads(response.content.decode())['items'])
                    objects_counts.append(object_count)
                except Exception as e:
                    print('\n'.join(traceback.format_exception(*sys.exc_info())), flush=True)

        return objects_counts

    def start(self):
        iter_count = 0
        while iter_count < api_limit:
            buildings = self.db.get_flats()
            parsed_info = {}
            for building in buildings:
                objects_counts = self.parse(building)
                parsed_info.update({building['id']: objects_counts})
                print(parsed_info, flush=True)
                iter_count += len(self.objects) * len(radius_values)
            self.db.save_flats(parsed_info)
            print('ITER COUNT', iter_count, flush=True)


if __name__ == '__main__':
    worker_instance = InfrastructureParser()
    worker_instance.start()
