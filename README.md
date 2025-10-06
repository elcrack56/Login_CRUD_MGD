# Login_Crud_MGD: Sistema de Inventario de Uniformes Escolares con Flask y MongoDB

## 📝 Descripción del Proyecto

Este proyecto implementa un sistema de gestión de inventario para uniformes escolares, construido bajo el patrón arquitectónico **Modelo-Vista-Controlador (MVC)** utilizando el microframework Python **Flask**. Incluye un sistema de autenticación de usuarios (login y registro) robusto y funcionalidades CRUD (Crear, Leer, Actualizar, Eliminar) completas para la administración de productos. La base de datos utilizada es **MongoDB**, y se hace uso de variables de entorno para la gestión segura de configuraciones sensibles.

### Características Principales:

*   **Autenticación de Usuarios (Login/Registro):**
    *   Registro de nuevos usuarios con hashing seguro de contraseñas (`Werkzeug`).
    *   Inicio de sesión para usuarios registrados.
    *   Protección de rutas: las secciones del CRUD son accesibles únicamente para usuarios autenticados.
    *   Cierre de sesión seguro.
    *   Manejo de sesiones con `Flask-Login`.
*   **Gestión de Inventario (CRUD de Productos):**
    *   **Crear:** Añadir nuevos uniformes al inventario.
    *   **Leer:** Visualizar la lista completa de uniformes y el detalle de cada uno.
    *   **Actualizar:** Modificar la información de los uniformes existentes.
    *   **Eliminar:** Eliminar uniformes del inventario.
*   **Arquitectura MVC:** Separación clara de responsabilidades para facilitar el mantenimiento y la escalabilidad.
*   **Base de Datos MongoDB:** Almacenamiento flexible y escalable de datos de usuarios y productos.
*   **Variables de Entorno:** Gestión segura de configuraciones sensibles (claves secretas, URI de base de datos) utilizando el archivo `.env`.
*   **Mensajes Flash:** Notificaciones informativas al usuario para acciones exitosas, errores o advertencias.

## 🚀 Tecnologías Utilizadas

*   **Backend:**
    *   **Python 3.x**
    *   **Flask:** Microframework web.
    *   **Flask-Login:** Gestión de sesiones de usuario.
    *   **Werkzeug:** Utilidades de hashing de contraseñas.
    *   **PyMongo:** Driver oficial de MongoDB para Python.
    *   **python-dotenv:** Carga de variables de entorno desde archivos `.env`.
*   **Base de Datos:**
    *   **MongoDB:** Base de datos NoSQL orientada a documentos.
    *   **MongoDB Compass:** Herramienta gráfica para interactuar con MongoDB.
*   **Frontend:**
    *   **HTML5**
    *   **CSS3**
    *   **Bootstrap 5.3:** Framework CSS para diseño responsivo.
    *   **Jinja2:** Motor de plantillas de Flask.