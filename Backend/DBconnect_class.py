from ast import Global
import os
import pymysql
from dotenv import load_dotenv

class Connect_to_DB:
    def __init__(self, server):
        self.server = server
        self.index = 0
        self.ID_index = 0
        self.sql = ''''''
        load_dotenv()

        try:
            self.wv_db_connection = pymysql.connect(
                user=os.getenv('DB_ID'),
                passwd=os.getenv('DB_PW'),
                host=os.getenv('DB_HOST'),
                port=int(os.getenv('DB_PORT')),
                db=os.getenv('DB_NAME'),
                charset='utf8'
            )
            self.cursor = self.wv_db_connection.cursor(pymysql.cursors.DictCursor)  # 딕셔너리 형태로 가져옴
            self.server.app.logger.info(f"DB연결 인스턴스 생성됨")
        except pymysql.MySQLError as e:
            self.server.app.logger.error(f"DB 연결 오류: {e}")
            raise ConnectionError(f"Failed to connect to the database: {e}")

    def add_sql(self, sql):
        self.sql += sql
        self.server.app.logger.info(f"추가된 SQL: {sql}\n최종 SQL: {self.sql}")
        return self

    def execute(self):
        try:
            self.cursor.execute(self.sql)
            self.inserted_id = self.cursor.lastrowid
            self.row_count = self.cursor.rowcount
            self.server.app.logger.info(f"SQL 쿼리 실행됨\ninserted_id: {self.inserted_id}   row_count: {self.row_count}\n SQL: {self.sql}")
        except pymysql.MySQLError as e:
            self.server.app.logger.error(f"SQL 실행 오류: {e}")
            raise RuntimeError(f"Failed to execute SQL query: {e}")
        return self

    def commit(self):
        try:
            self.wv_db_connection.commit()
            self.inserted_id = self.cursor.lastrowid
            self.row_count = self.cursor.rowcount
            self.server.app.logger.info(f"SQL 커밋됨\ninserted_id: {self.inserted_id}   row_count: {self.row_count}\n SQL: {self.sql}")
        except pymysql.MySQLError as e:
            self.server.app.logger.error(f"SQL 커밋 오류: {e}")
            raise RuntimeError(f"Failed to commit SQL query: {e}")
        return self

    def fetch(self):  # SELECT할때 결과 가져옴
        try:
            self.fetch_data = self.cursor.fetchone()  # 하나만 가져오는거 같은데...
            self.server.app.logger.info(f"페치됨 fetch_data:\n{self.fetch_data}")
        except pymysql.MySQLError as e:
            self.server.app.logger.error(f"데이터 페치 오류: {e}")
            raise RuntimeError(f"Failed to fetch data: {e}")
        return self



   



