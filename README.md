# Gnome-breeze

A GTK Theme Built to Match KDE's Breeze. GTK2 theme made by [scionicspectre](https://github.com/scionicspectre/BreezyGTK)

# Requirements

- GTK+ 3.16
- Pixmap/Pixbuf theme engine for GTK 2

# Install instructions
If your distribution doesn't provide a package, you can install the theme system-wide by copying it to the appropriate directory, usually "/usr/share/themes".
```
find Breeze* -type f -exec install -Dm644 '{}' "$pkgdir/usr/share/themes/{}" \;
```

To install only for the current user, copy the files to "~/.themes".

To set the theme in Plasma 5, use System Settings > Application Style > GNOME Application Style. If your distribution doesn't provide a package for kde-gtk-config, you can find it here: https://projects.kde.org/projects/kde/workspace/kde-gtk-config
