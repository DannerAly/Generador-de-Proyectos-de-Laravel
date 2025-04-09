import os
import psycopg2

def singularize_spanish(name):
    if name.endswith('es'):
        if name.endswith('ces'):
            return name[:-3] + 'z'
        return name[:-2]
    elif name.endswith('s'):
        return name[:-1]
    return name

def generar_vistas(host, port, user, password, database, project_path, project_name, selected_tables, fk_column_mapping):
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
            class_name = table.capitalize()
            view_path = os.path.join(project_path, project_name, "resources", "views", "gestion")
            os.makedirs(view_path, exist_ok=True)

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

            # Llamar a la función correspondiente en la carpeta vistas
            if num_foreign_keys == 0:
                from funciones.views.view_sin_llaves_foraneas import crear_vista
            else:
                from funciones.views.view_dos_llaves_foraneas import crear_vista
            # Llamar a la función para crear la vista
            crear_vista(host, port, user, password, database, table, project_path, project_name, foreign_keys, fk_column_mapping)

        connection.close()
        print('Vistas creadas exitosamente')
    except Exception as e:
        print(f"Error al crear las vistas: {e}")