#쓰래기-------------------------------------------------------------------------------------------------------------------------

    def db_reset(self): #리뷰 SQL테이블 초기화
        self.cursor = self.wv_db.cursor(pymysql.cursors.DictCursor)
        self.sql = '''TRUNCATE TPJ.All_Review;'''
        self.cursor.execute(self.sql)
        self.review_db.commit()
        self.server.app.logger.info(f"리뷰 SQL테이블 초기화")


    def review_reset(self): #리뷰 SQL테이블 초기화
        self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
        self.sql = '''TRUNCATE TPJ.All_Review;'''
        self.cursor.execute(self.sql)
        self.review_db.commit()
        print("Review_RESET")

    def user_reset(self): #리뷰 SQL테이블 초기화
        self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
        self.sql = '''TRUNCATE TPJ.All_User;'''
        self.cursor.execute(self.sql)
        self.review_db.commit()
        print("User_RESET")

    def registed_store_check(self,store):   #리뷰_사업장등록여부 확인
        try:
            self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
            self.sql = '''SELECT * FROM TPJ.All_Review WHERE store='%s';'''%store
            self.cursor.execute(self.sql)
            if self.cursor.fetchall():
                print(store+"은(는) 이미 등록되었음")
                return True
            else:
                self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
                self.sql = '''SELECT * FROM TPJ.All_Review WHERE store_num='%s';'''%store
                self.cursor.execute(self.sql)
                if self.cursor.fetchall():
                    print(store+"은(는) 이미 등록되었음")
                    return True
                else:
                    return False

        except:
            print("**Store Check Error**")
    #print(registed_store_check('1234'))

    
    def review_index_setting(self): #리뷰 최대인덱스 리턴, 지정
        try:
            self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
            self.sql = '''SELECT MAX(num) FROM TPJ.All_Review;'''
            self.cursor.execute(self.sql)
            self.maxindex = self.cursor.fetchall()
            self.index=self.maxindex[0]['MAX(num)']

            print('END_index:',self.index)
            if self.index==None:
                self.index=0
        except:
            print("**Index Setting Error**")
        return self.index
        
    #review_index_setting()
    def review_insert(self, id, store, store_num, score_flav, score_quan, score_deli, order, review, reply, date):    #리뷰 SQL 넣기
        self.log=str(self.index+1)+'\t'+"INSERT: "+str(id)+' '+str(store)+' '+str(store_num)+' '+str(score_flav)+' '+str(score_quan)+' '+str(score_deli)+' '+str(order)+' '+str(review)+' '+str(reply)+' '+str(date)+'\t\t'
        try:
            self.index+=1
            if reply==None:
                self.sql = '''INSERT INTO `All_Review` (num, id, store, store_num, score_flav, score_quan, score_deli, food, review, date) 
                VALUES ('%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');'''%(self.index ,id, store, store_num, score_flav, score_quan, score_deli, order, review, date)
            else:
                self.sql = '''INSERT INTO `All_Review` (num, id, store, store_num, score_flav, score_quan, score_deli, food, review, reply, date) 
                VALUES ('%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');'''%(self.index ,id, store, store_num, score_flav, score_quan, score_deli, order, review, reply, date)
            self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute(self.sql)
            self.review_db.commit()
            self.log+="SUCCESS"
            self.print_log()  
        except pymysql.err.DataError:
            self.log+="**DataError**"
            self.print_log()

        except pymysql.err.IntegrityError:      
            self.log+="IntegrityError"
            self.print_log()
            self.index+=1
            self.review_insert(id, store, store_num, score_flav, score_quan, score_deli, order, review, reply, date)
        except KeyError:
            self.log+="**DuplicationError**"
            self.print_log()
        except pymysql.err.ProgrammingError:
            self.log+="**ProgrammingError**"
            self.print_log()
        
    

    
    def return_score(self,id):     #사용자의 점수 데이터프레임 리턴
        try:
            self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
            self.sql = '''SELECT num,score_flav,score_quan,score_deli FROM TPJ.All_Review WHERE id='%s';'''%id
            self.cursor.execute(self.sql)
            df=pd.DataFrame(self.cursor.fetchall())
            df=df.set_index('num')
            print(df)
            return df
        except:
            print("**Get Score Error**")
    
    def updata_std_score(self,num,std_score):   #사용자의 표준화점수 업로드
        self.log=str(num)+'\t'+"UPDATE: "+str(num)+'\t'+str(std_score)+'\t\t'
        try:
            self.sql = '''UPDATE TPJ.All_Review SET std_score = '%s' WHERE num='%s';'''%(std_score,num)
            self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute(self.sql)
            self.review_db.commit()
            self.log+="SUCCESS"
            self.print_log()

        except pymysql.err.DataError:
            self.log+="**DataError**"
            self.print_log()
        except pymysql.err.IntegrityError:      
            self.log+="IntegrityError"
            self.print_log()
            self.updata_std_score(num,std_score)
        except KeyError:
            self.log+="**DuplicationError**"
            self.print_log()
        except pymysql.err.ProgrammingError:
            self.log+="**ProgrammingError**"
            self.print_log()            
    
    
    def not_std_user_review(self):  #표준화되지 않은 유저 접근
        self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
        self.sql = '''SELECT DISTINCT id,store FROM TPJ.All_Review WHERE std_score = 0;'''
        self.cursor.execute(self.sql)
        self.maxindex = pd.DataFrame(self.cursor.fetchall())
        print('NOT Standardization ID:\n',self.maxindex)
        return self.maxindex

    def review_store_score(self,store):  #가계별 리뷰점수
        self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
        self.sql = '''SELECT std_score,trust_level FROM TPJ.All_Review WHERE store ='%s';'''%store
        self.cursor.execute(self.sql)
        self.maxindex = pd.DataFrame(self.cursor.fetchall())
        print('Standardization Score:\n',self.maxindex)
        return self.maxindex
    
    def count_store_review(self,store): #사업장별 리뷰갯수
        self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
        self.sql = '''SELECT count(*) FROM TPJ.All_Review where store= '%s';'''%store
        self.cursor.execute(self.sql)
        self.many = pd.DataFrame(self.cursor.fetchall()).loc[0,'count(*)']
        print('Number of review:',self.many)
        return self.many
    
    def GUI_search_review(self,store): #GUI리뷰 검색
        self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
        self.sql = '''SELECT id, store, score_flav, score_quan, score_deli, food, review, date, std_score*trust_level FROM TPJ.All_Review WHERE store_num='%s';'''%(store)
        self.cursor.execute(self.sql)
        self.result = pd.DataFrame(self.cursor.fetchall())
        print('Review:\n',self.result)
        return self.result

    def AI_search_review(self): #AI리뷰 검색
        self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
        self.sql = '''SELECT num, std_score*trust_level, review FROM TPJ.All_Review WHERE trust_level=1 order by rand() limit 20;;'''
        print("Runing......")
        self.cursor.execute(self.sql)
        self.result = pd.DataFrame(self.cursor.fetchall())#.set_index('num')
        print('Review:\n',self.result)
        return self.result

    def AI_trust_level_updete(self,num,trust_level):  #AI신뢰도 업데이트
        self.log=str(num)+'\t'+"UPDATE: "+str(trust_level)+'\t\t'
        try:
            #self.Store_index+=1
            self.sql = '''UPDATE TPJ.All_Review SET trust_level = '%s' WHERE num='%s';'''%(trust_level,num)
            self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute(self.sql)
            self.review_db.commit()
            self.log+="SUCCESS"
            self.print_log()  
        except pymysql.err.DataError:
            self.log+="**DataError**"
            self.print_log()

        except pymysql.err.IntegrityError:      
            self.log+="IntegrityError"
            self.print_log()
            #self.Store_index+=1
            #self.review_insert(yogiyo, store, store_num, address)
        except KeyError:
            self.log+="**DuplicationError**"
            self.print_log()
        except pymysql.err.ProgrammingError:
            self.log+="**ProgrammingError**"
            self.print_log()

