import os
import psycopg2

def singularize_spanish(name):
   # if name.endswith('es'):
  #      if name.endswith('ces'):
  #          return name[:-3] + 'z'
  #      return name[:-2]
  ##  elif name.endswith('s'):
  #      return name[:-1]
    return name

def get_related_column(fk_column, fk_column_mapping): #-------------------------------------
    """
    Obtiene el nombre de la columna relacionada basado en el diccionario fk_column_mapping.
    Si no se encuentra en el diccionario, devuelve 'nombre' como valor predeterminado.
    """
    return fk_column_mapping.get(fk_column, 'nombre')

def crear_vista(host, port, user, password, database, table, project_path, project_name, foreign_keys, fk_column_mapping):
    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = connection.cursor()

        # Obtener los nombres de las columnas de la tabla y sus tipos
        cursor.execute(f"""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = '{table}';
        """)
        columns = cursor.fetchall()
        column_names = [column[0] for column in columns]

        # Obtener la información de las llaves foráneas
        foreign_key_methods = ""
        fk_class_names = []
        fk_display_columns = {}
        for fk_column, fk_table, fk_referenced_column in foreign_keys:
            fk_class_name = singularize_spanish(fk_table).capitalize()
            fk_class_names.append(fk_class_name)

            # Obtener el nombre de la columna relacionada dinámicamente
            related_column = get_related_column(fk_column, fk_column_mapping)

            foreign_key_methods += f"""
                        <div class="row">
                            <div class="col-12">
                                <label for="{fk_column}" class="form-label">{fk_class_name} <span class="text-danger">*</span></label>
                                <select class="form-select mb-3" name="{fk_column}" id="{fk_column}" required>
                                    @foreach(${fk_class_name.lower()} as ${fk_class_name.lower()})
                                        <option value="{{{{ ${fk_class_name.lower()}->{fk_referenced_column} }}}}">{{{{ ${fk_class_name.lower()}->{related_column} }}}}</option>
                                    @endforeach
                                </select>
                            </div>
                        </div>"""

            # Obtener el primer atributo que no tenga "id" en su nombre para mostrar en la tabla
            cursor.execute(f"""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = '{fk_table}' AND column_name NOT LIKE 'id%' AND column_name != '{fk_referenced_column}'
                LIMIT 1;
            """)
            display_column = cursor.fetchone()
            if display_column:
                fk_display_columns[fk_column] = fk_table #guarda el nombre de la tabla

        # Generar los campos del formulario dinámicamente


                # Generar los campos del formulario dinámicamente
        form_fields = ""  # Variable para almacenar los campos del formulario HTML
        table_headers = ""  # Variable para almacenar los encabezados de la tabla HTML
        table_columns = ""  # Variable para almacenar las columnas de la tabla para DataTables

        is_first_column = True  # Variable para verificar si es la primera columna

        # Iterar sobre las columnas de la tabla y sus tipos
        for col, col_type in columns:
            # Si la columna no es la llave primaria de la tabla
            #------------------------------------------------------
            # Si la columna es la primera, no concatenar nada a form_fields
            if is_first_column:
                is_first_column = False  # Marcar que ya se procesó la primera columna
                continue  # Saltar esta iteración del bucle

            if col != f"id_{singularize_spanish(table)}":
                
                # Si la columna es "estado", generar un campo de selección (dropdown)
                if col == "estado":
                    form_fields += f"""
                        <div class="row">
                            <div class="col-12">
                                <label for="{col}" class="form-label">{col.capitalize().replace('_', ' ')} <span class="text-danger">*</span></label>
                                <select class="form-select mb-3" name="{col}" id="{col}">
                                    <option value="S">Activado</option>
                                    <option value="N">Desactivado</option>
                                </select>
                            </div>
                        </div>"""
                    table_headers += f"<th>{col.capitalize().replace('_', ' ')}</th>\n"
                    table_columns += f"{{data: '{col}', name: '{col}'}},\n"  # Columna para DataTables
                # Si la columna es una llave foránea, agregar encabezados y columnas para DataTables
                
                elif col in fk_display_columns:
                    # Obtener el nombre de la relación y el atributo relacionado
                    related_table = fk_display_columns[col]  # Esto debería ser algo como 'roles' o 'menus_principales'
                    related_column = 'nombre'  # Por defecto, usamos 'nombre' como atributo relacionado

                    # Generar encabezado de la tabla
                    table_headers += f"<th>{related_table.capitalize().replace('_', ' ')} {related_column.capitalize()}</th>\n"

                    # Generar columna para DataTables
                    table_columns += f"{{data: '{related_table}_{related_column}', name: '{related_table}_{related_column}'}},\n"
                                
                # Si la columna es de tipo fecha o tiempo, generar un campo de entrada de tipo "date"
                elif "date" in col_type:
                    form_fields += f"""
                        <div class="row">
                            <div class="col-12">
                                <label for="{col}" class="form-label">{col.capitalize().replace('_', ' ')} <span class="text-danger">*</span></label>
                                <input type="date" class="form-control" name="{col}" id="{col}" required>
                            </div>
                        </div>"""
                # Si la columna es de tipo entero, generar un campo de entrada de tipo "number"
                    table_headers += f"<th>{col.capitalize().replace('_', ' ')}</th>\n"
                    table_columns += f"{{data: '{col}', name: '{col}'}},\n"  # Columna para DataTables

                elif "datetime-local" in col_type or "time" in col_type:
                    form_fields += f"""
                        <div class="row">
                            <div class="col-12">
                                <label for="{col}" class="form-label">{col.capitalize().replace('_', ' ')} <span class="text-danger">*</span></label>
                                <input type="datetime-local" class="form-control" name="{col}" id="{col}" required>
                            </div>
                        </div>"""
                # Si la columna es de tipo entero, generar un campo de entrada de tipo "number"
                    table_headers += f"<th>{col.capitalize().replace('_', ' ')}</th>\n"
                    table_columns += f"{{data: '{col}', name: '{col}'}},\n"  # Columna para DataTables


                elif "int" in col_type:
                    form_fields += f"""
                        <div class="row">
                            <div class="col-12">
                                <label for="{col}" class="form-label">{col.capitalize().replace('_', ' ')} <span class="text-danger">*</span></label>
                                <input type="number" class="form-control" name="{col}" id="{col}" placeholder="Introduzca {col}" required>
                            </div>
                        </div>"""
                # Para cualquier otro tipo de columna, generar un campo de entrada de tipo "text"
                    table_headers += f"<th>{col.capitalize().replace('_', ' ')}</th>\n"
                    table_columns += f"{{data: '{col}', name: '{col}'}},\n"  # Columna para DataTables
                else:
                    form_fields += f"""
                        <div class="row">
                            <div class="col-12">
                                <label for="{col}" class="form-label">{col.capitalize().replace('_', ' ')} <span class="text-danger">*</span></label>
                                <input type="text" class="form-control" name="{col}" id="{col}" placeholder="Introduzca {col}" required>
                            </div>
                        </div>"""
                    table_headers += f"<th>{col.capitalize().replace('_', ' ')}</th>\n"
                    table_columns += f"{{data: '{col}', name: '{col}'}},\n"  # Columna para DataTables
            else:
                # Si la columna es la llave primaria, agregarla como encabezado y columna para DataTables
                table_headers += f"<th>{col.capitalize().replace('_', ' ')}</th>\n"
                table_columns += f"{{data: '{col}', name: '{col}'}},\n"

        # Obtener el nombre de la clase en singular y capitalizado
        class_name = singularize_spanish(table).capitalize()

        # Convertir los nombres de las clases relacionadas (llaves foráneas) en una cadena separada por comas
        fk_class_names_str = ", ".join(fk_class_names)

        # Generar el contenido de la vista utilizando las variables generadas
        view_content = f"""@extends('template.layout')

        @section('title', 'Gestión de {class_name}')

        @section('css') 
        <link href="https://cdn.datatables.net/1.13.7/css/dataTables.bootstrap5.min.css" rel="stylesheet">
        <link href="https://cdn.datatables.net/1.13.7/css/jquery.dataTables.min.css" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        @endsection

        @section('cabeza_contenido') 
            <div class="mb-3">
                <h4>Gesti&oacute;n de {class_name}</h4>
            </div>
        @endsection

        @section('contenido') 
            <div class="row">
                <div class="p-3 col-4">
                    <a class="btn btn-success" href="javascript:void(0)" id="createNewRecord"> Nueva {class_name}</a>
                </div>
            </div>

            <div class="row">
                <div class="col-sm-12">
                    <div class="p-3 mb-2 bg-light bg-gradient text-dark border rounded-3 table-responsive">
                        <table class="table table-bordered stripe data-table display compact">
                            <thead>
                                <tr>
                                    <th>No</th>
                                    {table_headers} <!-- Encabezados de la tabla -->
                                    <th width="100px">Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            
            <!-- Modal -->
            <div class="modal fade" id="ajaxModel" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel">Titulo</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <form id="form" name="form" class="row g-3 needs-validation" autocomplete="off" novalidate>
                                @csrf
                                <input type="hidden" name="table_id" id="table_id">
                                {foreign_key_methods} <!-- Campos de llaves foráneas -->
                                {form_fields} <!-- Campos del formulario -->
                                <div class="row">
                                    <div class="col-6">
                                        <button class="btn btn-success w-100" type="submit">Guardar</button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
            <!-- /.modal -->
        @endsection

        @section('js')
            <meta name="csrf-token" content="{{{{ csrf_token() }}}}">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-validate/1.19.5/jquery.validate.js"></script>
            <script src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js"></script>
            <script src="https://cdn.datatables.net/1.13.7/js/dataTables.bootstrap5.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

            <script type="text/javascript">
                var titulo = '{class_name}';
                var URLindex = "{{{{ route('{table}.index') }}}}";
                var columnas = [
                    {{data: 'DT_RowIndex', name: 'DT_RowIndex'}},
                    {table_columns} <!-- Columnas de la tabla -->
                    {{data: 'action', name: 'action', orderable: false, searchable: false}},
                ];
            </script>
            <script src="{{{{ URL::asset('assets/js/custom/crud.js') }}}}"></script>
        @endsection
        """



        # Asignar nombre al archivo .blade.php en su forma singular en español
        singular_table = singularize_spanish(table)
        with open(os.path.join(project_path, project_name, "resources", "views", "gestion", f"{singular_table}.blade.php"), 'w') as file:
            file.write(view_content)

        connection.close()
        print(f'Vista para la tabla {table} creada exitosamente')
    except Exception as e:
        print(f"Error al crear la vista para la tabla {table}: {e}")