@echo off

call venv\Scripts\activate

echo Conectando a la base de datos local. 
echo Ingresa el usuario de tu base de datos (root por ejemplo)
set /p db_user=User:
echo Ingresa el puerto donde esta tu base de datos (3306 por ejemplo)
set /p db_port=Puerto:
echo Ingresa tu contrasena de la base de datos
set /p db_password=Contrasena:

python db/cargar_db.py %db_user% %db_password% %db_port%

pause