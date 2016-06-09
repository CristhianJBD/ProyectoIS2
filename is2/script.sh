#!/bin/bash
# -*- ENCODING: UTF-8 -*-
#tendra el parametro 'entornodesarrollop2' si quiere usar un entorno virtual existente
# o cualquier letra si quiere crear uno nuevo
var1=$1
mkdir SCRIPTDESARROLLO
cd SCRIPTDESARROLLO		
git clone ://github.com/CristhianJBD/ProyectoIS2.git
cd ..
#cp -r is2 script
echo $var1
if [ $var1 = "entornodesarrollop2" ]; then
    echo "Se activa entornodesarrollop2"
    source entornodesarrollop2/bin/activate
else
    echo "Se crea entorno nuevo entornodesarrollop2"
    virtualenv entornodesarrollop2
    source entornodesarrollop2/bin/activate
    pip install -r ProyectoIS2/is2/requerimientos.txt
fi

cd SCRIPTDESARROLLO/ProyectoIS2/is2
chmod a+x poblardatabase.sh
./poblardatabase.sh
#cd docs				
#google-chrome-stable principal.html		
#cd ..
python manage.py runserver			
