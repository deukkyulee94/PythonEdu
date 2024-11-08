from flask_restx import Resource

from api.user import user_api, user_register_model, response_model
from api.user.service import creat_user


@user_api.route('/register')
class Register(Resource):
    """회원가입 API"""

    @user_api.expect(user_register_model)
    @user_api.marshal_with(response_model)
    def post(self):
        data = user_api.payload

        result = creat_user(data)
        return result
