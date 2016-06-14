import cairo
import colorsys
from math import pi
import os
import errno
import sys
import argparse

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

        self.rgb = (r/255,g/255,b/255)
        self.dis = self._color_effect(self._intensity_effect(self.rgb,'Disabled'),'Disabled')
        self.dis_alpha = self._contrast_effect(self.rgb,'Disabled')

        if self.colordict['InactiveEnable'] == 'false':
            self.bd = self.rgb
            self.bd_alpha = 1.0
        else:
            self.bd = self._color_effect(self._intensity_effect(self.rgb,'Inactive'),'Inactive')
            self.bd_alpha = self._contrast_effect(self.rgb,'Inactive')
        self.bd_dis = self._color_effect(self._intensity_effect(self.bd,'Disabled'),'Disabled')
        self.bd_dis_alpha = max(self.bd_alpha - (1 - self.dis_alpha),0)

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


    def gradient(self,state='',alpha=1.0, stop=None):
        if state == 'active':
            stop1 = self._lighter(self.rgb,0.03)
            stop2 = self._darker(self.rgb,0.10)
        elif state == 'backdrop':
            stop1 = self._lighter(self.bd, 0.01)
            stop2 = self._darker(self.bd, 0.03)
        elif state == 'active-backdrop':
            stop1 = self._lighter(self.bd, 0.03)
            stop2 = self._darker(self.bd, 0.10)
        elif state == 'dis':
            stop1 = self._lighter(self.dis, 0.01)
            stop2 = self._darker(self.dis, 0.03)
        elif state == 'dis-active':
            stop1 = self._lighter(self.dis, 0.03)
            stop2 = self._darker(self.dis, 0.10)
        elif state == 'backdrop-dis-active':
            stop1 = self._lighter(self.bd_dis, 0.03)
            stop2 = self._darker(self.bd_dis, 0.10)
        elif state == 'backdrop-dis':
            stop1 = self._lighter(self.bd_dis, 0.01)
            stop2 = self._darker(self.bd_dis, 0.03)
        elif state == 'titlebar':
            stop1 = self._lighter(self.rgb, 0.2)
        else:
            stop1 = self._lighter(self.rgb,0.01)
            stop2 = self._darker(self.rgb,0.03)

        if stop == 'a':
            return stop1
        elif stop == 'b':
            return stop2
        else:
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
        self.surface.write_to_png(assetsdir + filename)


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

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def read_globals(filename):
    try:
        _colors={}
        with open(filename, 'r') as _kde_globals:
            for widget in ['Disabled', 'Inactive','Button', 'Selection', 'Tooltip', 'View', 'Window', 'WM']:
                for line in _kde_globals:
                    if line.strip().split(':')[-1].strip('[]') == widget:
                        break
                for line in _kde_globals:
                    if line == '\n':
                        break
                    _colors['{0}{1}'.format(widget,line.strip().split('=')[0])] = line.strip().split('=')[1]
        return _colors
    except:
        print 'Invalid or incomplete color scheme'
        sys.exit()

def mix(color, mix_color, amount):
    r = color[0] * amount + mix_color[0] * (1 - amount)
    g = color[1] * amount + mix_color[1] * (1 - amount)
    b = color[2] * amount + mix_color[2] * (1 - amount)
    return (r,g,b)

def add_color(gtk_version,name, color, alpha=1.0):
    if gtk_version == 2:
            gtkrc.write('gtk-color-scheme = "{0}:#{1:02x}{2:02x}{3:02x}"\n'.format(name, int(color[0]*255),int(color[1]*255),int(color[2]*255)))
    elif gtk_version == 3:
        if alpha == 1.0:
            gtkrc.write('@define-color {0} rgb({1},{2},{3});\n'.format(name, int(color[0]*255),int(color[1]*255),int(color[2]*255)))
        else:
            gtkrc.write('@define-color {0} rgba({1},{2},{3},{4});\n'.format(name, int(color[0]*255),int(color[1]*255),int(color[2]*255), alpha))
#___________________________________________________________________________________

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="path to colorfile")
parser.add_argument("-o", "--outputdir", help="path to outputdir")
parser.add_argument("-f", "--force", help="create assets even if theme is not installed", action="store_true")
args = parser.parse_args()

color_file = os.path.join(os.path.expanduser('~'),".config/kdeglobals")
themedir = os.path.join(os.path.expanduser('~'),".themes/")

