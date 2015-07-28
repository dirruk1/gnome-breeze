import svgwrite
import cairosvg
from colorFunctions import buttongradient

class Shapes:
    def __init__(self, name, w=20, h=20):
        self.dwg = svgwrite.Drawing(filename=name, size=(w,h))

    def base(self, color):
        self.dwg.add(self.dwg.rect((0,0),(20,20), fill=color))

    def shadow(self, color='black', alpha=0.15):
        self.dwg.add(self.dwg.path(d='m 3,18 c 0,0.5 1.5,1.5 2.5,1.5 l 10.5,0 c 2,0 3.5,-1.5 3.5,-3.5 l 0,-10 c 0,-1 -1,-2.5 -1.5,-2.5', fill='none', stroke=color, opacity=alpha))

    def background(self, color, x=1, y=1, w=18, h=18, rx=3, ry=3, alpha=1):
        self.dwg.add(self.dwg.rect((x,y), (w,h), rx, ry, fill=color, opacity=alpha))

    def background_gradient(self, color, state='', alpha=1):
        [stop1,stop2] = buttongradient(color,state)
        gradient = self.dwg.linearGradient((0, 0), (0, 1))
        self.dwg.defs.add(gradient)
        gradient.add_stop_color(0, stop1)
        gradient.add_stop_color(1, stop2)
        self.dwg.add(self.dwg.rect((1,1),(18,18), 3, 3, fill=gradient.get_paint_server(default='currentColor'), opacity=alpha))

    def border(self, color, x=1.5, y=1.5, w=17, h=17, rx=2.5, ry=2.5, alpha=1):
        self.dwg.add(self.dwg.rect((x,y), (w,h), rx, ry, fill='none', stroke=color, opacity=alpha))

    def checkmark(self, color, x=4, y=4, alpha=1):
        self.dwg.add(self.dwg.rect((x,y), (12,12), 1, 1, fill=color, opacity=alpha))

    def checkmark_mixed(self, color, alpha=1):
        self.dwg.add(self.dwg.path(d='M 4,5 4,15 c 0,0.5 0.5,1 1,1 l 10,0 c 0.5,0 1,-0.5 1,-1 l 0,-10 c 0,-0.5 -0.5,-1 -1,-1 l -10,0 c -0.5,0 -1,0.5 -1,1 z M 6,14 13,14 c 0.5,0 1,-0.5 1,-1 v -7 z', fill=color, fill_rule='evenodd', opacity=alpha))

    def radio(self, color, alpha):
        self.dwg.add(self.dwg.circle((10,10), 8.5, fill='none', stroke=color, stroke_opacity=alpha))

    def radio_shadow(self, color='black', alpha=0.15):
        self.dwg.add(self.dwg.path(d='M 14.127 2.572 A 8.5 8.5 0 0 1 18.5 10 A 8.5 8.5 0 0 1 10 18.5 A 8.5 8.5 0 0 1 2.549 14.072 A 9 9 0 0 0 11 20 A 9 9 0 0 0 20 11 A 9 9 0 0 0 14.127 2.572 z', fill=color, opacity=alpha))

    def radiomark(self, color, alpha=1):
        self.dwg.add(self.dwg.circle((10,10), 6, fill=color, opacity=alpha))

    def radiomark_mixed(self, color, alpha=1):
        self.dwg.add(self.dwg.path(d='M 16,10 a 6,6 0 0 1 -6,6 6,6 0 0 1 -6,-6 6,6 0 0 1 6,-6 6,6 0 0 1 6,6 z M 6,10 14,10 c 0,2 -2,4 -4,4 -2,0 -4,-2 -4,-4 z', transform='rotate(-45 10 10)', fill=color, fill_rule='evenodd', opacity=alpha))

    def tab(self, color, rotation=0, alpha=1):
        self.dwg.add(self.dwg.path(d='m 0,20 0,-17 c 0,-1.5 1.5,-3 3,-3 h 14,0 c 1.5,0 3,1.5 3,3 v 0,17 z', transform='rotate( %d 10 10)' %rotation, fill=color, opacity=alpha))

    def tab_border(self, color, rotation=0, alpha=1):
        self.dwg.add(self.dwg.path(d='m 0.5,20 0,-17 c 0,-1.25 1.25,-2.5 2.5,-2.5 h 14,0 c 1.25,0 2.5,1.25 2.5,2.5 v 0,17', transform='rotate( %d 10 10)' %rotation, stroke=color, fill='none'))

    def combo_entry(self, color, rotation=0, alpha=1):
        self.dwg.add(self.dwg.path(d='m 20,1 -16,0 c -1.5,0 -3,1.5 -3,3 l 0,12 c 0,1.5 1.5,3 3,3 l 16,0 z', fill=color, opacity=alpha, transform='rotate( %d 10 10)' %rotation))

    def combo_entry_border(self, color, rotation=0, alpha=1):
        self.dwg.add(self.dwg.path(d='m 20,1.5 -16,0 c -1.5,0 -2.5,1 -2.5,2.5 l 0,12 c 0,1.5 1,2.5 2.5,2.5 l 16,0', fill='none', stroke=color, opacity=alpha, transform='rotate( %d 10 10)' %rotation))

    def spinbutton(self, color, rotation=0, alpha=1):
        self.dwg.add(self.dwg.path(d='m 0,1 16,0 c 1.5,0 3,1.5 3,3 l 0,16 -19,0 z', fill=color, opacity=alpha, transform='rotate( %d 10 10)' %rotation))

    def spinbutton_border(self, color, rotation=0, alpha=1):
        self.dwg.add(self.dwg.path(d='m 0,1.5 16,0 c 1.5,0 2.5,1 2.5,2.5 l 0,16', fill='none', stroke=color, opacity=alpha, transform='rotate( %d 10 10)' %rotation))

    def arrow(self, color, rotation, alpha=1):
        self.dwg.add(self.dwg.polyline([(1,8), (6,3), (11,8)], stroke=color, fill='none', opacity=alpha, transform='rotate( %d 6 6)' %rotation))

    def arrow_small(self, color, rotation, alpha=1):
        self.dwg.add(self.dwg.polyline([(1,6), (4,3), (7,6)], stroke=color, fill='none', opacity=alpha, transform='rotate( %d 4 4)' %rotation))

    def tree_header(self, color, border_color):
        self.dwg.add(self.dwg.rect((0,0), (20,20), fill=color))
        self.dwg.add(self.dwg.path(d='m 0,19.5 19.5,0 0,-19.5', fill='none', stroke=border_color))

    def scale_slider(self, color):
        self.dwg.add(self.dwg.circle((10,10), 10, fill=color))

    def scale_border(self, color):
        self.dwg.add(self.dwg.circle((10,10), 9.5, fill='none', stroke=color))

    def titlebutton_background(self,color):
        self.dwg.add(self.dwg.circle((9,9), 9, fill=color))

    def close(self,color):
        self.dwg.add(self.dwg.line((5,5), (13,13), stroke=color))
        self.dwg.add(self.dwg.line((13,5), (5,13), stroke=color))

    def minimize(self,color):
        self.dwg.add(self.dwg.polyline([(4,7), (9,12), (14,7)], stroke=color, fill='none'))

    def maximize(self,color):
        self.dwg.add(self.dwg.polyline([(4,11), (9,6), (14,11)], stroke=color, fill='none'))

    def maximize_maximized(self,color):
        self.dwg.add(self.dwg.polygon([(4.5,9), (9,4.5), (13.5,9), (9,13.5)], stroke=color, fill='none'))

    def save(self, filename, dpi=90):
        cairosvg.svg2png(self.dwg.tostring(), write_to=filename, dpi=dpi)

