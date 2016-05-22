import cairo
import colorsys
from math import pi
import os
import errno
import sys

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

class ReadKdeGlobals():
    def __init__(self):
        self._colors = {}
        self._colors = self.read_globals('schemes/Breeze.colors')

    def read_globals(self,filename):
        with open(filename, 'r') as _kde:
            for widget in ['Disabled', 'Inactive','Button', 'Selection', 'Tooltip', 'View', 'Window', 'WM']:
                for line in _kde:
                    if line.strip().split(':')[-1].strip('[]') == widget:
                        break
                for line in _kde:
                    if line == '\n':
                        break
                    self._colors['{0}{1}'.format(widget,line.strip().split('=')[0])] = line.strip().split('=')[1]
        return self._colors

class Color(object):
    def __init__(self, colordict,name,name2=None,amount=0):
        color = colordict[name]
        self.colordict = colordict

        r = float(color.split(',')[0])
        g = float(color.split(',')[1])
        b = float(color.split(',')[2])
        if not name2 == None:
            color2 = colordict[name2]
            r = r * amount + float(color2.split(',')[0]) * (1 - amount)
            g = g * amount + float(color2.split(',')[1]) * (1 - amount)
            b = b * amount + float(color2.split(',')[2]) * (1 - amount)

        self.rgb255 = (r,g,b)
        self.rgb = (r/255,g/255,b/255)
        self.html = '#%02x%02x%02x' % self.rgb255
        self.insensitive = self._color_effect(self._intensity_effect(self.rgb,'Disabled'),'Disabled')
        self.insensitive_alpha = self._contrast_effect(self.rgb,'Disabled')

        if self.colordict['InactiveEnable'] == 'false':
            self.inactive = self.rgb
            self.inactive_alpha = 1.0
        else:
            self.inactive = self._color_effect(self._intensity_effect(self.rgb,'Inactive'),'Inactive')
            self.inactive_alpha = self._contrast_effect(self.rgb,'Inactive')
        self.inactive_insensitive = self._color_effect(self._intensity_effect(self.inactive,'Disabled'),'Disabled')
        self.inactive_insensitive_alpha = max(self.inactive_alpha - (1 - self.insensitive_alpha),0)

    def _mix(self,color, mix_color, amount):
        r = color[0] * amount + mix_color[0] * (1 - amount)
        g = color[1] * amount + mix_color[1] * (1 - amount)
        b = color[2] * amount + mix_color[2] * (1 - amount)
        return (r,g,b)

    def _lighter(self,color,amount):
        h,s,v = colorsys.rgb_to_hsv(color[0],color[1],color[2])
        v = min((1+amount)*v,1)
        r,g,b = colorsys.hsv_to_rgb(h,s,v)
        return (r,g,b)

    def _darker(self,color,amount):
        h,s,v = colorsys.rgb_to_hsv(color[0],color[1],color[2])
        if amount == -1:
            v = 1
        else:
            v = min(v/(1+amount),1)
        r,g,b = colorsys.hsv_to_rgb(h,s,v)
        return (r,g,b)

    def _desaturate(self,color,amount):
        h,s,v = colorsys.rgb_to_hsv(color[0],color[1],color[2])
        s = min(s * (1 - amount),1)
        r,g,b = colorsys.hsv_to_rgb(h,s,v)
        return (r,g,b)

    def _intensity_effect(self,color,state):
        effect = int(self.colordict[state + 'IntensityEffect'])
        amount = float(self.colordict[state + 'IntensityAmount'])
        if effect == 0:
            (r,g,b) = color
        elif effect == 1:
            if amount >= 0:
                (r,g,b) = self._mix((1.0,1.0,1.0),color,amount)
            else:
                (r,g,b) = self._mix((0.0,0.0,0.0),color,amount)
        elif effect == 2:
            (r,g,b) = self._darker(color,amount)
        elif effect == 3:
            (r,g,b) = self._lighter(color,amount)
        return (r,g,b)

    def _color_effect(self,color,state):
        effect = int(self.colordict[state + 'ColorEffect'])
        amount = float(self.colordict[state + 'ColorAmount'])
        effect_color = self.colordict[state + 'Color']
        effect_color = (float(effect_color.split(',')[0])/255,float(effect_color.split(',')[1])/255,float(effect_color.split(',')[2])/255)
        if effect == 0:
            (r,g,b) = color
        elif effect == 1:
            (r,g,b) = self._desaturate(color,amount)
        else:
            (r,g,b) = self._mix(effect_color,color,amount)
        return (r,g,b)

    def _contrast_effect(self,color,state):
        effect = int(self.colordict[state + 'ContrastEffect'])
        amount = float(self.colordict[state + 'ContrastAmount'])
        if effect == 0:
            return 1.0
        else:
            return 1.0 - amount

    def lighten_color(self,amount):
        h,s,v = colorsys.rgb_to_hsv(self.rgb[0], self.rgb[1], self.rgb[2])
        v = (1+amount)*v
        r,g,b = colorsys.hsv_to_rgb(h,s,v)
        self.rgb = (r,g,b)
        self.rgb255 = (r*255,g*255,b*255)


    def gradient(self,state='',alpha=1.0):
        if state == 'active':
            stop1 = self._lighter(self.rgb,0.03)
            stop2 = self._darker(self.rgb,0.10)
            linear = cairo.LinearGradient(1, 1, 1, 19)
            linear.add_color_stop_rgba(0.0,stop1[0],stop1[1],stop1[2],alpha)
            linear.add_color_stop_rgba(1.0,stop2[0],stop2[1],stop2[2],alpha)
        else:
            stop1 = self._lighter(self.rgb,0.01)
            stop2 = self._darker(self.rgb,0.03)
            linear = cairo.LinearGradient(1, 1, 1, 19)
            linear.add_color_stop_rgba(0.0,stop1[0],stop1[1],stop1[2],alpha)
            linear.add_color_stop_rgba(1.0,stop2[0],stop2[1],stop2[2],alpha)
        return linear

