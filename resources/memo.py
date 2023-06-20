

### memo 관련 API


# 라이브러리 ----------------------------

from flask_restful import Resource
from flask import request
import mysql.connector
from mysql.connector import Error
from mysql_connection import get_connection
from flask_jwt_extended import get_jwt_identity, jwt_required

# --------------------------------------




##### 내 메모 등록 API ------------------------------------------------

class MemoListResource(Resource) :
    
    @jwt_required()
    def post(self):

        # 데이터 가져오기
        data = request.get_json()
        user_id = get_jwt_identity()

        #
        try :
            connection = get_connection()
            # insert into memo
            # (title, date, content, userId)
            # values
            # ('점심', '2023-07-07 13:00', '맛있는 점심', 3);
            query = '''insert into memo
                        (title, date, content, userId)
                        values
                        (%s, %s, %s, %s);'''
            record = ( data['title'], 
                      data['date'],
                      data['content'],
                      user_id)
            
            # 쿼리 실행
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()

            cursor.close()
            connection.close()


        except Error as e:
            print('오류1', e)
            return {'result':'fail', 'error':str(e) }, 500


        return { 'result': 'success'}
    




##### 내 메모 가져오기 API ------------------------------------------------

    @jwt_required()
    def get(self) :

        # 1. 데이터가져와
        user_id = get_jwt_identity()

        try :
            connection = get_connection()
            # select *
            # from memo
            # where userId = 2
            # order by date desc;
            # 정렬 : 날짜 내림차순
            query = '''select *
                        from memo
                        where userId = %s
                        order by date desc;'''
            record = (user_id, )

            # 2. 쿼리 실행
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, record)
            # connection.commit() - 가져오는거라 이거 실행하면 안됨, 이건 바꾸는거

            result_list = cursor.fetchall()

            cursor.close()
            connection.close()


        except Error as e :
            print('오류2', e)
            return {'result':'fail', 'error':str(e) }, 500
        
        print('result_list', result_list)

        # 데이터 가공하기 date컬럼, createdAt컬럼, updatedAt 컬럼
        i = 0
        for row in result_list :
            # print(row) # 서버 내렸다가 다시 돌리고 포스트맨에서 send눌러봄 -> row는 딕셔너리
            result_list[i]['createdAt'] = row['createdAt'].isoformat()
            result_list[i]['updatedAt'] = row['updatedAt'].isoformat()
            result_list[i]['date'] = row['date'].isoformat()
            i = i + 1


        return { 'result': 'success', 
                'count':len(result_list),
                'items': result_list}








##### 내 메모 수정 및 삭제 API ------------------------------------------------

class MemoResource(Resource):

    @jwt_required()
    def put(self, memo_id):       # 메모 수정
        
        # 데이터 받아오기
        data = request.get_json()
        userId = get_jwt_identity()

        try :

            connection = get_connection()
            # update memo
            # set title = '', date = '', content = ''
            # where userId = 3;
            query = '''update memo
                        set title = %s, date = %s, content = %s
                        where id = %s and userId = %s;'''
            record = (data['title'], 
                      data['date'], 
                      data['content'],
                      memo_id,  
                      userId)
            
            cursor = connection.cursor()
            cursor.execute(query, record)

            connection.commit()

            cursor.close()
            connection.close()
            

        except Error as e :
            print('오류3', e)
            return { 'result' : 'fail', 'error' : str(e) }, 500
                
        
        return {'result' : 'success'}










    @jwt_required()
    def delete(self, memo_id):      # 메모 삭제
        
        user_id = get_jwt_identity()

        try :
            connection = get_connection()

            query = '''delete from memo
                        where id = %s and userId = %s;'''
            record = ( memo_id, user_id)
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()

        except Error as e :
            print('오류4', e)
            return { 'result' : 'fail', 'error' : str(e) }, 500
                
        
        return {'result' : 'success'}








##### 친구들 메모 가져오기 API ------------------------------------------------

class FollowMemoListResource(Resource):   

    @jwt_required()
    def get(self): 

        ### 1. 클라이언트로부터 데이터를 받아온다.
        # 어떻게 받아올까?
        # 바디에 있는거 보통 - request.get_.. 로 받아옴
        # 이 경우 바디에 데이터가 없음

        ### query params 는 딕셔너리로 받아오고,
        ### 없는 키값을 엑세스 해도 에러가 발생하지 않도록
        ### 딕셔너리의 get함수를 사용해서 데이터를 받아온다.

        # request.args

        offset = request.args.get('offset')
        limit = request.args.get('limit')

        user_id = get_jwt_identity()

        # print('request.args', request.args)
        # print('request.args', request.args.get('offset'))
        # print('request.args', request.args['offset'])

        try :

            connection = get_connection()
            query = '''select m.*, u.nickname
                        from follow f
                        join memo m
                            on f.followeeId = m.userId
                        join user u
                            on m.userId = u.id
                        where f.followerId = %s
                        order by date desc
                        limit '''+ offset +''', '''+ limit + ''';'''
                        # 파라미터는 %s로 바꿀 수 없음
                        # %s는 컬럼에서 가져올 수 있는 정보만 가능. 

            record = (user_id, )  # %s 에 해당하는것만 써줘야함.

            cursor = connection.cursor(dictionary = True)
            cursor.execute(query, record)

            result_list = cursor.fetchall()
            print('result_list', result_list)

            cursor.close()
            connection.close()




        except Error as e :
            print('오류4', e)
            return { 'result' : 'fail', 'error' : str(e) }, 500
        

        # 데이터 가공
        i = 0
        for row in result_list :
            # print(row) # 서버 내렸다가 다시 돌리고 포스트맨에서 send눌러봄 -> row는 딕셔너리
            result_list[i]['createdAt'] = row['createdAt'].isoformat()
            result_list[i]['updatedAt'] = row['updatedAt'].isoformat()
            result_list[i]['date'] = row['date'].isoformat()
            i = i + 1
                
        
        return {'result' : 'success',
                'count' : len(result_list), 
                'items' : result_list}
    








