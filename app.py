

############ 메모 앱 API 만들기 ############

##### <<  설치한 라이브러리 확인 >> #####
# lamda_app 가상환경
# 파이썬버전 - 3.10

# 설치 라이브러리 : 
# flask , flask-restful, email-validator, 
# psycopg2-binary, passlib, Flask-JWT-Extended
##### --------------------------- #####


# 라이브러리 임포트--------

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from config import Config

from resources.follow import FollowResource
from resources.memo import FollowMemoListResource, MemoListResource, MemoResource
from resources.user import UserLoginResource, UserLogoutResource, UserRegisterResource, jwt_blocklist

# ---------------------------


### 사용 규칙 : 기본 형식 ---------
# app = Flask(__name__)

# if __name__ == '__main__' :
#     app.run
# ----------------------------------



app = Flask(__name__)
print('1.app변수생성')

### 환경변수 세팅 - JWT 적용
app.config.from_object(Config)

### JWT 매니저 초기화
# flask프레임워크(app)를 가지고 jwt매니저 적용해라 
jwt = JWTManager(app)
print('2.jwt매니저 초기화')

### 로그아웃된 토큰으로 요청하는 경우 -->> 이건 는 비정상적인 접근.
### jwt가 알아서 처리하도록 코드 작성.
# 함수 이름 정해져있음
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload) :
    jti = jwt_payload['jti']
    return jti in jwt_blocklist





api = Api(app)

# 경로와 API 동작코드(Resource)를 연결한다.
# resource 폴더 만들기 - memo.py 파일 만들기
	              #   처리함수        ,  '경로'
api.add_resource( MemoListResource , '/memo')
# 		# 경로로 오는 것을 함수로 처리해라
api.add_resource( MemoResource , '/memo/<int:memo_id>') # 메모 수정 삭제 API
#         # memo/<int:recipe_id> 뒤에 숫자 오면 처리해달라
api.add_resource( UserRegisterResource  , '/user/register') # 회원가입 API
        # 회원가입 API
        # 클래스 이름을 이제 지어줘야 함.
        # 클래스이름에는 리소스라고 들어가야 다른사람들이 리소스를 상속받아
        # 쓰는거라고 이해 할 수 있음.
api.add_resource( UserLoginResource  , '/user/login') # 로그인API
api.add_resource( UserLogoutResource  , '/user/logout') # 로그아웃API
api.add_resource(  FollowResource  , '/follow/<int:followee_id>') # 친구API
api.add_resource(  FollowMemoListResource  , '/follow/memo') # 친구메모 API



if __name__ == '__main__' :
    app.run