class Assets(object):
    def __init__(self,width,height,scl=1, rotation=0, filename='png'):
        self.w = width; self.h = height
        if  filename == 'png':
            self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, scl*width, scl*height)
        else:
            self.surface = cairo.SVGSurface('assets/' + filename, scl*width, scl*height)
        cr = self.cr = cairo.Context(self.surface)
        if rotation != 0:
            cr.translate(scl*width/2,scl*height/2)
            cr.rotate(rotation*pi/2)
            cr.translate(-scl*width/2,-scl*height/2)
        cr.scale(scl,scl)

    def background(self,color):
        self.cr.rectangle(0,0,self.w,self.h)
        self.cr.set_source_rgb(color[0],color[1],color[2])
        self.cr.fill()

    def line(self,color,x,y,width,height):
        self.cr.rectangle(x,y,width,height)
        self.cr.set_source_rgb(color[0],color[1],color[2])
        self.cr.fill()

    def rounded_rectancle(self, color, width, height, x, y, radius, alpha=1.0, gradient=False):
        self.cr.new_sub_path()
        self.cr.arc(x + width - radius, y + radius, radius, -pi/2, 0)
        self.cr.arc(x + width - radius, y + height - radius, radius, 0, pi/2)
        self.cr.arc(x + radius, y + height - radius, radius, pi/2, pi)
        self.cr.arc(x + radius, y + radius, radius, pi, 3*pi/2)
        self.cr.close_path()
        if gradient:
            self.cr.set_source(color)
        elif color == None:
            self.cr.set_operator(cairo.OPERATOR_CLEAR)
        elif color == 'shadow':
            self.cr.set_source_rgba(0.0,0.0,0.0, 0.15)
        else:
            self.cr.set_source_rgba(color[0],color[1],color[2], alpha)
        self.cr.fill()

    def rounded_triangle(self, color, width, height, x, y, radius, alpha=1.0):
        self.cr.new_sub_path()
        self.cr.move_to(x + width, y)
        self.cr.line_to(x + width, y + height - radius)
        self.cr.arc(x + width - radius, y + height - radius,radius, 0, pi/2)
        self.cr.line_to(x, y + height)
        self.cr.close_path()
        self.cr.set_source_rgba(color[0],color[1],color[2], alpha)
        self.cr.fill()

    def circle(self, color, x, y, radius, alpha=1.0, gradient=False):
        self.cr.new_sub_path()
        self.cr.arc(x, y, radius, 0, 2*pi)
        self.cr.close_path()
        if gradient:
            self.cr.set_source(color)
        elif color == None:
            self.cr.set_operator(cairo.OPERATOR_CLEAR)
        elif color == 'shadow':
            self.cr.set_source_rgba(0.0,0.0,0.0, 0.15)
        else:
            self.cr.set_source_rgba(color[0],color[1],color[2], alpha)
        self.cr.fill()

    def half_circle(self, color, x, y, radius, alpha=1.0):
        self.cr.new_sub_path()
        self.cr.arc(x, y, radius, -pi/4, 3*pi/4)
        self.cr.close_path()
        self.cr.set_source_rgba(color[0],color[1],color[2],alpha)
        self.cr.fill()

    def arrow(self, color, alpha=1.0, shiftx=0, shifty=0):
        self.cr.new_sub_path()
        self.cr.move_to(shiftx + 1,shifty + 8)
        self.cr.line_to(shiftx + 6,shifty + 3)
        self.cr.line_to(shiftx + 11,shifty + 8)
        self.cr.set_source_rgba(color[0],color[1],color[2],alpha)
        self.cr.set_line_width(1.0)
        self.cr.stroke()

    def arrow_small(self, color,alpha=1.0):
        self.cr.new_sub_path()
        self.cr.move_to(1,6)
        self.cr.line_to(4,3)
        self.cr.line_to(7,6)
        self.cr.set_source_rgba(color[0],color[1],color[2], alpha)
        self.cr.set_line_width(1.0)
        self.cr.stroke()

    def tab(self, color, width, height, x, y, radius, alpha=1.0):
        self.cr.move_to(width + x, y)
        self.cr.line_to(width + x, height - radius + y)
        self.cr.arc(width - radius + x, height - radius + y, radius, 0, pi/2)
        self.cr.line_to(radius + x, height + y)
        self.cr.arc(radius + x,height - radius + y,radius,pi/2,pi)
        self.cr.line_to(x,y)
        self.cr.close_path
        if color == None:
            self.cr.set_operator(cairo.OPERATOR_CLEAR)
        else:
            self.cr.set_source_rgba(color[0],color[1],color[2], alpha)
        self.cr.fill()

    def spinbutton(self, color, width, height, x, y, radius,alpha=1.0):
        self.cr.move_to(width + x, y)
        self.cr.line_to(width + x, height - radius + y)
        self.cr.arc(width - radius + x, height - radius + y, radius, 0, pi/2)
        self.cr.line_to(x, height + y)
        self.cr.line_to(x,y)
        self.cr.close_path()
        if color == None:
            self.cr.set_operator(cairo.OPERATOR_CLEAR)
        else:
            self.cr.set_source_rgba(color[0],color[1],color[2],alpha)
        self.cr.fill()

    def notebook(self, color, width, height, x, y, radius):
        self.cr.move_to(x, y)
        self.cr.line_to(x + width - radius, y)
        self.cr.arc(x + width - radius, y + radius, radius, -pi/2, 0)
        self.cr.line_to(x + width, y + height-radius)
        self.cr.arc(x + width - radius, y + height - radius, radius, 0, pi/2)
        self.cr.line_to(x + radius,y + height)
        self.cr.arc(x + radius, y + height -radius, radius, pi/2, pi)
        self.cr.close_path()
        self.cr.set_source_rgb(color[0],color[1],color[2])
        self.cr.fill()

    def minimize(self,color=None):
        self.cr.move_to(4,7)
        self.cr.line_to(9,12)
        self.cr.line_to(14,7)
        if color == None:
            self.cr.set_operator(cairo.OPERATOR_CLEAR)
        else:
            self.cr.set_source_rgb(color[0],color[1],color[2])
        self.cr.set_line_width(1.0)
        self.cr.stroke()

    def maximize(self,color=None):
        self.cr.move_to(4,11)
        self.cr.line_to(9,6)
        self.cr.line_to(14,11)
        if color == None:
            self.cr.set_operator(cairo.OPERATOR_CLEAR)
        else:
            self.cr.set_source_rgb(color[0],color[1],color[2])
        self.cr.set_line_width(1.0)
        self.cr.stroke()

    def maximize_maximized(self,color=None):
        self.cr.move_to(4.5,9)
        self.cr.line_to(9,4.5)
        self.cr.line_to(13.5,9)
        self.cr.line_to(9,13.5)
        self.cr.close_path()
        if color == None:
            self.cr.set_operator(cairo.OPERATOR_CLEAR)
        else:
            self.cr.set_source_rgb(color[0],color[1],color[2])
        self.cr.set_line_width(1.0)
        self.cr.stroke()

    def close(self,color=None):
        self.cr.move_to(5,5)
        self.cr.line_to(13,13)
        self.cr.move_to(13,5)
        self.cr.line_to(5,13)
        if color == None:
            self.cr.set_operator(cairo.OPERATOR_CLEAR)
        else:
            self.cr.set_source_rgb(color[0],color[1],color[2])
        self.cr.set_line_width(1.0)
        self.cr.stroke()

    def save(self, filename):
        self.surface.write_to_png('assets/' + filename)


