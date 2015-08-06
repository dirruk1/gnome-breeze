# Gnome-breeze

A GTK Theme Built to Match KDE's Breeze. GTK2 theme made by [scionicspectre](https://github.com/scionicspectre/BreezyGTK)

# Requirements

- GTK+ 3.16
- Pixmap/Pixbuf theme engine for GTK 2

# Install instructions
Install files in the appropriate directory, usually "/usr/share/themes".
```
find Breeze* -type f -exec install -Dm644 '{}' "$pkgdir/usr/share/themes/{}" \;
```

However, it is advisable to make use of the package manager of your distribution.

It is also possible to put the files under "~/.local/share/themes" for a non-system-wide installation.

To actually use the theme in the Plasma 5 desktop enviroment, I'd recommend you to use "KDE GTK Configurator" from here: https://projects.kde.org/projects/kde/workspace/kde-gtk-config

Your distribution should provide a package for this tool. It let you configure the appearance of GTK apps in the KDE System Settings.
