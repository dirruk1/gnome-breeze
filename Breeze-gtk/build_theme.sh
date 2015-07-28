#! /bin/bash

SOURCE_DIR=src

if [ -d gtk-2.0 ];
	then rm -rf gtk-2.0;
fi

if [ -d gtk-3.0 ];
	then rm -rf gtk-3.0;
fi

mkdir gtk-2.0
mkdir gtk-2.0/assets
mkdir gtk-3.0

if [ $HOME/.config/kdeglobals ];
  then python $SOURCE_DIR/render_theme.py $HOME/.config/kdeglobals;
else python $SOURCE_DIR/render_theme.py;
fi

sass --cache-location /tmp/sass-cache $SOURCE_DIR/gtk3/gtk.scss $SOURCE_DIR/gtk3/gtk.css
cp -R $SOURCE_DIR/gtk3/assets gtk-3.0/
cp $SOURCE_DIR/gtk3/gtk.css gtk-3.0/
cp -R $SOURCE_DIR/gtk2/* gtk-2.0/
