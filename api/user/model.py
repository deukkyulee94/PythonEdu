from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model
from werkzeug.security import check_password_hash


# User 모델 정의
class UserModel(Model):
    class Meta:
        table_name = 'user_model'
        region = "ap-northeast-2"

    user_id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    email = UnicodeAttribute()
    password = UnicodeAttribute()

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
        }

    def check_password(self, password):
        return check_password_hash(self.password, password)


if not UserModel.exists():
    UserModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
