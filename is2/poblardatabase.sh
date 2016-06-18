#! /bin/bash
python crearBasedeDatos.py
if [ $? -eq 0 ];then
    echo "Creando migraciones..."
    python manage.py makemigrations
    echo "Migrando base de datos..."
    python manage.py migrate
    echo "Poblando base de datos..."
else
    echo "Lo sentimos, no se pudo realizar la poblacion."
fi

echo "Poblando la Base de datos"
python manage.py loaddata Datos.json