def check_items(color1,color2,state,alpha=1.0):
    for scl in  [1,2]:
        if scl == 2:
            ending = '@2.png'
        else:
            ending = '.png'
        # checkboxes
        box = Assets(20,20,scl)
        box.rounded_rectancle('shadow',18,18,2,2,3)
        box.rounded_rectancle(color2,18,18,1,1,3)
        box.rounded_rectancle(color1,18,18,1,1,3,alpha=alpha)
        box.rounded_rectancle(color2,16,16,2,2,2)
        box.save('check-unchecked' + state + ending)
        if state != '':
            box.rounded_rectancle(color1,12,12,4,4,1,alpha=alpha)
            box.save('check-checked' + state + ending)
            box.rounded_triangle(color2,8,8,6,6,1,alpha=alpha)
            box.save('check-mixed' + state + ending)

        # radio
        radio = Assets(20,20,scl)
        radio.circle('shadow',11,11,9)
        radio.circle(color2,10,10,9)
        radio.circle(color1,10,10,9,alpha=alpha)
        radio.circle(color2,10,10,8)
        radio.save('radio-unchecked' + state + ending)
        if state != '':
            radio.circle(color1,10,10,6,alpha=alpha)
            radio.save('radio-checked' + state + ending)
            radio.half_circle(color2,10,10,4,alpha=alpha)
            radio.save('radio-mixed' + state + ending)

        # selectionmode
        selectionmode = Assets(40,40,scl)
        selectionmode.rounded_rectancle('shadow',18,18,12,12,3)
        selectionmode.rounded_rectancle(color2,18,18,11,11,3)
        selectionmode.rounded_rectancle(color1,18,18,11,11,3,alpha=alpha)
        selectionmode.rounded_rectancle(color2,16,16,12,12,2)
        selectionmode.save('check-selectionmode-unchecked' + state + ending)
        if state != '':
            selectionmode.rounded_rectancle(color1,12,12,14,14,1,alpha=alpha)
            selectionmode.save('check-selectionmode-checked' + state + ending)