if args.input:
    if os.path.exists(args.input):
        color_file = args.input
    else:
        print "couldn't find {0}".format(args.input)
        sys.exit()

if args.outputdir:
    if os.path.exists(args.outputdir):
        themedir = args.outputdir

assetsdir = os.path.join(themedir, 'Breeze/assets/')
gtk2dir = os.path.join(themedir, 'Breeze/gtk-2.0/')
gtk3dir = os.path.join(themedir, 'Breeze/gtk-3.0/')

make_sure_path_exists(assetsdir)
make_sure_path_exists(gtk2dir)
make_sure_path_exists(gtk3dir)

if not args.force:
    if os.path.exists('/usr/share/themes/Breeze'):
        if not os.path.exists(os.path.join(gtk2dir,'widgets')):
            os.symlink('/usr/share/themes/Breeze/gtk-2.0/widgets', os.path.join(gtk2dir,'widgets'))
        if not os.path.exists(os.path.join(gtk3dir,'gtk-main.css')):
            os.symlink('/usr/share/themes/Breeze/gtk-3.0/gtk-main.css', os.path.join(gtk3dir,'gtk-main.css'))
    else:
        print 'Breeze-gtk is not installed'
        sys.exit()

kde_globals = read_globals(color_file)

border_color            = Color(kde_globals,'WindowBackgroundNormal','WindowForegroundNormal', 0.75)
check_color             = Color(kde_globals,'WindowBackgroundNormal','WindowForegroundNormal',0.5)

window_bg               = Color(kde_globals,'WindowBackgroundNormal')
window_fg               = Color(kde_globals,'WindowForegroundNormal')


button_bg               = Color(kde_globals,'ButtonBackgroundNormal')
button_fg               = Color(kde_globals,'ButtonForegroundNormal')
button_hover            = Color(kde_globals,'ButtonDecorationHover')
button_active           = Color(kde_globals,'ButtonDecorationFocus')

selection_bg            = Color(kde_globals,'SelectionBackgroundNormal')
selection_fg            = Color(kde_globals,'SelectionForegroundNormal')
selection_hover         = Color(kde_globals,'SelectionDecorationHover')

view_bg                 = Color(kde_globals,'ViewBackgroundNormal')
view_fg                 = Color(kde_globals,'ViewForegroundNormal')
view_hover              = Color(kde_globals,'ViewDecorationHover')
view_active             = Color(kde_globals,'ViewDecorationFocus')

titlebar_bg             = Color(kde_globals,'WMactiveBackground')
titlebar_fg             = Color(kde_globals,'WMactiveForeground')
titlebar_bd_bg          = Color(kde_globals,'WMinactiveBackground')
titlebar_bd_fg          = Color(kde_globals,'WMinactiveForeground')
titlebutton             = Color(kde_globals,'WMactiveForeground')
titlebutton_active      = Color(kde_globals,'WMactiveBackground','WMactiveForeground',0.3)
closebutton_hover       = Color(kde_globals,'ViewForegroundNegative');closebutton_hover.lighten_color(0.5)
closebutton_active      = Color(kde_globals,'ViewForegroundNegative')
titlebutton_bd          = Color(kde_globals,'WMinactiveForeground')
titlebutton_bd_active   = Color(kde_globals,'WMinactiveBackground','WMinactiveForeground',0.3)

link_color              = Color(kde_globals,'ViewForegroundLink')
link_visited            = Color(kde_globals,'ViewForegroundVisited')
warning                 = Color(kde_globals,'ViewForegroundNeutral')
error                   = Color(kde_globals,'ViewForegroundNegative')
success                 = Color(kde_globals,'ViewForegroundPositive')
trough                  = Color(kde_globals,'WindowForegroundNormal','WindowBackgroundNormal',0.3)
scrollbar               = mix(trough.rgb,view_fg.rgb,0.5)

tooltip_fg              = Color(kde_globals,'TooltipForegroundNormal')
tooltip_bg              = Color(kde_globals,'TooltipBackgroundNormal')

check_items(check_color.rgb,window_bg.rgb,'')
check_items(button_hover.rgb,window_bg.rgb,'-hover')
check_items(button_active.rgb,window_bg.rgb,'-active')
check_items(check_color.dis,window_bg.rgb,'-insensitive',border_color.dis_alpha)
check_items(check_color.bd,window_bg.rgb,'-backdrop',border_color.bd_alpha)
check_items(check_color.bd_dis,window_bg.rgb,'-backdrop-insensitive',border_color.bd_dis_alpha)

