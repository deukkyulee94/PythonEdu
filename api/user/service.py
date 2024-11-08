import logging
from http import HTTPStatus
from api.user.model import UserModel


def creat_user(data):
    in_user_id = data.get('user_id')

    filter_condition = None
    filter_condition &= (UserModel.user_id == in_user_id)

    scan_user = UserModel.scan(filter_condition)
    print(f'[service] len(list(scan_user)): ${len(list(scan_user))}')

    if len(list(scan_user)) > 0:
        return {
            'status': HTTPStatus.CONFLICT,
            'message': '회원가입 실패, 이미 존재하는 유저입니다.',
            'data': ''
        }
    else:
        new_user = UserModel(
            user_id=data.get('user_id'),
            name=data.get('name'),
            email=data.get('email'),
            password=data.get('password'),
        )
        save_response = new_user.save()
        logging.debug(save_response)
        print(f'[service] save_response: ${save_response}')
        return {
            'status': HTTPStatus.OK,
            'message': '회원가입 성공.',
            'data': new_user.to_dict()
        }


def login_user(data):
    in_user_id = data.get('userid')
    in_password = data.get('password')

    filter_condition = None
    filter_condition &= (UserModel.user_id == in_user_id)
    filter_condition &= (UserModel.password == in_password)
    user = UserModel.scan(filter_condition)

    if len(list(user)) == 1:
        access_token = 'jwt token'
        return {'message': '로그인 성공', 'jwt': access_token}, HTTPStatus.OK
    else:
        return {'message': '로그인 실패'}, HTTPStatus.UNAUTHORIZED
