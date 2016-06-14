#!/bin/bash

python apply-gtk-colors.py -f -i ./Breeze.colors -o .

#sass --cache-location /tmp/sass-cache gtk316/gtk.scss $2/gtk-3.0/gtk.css
#sass --cache-location /tmp/sass-cache gtk318/gtk.scss $2/gtk-3.18/gtk.css
sass --cache-location /tmp/sass-cache sass/gtk320/gtk-main.scss ./Breeze/gtk-3.0/gtk-main.css --style expanded --sourcemap=none
  
cp -R gtk2/widgets Breeze/gtk-2.0/

#if [ -d /usr/share/themes/Breeze ]
#  then sudo rm -rf /usr/share/themes/Breeze
#fi

#sudo mv -f ./Breeze /usr/share/themes/Breeze
        
