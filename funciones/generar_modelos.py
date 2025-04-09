import os
import psycopg2

def singularize(name):
    if name.endswith('es'):
        return name[:-2]
    elif name.endswith('s'):
        return name[:-1]
    return name

def get_foreign_key_name(fk_name):
    if fk_name.startswith('id_'):
        return fk_name[3:]
    return fk_name

def generar_modelos(host, port, user, password, database, selected_tables, project_path, project_name):
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
           
           
             # Obtener las llaves foráneas
#            cursor.execute(f"""
 #               SELECT
  ###                ccu.column_name AS foreign_column_name
   #             FROM
   ##                JOIN information_schema.key_column_usage AS kcu
   #                   ON tc.constraint_name = kcu.constraint_name
   #                   AND tc.table_schema = kcu.table_schema
   ##                 JOIN information_schema.constraint_column_usage AS ccu
    #                  ON ccu.constraint_name = tc.constraint_name
   #                   AND ccu.table_schema = tc.table_schema
   #             WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name='{table}';
   #         """)

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

            # Llamar a la función correspondiente en la carpeta modelos
            if num_foreign_keys == 0:
                from funciones.models.modelo_sin_llaves_foraneas import crear_modelo
            elif num_foreign_keys == 1:
                from funciones.models.modelo_una_llave_foranea import crear_modelo
            elif num_foreign_keys == 2:
                from funciones.models.modelo_dos_llaves_foraneas import crear_modelo
            elif num_foreign_keys == 3:
                from funciones.models.modelo_tres_llaves_foraneas import crear_modelo
            elif num_foreign_keys == 4:
                from funciones.models.modelo_cuatro_llaves_foraneas import crear_modelo
            elif num_foreign_keys == 5:
                from funciones.models.modelo_cinco_llaves_foraneas import crear_modelo
            elif num_foreign_keys == 6:
                from funciones.models.modelo_cinco_llaves_foraneas import crear_modelo
            elif num_foreign_keys == 7:
                from funciones.models.modelo_cinco_llaves_foraneas import crear_modelo
            elif num_foreign_keys == 8:
                from funciones.models.modelo_cinco_llaves_foraneas import crear_modelo
            elif num_foreign_keys == 9:
                from funciones.models.modelo_cinco_llaves_foraneas import crear_modelo                   
            else:
                from funciones.models.modelo_cinco_llaves_foraneas import crear_modelo
            # Llamar a la función para crear el modelo
            crear_modelo(host, port, user, password, database, table, project_path, project_name, foreign_keys)

        connection.close()
        print('Modelos creados exitosamente')
    except Exception as e:
        print(f"Error al crear los modelos: {e}")