#유저-----------------------------------------------------------------------------------------------------------------------

    def ID_index_setting(self): #ID 최대인덱스 리턴, 지정
        try:
            self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
            self.sql = '''SELECT MAX(num) FROM TPJ.All_User;'''
            self.cursor.execute(self.sql)
            self.maxindex = self.cursor.fetchall()
            self.ID_index=self.maxindex[0]['MAX(num)']

            print('END ID_index:',self.ID_index)
            if self.ID_index==None:
                self.ID_index=0
        except:
            print("**ID Index Setting Error**")
        return self.ID_index

    def get_ID(self,num):   #인덱스로 ID리턴
        self.log="Get ID: "+str(num)+' =>\t'
        try:
            self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
            self.sql = '''SELECT id FROM TPJ.All_Review WHERE num='%s';'''%num
            self.cursor.execute(self.sql)
            id=pd.DataFrame(self.cursor.fetchall()).iloc[0]['id']
            self.log+=id
            self.print_log()
            return id
        except:
            self.log+="**Get ID Error**"
            self.print_log()
    
    def registed_ID_check(self,id):  #유저테이블에서 ID중복여부 확인
        try:
            self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
            self.sql = '''SELECT * FROM TPJ.All_User WHERE id='%s';'''%id
            self.cursor.execute(self.sql)
            if self.cursor.fetchall():
                print(id+"님은 이미 등록되었음")
                return True
            else:
                return False

        except:
            print("**ID Check Error**")
    
    def ID_insert(self,id): #유저테이블에 ID업로드
        self.log=str(self.ID_index+1)+'\t'"INSERT User: "+str(id)+'\t\t'
        try:
            if self.registed_ID_check(id):
                raise KeyError
            self.ID_index+=1
            self.sql = '''INSERT INTO `All_User` (num, id) 
            VALUES ('%s','%s');'''%(self.ID_index ,id)
            self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute(self.sql)
            self.review_db.commit()
            self.log+="SUCCESS"
            self.print_log()  
        except pymysql.err.DataError:
            self.log+="**DataError**"
            self.print_log()

        except pymysql.err.IntegrityError:      
            self.log+="IntegrityError"
            self.print_log()
            self.ID_index+=1
            self.ID_insert(id)
        except KeyError:
            self.log+="**DuplicationError**"
            self.print_log()
        except pymysql.err.ProgrammingError:
            self.log+="**ProgrammingError**"
            self.print_log()
