@echo off

echo Creando entorno virtual...

python -m venv venv
call venv\Scripts\activate

echo Entorno virtual creado

echo Instalando dependencias...

pip install -r requirements.txt

echo Dependencias instaladas.

echo ANTES DE CONTINUAR, ejecuta setup_db.bat para configurar la base de datos MySQL (debe estar instalada en el sistema).

pause

echo Iniciando proyecto...

python main.py