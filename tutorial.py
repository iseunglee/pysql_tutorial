# postgresql sample db에서 country table을 이용하여 CRUD를 만들기
# 1. country table의 모든 데이터를 조회하기
# 2. country table에 데이터를 추가하기
# 3. country table의 데이터를 수정하기
# 4. country table의 데이터를 삭제하기
# class로 만들기

import psycopg2

class CountyCRUD:
    def __init__(self):
        self.conn_params = {
            'dbname': 'testdb_leesh',
            'user': 'postgres',
            'password': 'G=nf_-}EKl',
            'host': 'hanslab.org',
            'port': '25432'
        }
        self.conn = None
        self.connect()

    def connect(self):
        """데이터베이스에 연결합니다."""
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            print("데이터베이스에 성공적으로 연결되었습니다.")
        except psycopg2.Error as e:
            print(f"데이터베이스 연결 중 오류가 발생했습니다: {e}")

    def create_country(self, country):
        """country 테이블에 새로운 나라를 추가합니다."""
        print(country)
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO country (country)
                VALUES (%s) RETURNING country_id;
            """, (country,))
            country_id = cur.fetchone()[0]
            self.conn.commit()
            print(f"국가 '{country}'이(가) country {country_id}로 추가되었습니다.")
            return country_id
        # with self.conn.cursor() as cur:
        #     cur.execute("""
        #         INSERT INTO country (country)
        #         VALUES (%s);
        #     """, (country,))
        #     # country_id = cur.fetchone()[0]
        #     self.conn.commit()
        #     # print(f"국가 '{country}'이(가) country {country_id}로 추가되었습니다.")
        #     # return country_id
    def read_country(self,country_id):
        """country_id 기반으로 국가 정보를 조회합니다."""
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM country WHERE country_id = %s;", (country_id,))
            country = cur.fetchone()
            if country:
                print(country)
                return country
            else:
                print("국가를 찾을 수 없습니다.")
                return None
    def read_all_country(self):
        """country_id 기반으로 국가 정보를 전체 조회합니다."""
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM country;")
            countrys = cur.fetchall()
            for country in countrys:
                print(country)

    def update_country(self, country_id, country):
        """country 정보를 업데이트합니다."""
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE country
                SET country = %s
                WHERE country_id = %s;
            """, (country, country_id))
            self.conn.commit()
            print(f"국가 {country_id}의 정보가 업데이트되었습니다.")
    def delete_country(self,country_id):
        """영화 정보를 삭제합니다."""
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM country WHERE country_id = %s;", (country_id,))
            self.conn.commit()
            print(f"country {country_id}의 정보가 삭제되었습니다.")
    def close(self):
        self.conn.close()

country_crud = CountyCRUD()
country_id = country_crud.create_country("Lion")
country_crud.read_country(country_id)
country_crud.read_all_country()
country_crud.update_country(country="Tiger", country_id=country_id )
country_crud.delete_country(country_id)
country_crud.close()