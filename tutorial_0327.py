# DB 연결 -> cursor 생성 -> CRUD 
# 위의 과정들을 클래스화 해보자.

import psycopg2
import os
from dotenv import load_dotenv

# 보안 사항 .env
load_dotenv()
DBNAME = os.getenv('dbname_1')
USER = os.getenv('user_1')
PASSWORD = os.getenv('db_password_1')
HOST = os.getenv('host_1')
PORT = os.getenv('port_1')

# DB 클래스
class Database:
    def __init__(self, dbname, user, password, host, port):
        self.conn_params = {
            'dbname' : dbname,
            'user' : user,
            'password' : password,
            'host' : host,
            'port' : port
        }
        
        # self.conn = None 과 같이 명시하여 인스턴스 생성 시, conn 객체가 생성될 것을 암시할 수 있음
        self.make_conn() # make_conn() 메서드를 통한 커넥션 객체 생성 (DB와 연결)
        self.cur = self.make_cur() # make_cur() 메서드를 통한 커서 생성 -> self.cur 변수에 저장
        

    # 커넥션
    def make_conn(self):
        self.conn = psycopg2.connect(**self.conn_params)
    
    # 커서 생성
    def make_cur(self):
        return self.conn.cursor()

    # 쿼리 실행(execute) 메서드
    def execute_query(self, sql): # insert, update, delete 문 실행 시 실행될 메서드, 결과를 반환할 필요 x
        self.cur.execute(sql)
        self.conn.commit()

    # 결과 불러오기(fetch) 메서드
    def fetch_datas(self, sql): # select, select문 실행 시 결과를 반환해야 하므로 fetchall() 추가, commit할 필요 x(단지 조회하는 것이기 때문에)
        self.cur.execute(sql)
        output = self.cur.fetchall()
        return output
    
    # 연결 종료
    def close(self):
        self.cur.close()
        self.conn.close()

# CRUD 클래스, Actor 테이블을 예시로
class ActorCRUD:
    def __init__(self, db):
        self.db = db # db 연결
    
    def create(self, first_name, last_name):
        sql = f"""
            insert into actor (first_name, last_name) values ('{first_name}', '{last_name}')
        """
        self.db.execute_query(sql) # create이기 때문에 execute_query() 메서드 이용
    
    def read(self, first_name, last_name):
        sql = f"""
            select * from actor where first_name = '{first_name}' and last_name = '{last_name}'       
        """
        print(self.db.fetch_datas(sql)) # read는 fetch_datas() 메서드 이용
        
    def update(self, new_first_name, first_name):
        sql = f"""
            update actor set first_name = '{new_first_name}' where first_name = '{first_name}'
        """
        self.db.execute_query(sql)
        
    
    def delete(self, last_name):
        sql = f"""
            delete from actor where last_name = '{last_name}'
        """
        self.db.execute_query(sql)

# Database 인스턴스 생성
db = Database(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
# ActorCRUD 인스턴스 생성
actor_crud = ActorCRUD(db) # 인자로 생성된 db 인스턴스 넣어줌 -> 연결

# actor가 아래와 같이 여러 명일 때,
actor_names = [
    ('하늬', '이'),
    ('우성', '정'),
    ('정민', '황')
]
# 다음과 같은 반복문을 통해 데이터 생성 가능
for first_name_1, last_name_1 in actor_names:
    actor_crud.create(first_name=first_name_1, last_name=last_name_1)

# 황정민 배우 조회
actor_crud.read(first_name='정민', last_name='황')

# 이하늬 배우 이후희로 변경
actor_crud.update(new_first_name='후희', first_name='하늬')

# 성이 정인 배우 삭제
actor_crud.delete(last_name='정')
