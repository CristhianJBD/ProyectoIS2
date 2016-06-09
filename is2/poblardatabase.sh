#! /bin/bash
python crearBasedeDatos.py
#Solucion de Problema
#rm administracion/urls.py
#rm is2/urls.py 
#cp herramienta/urlsadmC.py administracion/urls.py
#cp herramienta/urlsis2C.py is2/urls.py
if [ $? -eq 0 ];then
    echo "Creando migraciones..."
    python manage.py makemigrations
    echo "Migrando base de datos..."
    python manage.py migrate
    echo "Poblando base de datos..."
else
    echo "Lo sentimos, no se pudo realizar la poblacion."
fi
#Solucion de Problema 2
#rm administracion/urls.py
#rm is2/urls.py 
#cp herramienta/urlsadm.py administracion/urls.py
#cp herramienta/urlsis2.py is2/urls.py
echo "from django.contrib.auth.models import User;
User.objects.create_superuser('admin', 'admin@is2.com', 'adminadmin')" | python manage.py shell
echo "from django.contrib.auth.models import User;
User.objects.create_superuser('capi', 'capi@is2.com', 'adminadmin')" | python manage.py shell
