from flask_restx import Namespace, fields

user_api = Namespace(
    name='user',
    path='/users',
    description='사용자와 관련된 API 모음입니다.'
)

user_register_model = user_api.model('user_register_model', {
    'user_id': fields.String(required=True, description='아이디', example='deukkyu'),
    'email': fields.String(required=True, description='이메일', example='deukkyu@gsitm.com'),
    'name': fields.String(required=True, description='사용자 이름', example='이득규'),
    'password': fields.String(required=True, description='비밀번호', example='1234')
})

user_update_model = user_api.model('user_update_model', {
    'email': fields.String(required=True, description='이메일', example='deukkyu@gsitm.com'),
    'name': fields.String(required=True, description='사용자 이름', example='이득규'),
    'password': fields.String(required=True, description='비밀번호', example='1234')
})

user_delete_model = user_api.model('user_delete_model', {
    'password': fields.String(required=True, description='비밀번호', example='1234')
})

user_login_model = user_api.model('user_login_model', {
    'user_id': fields.String(required=True, description='아이디', example='deukkyu'),
    'password': fields.String(required=True, description='비밀번호', example='1234')
})

response_model = user_api.model('response_model', {
    'status': fields.Raw(required=True, description='응답 상태'),
    'message': fields.String(required=True, description='응답 메시지'),
    'data': fields.Raw(drequired=True, escription='응답 데이터'),
})
