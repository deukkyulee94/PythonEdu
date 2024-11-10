from flask_restx import Resource

from api.user import user_api, user_register_model, user_update_model, user_delete_model, user_login_model, \
    response_model
from api.user.service import creat_user, login_user, update_user, get_user, delete_user


@user_api.route('/register')
class Register(Resource):
    @user_api.expect(user_register_model)
    @user_api.marshal_with(response_model)
    def post(self):
        return creat_user(user_api.payload)


@user_api.route('/login')
class Login(Resource):
    @user_api.expect(user_login_model)
    @user_api.marshal_with(response_model)
    def post(self):  # 로그인
        return login_user(user_api.payload)


@user_api.route('/<user_id>')
class UserId(Resource):

    @user_api.marshal_with(response_model)
    def get(self, user_id=None):  # 유저 조회
        return get_user(user_id)

    @user_api.expect(user_update_model)
    @user_api.marshal_with(response_model)
    def put(self, user_id=None):  # 유저 수정
        return update_user(user_id, user_api.payload)

    @user_api.expect(user_delete_model)
    @user_api.marshal_with(response_model)
    def delete(self, user_id=None):  # 유저 삭제
        return delete_user(user_id, user_api.payload)
