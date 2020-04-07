import psycopg2

from settings_local import db_info, query_limit


class QueryMaker:

    def __init__(self):
        self.conn = psycopg2.connect(host=db_info['host'], dbname=db_info['name'], user=db_info['user'],
                                     password=db_info['password'])
        self.cur = self.conn.cursor()

    def get_flats(self):
        query = f"""SELECT id, longitude, latitude FROM buildings WHERE schools_500m IS NULL LIMIT {query_limit};"""
        self.cur.execute(query)
        columns = [column[0] for column in self.cur.description]
        buildings_coord = []
        for row in self.cur.fetchall():
            buildings_coord.append(dict(zip(columns, row)))
        return buildings_coord

    def save_flats(self, parsed_info):
        query = """
        UPDATE buildings
        SET schools_500m={}, schools_1000m={}, kindergartens_500m={}, kindergartens_1000m={},
        clinics_500m={}, clinics_1000m={}, shops_500m={}, shops_1000m={}
        WHERE id={};
        """
        for id, params in parsed_info.items():
            print(query.format(*params, id), flush=True)
            self.cur.execute(query.format(*params, id))
            print('SAVE OK', flush=True)
        self.conn.commit()
        print('SUCCESS TRANSACTION', flush=True)
