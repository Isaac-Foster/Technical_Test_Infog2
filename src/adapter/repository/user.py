from src.infra.models.user import UserModel

from src.adapter.repository.public import BaseRepo
from src.interfaces.schema.auth import UserRegisterSchema, UserPublicSchema


class UserRepo(BaseRepo):
    def __init__(self):
        super().__init__()
        self.model = UserModel
        self.public = UserPublicSchema

    def create(self, data: UserRegisterSchema):
        already = self.find_all(email=data.email, document=data.document)

        if already.get('results'):
            return Exception('User already exists')

        model = self.model(**data.dict())

        with self.session() as session:
            session.add(model)
            session.commit()
            session.refresh(model)
        return self.public(**model.__dict__)

    def update(self, data: UserRegisterSchema):
        model = self.find(id=data.id)
        for key, value in data.dict().items():
            setattr(model, key, value)
