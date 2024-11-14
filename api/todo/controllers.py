from flask_jwt_extended import jwt_required
from flask_restx import Resource

from api.todo import todo_api, todo_register_model, todo_update_model, response_model

from api.todo.service import create_todo, get_todo_by_id, get_todo_list, update_todo, delete_todo


@todo_api.route('/')
class Todo(Resource):

    @jwt_required()
    @todo_api.marshal_with(response_model)
    def get(self):
        return get_todo_list()

    @jwt_required()
    @todo_api.expect(todo_register_model)
    @todo_api.marshal_with(response_model)
    def post(self):
        return create_todo(todo_api.payload)


@todo_api.route('/<todo_id>')
class TodoDetail(Resource):

    @jwt_required()
    @todo_api.marshal_with(response_model)
    def get(self, todo_id=None):
        return get_todo_by_id(todo_id)

    @jwt_required()
    @todo_api.expect(todo_update_model)
    @todo_api.marshal_with(response_model)
    def put(self, todo_id=None):
        return update_todo(todo_id, todo_api.payload)

    @jwt_required()
    @todo_api.marshal_with(response_model)
    def delete(self, todo_id=None):
        return delete_todo(todo_id)
