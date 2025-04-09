# 📌 Proyecto: Generador de Proyectos Laravel con PyQt6

## 🧩 Descripción

Este proyecto es una herramienta gráfica desarrollada en **Python** utilizando **PyQt6** para generar automáticamente proyectos Laravel con **modelos**, **controladores**, **vistas**, **rutas** y otros archivos necesarios.

La aplicación se conecta a una base de datos **PostgreSQL** para obtener la información de las tablas y generar el código correspondiente.

### Funcionalidades principales

- ✅ Crea un proyecto Laravel con las dependencias necesarias.
- ✅ Modifica automáticamente el archivo `.env` para configurar la conexión a la base de datos.
- ✅ Generación de **MVC** y **rutas** basados en las tablas seleccionadas.
- ✅ Soporte para tablas con **llaves foráneas**.
- ✅ Interfaz gráfica para selección de tablas y configuración del proyecto.
- ✅ Generación de archivo `crud.js` para operaciones CRUD dinámicas en las vistas generadas.

---

## 🚀 Características

- 🔐 **Autenticación:** Sistema de login con credenciales predefinidas.
- 🛢️ **Conexión a base de datos:** Verifica la conexión a una base de datos PostgreSQL.
- 🧠 **Inteligencia para relaciones:** Soporte para llaves foráneas, evita duplicación de rutas y campos.

---

## 📋 Requisitos

- Python 3.8 o superior
 - PyQT
 - psycopg2
 - subprocess
 - webbrowser
- PostgreSQL  
- Composer (para instalar Laravel y dependencias)  
- Node.js y npm (para dependencias frontend)  
- Laravel 11.\*

---

## ⚙️ Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu-usuario/tu-repo.git
   cd tu-repo   


## ⚙️ Uso 
### 🔐 Inicia sesión con las credenciales predefinidas:

- **Usuario:** `danner`  
- **Contraseña:** `abelalydel`

---

### 🛠️ Configura la conexión a la base de datos PostgreSQL:

1. Ingresa el **host**, **puerto**, **usuario**, **contraseña** y **nombre de la base de datos**.
2. Haz clic en **"Verificar conexión"** para comprobarla.

---

### 🧱 Crea el proyecto Laravel:

1. Selecciona la **ruta** donde se creará el proyecto.
2. Ingresa el **nombre del proyecto**.
3. Haz clic en **"Crear Proyecto"**.

---

### ⚙️ Genera el código:

1. Haz clic en **"Listar Tablas"** para cargar las tablas de la base de datos.
2. Selecciona las **tablas** que deseas incluir.
3. Haz clic en **"Generar MVC y Rutas"**.
4. Haz clic en **"Launch"** para que se ejecute el proyecto en tu navegador
5. Ingresa la **http://127.0.0.1:8000/nombre_de_la_tabla_que_creaste(el mismo nombre que esta en la base de datos)**, si el nombre es mas de 30 caracteres, escribe solo los primero 30, recuerda 


## 🧩 Funciones principales

### 🔑 Login
- **`on_login`**: Verifica las credenciales del usuario y abre la ventana principal si son correctas.

---

### 🔌 Conexión a la base de datos
- **`verificar_conexion`**: Comprueba la conexión a la base de datos PostgreSQL.

---

### 🏗️ Generación de proyectos
- **`crear_proyecto`**: Crea un proyecto Laravel con las dependencias necesarias y configura automáticamente el archivo `.env`.

---

### 🧱 Generación de MVC y rutas
- **`generar_mvc_rutas`**: Genera modelos, controladores, vistas y rutas para las tablas seleccionadas.
- **`crear_modelos`**: Genera modelos basados en las tablas seleccionadas.
- **`crear_controladores`**: Genera controladores con soporte para llaves foráneas.
- **`generar_vistas`**: Genera vistas con formularios y tablas dinámicas.
- **`crear_rutas`**: Agrega rutas al archivo `web.php`, evitando duplicados.

---

### ⚙️ CRUD dinámico
- **`crear_crudjs`**: Genera el archivo `crud.js` para manejar operaciones CRUD en las vistas generadas.



## 📝 Notas importantes

- 🔗 **Soporte para llaves foráneas:**  
  Si una tabla tiene llaves foráneas, se genera código adicional para manejar correctamente las relaciones entre modelos.

- 🚫 **Evitar duplicados:**  
  Antes de agregar rutas al archivo `web.php`, el sistema verifica si ya existen para evitar duplicaciones innecesarias.

- ⚙️ **Configuración predeterminada:**  
  Algunos valores, como el **host** de la base de datos o el **nombre del proyecto**, tienen valores por defecto para facilitar el proceso de configuración.

---

## 🤝 Contribuciones

¿Quieres mejorar este proyecto?  
¡Eres bienvenido! Puedes:

- Enviar un **Pull Request** con mejoras o correcciones.
- Reportar errores o sugerencias creando un **Issue** en el repositorio.
