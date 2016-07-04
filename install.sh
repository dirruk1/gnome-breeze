
INSTALL_DIR="/usr/share/themes/Breeze"
THEME_DIR="Breeze"

if [ "$#" -ne 1 ]
then
  echo "specify gtk version"
  exit 1
fi

if [ -d $INSTALL_DIR ]
  then  sudo rm -rf $INSTALL_DIR
fi

sudo mkdir $INSTALL_DIR
sudo cp -R $THEME_DIR/gtk-2.0  $INSTALL_DIR/gtk-2.0
case "$1" in
    3.16)   sudo cp -R $THEME_DIR/gtk-3.16 $INSTALL_DIR/gtk-3.0
            ;;
    3.18)   sudo cp -R $THEME_DIR/gtk-3.18 $INSTALL_DIR/gtk-3.0
            ;;
    3.20)   sudo cp -R $THEME_DIR/gtk-3.20 $INSTALL_DIR/gtk-3.0
            ;;
    *)      echo "invalid option"
esac

chmod 755 breeze-gtk-colors
sudo cp breeze-gtk-colors /usr/bin/
