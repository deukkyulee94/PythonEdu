import uuid

from http import HTTPStatus
from api.todo.model import TodoModel
from flask_jwt_extended import get_jwt_identity

def create_todo(data):

    print(f'[service] :: create_todo - data: {data}')

    new_todo = TodoModel(
        todo_id = str(uuid.uuid4()),
        user_id = get_jwt_identity(),
        todo = data.get('todo'),
        done = False
    )


    save_response = new_todo.save()
    print(f'[service] :: create_todo - save_response: {save_response}')

    return {
        'status': HTTPStatus.OK,
        'message': '할일 생성 완료',
        'data': new_todo.to_dict()
    }

def get_todo_by_id(todo_id):

    print(f'[service] :: get_todo_by_id - todo_id: {todo_id}')

    todo = list(TodoModel.query(todo_id))

    if len(todo) == 1:

        return {
            'status': HTTPStatus.OK,
            'message': '할일 생성 완료',
            'data': todo[0].to_dict()
        }

    elif len(todo) == 0:

        return {
            'status': HTTPStatus.NO_CONTENT,
            'message': '데이터가 없습니다.',
            'data': None
        }

    else:
        return {
            'status': HTTPStatus.INTERNAL_SERVER_ERROR,
            'message': '하나 이상의 데이터가 조회됩니다.',
            'data': None
        }

def get_todo_list():
    todos = []
    filter_condition = None
    filter_condition &= (TodoModel.user_id == get_jwt_identity())
    for todo in TodoModel.scan(filter_condition):
        todos.append(todo.to_simple_dict())

    return {
        'status': HTTPStatus.OK,
        'message': '할일 수정 성공.',
        'data': todos
    }

def update_todo(todo_id, data):
    print(f'[service] :: update_todo - todo_id: {todo_id} | data: {data}')

    result = get_todo_by_id(todo_id)
    print(f'[service] :: update_todo - result: {result}')

    if result.status == HTTPStatus.OK:

        if result.data.get('user_id') != get_jwt_identity():

            return {
                'status': HTTPStatus.UNAUTHORIZED,
                'message': '인증에 실패하였습니다.',
                'data': None
            }

        upd_todo = TodoModel(
            todo_id = todo_id,
            user_id = data.get('user_id'),
            todo = data.get('todo'),
            done = data.get('done'),
        )

        save_response = upd_todo.save()
        print(f'[service] :: update_todo - save_response: {save_response}')

        return {
            'status': HTTPStatus.OK,
            'message': '할일 수정 성공.',
            'data': upd_todo.to_dict()
        }

    else :
        return {
            'status': HTTPStatus.NOT_FOUND,
            'message': '수정 대상을 찾을 수 없습니다.',
            'data': None
        }

def delete_todo(todo_id):
    print(f'[service] :: delete_todo - todo_id: {todo_id}')

    selected_todo = list(TodoModel.query(hash_key=id))
    print(f'[service] :: delete_todo - selected_todo: {selected_todo}')

    if len(selected_todo) == 1:
        if selected_todo[0].user_id != get_jwt_identity():
            return {
                'status': HTTPStatus.UNAUTHORIZED,
                'message': '삭제권한이 없습니다.',
                'data': None
            }

        selected_todo[0].delete()
        return {
            'status': HTTPStatus.OK,
            'message': '할일 삭제 성공',
            'data': None
        }
    else:
        return {
            'status': HTTPStatus.NO_CONTENT,
            'message': '삭제 대상을 찾을 수 없습니다.',
            'data': None
        }

