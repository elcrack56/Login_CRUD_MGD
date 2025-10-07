from flask_login import UserMixin
from bson.objectid import ObjectId

class User(UserMixin):
    """
    Clase para representar a un usuario, compatible con Flask-Login.
    """
    def __init__(self, id, username, password):
        self._id = ObjectId(id) if isinstance(id, str) and ObjectId.is_valid(id) else id
        self.username = username
        self.password = password

    def get_id(self):
        """
        Retorna el ID del usuario como una cadena (requerido por Flask-Login).
        """
        return str(self._id)

    @staticmethod
    def get_by_username(username, db):
        """
        Busca un usuario por su nombre de usuario en la base de datos.
        """
        user_data = db.users.find_one({'username': username})
        if user_data:
            return User(user_data['_id'], user_data['username'], user_data['password'])
        return None

    @staticmethod
    def get_by_id(user_id, db):
        """
        Busca un usuario por su ID en la base de datos.
        """
        try:
            user_data = db.users.find_one({'_id': ObjectId(user_id)})
            if user_data:
                return User(user_data['_id'], user_data['username'], user_data['password'])
            return None
        except:
            return None