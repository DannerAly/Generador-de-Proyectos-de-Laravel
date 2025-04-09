import os
import psycopg2

def singularize_spanish(name):
  
    return name

def crear_vista(host, port, user, password, database, table, project_path, project_name, foreign_keys=None, fk_column_mapping=None):
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

        # Identificar la llave primaria
        primary_key = column_names[0]

        # Generar los campos del formulario dinámicamente
        form_fields = ""
        table_headers = ""
        table_columns = ""
        is_first_column = True  # Variable para controlar la primera columna
        for col, col_type in columns:
            
            #------------------------------------------------------
            # Si la columna es la primera, no concatenar nada a form_fields
            if is_first_column:
                is_first_column = False  # Marcar que ya se procesó la primera columna
                continue  # Saltar esta iteración del bucle

            if col != f"id_{singularize_spanish(table)}":
                
                if col != primary_key:
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
                    elif "date" in col_type or "time" in col_type:
                        form_fields += f"""
                            <div class="row">
                                <div class="col-12">
                                    <label for="{col}" class="form-label">{col.capitalize().replace('_', ' ')} <span class="text-danger">*</span></label>
                                    <input type="date" class="form-control" name="{col}" id="{col}" required>
                                </div>
                            </div>"""
                    elif "int" in col_type:
                        form_fields += f"""
                            <div class="row">
                                <div class="col-12">
                                    <label for="{col}" class="form-label">{col.capitalize().replace('_', ' ')} <span class="text-danger">*</span></label>
                                    <input type="number" class="form-control" name="{col}" id="{col}" placeholder="Introduzca {col}" required>
                                </div>
                            </div>"""
                    else:
                        form_fields += f"""
                            <div class="row">
                                <div class="col-12">
                                    <label for="{col}" class="form-label">{col.capitalize().replace('_', ' ')} <span class="text-danger">*</span></label>
                                    <input type="text" class="form-control" name="{col}" id="{col}" placeholder="Introduzca {col}" required>
                                </div>
                            </div>"""
                table_headers += f"<th>{col.capitalize().replace('_', ' ')}</th>\n"
                table_columns += f"{{data: '{col}', name: '{col}'}},\n"

        class_name = singularize_spanish(table).capitalize()
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
                            {table_headers}
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
                        {form_fields}
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
            {table_columns}
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