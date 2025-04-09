import os
import psycopg2

#def singularize(name):
#    if name.endswith('es'):
##        return name[:-2]
 #   elif name.endswith('s'):
  #      return name[:-1]
   # return name


def singularize(name):
    return name

def crear_controlador(host, port, user, password, database, table, project_path, project_name, foreign_keys=None, fk_column_mapping=None):
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

        # Generar el contenido del controlador
        class_name = singularize(table).capitalize()
        validation_rules = ",\n            '".join([f"{col}' => 'required'" for col in column_names if col != primary_key])
        update_fields = ",\n                    '".join([f"{col}' => $request->{col}" for col in column_names if col != primary_key])

        controller_content = f"""<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\{class_name};
use Yajra\DataTables\DataTables;

class {class_name}Controller extends Controller
{{
    private $model;

    public function __construct()
    {{
        // $this->middleware("auth");
        $this->model = new {class_name}();
    }}

    public function index(Request $request)
    {{
        if ($request->ajax()) {{
            $data = $this->model::get();
            return Datatables::of($data)
                    ->addIndexColumn()
                    ->addColumn('action', function($row){{
                        $btn = '<button type="button" class="btn btn-primary btn-sm editRecord" data-id="'.$row->{primary_key}.'" data-bs-toggle="modal" data-bs-target="#modal-center">Editar<i class="fa fa-edit"></i></button>';
                        $btn = $btn.' <a href="javascript:void(0)" class="btn btn-danger btn-sm deleteRecord" data-id="'.$row->{primary_key}.'">Eliminar<i class="fa fa-trash"></i></a>';
                        return $btn;
                    }})
                    ->rawColumns(['action'])
                    ->make(true);
        }}
        return view('gestion.{singularize(table)}');
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