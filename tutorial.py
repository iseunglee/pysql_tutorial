# postgresql sample db에서 country table을 이용하여 CRUD를 만들기
# 1. country table의 모든 데이터를 조회하기
# 2. country table에 데이터를 추가하기
# 3. country table의 데이터를 수정하기
# 4. country table의 데이터를 삭제하기
# class로 만들기

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DBNAME = os.getenv('dbname')
USER = os.getenv('user')
PASSWORD = os.getenv('db_password')
HOST = os.getenv('host')
PORT = os.getenv('port')

class CountryCRUD:

    def __init__(self, dbname, user, password, host, port):
        # 연결 파라미터 설정
        self.conn_params = {
            'dbname' : dbname,
            'user' : user,
            'password' : password,
            'host' : host,
            'port': port
        }
        self.conn = None
        self.connect()

    def connect(self):
        '''DB에 연결합니다.'''
        try:
            self.conn = psycopg2.connect(**self.conn_params) # conn_params로 DB 연결 시도
            print("DB에 성공적으로 연결되었습니다.")
        except psycopg2.Error as e:
            print(f"DB 연결 중 오류가 발생했습니다. : {e}")

    def create_country(self, country):
        '''country 테이블에 새로운 나라를 추가합니다.'''
        print(country)
        with self.conn.cursor() as cur: # 커서 객체를 사용하여 DB 작업 수행
            cur.execute("""
                INSERT INTO country (country)
                VALUES (%s) RETURNING country_id;""", (country))
            country_id = cur.fetchone()[0] # 쿼리 결과 country_id 변수에 저장
            self.conn.commit() # 변경 사항을 DB에 커밋
            print(f"국가 '{country}'이 (가) country {country_id}로 추가되었습니다.")
            return country_id
        
    def read_country(self, country_id):
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
    
    def update_country(self, country_id, country=None):
        """country 정보를 업데이트합니다."""
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE country
                SET country = %s
                WHERE country_id = %s;
            """, (country, country_id))
            self.conn.commit()
            print(f"국가 {country_id}의 정보가 업데이트되었습니다.")

    def delete_country(self, country_id):
        """country 정보를 삭제합니다."""
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM country WHERE country_id = %s;", (country_id,))
            self.conn.commit()
            print(f"country {country_id}의 정보가 삭제되었습니다.")
    
    def close(self):
        """데이터베이스 연결을 종료합니다."""
        if self.conn:
            self.conn.close()
            print("데이터베이스 연결이 종료되었습니다.")

# CountryCRUD 인스턴스 생성
country_crud = CountryCRUD(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)

# 새로운 country 추가
country_id = country_crud.create_country("mountain")

# country 정보 조회
country_crud.read_country(country_id)

# country 정보 업데이트
country_crud.update_country(country_id, country="mountain")

# country 정보 삭제
country_crud.delete_country(country_id)

# 데이터베이스 연결 종료
country_crud.close()