#-------------------------------------------------------------------------------
# assets
#-------------------------------------------------------------------------------

def assets(widget, suffix='' ,state='', w=20, h=20, color='none', color2='none', color3='none', prefix='', alpha=1, gtk_version ='gtk2'):
    filename = 'src/{0}/assets/{1}{2}{3}{4}.png'.format(gtk_version,prefix,widget,suffix,state)
    drawing = Shapes(filename,w,h)
    rotation = 0

    if widget == 'button':
        drawing.shadow()
        drawing.background_gradient(color, state=state)
        drawing.border(color2, alpha=alpha)

    elif widget == 'toolbutton':
        drawing.background(color)
        drawing.border(color2)

    elif widget == 'spinbutton':
        if suffix == '-down':
            rotation = 90
        drawing.spinbutton(color, rotation)
        drawing.spinbutton_border(color2, rotation, alpha=alpha)

    elif widget == 'checkbox':
        drawing.shadow()
        drawing.border(color, alpha=alpha)
        if suffix == '-checked':
            drawing.checkmark(color, alpha=alpha)
        if suffix == '-mixed':
            drawing.checkmark_mixed(color, alpha=alpha)

    elif widget == 'checkbox-selectionmode':
        drawing.background(color2,8,8,24,24,6,6,alpha=max(0,0.8 - 1 + alpha))
        drawing.border(color,11.5,11.5, alpha=alpha)
        if suffix == '-checked':
            drawing.checkmark(color,14,14, alpha=alpha)

    elif widget == 'radio':
        drawing.radio_shadow()
        drawing.radio(color, alpha=alpha)
        if suffix == '-checked':
            drawing.radiomark(color, alpha=alpha)
        if suffix == '-mixed':
            drawing.radiomark_mixed(color, alpha=alpha)

    elif widget == 'arrow':
        if suffix == '-right':
            rotation = 90
        elif suffix == '-down':
            rotation = 180
        elif suffix == '-left':
            rotation = 270
        drawing.arrow(color, rotation, alpha=alpha)

    elif widget == 'arrow-small':
        if suffix == '-right':
            rotation = 90
        elif suffix == '-down':
            rotation = 180
        elif suffix == '-left':
            rotation = 270
        drawing.arrow_small(color, rotation, alpha=alpha)

    elif widget == 'entry':
        drawing.base(color)
        drawing.background(color3)
        drawing.border(color2, alpha=alpha)

    elif widget == 'combo-entry':
        if suffix == '-button':
            rotation = 180
        drawing.base(color)
        drawing.combo_entry(color3,rotation)
        drawing.combo_entry_border(color2,rotation, alpha=alpha)

    elif widget == 'tab':
        if suffix == '-right':
            rotation = 90
        if suffix == '-bottom':
            rotation = 180
        if suffix == '-left':
            rotation = 270
        drawing.tab(color, rotation, alpha=alpha)
        if state == '-active':
            drawing.tab_border(color2, rotation, alpha=alpha)

    elif widget == 'notebook-gap':
        if suffix == '-horizontal':
            drawing.background(color,1,0,2,2,0,0)
        else:
            drawing.background(color,0,1,2,2,0,0)

    elif widget == 'notebook':
        drawing.background(color,0,0,20,20)
        drawing.border(color2,0.5,0.5,19,19)

    elif widget == 'progressbar':
        drawing.background(color,0,0,10,10)

    elif widget == 'scale-slider':
        drawing.scale_slider(color)
        drawing.scale_border(color2)

    elif widget == 'scale-trough':
        if suffix == '-vertical':
            drawing.background(color,7,0,6,20)
        else:
            drawing.background(color,0,7,20,6)

    elif widget == 'scrollbar-slider':
        if gtk_version=='gtk-2.0':
            if suffix == '-horizontal':
                drawing.background(color, 2,0,26,10,5,5,alpha=alpha)
            else:
                drawing.background(color, 0,2,10,26,5,5,alpha=alpha)
        else:
            if suffix == '-horizontal':
                drawing.background(color, 1,5,26,10,5,5,alpha=alpha)
            else:
                drawing.background(color, 5,1,10,26,5,5,alpha=alpha)

    elif widget == 'scrollbar-trough':
        if suffix == '-horizontal':
            drawing.background(color, 15,5,26,10,5,5, alpha=alpha)
        else:
            drawing.background(color, 5,15,10,26,5,5, alpha=alpha)

    elif widget == 'plus':
        drawing.arrow(color, 90)

    elif widget == 'minus':
        drawing.arrow(color, 180)

    elif widget == 'menu-arrow':
        drawing.arrow(color, 90, alpha=alpha)

    elif widget == 'handle':
        if suffix == '-h':
            drawing.background(color,0,0,20,2,0,0)
        else:
            drawing.background(color,0,0,2,20,0,0)

    elif widget == 'line':
        if suffix == '-h':
            drawing.background(color,0,1,8,1,0,0)
        elif suffix == '-v':
            drawing.background(color,1,0,1,8,0,0)
        elif prefix == 'menu-':
            drawing.background(color,0,0,8,1,0,0)

    elif widget == 'menubar-button':
        drawing.background(color,1,1,18,18,0,0)

    elif widget == 'toolbar-background':
        drawing.base(color)

    elif widget == 'null':
        drawing.base('none')

    elif widget == 'tree-header':
        drawing.tree_header(color,color2)

    elif widget == 'frame':
        drawing.background(color,0,0,20,20)
        drawing.border(color2,0.5,0.5,19,19)

    elif widget == 'frame-gap':
        if suffix == '-start':
            drawing.background(color,1,0,1,1,0,0)
        else:
            drawing.background(color,0,0,1,1,0,0)

    elif widget == 'titlebutton':
        drawing.titlebutton_background(color)
        if suffix == '-close':
            drawing.close(color2)
        elif suffix == '-minimize':
            drawing.minimize(color2)
        elif suffix == '-maximize':
            drawing.maximize(color2)
        elif suffix == '-maximize-maximized':
            drawing.maximize_maximized(color2)

    drawing.save(filename)
    if gtk_version == 'gtk-3.0':
        drawing.save('{0}/assets/{1}{2}{3}{4}@2.png'.format(gtk_version,prefix,widget,suffix,state), dpi=180)
