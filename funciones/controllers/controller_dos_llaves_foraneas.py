import os
import psycopg2

def singularize(name):
    #if name.endswith('es'):
    #    return name[:-2]
    #elif name.endswith('s'):
    #    return name[:-1]
    return name

def crear_controlador(host, port, user, password, database, table, project_path, project_name, foreign_keys, fk_column_mapping):
    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = connection.cursor()

        # Obtener los nombres de las columnas de la tabla
        cursor.execute(f"""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = '{table}';
        """)
        columns = cursor.fetchall()
        column_names = [column[0] for column in columns]

        # Identificar la llave primaria
        primary_key = column_names[0]

        # Obtener la información de las llaves foráneas
        fk_columns = []
        fk_class_names = []
        for fk_column, fk_table, fk_referenced_column in foreign_keys:
            fk_columns.append(fk_column)
            fk_class_names.append(singularize(fk_table).capitalize())

        # Generar las reglas de validación
        validation_rules = ",\n            '".join([f"{col}' => 'required'" for col in column_names if col != primary_key])

        # Generar los campos de actualización
        update_fields = ",\n                    '".join([f"{col}' => $request->{col}" for col in column_names if col != primary_key])

        class_name = singularize(table).capitalize()
        view_name = singularize(table).lower()
        fk_class_names_lower_str = ", ".join([f"'{fk_class_name.lower()}'" for fk_class_name in fk_class_names])
        fk_class_names_compact_str = ", ".join([f"'{fk_class_name.lower()}'" for fk_class_name in fk_class_names])

        fk_class_imports = "\n".join([f"use App\Models\\{fk_class_name};" for fk_class_name in fk_class_names])
        fk_class_instances = "\n        ".join([f"${fk_class_name.lower()} = {fk_class_name}::all();" for fk_class_name in fk_class_names])


        # Generar las columnas dinámicas para el DataTable ADDCOLUMNS -------------------------------------------------   
        add_columns = []
        for column in column_names:
            if column in fk_columns:  # Si la columna es una llave foránea
                fk_class_name = fk_class_names[fk_columns.index(column)]
                # Obtener el atributo relacionado (nombre o el siguiente disponible)--------------------------
                if column in fk_column_mapping:
                    related_column = fk_column_mapping[column]  # Obtener el valor del diccionario
                else:
                    # Si no está en el diccionario, usar un valor predeterminado
                    related_column = 'nombre'
                # Generar el addColumn con el atributo relacionado
                add_columns.append(f"""->addColumn('{fk_class_name.lower()}_nombre', function($row) {{
                                return $row->{fk_class_name.lower()} ? $row->{fk_class_name.lower()}->{related_column} : '';
                            }})""")
            else:  # Si no es llave foránea
                add_columns.append(f"""->addColumn('{column}', function($row) {{
                                return $row->{column};
                            }})""")

        # Agregar la columna de acciones
        add_columns.append(f"""->addColumn('action', function($row) {{
                                $btn = '<button type="button" class="btn btn-primary btn-sm editRecord" data-id="'.$row->{primary_key}.'" data-bs-toggle="modal" data-bs-target="#modal-center">Editar<i class="fa fa-edit"></i></button>';
                                $btn = $btn.' <a href="javascript:void(0)" class="btn btn-danger btn-sm deleteRecord" data-id="'.$row->{primary_key}.'">Eliminar<i class="fa fa-trash"></i></a>';
                                return $btn;
                            }})""")

        # Agregar la columna de estado si existe
        if 'estado' in column_names:
            add_columns.append(f"""->addColumn('estado', function($row) {{
                                return $row->estado == 'S' ? 'Activo' : 'Inactivo';
                            }})""")

        # Unir todas las columnas generadas
        add_columns_str = "\n                    ".join(add_columns)
        #-----------------------------------------------------------------

        controller_content = f"""<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\{class_name};
{fk_class_imports};
use Yajra\DataTables\DataTables;

class {class_name}Controller extends Controller
{{
    private $model;

    public function __construct()
    {{
        // $this->middleware("auth");
        $this->model = new {class_name};
    }}

    public function index(Request $request)
    {{
        if ($request->ajax()) {{
            $data = $this->model::with({fk_class_names_compact_str})->get();
            return Datatables::of($data)
                    ->addIndexColumn()
                    {add_columns_str}
                    ->rawColumns(['action'])
                    ->make(true);
        }}
        {fk_class_instances}
        return view('gestion.{view_name}', compact({fk_class_names_lower_str}));
    }}

    public function store(Request $request)
    {{
        $request->validate([
            '{validation_rules}
        ]); 
        
        $this->model::updateOrCreate([
                    '{primary_key}' => $request->table_id
                ],
                [
                    '{update_fields}
                ]);        
        
        return response()->json(['success'=>'Registro guardado exitosamente.']);
    }}

    public function edit($id)
    {{
        $where = array('{primary_key}' => $id);
        $table  = $this->model::where($where)->first();
        $table['id'] = $table->{primary_key};
        return response()->json($table);
    }}
    
    public function destroy($id)
    {{
        $this->model::find($id)->delete();
        return response()->json(['success'=>'Registro borrado exitosamente.']);
    }}
}}
"""

        # Crear la ruta del archivo del controlador
        controllers_path = os.path.join(project_path, project_name, "app", "Http", "Controllers")
        os.makedirs(controllers_path, exist_ok=True)
        controller_file_path = os.path.join(controllers_path, f"{class_name}Controller.php")

        # Escribir el contenido del controlador en el archivo
        with open(controller_file_path, 'w') as file:
            file.write(controller_content)

        connection.close()
        print(f'Controlador para la tabla {table} creado exitosamente')
    except Exception as e:
        print(f"Error al crear el controlador para la tabla {table}: {e}")