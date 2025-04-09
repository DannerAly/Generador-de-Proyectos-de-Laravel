import os
import psycopg2

def singularize(name):
    #if name.endswith('es'):
    #    return name[:-2]
    #elif name.endswith('s'):
    #    return name[:-1]
    return name

def crear_modelo(host, port, user, password, database, table, project_path, project_name, foreign_keys):
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

        # Generar el contenido del modelo
        class_name = singularize(table).capitalize()
        fillable_fields = "',\n        '".join([col for col in column_names if col != primary_key])

        # Obtener la información de la llave foránea
        fk_column, fk_table, fk_referenced_column = foreign_keys[0]
        fk_class_name = singularize(fk_table).capitalize()

        model_content = f"""<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class {class_name} extends Model
{{
    use HasFactory;

    protected $table = '{table}';
    protected $primaryKey = '{primary_key}';
    public $timestamps = false;

    protected $fillable = [
        '{fillable_fields}'
    ];

    public function {fk_class_name.lower()}()
    {{
        return $this->belongsTo({fk_class_name}::class, '{fk_column}');
    }}
}}
"""

        # Crear la ruta del archivo del modelo
        models_path = os.path.join(project_path, project_name, "app", "Models")
        os.makedirs(models_path, exist_ok=True)
        model_file_path = os.path.join(models_path, f"{class_name}.php")

        # Escribir el contenido del modelo en el archivo
        with open(model_file_path, 'w') as file:
            file.write(model_content)

        connection.close()
        print(f'Modelo para la tabla {table} creado exitosamente')
    except Exception as e:
        print(f"Error al crear el modelo para la tabla {table}: {e}")