from pynamodb.attributes import UnicodeAttribute, BooleanAttribute
from pynamodb.models import Model


class TodoModel(Model):
    class Meta:
        table_name = 'todo_model'
        region = "ap-northeast-2"

    todo_id = UnicodeAttribute(hash_key=True)
    user_id = UnicodeAttribute()
    todo = UnicodeAttribute()
    done = BooleanAttribute(default=False)

    def to_dict(self):
        return {
            'todo_id': self.todo_id,
            'user_id': self.user_id,
            'todo': self.todo,
            'done': self.done,
        }


if not TodoModel.exists():
    TodoModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