def buttons(color1,color2,color3,state,alpha=1.0):
    button = Assets(20,20)
    button.rounded_rectancle('shadow',18,18,2,2,3)
    button.rounded_rectancle(color1,18,18,1,1,3)
    button.rounded_rectancle(color2,18,18,1,1,3,alpha=alpha)
    if state == '-active':
        button.rounded_rectancle(color3,18,18,1,1,3, gradient=True)
    else:
        button.rounded_rectancle(color1,16,16,2,2,2)
        button.rounded_rectancle(color3,16,16,2,2,2, gradient=True)
    button.save('button' + state + '.png')

def togglebuttons(color1,color2,color3,state,alpha=1.0):
    button = Assets(20,20)
    button.rounded_rectancle(color1,18,18,1,1,3)
    button.rounded_rectancle(color2,18,18,1,1,3,alpha=alpha)
    if state == '-active':
        button.rounded_rectancle(color3,18,18,1,1,3, gradient=True)
    else:
        button.rounded_rectancle(color1,16,16,2,2,2)
        button.rounded_rectancle(color3,16,16,2,2,2, gradient=True)
    button.save('togglebutton' + state + '.png')

def scale_slider(color1,color2,color3,state,alpha=1.0):
    scale = Assets(20,20)
    scale.circle(color1,10,10,10)
    scale.circle(color2,10,10,10,alpha=alpha)
    scale.circle(color1,10,10,9)
    scale.circle(color3,10,10,9,gradient=True)
    scale.save('scale-slider' + state + '.png')

