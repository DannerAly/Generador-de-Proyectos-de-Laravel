import os
import psycopg2

def singularize(name):
    if name.endswith('es'):
        return name[:-2]
    elif name.endswith('s'):
        return name[:-1]
    return name

def correct_pluralize(name):
    if name.endswith('z'):
        return name[:-1] + 'ces'
    elif name.endswith('ión'):
        return name[:-3] + 'iones'
    elif name.endswith('dad'):
        return name[:-3] + 'dades'
    elif name.endswith('y'):
        return name[:-1] + 'ies'
    elif name.endswith('s'):
        return name
    return name + 'es'

def get_foreign_key_name(fk_name):
    if fk_name.startswith('id_'):
        return fk_name[3:]
    return fk_name

def generar_controladores(host, port, user, password, database, project_path, project_name, selected_tables, fk_column_mapping):
    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = connection.cursor()

        for table in selected_tables:
            class_name = singularize(table).capitalize()
            primary_key = f"id_{singularize(table)}"

            cursor.execute(f""" SELECT DISTINCT ON (kcu.column_name, ccu.table_name, ccu.column_name)
    kcu.column_name AS foreign_column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu 
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu 
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY' 
AND tc.table_name = '{table}';
""")


            foreign_keys = cursor.fetchall()

            # Contar el número de llaves foráneas
            num_foreign_keys = len(foreign_keys)

            # Llamar a la función correspondiente en la carpeta controladores
            if num_foreign_keys == 0:
                from funciones.controllers.controller_sin_llaves_foraneas import crear_controlador
            else:
                from funciones.controllers.controller_dos_llaves_foraneas import crear_controlador
            # Llamar a la función para crear el controlador
            crear_controlador(host, port, user, password, database, table, project_path, project_name, foreign_keys, fk_column_mapping)

        connection.close()
        print('Controladores creados exitosamente')
    except Exception as e:
        print(f"Error al crear los controladores: {e}")