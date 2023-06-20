

### 친구 관련 API

# 라이브러리 ----------------------------

from flask_restful import Resource
from flask import request
import mysql.connector
from mysql.connector import Error
from mysql_connection import get_connection
from flask_jwt_extended import get_jwt_identity, jwt_required

# --------------------------------------



##### 친구 등록 API ---------------------------------------------------------

class FollowResource(Resource) :

    @jwt_required()
    def post(self, followee_id):  # 친구 맺기

        user_id = get_jwt_identity()

        try :
            
            connection = get_connection()
            query = '''insert into follow
                        (followerId, followeeId)
                        values
                        (%s, %s);'''
            record = ( user_id, followee_id)

            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()


        except Error as e :
            print('오류5', e)
            return { 'result' : 'fail', 'error' : str(e) }, 500
                
        
        return {'result' : 'success'}





##### 친구 삭제 API ---------------------------------------------------------

    @jwt_required()
    def delete(self, followee_id):


        user_id = get_jwt_identity()

        try :
            
            connection = get_connection()
            query = '''delete from follow
                        where followerId = %s and followeeId = %s;'''
            record = ( user_id, followee_id)  
                    # 로그인한 유저아이디/ 팔로이 아이디

            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()

        except Error as e :
            print('오류6', e)
            return { 'result' : 'fail', 'error' : str(e) }, 500
                
        
        return {'result' : 'success'}