def scale_trough(color):
    trough_h = Assets(20,20)
    trough_h.rounded_rectancle(color,20,6,0,7,3)
    trough_h.save('scale-trough-horizontal.png')

    trough_h = Assets(20,20)
    trough_h.rounded_rectancle(color,6,20,7,0,3)
    trough_h.save('scale-trough-vertical.png')


def tabs(color1,color2,state):
    if state == '-inactive':
        alpha = 0.2
    else:
        alpha = 1.0
    direction = ['-bottom','-left','-top','-right']
    for i in range(0,4):
        tab = Assets(20,20,rotation=i)
        tab.tab(color1,20,20,0,0,3,alpha)
        if state == '-active':
            tab.tab(color2,18,19,1,0,2)
        tab.save('tab' + direction[i] + state + '.png')

def arrows(color,state,alpha=1.0):
    direction = ['-up','-right','-down','-left']
    for i in range(0,4):
        arw = Assets(12,12,rotation=i)
        arw.arrow(color,alpha)
        arw.save('arrow' + direction[i] + state + '.png')

        arw = Assets(8,8,rotation=i)
        arw.arrow_small(color,alpha)
        arw.save('arrow-small' + direction[i] + state + '.png')

def menu_arrow(color,state,alpha=1.0):
    arrow = Assets(12,12,rotation=1)
    arrow.arrow(color,alpha)
    arrow.save('menu-arrow' + state + '.png')

def scrollbar_slider(color,state,alpha=1):
    for scl in [1,2]:
        if scl == 2:
            ending = '@2.png'
        else:
            ending = '.png'
        slider = Assets(30,20,scl)
        slider.rounded_rectancle(color,30,10,0,5,5,alpha)
        slider.save('scrollbar-slider-horizontal' + state + ending)

        slider = Assets(20,30,scl)
        slider.rounded_rectancle(color,10,30,5,0,5,alpha)
        slider.save('scrollbar-slider-vertical' + state + ending)

def scrollbar_trough(color):
    for scl in [1,2]:
        if scl == 2:
            ending = '@2.png'
        else:
            ending = '.png'
        trough = Assets(56,20,scl)
        trough.rounded_rectancle(color,26,10,15,5,5,0.3)
        trough.save('scrollbar-trough-horizontal' + ending)

        trough = Assets(20,56,scl)
        trough.rounded_rectancle(color,10,26,5,15,5,0.3)
        trough.save('scrollbar-trough-vertical' + ending)

def titlebuttons(color1,color2,state):
    for scl in [1,2]:
        if scl == 2:
            ending = '@2.png'
        else:
            ending = '.png'
        title_minimize = Assets(18,18,scl)
        title_maximize = Assets(18,18,scl)
        title_maximized = Assets(18,18,scl)
        if state == '' or state == '-backdrop':
            title_minimize.minimize(color1)
            title_maximize.maximize(color1)
            title_maximized.maximize_maximized(color1)
        else:
            title_minimize.circle(color1,9,9,9)
            title_maximize.circle(color1,9,9,9)
            title_maximized.circle(color1,9,9,9)
            title_minimize.minimize()
            title_maximize.maximize()
            title_maximized.maximize_maximized()
        title_minimize.save('titlebutton-minimize' + state + ending)
        title_maximize.save('titlebutton-maximize' + state + ending)
        title_maximized.save('titlebutton-maximize-maximized' + state + ending)

        title_close = Assets(18,18,scl)
        title_close.circle(color2,9,9,9)
        title_close.close()
        title_close.save('titlebutton-close' + state + ending)

def entry(color1,color2,color3,state,alpha=1.0):
    entry = Assets(20,20)
    entry.background(color1)
    entry.rounded_rectancle(color2,18,18,1,1,3,alpha=alpha)
    entry.rounded_rectancle(color3,16,16,2,2,2)
    entry.rounded_rectancle(color3,16,16,2,2,2)
    entry.save('entry' + state + '.png')

    entry = Assets(20,20,rotation=1)
    entry.background(color1)
    entry.tab(color2,18,19,1,0,3,alpha=alpha)
    entry.tab(color3,16,18,2,0,2)
    entry.save('combo-entry' + state + '.png')

    entry_button = Assets(20,20,rotation=3)
    entry_button.background(color1)
    entry_button.tab(color2,18,19,1,0,3,alpha=alpha)
    entry_button.tab(color3,16,18,2,0,2)
    entry_button.save('combo-entry-button' + state + '.png')

    if state != '-active':
        direction = ['-down','-down-rtl','-up-rtl','-up']
        for i in range(0,4):
            spin = Assets(20,20,rotation=i)
            spin.background(color1)
            spin.spinbutton(color2,19,19,0,0,3,alpha=alpha)
            spin.spinbutton(color3,18,18,0,0,2)
            spin.save('spinbutton' + direction[i] + state + '.png')

