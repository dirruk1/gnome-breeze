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

To set the theme in Plasma 5, install kde-gtk-config and use System Settings > Application Style > GNOME Application Style.
Also make sure to disable "apply colors to non-Qt applications" in System Settings > Colors > Options.

# Color support
To enable color support move the files folder for the version of gtk you are running into the gtk-3.0 folder and move the theme to "/usr/share/themes".
Make sure breeze-gtk-colors is executable and move it to whereever you like.

or you can run the instal script:
```
git clone https://github.com/dirruk1/gnome-breeze && cd gnome-breeze;
bash install.sh "your_gtk_version"
```
Don't forget to replace "your_gtk_version" with 3.16,3.18 or 3.20

To change the colors, select a color scheme in System Settings and run breeze-gtk-colors to apply the colors.
If you don't have Plasma installed you can specify a colorfile by using breeze-gtk-colors -i {path_to_file}.
