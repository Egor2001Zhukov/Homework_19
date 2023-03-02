from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_by_username(self, username):
        return self.session.query(User).filter(User.username == username).one()

    def get_all(self):
        return self.session.query(User).all()

    def get_by_user_id(self, val):
        return self.session.query(User).get(val)

    def create(self, user_d):
        user_ = User(**user_d)
        self.session.add(user_)
        self.session.commit()
        return user_

    def delete(self, uid):
        user_ = self.get_by_user_id(uid)
        self.session.delete(user_)
        self.session.commit()

    def update(self, user_d):
        user_ = self.get_by_user_id(user_d.get("id"))
        user_.username = user_d.get("username")
        user_.password = user_d.get("password")
        user_.role = user_d.get("role")
        self.session.add(user_)
        self.session.commit()