def mixed(color1, color2,color3):
    nll = Assets(20,20)
    nll.save('null.png')

    # Frame
    frame = Assets(20,20)
    frame.rounded_rectancle(color1,20,20,0,0,3)
    frame.rounded_rectancle(color2,18,18,1,1,2)
    frame.save('frame.png')

    # Tree header
    header = Assets(20,20)
    header.background(color2)
    header.line(color1,0,19,20,1)
    header.line(color1,19,0,1,20)
    header.save('tree-header.png')

    # Notebook gap
    notebook_gap = Assets(4,2)
    notebook_gap.line(color2,1,0,2,2)
    notebook_gap.save('notebook-gap-horizontal.png')

    notebook_gap = Assets(2,4)
    notebook_gap.line(color2,0,1,2,2)
    notebook_gap.save('notebook-gap-vertical.png')

    # Notebook frame
    direction = ['-top','-right','-bottom','-bottom']
    for i in range(0,4):
        notebook_frame = Assets(20,20,rotation=i)
        notebook_frame.notebook(color1,20,20,0,0,3)
        notebook_frame.notebook(color2,18,18,1,1,2)
        notebook_frame.save('notebook-frame' + direction[i] + '.png')


    # Frame gap
    frame_gap = Assets(2,1)
    frame_gap.line(color1,1,0,1,1)
    frame_gap.save('frame-gap-start.png')

    frame_gap = Assets(2,1)
    frame_gap.line(color1,0,0,1,1)
    frame_gap.save('frame-gap-end.png')

    # Lines
    lines = Assets(20,1)
    lines.line(color1,0,0,20,1)
    lines.save('line-h.png')

    lines = Assets(1,20)
    lines.line(color1,0,0,1,20)
    lines.save('line-v.png')

    lines = Assets(20,1)
    lines.line(color2,0,0,20,1)
    lines.save('handle-h.png')

    lines = Assets(1,20)
    lines.line(color2,0,0,1,20)
    lines.save('handle-v.png')

    menubar = Assets(20,20)
    menubar.line(color3,1,1,18,18)
    menubar.save('menubar-button.png')

def toolbar(color1, color2, color3):
    # Toolbar background
    bar = Assets(20,20)
    bar.background(color2)
    bar.save('toolbar-background.png')

    # Toolbutton toggled
    toolbutton = Assets(20,20)
    toolbutton.rounded_rectancle(color1,18,18,1,1,3)
    toolbutton.save('toolbutton-toggled.png')

    # Toolbutton hover
    toolbutton = Assets(20,20)
    toolbutton.rounded_rectancle(color3,18,18,1,1,3)
    toolbutton.rounded_rectancle(color2,16,16,2,2,2)
    toolbutton.save('toolbutton-hover.png')

    # Toolbutton active
    toolbutton = Assets(20,20)
    toolbutton.rounded_rectancle(color3,18,18,1,1,3)
    toolbutton.save('toolbutton-active.png')

def progressbar(color1, color2, state=''):
    bar = Assets(10,10)
    bar.rounded_rectancle(color1,10,10,0,0,3)
    bar.save('progressbar-bar' + state + '.png')

    trough = Assets(10,10)
    trough.rounded_rectancle(color2,10,10,0,0,3)
    trough.save('progressbar-trough' + state + '.png')



def html(color):
    return '#%02x%02x%02x' % (color[0]*255,color[1]*255,color[2]*255)

def mix(color, mix_color, amount):
    r = color[0] * amount + mix_color[0] * (1 - amount)
    g = color[1] * amount + mix_color[1] * (1 - amount)
    b = color[2] * amount + mix_color[2] * (1 - amount)
    return (r,g,b)
#___________________________________________________________________________________

