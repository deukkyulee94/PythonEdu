from flask_restx import Namespace, fields

todo_api = Namespace(
    name='todo',
    path='/todos',
    description='할일과 관련된 API 모음입니다.'
)

todo_register_model = todo_api.model('todo_register_model', {
    'todo': fields.String(required=True, description='할 일 내용', example='강아지 산책'),
})

todo_update_model = todo_api.model('todo_update_model', {
    'todo': fields.String(required=True, description='할 일 내용', example='강아지 산책'),
    'done': fields.Boolean(required=True, description='완료 여부')
})

response_model = todo_api.model('response_model', {
    'status': fields.Raw(required=True, description='응답 상태'),
    'message': fields.String(required=True, description='응답 메시지'),
    'data': fields.Raw(drequired=True, escription='응답 데이터'),
})