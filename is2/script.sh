#!/bin/bash
# -*- ENCODING: UTF-8 -*-
#tendra el parametro 'S' si quiere usar un entorno virtual existente
# o cualquier letra si quiere crear uno nuevo
var1=$1

#mkdir pruebaScript
#cd pruebaScript		
#git clone ://github.com/CristhianJBD/ProyectoIS2.git
#cd ..

if [ $var1 = "S" ]; then
    echo "Se activa entornodesarrollop3"
    source entornodesarrollop3/bin/activate
else
    echo "Se crea entorno nuevo envp3"
    virtualenv envp3
    source envp3/bin/activate
    #pip install -r pruebaScript/ProyectoIS2/is2/requerimientos.txt
    pip install -r ProyectoIS2/is2/requerimientos.txt
fi

cd ProyectoIS2/is2
chmod a+x poblardatabase.sh
./poblardatabase.sh
#cd docs				
#google-chrome-stable principal.html		
#cd ..
python manage.py runserver			
