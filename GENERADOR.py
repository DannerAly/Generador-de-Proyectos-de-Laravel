import sys
import os
import psycopg2
import subprocess
import webbrowser
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFileDialog, QCheckBox, QDialog, QScrollArea, QFormLayout
from funciones.generar_modelos import generar_modelos
from funciones.generar_controladores import generar_controladores
from funciones.generar_vistas import generar_vistas


#redirigir salida a la terminal 

sys.stdout = open('Conout$', 'w')
sys.stderr = open('Conout$', 'w')
# Credenciales únicas
USERNAME = "danner"
PASSWORD = "abelalydel"

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.resize(500, 500)
        layout = QVBoxLayout()

        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText('Usuario')
        layout.addWidget(QLabel('Usuario:'))
        layout.addWidget(self.user_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Contraseña')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel('Contraseña:'))
        layout.addWidget(self.password_input)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.on_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)
        self.setWindowTitle('Login')
        self.show()

    def on_login(self):
        user = self.user_input.text()
        password = self.password_input.text()

        if user == USERNAME and password == PASSWORD:
            self.main_window = conectionBD()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Error', 'Usuario o contraseña incorrectos')


# Menú conexión a base de datos
class conectionBD(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.resize(500, 500)
        layout = QVBoxLayout()

        self.host_input = QLineEdit(self)
        self.host_input.setPlaceholderText('Host')
        self.host_input.setText('localhost')  # Valor predeterminado
        layout.addWidget(QLabel('Host:'))
        layout.addWidget(self.host_input)

        self.port_input = QLineEdit(self)
        self.port_input.setPlaceholderText('Puerto')
        self.port_input.setText('5432')  # Valor predeterminado
        layout.addWidget(QLabel('Puerto:'))
        layout.addWidget(self.port_input)

        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText('Usuario')
        self.user_input.setText('postgres')  # Valor predeterminado
        layout.addWidget(QLabel('Usuario:'))
        layout.addWidget(self.user_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Contraseña')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setText('abelalydel')  # Valor predeterminado
        layout.addWidget(QLabel('Contraseña:'))
        layout.addWidget(self.password_input)

        self.database_input = QLineEdit(self)
        self.database_input.setPlaceholderText('Nombre Base de datos')
        self.database_input.setText('pruebaSHC')  # Valor predeterminado
        layout.addWidget(QLabel('Nombre Base de datos:'))
        layout.addWidget(self.database_input)

        self.submit_button = QPushButton('Verificar conexión', self)
        self.submit_button.clicked.connect(self.verificar_conexion)
        layout.addWidget(self.submit_button)

        self.project_name_label = QLabel('Nombre del proyecto:', self)
        layout.addWidget(self.project_name_label)

        self.project_name_input = QLineEdit(self)
        self.project_name_input.setPlaceholderText('Ingrese el nombre del proyecto')
        self.project_name_input.setText('mylaravelproject')  # Valor predeterminado
        layout.addWidget(self.project_name_input)

        self.select_path_button = QPushButton('Seleccionar ruta', self)
        self.select_path_button.clicked.connect(self.seleccionar_ruta)
        layout.addWidget(self.select_path_button)

        self.path_label = QLabel('Ruta seleccionada:', self)
        layout.addWidget(self.path_label)

        self.path_input = QLineEdit(self)
        self.path_input.setPlaceholderText('Ruta donde se creará el proyecto')
        layout.addWidget(self.path_input)

        self.create_project_button = QPushButton('Crear Proyecto', self)
        self.create_project_button.clicked.connect(self.crear_proyecto)
        layout.addWidget(self.create_project_button)

        self.list_tables_button = QPushButton('Listar Tablas', self)
        self.list_tables_button.clicked.connect(self.listar_tablas)
        layout.addWidget(self.list_tables_button)

        self.launch_button = QPushButton('Launch', self)
        self.launch_button.clicked.connect(self.launch_project)
        layout.addWidget(self.launch_button)

        self.setLayout(layout)
        self.setWindowTitle('Generador de proyectos Laravel')
        self.show()

    def verificar_conexion(self):
        host = self.host_input.text()
        port = self.port_input.text()
        user = self.user_input.text()
        password = self.password_input.text()
        database = self.database_input.text()

        try:
            connection = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            connection.close()
            QMessageBox.information(self, 'Éxito', 'Check connection')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Connection failed: {e}')

    def seleccionar_ruta(self):
        options = QFileDialog.Option.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "Seleccionar ruta", options=options)
        if directory:
            self.path_input.setText(directory)

    def crear_proyecto(self):
        project_name = self.project_name_input.text()
        project_path = self.path_input.text()

        if not project_name:
            QMessageBox.warning(self, 'Error', 'Por favor, ingrese el nombre del proyecto')
            return

        if not project_path:
            QMessageBox.warning(self, 'Error', 'Por favor, seleccione la ruta donde se creará el proyecto')
            return

        try:
            # Usar shell=True para ejecutar el comando en el shell
            result = subprocess.run(["composer", "create-project", "--prefer-dist", "laravel/laravel:11.*", f"{project_path}/{project_name}"], check=True, shell=True)
            # Modificar el archivo .env
            env_path = os.path.join(project_path, project_name, '.env')
            self.modificar_env(env_path)

            # Instalar Yajra DataTables con Composer
            subprocess.run(["composer", "require", "yajra/laravel-datatables-oracle"], cwd=os.path.join(project_path, project_name), check=True, shell=True)
            
            # Publicar los archivos de configuración de DataTables
            subprocess.run(["php", "artisan", "vendor:publish", "--provider=Yajra\\DataTables\\DataTablesServiceProvider"], cwd=os.path.join(project_path, project_name), check=True, shell=True)
            
            # Instalar dependencias con npm
            subprocess.run(["npm", "install", "bootstrap@5.3.0"], cwd=os.path.join(project_path, project_name), check=True, shell=True)
            subprocess.run(["npm", "install", "jquery@3.6.0"], cwd=os.path.join(project_path, project_name), check=True, shell=True)
            subprocess.run(["npm", "install", "datatables.net-bs5", "datatables.net-responsive-bs5"], cwd=os.path.join(project_path, project_name), check=True, shell=True)
            
            # Inicializar npm (si aún no se ha hecho)
            subprocess.run(["npm", "init", "-y"], cwd=os.path.join(project_path, project_name), check=True, shell=True)
            
            # Compilar los archivos CSS y JavaScript
            # subprocess.run(["npm", "run", "dev"], cwd=os.path.join(project_path, project_name), check=True, shell=True)


            QMessageBox.information(self, 'Éxito', f'Proyecto {project_name} creado exitosamente en {project_path}')
        except subprocess.CalledProcessError as e:
            QMessageBox.warning(self, 'Error', f'Error al crear el proyecto: {e}')

    def modificar_env(self, env_path):
        try:
            with open(env_path, 'r') as file:
                env_content = file.read()

            env_content = env_content.replace('DB_CONNECTION=sqlite', 'DB_CONNECTION=pgsql')
            env_content = env_content.replace('# DB_HOST=127.0.0.1', f'DB_HOST={self.host_input.text()}')
            env_content = env_content.replace('# DB_PORT=3306', f'DB_PORT={self.port_input.text()}')
            env_content = env_content.replace('# DB_DATABASE=laravel', f'DB_DATABASE={self.database_input.text()}')
            env_content = env_content.replace('# DB_USERNAME=root', f'DB_USERNAME={self.user_input.text()}')
            env_content = env_content.replace('# DB_PASSWORD=', f'DB_PASSWORD={self.password_input.text()}')
            env_content = env_content.replace('SESSION_DRIVER=file', 'SESSION_DRIVER=database')

            with open(env_path, 'w') as file:
                file.write(env_content)

            QMessageBox.information(self, 'Éxito', 'Archivo .env modificado exitosamente')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error al modificar el archivo .env: {e}')

    def listar_tablas(self):
        try:
            connection = psycopg2.connect(
                host=self.host_input.text(),
                port=self.port_input.text(),
                user=self.user_input.text(),
                password=self.password_input.text(),
                database=self.database_input.text()
            )
            cursor = connection.cursor()
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = cursor.fetchall()
            connection.close()

            self.table_selection_window = TableSelectionWindow(tables, self.path_input.text(), 
                                                               self.project_name_input.text(), 
                                                               self.host_input.text(), 
                                                               self.port_input.text(), 
                                                               self.user_input.text(), 
                                                               self.password_input.text(), 
                                                               self.database_input.text())
            self.table_selection_window.show()
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error al listar las tablas: {e}')

    def launch_project(self):
        project_path = self.path_input.text()
        project_name = self.project_name_input.text()

        if not project_path or not project_name:
            QMessageBox.warning(self, 'Error', 'Por favor, asegúrese de que el proyecto esté creado y la ruta esté seleccionada')
            return

        try:
            # Iniciar el servidor de Laravel
            subprocess.Popen(["php", "artisan", "serve"], cwd=os.path.join(project_path, project_name), shell=True)
            # Abrir el navegador en la ruta del proyecto
            webbrowser.open("http://127.0.0.1:8000")
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error al iniciar el proyecto: {e}')


class TableSelectionWindow(QDialog):
    def __init__(self, tables, project_path, project_name, host, port, user, password, database):
        super().__init__()

        self.foreign_key_tables = set()  # Inicializar correctamente como un conjunto vacío 
        self.project_path = project_path
        self.project_name = project_name
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.selected_tables = []
        self.tables = tables  # Guardamos todas las tablas para el filtro
        self.fk_column_mapping = {}  # Diccionario para guardar las selecciones de columnas alternativas

        self.setWindowTitle('Seleccionar Tablas')
        self.resize(500, 500)

        layout = QVBoxLayout()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Buscar tabla...")
        self.search_box.textChanged.connect(self.filtrar_tablas)
        layout.addWidget(self.search_box)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        self.checkboxes = []
        self.actualizar_checkboxes(tables)

        scroll_area.setWidget(self.scroll_content)
        layout.addWidget(scroll_area)

        # Para seleccionar todos los checkboxes
        self.select_all_button = QPushButton('Seleccionar Todos', self)
        self.select_all_button.clicked.connect(self.seleccionar_todos)
        layout.addWidget(self.select_all_button)

        self.generate_button = QPushButton('Generar MVC y Rutas', self)
        self.generate_button.clicked.connect(self.generar_mvc_rutas)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)


    def marcar_relaciones(self, table):
        """Marcar automáticamente los checkboxes de las tablas referenciadas como llaves foráneas."""
        if hasattr(self, 'foreign_key_tables') and self.foreign_key_tables:
            for checkbox in self.checkboxes:
                # Verificar si el texto del checkbox coincide con una tabla referenciada
                if checkbox.text() in self.foreign_key_tables:
                    #print(f"Marcando automáticamente la tabla: {checkbox.text()}")
                    checkbox.setChecked(True)


    def actualizar_checkboxes(self, tables):
        """Actualiza los checkboxes según la lista de tablas."""
        # Limpiar los widgets existentes en el diseño
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        self.checkboxes = []

        # Crear un checkbox para cada tabla
        for table in tables:
            checkbox = QCheckBox(table[0])
            
            # Conectar el evento stateChanged para ejecutar verificar_llaves_foraneas y marcar_relaciones
            checkbox.stateChanged.connect(lambda state, table=table[0]: self.on_checkbox_state_changed(table, state))
            
            self.checkboxes.append(checkbox)
            self.scroll_layout.addWidget(checkbox)

    def on_checkbox_state_changed(self, table, state):
        """Maneja el evento stateChanged de un checkbox."""
        # Ejecutar verificar_llaves_foraneas
        self.verificar_llaves_foraneas(table, state)
        # Ejecutar marcar_relaciones
        self.marcar_relaciones(table)



    def verificar_llaves_foraneas(self, table, state):
        """Verifica las llaves foráneas de una tabla y muestra una ventana si no tienen 'nombre'."""
        if state == 2:  # Checkbox seleccionado
            try:
                connection = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
                cursor = connection.cursor()

                # Obtener las llaves foráneas de la tabla
                cursor.execute(f"""
                    SELECT
                        kcu.column_name AS fk_column,  -- Nombre de la columna que es llave foránea
                        ccu.table_name AS referenced_table,  -- Nombre de la tabla referenciada
                        ccu.column_name AS referenced_column  -- Nombre de la columna referenciada
                    FROM
                        information_schema.key_column_usage kcu
                    JOIN
                        information_schema.constraint_column_usage ccu
                        ON kcu.constraint_name = ccu.constraint_name
                    WHERE
                        kcu.table_name = '{table}'
                    ORDER BY
                        kcu.ordinal_position  -- Asegura un orden consistente si está disponible
                    OFFSET 1;
                """)
                foreign_keys = cursor.fetchall()

                 # Guardar las tablas referenciadas como llaves foráneas
                self.foreign_key_tables.update({fk[1] for fk in foreign_keys})  # Actualizar el conjunto con las tablas referenciadas
                print("Tablas referenciadas como llaves foráneas:", self.foreign_key_tables)

                for fk_column, referenced_table, referenced_column in foreign_keys:
                    # Verificar si la tabla relacionada tiene el atributo 'nombre'
                    cursor.execute(f"""
                        SELECT column_name
                        FROM information_schema.columns
                        WHERE table_name = '{referenced_table}' AND column_name = 'nombre';
                    """)
                    has_nombre = cursor.fetchone()

                    if not has_nombre:
                        # Si no tiene 'nombre', abrir una ventana para seleccionar un atributo
                        self.mostrar_ventana_seleccion(referenced_table, fk_column)

                connection.close()
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Error al verificar las llaves foráneas: {e}')


    
    def mostrar_ventana_seleccion(self, referenced_table, fk_column):
        """Muestra una ventana para seleccionar un atributo de la tabla relacionada."""
        try:
            connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            cursor = connection.cursor()

            # Obtener todas las columnas de la tabla relacionada
            cursor.execute(f"""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = '{referenced_table}';
            """)
            columns = cursor.fetchall()
            connection.close()

            # Crear una nueva ventana para seleccionar el atributo
            selection_window = QDialog(self)
            selection_window.setWindowTitle(f"Seleccionar atributo para {referenced_table} (FK: {fk_column})")
            selection_window.resize(400, 300)

            layout = QVBoxLayout()

            label = QLabel(f"Seleccione un atributo de la tabla '{referenced_table}':")
            layout.addWidget(label)

            for column in columns:
                column_button = QPushButton(column[0], selection_window)
                column_button.clicked.connect(lambda _, col=column[0]: self.guardar_seleccion(fk_column, col, selection_window))
                # Conecta el evento `clicked` del botón a la función `guardar_seleccion`.
                # Cuando el botón es presionado, se llama a `guardar_seleccion` con los parámetros:
                # - `fk_column`: La llave foránea actual.
                # - `col`: El nombre de la columna seleccionada.
                # - `selection_window`: La ventana de selección, que se cerrará después de guardar la selección.
                layout.addWidget(column_button)

            selection_window.setLayout(layout)
            selection_window.exec()

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error al mostrar la ventana de selección: {e}')


    def guardar_seleccion(self, fk_column, column, window):
        """Guarda la columna seleccionada como alternativa para una llave foránea."""
        self.fk_column_mapping[fk_column] = column
        QMessageBox.information(self, 'Éxito', f'Seleccionado "{column}" para la llave foránea "{fk_column}"')
        print(f"Selección xxguardada: {fk_column} -> {column}")
        window.accept()

    def seleccionar_todos(self):
        """Marca todos los checkboxes."""
        for checkbox in self.checkboxes:
            checkbox.setChecked(True)

    def filtrar_tablas(self):
        """Filtra las tablas según el texto del buscador y organiza las coincidencias arriba."""
        filtro = self.search_box.text().lower()

        # Dividir las tablas en dos listas: con coincidencias y sin coincidencias
        tablas_con_coincidencia = [table for table in self.tables if filtro in table[0].lower()]
        tablas_sin_coincidencia = [table for table in self.tables if filtro not in table[0].lower()]

        # Combinar las listas: primero las coincidencias, luego las que no coinciden
        tablas_ordenadas = tablas_con_coincidencia + tablas_sin_coincidencia

        # Actualizar los checkboxes con las tablas ordenadas
        self.actualizar_checkboxes(tablas_ordenadas)

    def seleccionar_todos(self):
        """Marca todos los checkboxes."""
        for checkbox in self.checkboxes:
            checkbox.setChecked(True)

            
    def crear_crudjs(self):
        try:
            # Crear carpetas dentro de public/assets/js/custom
            custom_js_path = os.path.join(self.project_path, self.project_name, "public", "assets", "js","custom")
            os.makedirs(custom_js_path, exist_ok=True)

            # Crear el archivo crud.js con el contenido proporcionado
            crud_js_content = """



    $(function () {
    $.ajaxSetup({
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        }
    });

    var table = $('.data-table').DataTable({
        processing: true,
        serverSide: true,
        ajax: window.URLindex,
        columns: window.columnas,
    });

    $('#createNewRecord').click(function () {
        $('#table_id').val('');
        $('#form').trigger("reset");
        $('#ajaxModel').modal('show');
    });

    $('body').on('click', '.editRecord', function () {
        var table_id = $(this).data('id');
        $.get(window.URLindex + '/' + table_id + '/edit', function (data) {
            $('#ajaxModel').modal('show');
            $('#table_id').val(data.id);
            $('#nombre').val(data.nombre);
            $('#nombre_abreviado').val(data.nombre_abreviado);
            $('#inicial').val(data.inicial);
            $('#estado').val(data.estado);
        })
    });

    $('#form').on('submit', function (event) {
        event.preventDefault();
        $.ajax({
            data: $(this).serialize(),
            url: window.URLindex,
            type: "POST",
            dataType: 'json',
            success: function (data) {
                $('#form').trigger("reset");
                $('#ajaxModel').modal('hide');
                table.draw();
            },
            error: function (data) {
                console.log('Error:', data);
            }
        });
    });

    $('body').on('click', '.deleteRecord', function () {
        var table_id = $(this).data("id");
        if (confirm("Are you sure want to delete?")) {
            $.ajax({
                type: "DELETE",
                url: window.URLindex + '/' + table_id,
                success: function (data) {
                    table.draw();
                },
                error: function (data) {
                    console.log('Error:', data);
                }
            });
        }
    });
});
    
    
    
    
    """

            with open(os.path.join(custom_js_path, "crud.js"), 'w') as file:
                file.write(crud_js_content)

            QMessageBox.information(self, 'Éxito', 'Archivo crud.js creado exitosamente')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error al crear el archivo crud.js: {e}')

    def crear_template(self):
        try:
            # Crear carpeta dentro de resources/views/template
            template_path = os.path.join(self.project_path, self.project_name, "resources", "views", "template")
            os.makedirs(template_path, exist_ok=True)

            # Crear el archivo layout.blade.php con el contenido proporcionado
            layout_content = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>@yield('title', 'Laravel')</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        @yield('css')
    </head>
    <body>
        <div class="container">
            <header class="my-4">
                @yield('cabeza_contenido')
            </header>
            <main>
                @yield('contenido')
            </main>
        </div>

        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
        @yield('js')
    </body>
    </html>"""

            with open(os.path.join(template_path, "layout.blade.php"), 'w') as file:
                file.write(layout_content)

            QMessageBox.information(self, 'Éxito', 'Archivo layout.blade.php creado exitosamente')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error al crear el archivo layout.blade.php: {e}')


    def crear_modelos(self):
        try:
            generar_modelos(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                selected_tables=self.selected_tables,
                project_path=self.project_path,
                project_name=self.project_name
            )
            QMessageBox.information(self, 'Éxito', 'Modelos creados exitosamente')
        except Exception as e:
            # Mensaje de depuración para capturar cualquier excepción
            print(f"Error al crear los modelos: {e}")
            QMessageBox.warning(self, 'Error', f'Error al crear los modelos: {e}')

    
    def crear_controladores(self):
        try:
            generar_controladores(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                project_path=self.project_path,
                project_name=self.project_name,
                selected_tables=self.selected_tables,
                fk_column_mapping=self.fk_column_mapping
            )
            QMessageBox.information(self, 'Éxito', 'Controladores creados exitosamente')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error al crear los controladores: {e}')

    
    def generar_vistas(self):
        try:
            generar_vistas(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                project_path=self.project_path,
                project_name=self.project_name,
                selected_tables=self.selected_tables,
                fk_column_mapping=self.fk_column_mapping
            )
            QMessageBox.information(self, 'Éxito', 'Vistas creadas exitosamente')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error al crear las vistas: {e}')

    def crear_rutas(self):
        def singularize(name):
            #    if name.endswith('es'):
            #        return name[:-2]
            #    elif name.endswith('s'):
            #        return name[:-1]
            return name

        try:
            routes_path = os.path.join(self.project_path, self.project_name, "routes", "web.php")

            # Mensaje de depuración para verificar la ruta del archivo web.php
            print(f"Agregando rutas en: {routes_path}")

            # Leer el contenido actual del archivo web.php
            if os.path.exists(routes_path):
                with open(routes_path, 'r') as file:
                    existing_routes = file.read()
            else:
                existing_routes = ""

            with open(routes_path, 'a') as file:
                for table in self.selected_tables:
                    singular_table = singularize(table)
                    controller_name = f"{singular_table.capitalize()}Controller"
                    route_content = f"\nuse App\Http\Controllers\\{controller_name};\n"

                    # Si el nombre de la tabla tiene más de 30 caracteres, recortarlo a 30
                    if len(table) > 30:
                        tablerecort = table[:30]
                        # Generar el contenido de namesmetod dinámicamente
                        namesmetod = f"""->names([
                            'index' => '{table}.index',
                            'create' => '{table}.create',
                            'store' => '{table}.store',
                            'show' => '{table}.show',
                            'edit' => '{table}.edit',
                            'update' => '{table}.update',
                            'destroy' => '{table}.destroy',
                        ])"""
                        route_content += f"Route::resource('{tablerecort}', {controller_name}::class) {namesmetod};"
                    else:
                        tablerecort = table
                        route_content += f"Route::resource('{tablerecort}', {controller_name}::class);"

                    # Verificar si la ruta ya existe en el archivo
                    if route_content.strip() in existing_routes:
                        print(f"La ruta para {table} ya existe. No se agregará nuevamente.")
                        continue

                    # Mensaje de depuración para verificar el contenido que se va a agregar
                    print(f"Agregando ruta para {table}: {route_content}")

                    file.write(route_content)

            QMessageBox.information(self, 'Éxito', 'Rutas agregadas exitosamente')
        except Exception as e:
            # Mensaje de depuración para capturar cualquier excepción
            print(f"Error al agregar las rutas: {e}")
            QMessageBox.warning(self, 'Error', f'Error al agregar las rutas: {e}')

            
    def generar_mvc_rutas(self):
        selected_tables = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]

        if not selected_tables:
            QMessageBox.warning(self, 'Error', 'Por favor, seleccione al menos una tabla')
            return

        self.selected_tables = selected_tables

        # Mensaje de depuración para verificar las tablas seleccionadas
        print(f"Tablas seleccionadas para generar MVC y Rutas: {self.selected_tables}")

        try:
            self.crear_crudjs()
            self.crear_template()
            self.crear_modelos()
            self.crear_controladores()
            self.generar_vistas()
            self.crear_rutas()

            QMessageBox.information(self, 'Éxito', 'MVC y Rutas generados exitosamente')
        except subprocess.CalledProcessError as e:
            QMessageBox.warning(self, 'Error', f'Error al generar MVC y Rutas: {e}')
    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    sys.exit(app.exec())