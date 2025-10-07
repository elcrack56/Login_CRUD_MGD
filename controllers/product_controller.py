from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user 
from models.product_model import Product
from bson.objectid import ObjectId
from datetime import datetime

product_bp = Blueprint('product', __name__)

@product_bp.route('/')
@login_required
def list_products():
    from app import db
    """
    Muestra una lista de todos los productos en el inventario.
    """
    products = Product.get_all_products(db)
    return render_template('products/index.html', products=products)

@product_bp.route('/create', methods=['GET', 'POST'])
@login_required 
def create_product():
    from app import db
    """
    Permite crear un nuevo producto.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        size = request.form.get('size')
        stock_str = request.form.get('stock')
        price_str = request.form.get('price')

        if not all([name, description, size, stock_str, price_str]):
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('products/create.html', product=request.form)

        try:
            stock = int(stock_str)
            price = float(price_str)
            if stock < 0 or price < 0:
                flash('Stock y precio no pueden ser números negativos.', 'danger')
                return render_template('products/create.html', product=request.form)
        except ValueError:
            flash('Stock y Precio deben ser números válidos.', 'danger')
            return render_template('products/create.html', product=request.form)


        new_product = Product(None, name, description, size, stock, price, datetime.now().isoformat())
        new_product.save(db)
        flash('Producto creado exitosamente.', 'success')
        return redirect(url_for('product.list_products'))
    
    return render_template('products/create.html')

@product_bp.route('/view/<id>')
@login_required
def view_product(id):
    from app import db
    """
    Muestra los detalles de un producto específico.
    """
    product = Product.get_product_by_id(id, db)
    if product:
        return render_template('products/view.html', product=product)
    
    flash('Producto no encontrado.', 'danger')
    return redirect(url_for('product.list_products'))

@product_bp.route('/edit/<id>', methods=['GET', 'POST'])
@login_required 
def edit_product(id):
    from app import db
    """
    Permite editar un producto existente.
    """
    product = Product.get_product_by_id(id, db)
    if not product:
        flash('Producto no encontrado.', 'danger')
        return redirect(url_for('product.list_products'))

    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.size = request.form.get('size')
        stock_str = request.form.get('stock')
        price_str = request.form.get('price')

        if not all([product.name, product.description, product.size, stock_str, price_str]):
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('products/edit.html', product=product)
        
        try:
            product.stock = int(stock_str)
            product.price = float(price_str)
            if product.stock < 0 or product.price < 0:
                flash('Stock y precio no pueden ser números negativos.', 'danger')
                return render_template('products/edit.html', product=product)
        except ValueError:
            flash('Stock y Precio deben ser números válidos.', 'danger')
            return render_template('products/edit.html', product=product)

        product.save(db)
        flash('Producto actualizado exitosamente.', 'success')
        return redirect(url_for('product.list_products'))
    
    return render_template('products/edit.html', product=product)

@product_bp.route('/delete/<id>', methods=['POST'])
@login_required
def delete_product(id):
    from app import db
    """
    Elimina un producto existente.
    """
    if Product.delete_product_by_id(id, db):
        flash('Producto eliminado exitosamente.', 'success')
    else:
        flash('Error al eliminar el producto o producto no encontrado.', 'danger')
    
    return redirect(url_for('product.list_products'))