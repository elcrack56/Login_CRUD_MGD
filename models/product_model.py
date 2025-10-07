from bson.objectid import ObjectId
from datetime import datetime

class Product:
    """
    Clase para representar un producto (uniforme escolar) en el inventario.
    """
    def __init__(self, id, name, description, size, stock, price, last_updated=None):
        self._id = ObjectId(id) if isinstance(id, str) and ObjectId.is_valid(id) else id
        self.name = name
        self.description = description
        self.size = size 
        self.stock = stock 
        self.price = price
        self.last_updated = last_updated if last_updated else datetime.now().isoformat()

    def to_dict(self):
        """
        Convierte la instancia del producto a un diccionario, útil para guardar en DB o JSON.
        """
        return {
            '_id': str(self._id), 
            'name': self.name,
            'description': self.description,
            'size': self.size,
            'stock': self.stock,
            'price': self.price,
            'last_updated': self.last_updated
        }

    @staticmethod
    def from_mongo_document(doc):
        """
        Crea una instancia de Product a partir de un documento de MongoDB.
        """
        if doc:
            return Product(
                doc['_id'],
                doc['name'],
                doc['description'],
                doc['size'],
                doc['stock'],
                doc['price'],
                doc.get('last_updated')
            )
        return None

    @staticmethod
    def get_all_products(db):
        """
        Obtiene todos los productos de la colección 'products'.
        """
        products_data = db.products.find()
        return [Product.from_mongo_document(p) for p in products_data]

    @staticmethod
    def get_product_by_id(product_id, db):
        """
        Busca un producto por su ID en la base de datos.
        """
        try:
            product_data = db.products.find_one({'_id': ObjectId(product_id)})
            return Product.from_mongo_document(product_data)
        except:
            return None
            
    def save(self, db):
        """
        Guarda o actualiza el producto en la base de datos.
        Si self._id existe, actualiza; de lo contrario, inserta.
        """
        self.last_updated = datetime.now().isoformat() 

        product_data = {
            'name': self.name,
            'description': self.description,
            'size': self.size,
            'stock': self.stock,
            'price': self.price,
            'last_updated': self.last_updated
        }
        if self._id and isinstance(self._id, ObjectId): 
            db.products.update_one({'_id': self._id}, {'$set': product_data})
        else: 
            result = db.products.insert_one(product_data)
            self._id = result.inserted_id 
        return self._id

    @staticmethod
    def delete_product_by_id(product_id, db):
        """
        Elimina un producto por su ID de la base de datos.
        """
        try:
            result = db.products.delete_one({'_id': ObjectId(product_id)})
            return result.deleted_count > 0 
        except:
            return False