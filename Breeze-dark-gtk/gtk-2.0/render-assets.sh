#! /bin/bash

INKSCAPE="/usr/bin/inkscape"
OPTIPNG="/usr/bin/optipng"

SRC_FILE="assets.svg"
INDEX="assets.txt"

for i in `cat $INDEX`
do 
ASSETS_DIR=`echo $i | cut -f1 -d '/'`
	if [ '!' -d $ASSETS_DIR ]; 
		then mkdir $ASSETS_DIR; 
	fi
	i=`echo $i | cut -f2 -d '/'`

if [ -f $ASSETS_DIR/$i.png ]; then
    echo $ASSETS_DIR/$i.png exists.
else
    echo
    echo Rendering $ASSETS_DIR/$i.png
    $INKSCAPE --export-id=$i \
              --export-id-only \
              --export-png=$ASSETS_DIR/$i.png $SRC_FILE >/dev/null #\
    # && $OPTIPNG -o7 --quiet $ASSETS_DIR/$i.png 
fi
done
exit 0