#업장----------------------------------------------------------------------------------------------------------------------

    def store_yogiyo_setting(self): #업장 최대요기요 리턴, 지정
            try:
                self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
                self.sql = '''SELECT MAX(yogiyo) FROM TPJ.All_Store;'''
                self.cursor.execute(self.sql)
                self.maxindex = self.cursor.fetchall()
                self.yogiyo=self.maxindex[0]['MAX(yogiyo)']

                print('END_yogiyo:',self.yogiyo)
                if self.yogiyo==None:
                    self.yogiyo=0
            except:
                print("**yogiyo Setting Error**")
            return self.yogiyo

    def registed_store_table_check(self,yogiyo):   #업장_기등록여부 확인
        try:
            self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
            self.sql = '''SELECT * FROM TPJ.All_Store WHERE yogiyo='%s';'''%yogiyo
            self.cursor.execute(self.sql)
            if self.cursor.fetchall():
                print(yogiyo+"은(는) 이미 등록되었음")
                return True
            else:
                self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
                self.sql = '''SELECT * FROM TPJ.All_Store WHERE store_num='%s';'''%yogiyo
                self.cursor.execute(self.sql)
                if self.cursor.fetchall():
                    print(yogiyo+"은(는) 이미 등록되었음")
                    return True
                else:
                    return False
        except:
            print("**Store Check Error**")

    def store_insert(self, yogiyo):    #업장 SQL 넣기
        self.log="yogiyo INSERT: "+str(yogiyo)+'\t\t'
        try:
            #self.Store_index+=1
            self.sql = '''INSERT INTO `All_Store` (yogiyo) 
                VALUES ('%s');'''%(yogiyo)
            self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute(self.sql)
            self.review_db.commit()
            self.log+="SUCCESS"
            self.print_log()
        except pymysql.err.DataError:
            self.log+="**DataError**"
            self.print_log()

        except pymysql.err.IntegrityError:
            self.log+="IntegrityError"
            self.print_log()
            #self.Store_index+=1 인덱스 삭제
            #self.store_insert(yogiyo)
        except KeyError:
            self.log+="**DuplicationError**"
            self.print_log()
        except pymysql.err.ProgrammingError:
            self.log+="**ProgrammingError**"
            self.print_log()
    
    def get_rand_empty_yogiyo(self):  #업장 요기요 렌덤 접근
        try:
            self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
            self.sql = '''SELECT yogiyo FROM TPJ.All_Store WHERE store is null AND store_num is null AND address is null ORDER BY rand() LIMIT 1;'''
            self.cursor.execute(self.sql)
            self.maxindex = self.cursor.fetchall()
            self.yogiyo=self.maxindex[0]['yogiyo']

            print('Empty_random_yogiyo:',self.yogiyo)
            if self.yogiyo==None:
                self.yogiyo=0
        except:
            print("**Random Empty yogiyo Error**")
        return self.yogiyo


    def store_update(self, yogiyo, store, store_num, address):    #업장 SQL 업데이트
        self.log=str(yogiyo)+'\t'+"UPDATE: "+str(store)+' '+str(store_num)+' '+str(address)+'\t\t'
        try:
            #self.Store_index+=1
            self.sql = '''UPDATE TPJ.All_Store SET store = '%s',store_num = '%s',address = '%s' WHERE yogiyo='%s';'''%(store, store_num, address, yogiyo)
            self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute(self.sql)
            self.review_db.commit()
            self.log+="SUCCESS"
            self.print_log()  
        except pymysql.err.DataError:
            self.log+="**DataError**"
            self.print_log()

        except pymysql.err.IntegrityError:      
            self.log+="IntegrityError"
            self.print_log()
            #self.Store_index+=1
            #self.review_insert(yogiyo, store, store_num, address)
        except KeyError:
            self.log+="**DuplicationError**"
            self.print_log()
        except pymysql.err.ProgrammingError:
            self.log+="**ProgrammingError**"
            self.print_log()


    def get_store_num(self,yogiyo):   #요기요로 사업자번호 리턴
        self.log="Get Store num: "+str(yogiyo)+' =>\t'
        try:
            self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
            self.sql = '''SELECT store_num FROM TPJ.All_Store WHERE yogiyo='%s';'''%yogiyo
            self.cursor.execute(self.sql)
            store_num=pd.DataFrame(self.cursor.fetchall()).iloc[0]['store_num']
            self.log+=store_num
            self.print_log()
            return store_num
        except:
            self.log+="**Get yogiyo Error**"
            self.print_log()

    def store_score_updete(self,store,final_score,review):
        self.log=str(store)+'\t'+"UPDATE: "+str(final_score)+'\t\t'
        try:
            #self.Store_index+=1
            self.sql = '''UPDATE TPJ.All_Store SET final_score = '%s',review_many='%s' WHERE store='%s';'''%(final_score,review, store)
            self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute(self.sql)
            self.review_db.commit()
            self.log+="SUCCESS"
            self.print_log()  
        except pymysql.err.DataError:
            self.log+="**DataError**"
            self.print_log()

        except pymysql.err.IntegrityError:      
            self.log+="IntegrityError"
            self.print_log()
            #self.Store_index+=1
            #self.review_insert(yogiyo, store, store_num, address)
        except KeyError:
            self.log+="**DuplicationError**"
            self.print_log()
        except pymysql.err.ProgrammingError:
            self.log+="**ProgrammingError**"
            self.print_log()
    
    
    def get_store_df(self,max,min): #사업장 데이터프레임 리턴
        self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
        self.sql = '''SELECT store FROM TPJ.All_Store where store is not null and %s>=yogiyo and yogiyo>=%s;'''%(max,min)
        self.cursor.execute(self.sql)
        self.maxindex = pd.DataFrame(self.cursor.fetchall())
        print('Store:\n',self.maxindex)
        return self.maxindex
    
    def not_fin_store_df(self): #사업장 데이터프레임 리턴
        self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
        self.sql = '''SELECT store FROM TPJ.All_Store where store is not null AND (final_score=0 OR review_many=0)'''
        self.cursor.execute(self.sql)
        self.maxindex = pd.DataFrame(self.cursor.fetchall())
        print('Store:\n',self.maxindex)
        return self.maxindex

    def GUI_search_store(self,type,search): #GUI업장 검색
        self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
        self.sql = '''SELECT store_num,store,address,final_score,review_many FROM TPJ.All_Store WHERE {0} LIKE '%{1}%';'''.format(type,search)
        self.cursor.execute(self.sql)
        self.result = pd.DataFrame(self.cursor.fetchall())
        print('Store:\n',self.result)
        return self.result
            


