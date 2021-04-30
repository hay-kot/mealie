from mealie.core.config import settings
from mealie.db.models.group import Group
from mealie.db.models.model_base import BaseMixins, SqlAlchemyBase
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, orm

# I'm not sure this is necessasry, browser based settings may be sufficient
# class UserSettings(SqlAlchemyBase, BaseMixins):
#     __tablename__ = "user_settings"
#     id = Column(Integer, primary_key=True, index=True)
#     parent_id = Column(String, ForeignKey("users.id"))


class User(SqlAlchemyBase, BaseMixins):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    group_id = Column(Integer, ForeignKey("groups.id"))
    group = orm.relationship("Group", back_populates="users")
    admin = Column(Boolean, default=False)

    def __init__(
        self,
        session,
        full_name,
        email,
        password,
        group: str = settings.DEFAULT_GROUP,
        admin=False,
        id=None,
    ) -> None:

        group = group or settings.DEFAULT_GROUP
        self.full_name = full_name
        self.email = email
        self.group = Group.get_ref(session, group)
        self.admin = admin
        self.password = password

    def update(self, full_name, email, group, admin, session=None, id=None, password=None):
        self.full_name = full_name
        self.email = email
        self.group = Group.get_ref(session, group)
        self.admin = admin

        if password:
            self.password = password

    def update_password(self, password):
        self.password = password