if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    filename = 'schemes/Breeze.colors'

make_sure_path_exists('assets')

_colors = ReadKdeGlobals().read_globals(filename)

border_color    = Color(_colors,'WindowBackgroundNormal','WindowForegroundNormal', 0.75)
window_bg       = Color(_colors,'WindowBackgroundNormal')
window_fg       = Color(_colors,'WindowForegroundNormal')
check_color     = Color(_colors,'WindowBackgroundNormal','WindowForegroundNormal',0.5)
button_bg       = Color(_colors,'ButtonBackgroundNormal')
button_fg       = Color(_colors,'ButtonForegroundNormal')
button_hover    = Color(_colors,'ButtonDecorationHover')
button_active   = Color(_colors,'ButtonDecorationFocus')
selection_bg    = Color(_colors,'SelectionBackgroundNormal')
selection_fg    = Color(_colors,'SelectionForegroundNormal')
view_bg         = Color(_colors,'ViewBackgroundNormal')
view_fg         = Color(_colors,'ViewForegroundNormal')
view_hover      = Color(_colors,'ViewDecorationHover')
view_active     = Color(_colors,'ViewDecorationFocus')
titlebutton     = Color(_colors,'WMactiveForeground')
titlebutton_active = Color(_colors,'WMactiveBackground','WMactiveForeground',0.3)
closebutton_hover = Color(_colors,'ViewForegroundNegative');closebutton_hover.lighten_color(0.5)
closebutton_active = Color(_colors,'ViewForegroundNegative')
titlebutton_inactive = Color(_colors,'WMinactiveForeground')
titlebutton_inactive_active = Color(_colors,'WMinactiveBackground','WMinactiveForeground',0.3)

tooltip_fg = Color(_colors,'TooltipForegroundNormal')
tooltip_bg = Color(_colors,'TooltipBackgroundNormal')

check_items(check_color.rgb,window_bg.rgb,'')
check_items(button_hover.rgb,window_bg.rgb,'-hover')
check_items(button_active.rgb,window_bg.rgb,'-active')
check_items(check_color.insensitive,window_bg.rgb,'-insensitive',border_color.insensitive_alpha)
check_items(check_color.inactive,window_bg.rgb,'-backdrop',border_color.inactive_alpha)
check_items(check_color.inactive_insensitive,window_bg.rgb,'-backdrop-insensitive',border_color.inactive_insensitive_alpha)

buttons(window_bg.rgb,border_color.rgb,button_bg.gradient(),'')
buttons(window_bg.rgb,button_hover.rgb,button_bg.gradient(),'-hover')
buttons(window_bg.rgb,button_hover.rgb,button_hover.gradient('active'),'-active')
buttons(window_bg.rgb,border_color.rgb,button_bg.gradient(alpha=button_bg.insensitive_alpha),'-insensitive',border_color.insensitive_alpha)

togglebuttons(window_bg.rgb,border_color.rgb,button_bg.gradient(),'')
togglebuttons(window_bg.rgb,button_hover.rgb,button_bg.gradient(),'-hover')
togglebuttons(window_bg.rgb,button_hover.rgb,button_hover.gradient('active'),'-active')
togglebuttons(window_bg.rgb,border_color.rgb,button_bg.gradient(alpha=button_bg.insensitive_alpha),'-insensitive',border_color.insensitive_alpha)

scale_slider(window_bg.rgb,border_color.rgb,button_bg.gradient(),'')
scale_slider(window_bg.rgb,button_hover.rgb,button_bg.gradient(),'-hover')
scale_slider(window_bg.rgb,button_active.rgb,button_bg.gradient(),'-active')
scale_slider(window_bg.rgb,border_color.rgb,button_bg.gradient(alpha=button_bg.insensitive_alpha),'-insensitive',border_color.insensitive_alpha)
scale_trough(border_color.rgb)

tabs(border_color.rgb,window_bg.rgb,'-active')
tabs(window_fg.rgb,window_bg.rgb,'-inactive')

arrows(button_fg.rgb,'')
arrows(button_hover.rgb,'-hover')
arrows(button_active.rgb,'-active')
arrows(button_fg.insensitive,'-insensitive',button_fg.insensitive_alpha)
menu_arrow(window_fg.rgb,'')
menu_arrow(selection_fg.rgb,'-selected')
menu_arrow(window_fg.insensitive,'-insensitive',window_fg.insensitive_alpha)

