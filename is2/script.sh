#!/bin/bash
# -*- ENCODING: UTF-8 -*-
#tendra el parametro 'entornodesarrollop3' si quiere usar un entorno virtual existente
# o cualquier letra si quiere crear uno nuevo
var1=$1
mkdir SCRIPTDESARROLLO
cd SCRIPTDESARROLLO		
git clone ://github.com/CristhianJBD/ProyectoIS2.git
cd ..
echo $var1
if [ $var1 = "entornodesarrollop3" ]; then
    echo "Se activa entornodesarrollop3"
    source entornodesarrollop3/bin/activate
else
    echo "Se crea entorno nuevo envp3"
    virtualenv envp3
    source envp3/bin/activate
    pip install -r SCRIPTDESARROLLO/ProyectoIS2/is2/requerimientos.txt
fi

cd SCRIPTDESARROLLO/ProyectoIS2/is2
chmod a+x poblardatabase.sh
./poblardatabase.sh
#cd docs				
#google-chrome-stable principal.html		
#cd ..
python manage.py runserver			