#AI_Sampler----------------------------------------------------------------------------------
    def return_deviation(self,review,store):
        div=store.loc[review[0],'final_score']-review[1]
        print('reivew', review[0],review[1],div)

        if review[0]in store.index:
            return abs(div)
        else:
            return NaN
            

    def positive_sampler(self,sort,many):
        self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
        self.sql = '''SELECT num,store,score_flav,score_quan,score_deli,review,reply,std_score*trust_level FROM TPJ.All_Review WHERE std_score*trust_level!=0;'''
        print("Start SQL Runing and Fetching")
        self.cursor.execute(self.sql)
        self.review_df = pd.DataFrame(self.cursor.fetchall())
        print('review',self.review_df)

        self.cursor = self.review_db.cursor(pymysql.cursors.DictCursor)
        self.sql = '''SELECT store,final_score FROM TPJ.All_Store WHERE store is not null and store_num is not null and address is not null and final_score !=0 and review_many >=100;'''
        self.cursor.execute(self.sql)
        self.store_df = pd.DataFrame(self.cursor.fetchall())
        self.store_df.set_index("store",inplace=True)
        print('store',self.store_df)

        print(self.store_df.index)
        
        new_review_df=self.review_df[self.review_df['store'].isin(self.store_df.index)]
        new_store_df=self.store_df[self.store_df.index.isin(self.review_df["store"])]

        print("리뷰필터:",self.review_df[self.review_df['store'].isin(self.store_df.index)])
        print("업장필터",self.store_df[self.store_df.index.isin(self.review_df["store"])])
        print("중복값",new_store_df[new_store_df.index.duplicated()],new_review_df[new_review_df.index.duplicated()])
   
        new_review_df['deviation']=new_review_df[['store','std_score*trust_level']].apply(self.return_deviation,axis =True,args=(new_store_df,))
        #new_review_df.drop(new_review_df.loc[new_review_df['deviation']==None].index,inplace=True)
        print("Return")
        
        new_review_df['deviation'] = pd.to_numeric(new_review_df['deviation'],errors='coerce')
        print(new_review_df)
        print(new_review_df.dtypes)
        return new_review_df.sort_values(by='deviation', ascending=sort, ignore_index=True,na_position='last').head(many)
        #.sort_values(by='deviation', ascending=sort)
        #.head(many)