scrollbar_slider(window_fg.rgb,'',alpha=0.5)
scrollbar_slider(button_hover.rgb,'-hover')
scrollbar_slider(button_active.rgb,'-active')

scrollbar_trough(window_fg.rgb)

titlebuttons(titlebutton.rgb,titlebutton.rgb,'')
titlebuttons(titlebutton.rgb,closebutton_hover.rgb,'-hover')
titlebuttons(titlebutton_active.rgb,closebutton_active.rgb,'-active')
titlebuttons(titlebutton_inactive.rgb,titlebutton_inactive.rgb,'-backdrop')
titlebuttons(titlebutton_inactive.rgb,closebutton_hover.rgb,'-hover-backdrop')
titlebuttons(titlebutton_inactive_active.rgb,closebutton_active.rgb,'-active-backdrop')

entry(window_bg.rgb,border_color.rgb,view_bg.rgb,'')
entry(window_bg.rgb,view_active.rgb,view_bg.rgb,'-active')
entry(window_bg.rgb,border_color.insensitive,None,'-insensitive',border_color.insensitive_alpha)

progressbar(selection_bg.rgb,mix(window_fg.rgb,window_bg.rgb,0.3))

mixed(border_color.rgb,window_bg.rgb,button_active.rgb)

toolbar(border_color.rgb,window_bg.rgb,button_hover.rgb)

gtk2 = open('gtk2/gtkrc', 'w')
gtk2.write(
'# Theme:       Breeze-gtk\n'
'# Description: Breeze theme for GTK+2.0\n'
'\n'
'gtk-color-scheme = "text_color:' + html(window_fg.rgb) + '"\n'
'gtk-color-scheme = "base_color:'+ html(view_bg.rgb) + '"\n'
'gtk-color-scheme = "insensitive_base_color:'+ html(view_bg.insensitive) + '"\n'
'gtk-color-scheme = "fg_color:'+ html(window_fg.rgb) + '"\n'
'gtk-color-scheme = "bg_color:' + html(window_bg.rgb) + '"\n'
'gtk-color-scheme = "selected_fg_color:' + html(selection_fg.rgb) + '"\n'
'gtk-color-scheme = "selected_bg_color:' + html(selection_bg.rgb) + '"\n'
'gtk-color-scheme = "button_fg_color:' + html(button_fg.rgb) + '"\n'
'gtk-color-scheme = "tooltip_fg_color:' + html(tooltip_fg.rgb) + '"\n'
'gtk-color-scheme = "tooltip_bg_color:' + html(tooltip_bg.rgb) + '"\n'
'gtk-color-scheme = "insensitive_fg_color:' + html(mix(window_fg.insensitive,window_bg.rgb,window_fg.insensitive_alpha)) + '"\n'
'gtk-color-scheme = "insensitive_text_color:' + html(mix(view_fg.insensitive,view_bg.rgb,view_fg.insensitive_alpha)) + '"\n'
'gtk-color-scheme = "button_insensitive_fg_color:' + html(mix(button_fg.insensitive,button_bg.rgb,button_fg.insensitive_alpha)) + '"\n'
'gtk-color-scheme = "button_active:' + html(button_active.rgb) + '"\n'
'gtk-color-scheme = "border_color:' + html(border_color.rgb) + '"\n'
'\n'
'include "widgets/default"\n'
'include "widgets/buttons"\n'
'include "widgets/menu"\n'
'include "widgets/entry"\n'
'include "widgets/notebook"\n'
'include "widgets/range"\n'
'include "widgets/scrollbar"\n'
'include "widgets/toolbar"\n'
'include "widgets/progressbar"\n'
'include "widgets/misc"\n'
'include "widgets/styles"\n'
)
gtk2.close()

gtk3 = open('_global.scss', 'w')
for key in _colors:
    if key == 'DisabledColor' or key == 'InactiveColor':
        gtk3.write('${0}:rgb({1});\n'.format(key,_colors[key]))
    elif 'Disabled' in key or 'Inactive' in key:
        gtk3.write('${0}:{1};\n'.format(key,_colors[key]))
    else:
        gtk3.write('${0}:rgb({1});\n'.format(key,_colors[key]))
gtk3.close()