buttons(window_bg.rgb,border_color.rgb,button_bg.gradient(),'')
buttons(window_bg.rgb,button_hover.rgb,button_bg.gradient(),'-hover')
buttons(window_bg.rgb,button_hover.rgb,button_hover.gradient('active'),'-active')
buttons(window_bg.rgb,border_color.rgb,button_bg.gradient('dis', alpha=button_bg.dis_alpha),'-insensitive',border_color.dis_alpha)

togglebuttons(window_bg.rgb,border_color.rgb,button_bg.gradient(),'')
togglebuttons(window_bg.rgb,button_hover.rgb,button_bg.gradient(),'-hover')
togglebuttons(window_bg.rgb,button_hover.rgb,button_hover.gradient('active'),'-active')
togglebuttons(window_bg.rgb,border_color.rgb,button_bg.gradient(alpha=button_bg.dis_alpha),'-insensitive',border_color.dis_alpha)

scale_slider(window_bg.rgb,border_color.rgb,button_bg.gradient(),'')
scale_slider(window_bg.rgb,button_hover.rgb,button_bg.gradient(),'-hover')
scale_slider(window_bg.rgb,button_active.rgb,button_bg.gradient(),'-active')
scale_slider(window_bg.rgb,border_color.rgb,button_bg.gradient(alpha=button_bg.dis_alpha),'-insensitive',border_color.dis_alpha)
scale_trough(border_color.rgb)

tabs(border_color.rgb,window_bg.rgb,'-active')
tabs(window_fg.rgb,window_bg.rgb,'-inactive')

arrows(button_fg.rgb,'')
arrows(button_hover.rgb,'-hover')
arrows(button_active.rgb,'-active')
arrows(button_fg.dis,'-insensitive',button_fg.dis_alpha)
menu_arrow(window_fg.rgb,'')
menu_arrow(selection_fg.rgb,'-selected')
menu_arrow(window_fg.dis,'-insensitive',window_fg.dis_alpha)

scrollbar_slider(window_fg.rgb,'',alpha=0.5)
scrollbar_slider(button_hover.rgb,'-hover')
scrollbar_slider(button_active.rgb,'-active')

scrollbar_trough(window_fg.rgb)

titlebuttons(titlebutton.rgb,titlebutton.rgb,'')
titlebuttons(titlebutton.rgb,closebutton_hover.rgb,'-hover')
titlebuttons(titlebutton_active.rgb,closebutton_active.rgb,'-active')
titlebuttons(titlebutton_bd.rgb,titlebutton_bd.rgb,'-backdrop')
titlebuttons(titlebutton_bd.rgb,closebutton_hover.rgb,'-hover-backdrop')
titlebuttons(titlebutton_bd_active.rgb,closebutton_active.rgb,'-active-backdrop')

entry(window_bg.rgb,border_color.rgb,view_bg.rgb,'')
entry(window_bg.rgb,view_active.rgb,view_bg.rgb,'-active')
entry(window_bg.rgb,border_color.dis,None,'-insensitive',border_color.dis_alpha)

progressbar(selection_bg.rgb,mix(window_fg.rgb,window_bg.rgb,0.3))

mixed(border_color.rgb,window_bg.rgb,button_active.rgb)

toolbar(border_color.rgb,window_bg.rgb,button_hover.rgb)

gtkrc = open(gtk2dir + 'gtkrc', 'w').close()
gtkrc = open(gtk2dir + 'gtkrc', 'a')

gtkrc.write(
'# Theme:       Breeze-gtk\n'
'# Description: Breeze theme for GTK+2.0\n'
'\n')

add_color(2, 'text_color', window_fg.rgb)
add_color(2, 'base_color', view_bg.rgb)
add_color(2, 'insensitive_base_color', mix(view_bg.dis, window_bg.rgb, view_bg.dis_alpha))
add_color(2, 'fg_color', window_fg.rgb)
add_color(2, 'bg_color', window_bg.rgb)
add_color(2, 'selected_fg_color', selection_fg.rgb)
add_color(2, 'selected_bg_color', selection_bg.rgb)
add_color(2, 'button_fg_color', button_fg.rgb)
add_color(2, 'tooltip_fg_color', tooltip_fg.rgb)
add_color(2, 'tooltip_bg_color', tooltip_bg.rgb)
add_color(2, 'insensitive_fg_color', mix(window_fg.dis, window_bg.rgb, window_fg.dis_alpha))
add_color(2, 'insensitive_text_color', mix(view_fg.dis, view_bg.rgb, view_fg.dis_alpha))
add_color(2, 'button_insensitive_fg_color', mix(button_fg.dis, button_bg.rgb, button_fg.dis_alpha))
add_color(2, 'button_active', button_active.rgb)
add_color(2, 'border_color', border_color.rgb)

