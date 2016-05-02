#! /bin/bash

colors=(Breeze BreezeDark)
folders=(gtk-2.0 gtk-3.0 gtk-3.16 gtk-3.18 gtk-3.20)

for i in "${colors[@]}"
do 
  for j in "${folders[@]}"
  do
    if ! [ -d $i/$j ]
      then mkdir -p $i/$j;
    fi
  done 
  python render_assets.py "schemes/$i.colors"
  sass --cache-location /tmp/sass-cache gtk316/gtk.scss $i/gtk-3.16/gtk.css
  sass --cache-location /tmp/sass-cache gtk318/gtk.scss $i/gtk-3.18/gtk.css
  sass --cache-location /tmp/sass-cache gtk320/gtk.scss $i/gtk-3.20/gtk.css
  cp -R assets $i/
  cp -R gtk2/* $i/gtk-2.0/
  if [ -d $HOME/.themes/$i ]
    then rm -rf $HOME/.themes/$i;
  fi
  mv -f $i $HOME/.themes/
done


