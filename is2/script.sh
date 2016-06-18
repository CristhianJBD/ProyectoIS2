#!/bin/bash
# -*- ENCODING: UTF-8 -*-
#tendra el parametro 'entornodesarrollop2' si quiere usar un entorno virtual existente
# o cualquier letra si quiere crear uno nuevo
var1=$1
cd SCRIPTDESARROLLO		
git clone ://github.com/CristhianJBD/ProyectoIS2.git
cd ..
echo $var1
if [ $var1 = "entornodesarrollop2" ]; then
    echo "Se activa entornodesarrollop2"
    source entornodesarrollop2/bin/activate
else
    echo "Se crea entorno nuevo envp2"
    virtualenv -p /usr/bin/python2 envp2
    source envp2/bin/activate
    pip install -r SCRIPTDESARROLLO/ProyectoIS2/is2/requerimientos.txt
fi

cd SCRIPTDESARROLLO/ProyectoIS2/is2
chmod a+x poblardatabase.sh
./poblardatabase.sh
python manage.py runserver			
