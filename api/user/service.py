import datetime
from http import HTTPStatus
from api.user.model import UserModel
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from flask import current_app


def util_jwt_create_access_token(identity):
    current_app.config['JWT_SECRET_KEY'] = 'your_default_secret_key'
    expires_delta = datetime.timedelta(seconds=60 * 60 * 24)  # 24 hours
    access_token = create_access_token(identity, expires_delta)
    return access_token


def creat_user(data):
    # 파라미터로 넘어온 값으로 유저 조회
    selected_user = next(iter(UserModel.query(data.get('user_id'))), None)
    print(f'[service] :: create_user - selected_user: {selected_user}')

    # 유저가 None이 아니면 실패 처리
    if selected_user is not None:
        return {
            'status': HTTPStatus.CONFLICT,
            'message': '회원가입 실패, 이미 존재하는 유저입니다.',
            'data': None
        }
    # 조회한 유저가 None이면 회원 생성
    else:
        new_user = UserModel(
            user_id = data.get('user_id'),
            name = data.get('name'),
            email = data.get('email'),
            password = data.get('password'),
        )

        # 유저 저장
        save_response = new_user.save()
        print(f'[service] save_response: {save_response}')

        return {
            'status': HTTPStatus.OK,
            'message': '회원가입 성공.',
            'data': new_user.to_dict()
        }


def login_user(data):  # 로그인 서비스
    print(f'[service] :: login_user - data: {data}')

    selected_user = next(iter(UserModel.query(data.get('user_id'))), None)
    print(f'[service] :: login_user - selected_user: {selected_user}')

    is_valid = selected_user.password == data.get('password')
    print(f'[service] :: login_user - is_valid: {is_valid}')

    if is_valid:
        access_token = util_jwt_create_access_token(identity=selected_user.user_id)

        return {
            'status': HTTPStatus.OK,
            'message': '로그인 성공',
            'data': {'token': access_token}
        }

    else:
        return {
            'status': HTTPStatus.UNAUTHORIZED,
            'message': '로그인 실패',
            'data': None
        }


def get_user(user_id):
    print(f'[service] :: get_user - data: {user_id}')

    user = next(iter(UserModel.query(user_id)), None)
    print(f'[service] :: get_user - user: {user}')

    if user:
        return {
            'status': HTTPStatus.OK,
            'message': '유저 조회 성공.',
            'data': user.to_dict()
        }
    else:
        return {
            'status': HTTPStatus.NOT_FOUND,
            'message': '일치하는 유저가 없습니다.',
            'data': None
        }


def update_user(user_id, data):
    print(f'[service] :: update_user - user_id: {user_id} | data: {data}')

    selected_user = next(iter(UserModel.query(user_id)), None)
    print(f'[service] :: update_user - selected_user: {selected_user}')

    if selected_user:
        selected_user.name = data.get('name')
        selected_user.email = data.get('email')
        selected_user.password = data.get('password')
        save_response = selected_user.save()

        print(f'[service] update_user - save_response: {save_response}')

        return {
            'status': HTTPStatus.OK,
            'message': '유저 정보 수정 성공.',
            'data': selected_user.to_dict()
        }
    else:
        return {
            'status': HTTPStatus.NOT_FOUND,
            'message': '일치하는 유저가 없습니다.',
            'data': None
        }


def delete_user(user_id, data):
    print(f'[service] :: delete_user - user_id: {user_id} | data: {data}')

    selected_user = next(iter(UserModel.query(user_id)), None)
    print(f'[service] :: login_user - selected_user: {selected_user}')

    is_valid = check_password_hash(selected_user.password, data.get('password'))
    print(f'[service] :: login_user - is_valid: {is_valid}')

    if is_valid:
        delete_response = selected_user.delete()
        print(f'[service] :: delete_user - delete_response: {delete_response}')
        return {
            'status': HTTPStatus.OK,
            'message': '유저 삭제 성공',
            'data': None
        }
    else:
        return {
            'status': HTTPStatus.UNAUTHORIZED,
            'message': '유저 삭제 실패, 비밀번호가 일치하지 않습니다.',
            'data': None
        }
