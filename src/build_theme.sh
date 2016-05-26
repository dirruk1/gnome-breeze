#!/bin/bash

create_folders () {
  FOLDERS=(gtk-2.0 gtk-3.0 gtk-3.18 gtk-3.20)
  for j in "${FOLDERS[@]}"
    do
      if ! [ -d $1/$j ]
        then mkdir -p $1/$j;
      fi
  done 
}

render_theme () {
  python render_assets.py $1
  create_folders $2
  sass --cache-location /tmp/sass-cache gtk316/gtk.scss $2/gtk-3.0/gtk.css
  sass --cache-location /tmp/sass-cache gtk318/gtk.scss $2/gtk-3.18/gtk.css
  sass --cache-location /tmp/sass-cache gtk320/gtk.scss $2/gtk-3.20/gtk.css
  mv assets $2/
  cp -R gtk2/* $2/gtk-2.0/
  if [ -d $HOME/.themes/$2 ]
    then rm -rf $HOME/.themes/$2;
  fi
  mv -f $2 $HOME/.themes/
}

if [ -z "$1" ]
then
  if [ -f "$HOME/.config/kdeglobals" ]
  then
    render_theme "$HOME/.config/kdeglobals" Breeze
  else
    echo "$HOME/.config/kdeglobals not found, using defaults"
    render_theme schemes/Breeze.colors Breeze
  fi
else
  if [ -f "schemes/$1.colors" ]
  then 
    render_theme schemes/$1.colors $1
  else
    echo "colorscheme $1 not found"
  fi
fi
        
