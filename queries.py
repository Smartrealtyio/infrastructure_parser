import psycopg2

from settings_local import db_info


class QueryMaker:

    def __init__(self):
        self.conn = psycopg2.connect(host=db_info['host'], dbname=db_info['name'], user=db_info['user'],
                                     password=db_info['password'])
        self.cur = self.conn.cursor()

    def get_flats(self):
        query = """SELECT id, longitude, latitude FROM buildings WHERE schools_500m IS NULL LIMIT 10;"""
        buildings_coord = self.cur.execute(query)
        print(buildings_coord)
        return buildings_coord

    def save_flats(self, parsed_info):
        query = """
        UPDATE buildings 
        SET schools_500m=%s, schools_1000m=%s, kindergartens_500m=%s, kindergartens_1000m=%s, 
        clinics_500m=%s, clinics_1000m=%s, shops_500m=%s, shops_1000m=%s 
        WHERE id=%s
        """
        for params in parsed_info:
            self.cur.execute(query, params)
        self.conn.commit()