gtkrc.write(
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
gtkrc.close()

gtkrc = open(gtk3dir + 'gtk.css', 'w').close()
gtkrc = open(gtk3dir + 'gtk.css', 'a')

gtkrc.write('\n/* Button Colors */\n')

add_color(3, 'button_bg_a', button_bg.gradient(stop='a'))
add_color(3, 'button_bg_b', button_bg.gradient(stop='b'))
add_color(3, 'button_bg_color', button_bg.rgb)
add_color(3, 'button_dis_bg_color', button_bg.dis, button_bg.dis_alpha)
add_color(3, 'button_bd_bg_color', button_bg.bd, button_bg.bd_alpha)
add_color(3, 'button_fg', button_fg.rgb)
add_color(3, 'button_hover', button_hover.rgb)
add_color(3, 'button_active', button_active.rgb)
add_color(3, 'button_bd_active', button_active.rgb)
add_color(3, 'button_active_bg_a', button_active.gradient(state='active',stop='a'))
add_color(3, 'button_active_bg_b', button_active.gradient(state='active', stop='b'))
add_color(3, 'button_active_hover_a',button_hover.gradient(state='active', stop='a'))
add_color(3, 'button_active_hover_b',button_hover.gradient(state='active', stop='b'))
add_color(3, 'button_dis_active_bg_a', button_active.gradient(state='dis-active',stop='a'), button_active.dis_alpha)
add_color(3, 'button_dis_active_bg_b', button_active.gradient(state='dis-active', stop='b'), button_active.dis_alpha)
add_color(3, 'button_dis_fg', button_fg.dis, button_fg.dis_alpha)
add_color(3, 'button_dis_bg_a', button_bg.gradient(state='dis', stop='a'), button_bg.dis_alpha)
add_color(3, 'button_dis_bg_b', button_bg.gradient(state='dis', stop='b'), button_bg.dis_alpha)
add_color(3, 'button_bd_bg_a', button_bg.gradient(state='backdrop', stop='a'), button_bg.bd_alpha)
add_color(3, 'button_bd_bg_b', button_bg.gradient(state='backdrop', stop='b'), button_bg.bd_alpha)
add_color(3, 'button_bd_active_bg_a', button_active.gradient(state='active-backdrop', stop='a'), button_active.bd_alpha)
add_color(3, 'button_bd_active_bg_b', button_active.gradient(state='active-backdrop', stop='b'), button_active.bd_alpha)
add_color(3, 'button_bd_fg', button_fg.bd, button_fg.bd_alpha)
add_color(3, 'button_bd_dis_fg', button_fg.bd_dis, button_fg.bd_dis_alpha)
add_color(3, 'button_bd_dis_bg_a', button_bg.gradient(state='backdrop-dis', stop='a'), button_bg.bd_dis_alpha)
add_color(3, 'button_bd_dis_bg_b', button_bg.gradient(state='backdrop-dis', stop='b'), button_bg.bd_dis_alpha)
add_color(3, 'button_bd_dis_active_bg_a', button_active.gradient(state='backdrop-dis-active', stop='a'), button_active.bd_dis_alpha)
add_color(3, 'button_bd_dis_active_bg_b', button_active.gradient(state='backdrop-dis-active', stop='b'), button_active.bd_dis_alpha)

gtkrc.write('\n/* Selection Colors */\n')

add_color(3, 'selection_bg', selection_bg.rgb)
add_color(3, 'selection_fg', selection_fg.rgb)
add_color(3, 'selection_hover', selection_hover.rgb)
if kde_globals['InactiveChangeSelectionColor'] == 'true':
    add_color(3, 'selection_bd_bg', selection_bg.bd, max(selection_bg.bd_alpha - 0.5,0))
else:
    add_color(3, 'selection_bd_bg', selection_bg.bd, selection_bg.bd_alpha)
add_color(3, 'selection_bd_fg', selection_fg.bd, selection_fg.bd_alpha)
add_color(3, 'selection_dis_fg', selection_fg.dis, selection_fg.dis_alpha)
add_color(3, 'selection_dis_bg', selection_bg.dis, selection_bg.dis_alpha)
add_color(3, 'selection_bd_dis_fg', selection_fg.bd_dis, selection_fg.bd_dis_alpha)
add_color(3, 'selection_bd_dis_bg', selection_bg.bd_dis, selection_bg.bd_dis_alpha)

gtkrc.write('\n/* View Colors */\n')

add_color(3, 'view_bg', view_bg.rgb)
add_color(3, 'view_fg', view_fg.rgb)
add_color(3, 'view_hover', view_hover.rgb)
add_color(3, 'view_active', view_active.rgb)
add_color(3, 'view_dis_bg', view_bg.dis, view_bg.dis_alpha)
add_color(3, 'view_dis_fg', view_fg.dis, view_fg.dis_alpha)
add_color(3, 'view_bd_bg', view_bg.bd, view_bg.bd_alpha)
add_color(3, 'view_bd_fg', view_fg.bd, view_fg.bd_alpha)
add_color(3, 'view_bd_dis_bg', view_bg.bd_dis, view_bg.bd_dis_alpha)
add_color(3, 'view_bd_dis_fg', view_fg.bd_dis, view_fg.bd_dis_alpha)

gtkrc.write('\n/* Window Colors */\n')

add_color(3, 'window_bg', window_bg.rgb)
add_color(3, 'window_fg', window_fg.rgb)
add_color(3, 'window_dis_bg', window_bg.dis, window_bg.dis_alpha)
add_color(3, 'window_dis_fg', window_fg.dis, window_fg.dis_alpha)
add_color(3, 'window_bd_bg', window_bg.bd, window_bg.bd_alpha)
add_color(3, 'window_bd_fg', window_fg.bd, window_fg.bd_alpha)
add_color(3, 'window_bd_dis_bg', window_bg.bd_dis, window_bg.bd_dis_alpha)
add_color(3, 'window_bd_dis_fg', window_fg.bd_dis, window_fg.bd_dis_alpha)

gtkrc.write('\n/* Titlebar Colors */\n')

add_color(3, 'titlebar_bg_a', titlebar_bg.gradient(state='titlebar', stop='a'))
add_color(3, 'titlebar_bg_b', titlebar_bg.rgb)
add_color(3, 'titlebar_fg', titlebar_fg.rgb)
add_color(3, 'titlebar_bd_bg', titlebar_bd_bg.rgb)
add_color(3, 'titlebar_bd_fg', titlebar_bd_fg.rgb)
add_color(3, 'titlebar_dis_bg', titlebar_bg.dis, titlebar_bg.dis_alpha)
add_color(3, 'titlebar_dis_fg', titlebar_fg.dis, titlebar_fg.dis_alpha)

gtkrc.write('\n/* Tooltip Colors */\n')

add_color(3, 'tooltip_bg', tooltip_bg.rgb)
add_color(3, 'tooltip_fg', tooltip_fg.rgb)

gtkrc.write('\n/* Border Colors */\n')

add_color(3, 'borders', border_color.rgb)
add_color(3, 'borders_dis', border_color.dis, border_color.dis_alpha)
add_color(3, 'borders_bd', border_color.bd, border_color.bd_alpha)
add_color(3, 'borders_bd_dis', border_color.bd_dis, border_color.bd_dis_alpha)

gtkrc.write('\n/* Other Colors */\n')

add_color(3, 'menu_color', window_bg.rgb)
add_color(3, 'menu_bd_color', window_bg.bd, window_bg.bd_alpha)
add_color(3, 'link_color', link_color.rgb)
add_color(3, 'link_visited', link_visited.rgb)
add_color(3, 'warning_color', warning.rgb)
add_color(3, 'warning_bd_color', warning.bd, warning.bd_alpha)
add_color(3, 'error_color', error.rgb)
add_color(3, 'error_bd_color', error.bd, error.bd_alpha)
add_color(3, 'success_color', success.rgb)
add_color(3, 'success_bd_color', success.bd, success.bd_alpha)
add_color(3, 'trough_color', trough.rgb)
add_color(3, 'trough_dis_color', trough.dis, trough.dis_alpha)
add_color(3, 'trough_bd_color', trough.bd, trough.bd_alpha)
add_color(3, 'trough_bd_dis_color', trough.bd_dis, trough.bd_dis_alpha)
add_color(3, 'scrollbar_color', scrollbar)

gtkrc.write('\n@import url("gtk-main.css");')

gtkrc.close()
