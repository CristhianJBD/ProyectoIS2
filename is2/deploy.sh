#!/bin/bash
# -*- ENCODING: UTF-8 -*-
#tendra el parametro 'entornodesarrollop2' si quiere usar un entorno virtual existente
# o cualquier letra si quiere crear uno nuevo
var1=$1
source entornodesarrollop2/bin/activate
cd is2		
git clone https://github.com/CristhianJBD/ProyectoIS2.git
cd ProyectoIS2/is2
chmod a+x poblardatabase.sh
./poblardatabase.sh
deactivate
sudo service apache2 restart			
