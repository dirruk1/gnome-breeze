from assets import assets
import colorFunctions as cF
import sys

if len(sys.argv) == 2:
    Filename = sys.argv[1]
else:
    Filename = 'Breeze.colors'
#-------------------------------------------------------------------------------
# color schemes
#-------------------------------------------------------------------------------
gtk3_file = 'src/gtk3/_global.scss'
gtk3 = open(gtk3_file, 'w').close()
Colors = cF.readColors(Filename,gtk3_file)
ColorEffects = cF.readColorEffects(Filename,gtk3_file)

border_color = cF.mixColor(Colors['Window_BackgroundNormal'],Colors['Window_ForegroundNormal'], 0.75)
check_border = cF.mixColor(Colors['Window_BackgroundNormal'], Colors['Window_ForegroundNormal'], 0.5)
insensitive_check_border = cF.mixColor(Colors['Window_BackgroundNormal'], Colors['Window_ForegroundNormal'], 0.5)
entry_border = cF.mixColor(Colors['Window_BackgroundNormal'],Colors['Window_ForegroundNormal'],0.7)
menu_color = cF.mixColor(Colors['View_BackgroundNormal'],Colors['Window_BackgroundNormal'], 0.7)

# insensitive
def Insensitive(color):
    global ColorEffects

    color = cF.intensityEffect(color, int(ColorEffects['Disabled_IntensityEffect']), float(ColorEffects['Disabled_IntensityAmount']))
    color = cF.colorEffect(color,ColorEffects['Disabled_Color'],int(ColorEffects['Disabled_ColorEffect']),float(ColorEffects['Disabled_ColorAmount']))
    return color

def InsensitiveAlpha(color):
    global Colors
    global ColorEffects

    return cF.contrastEffect(Colors['Window_BackgroundNormal'],Colors['Window_ForegroundNormal'],color,int(ColorEffects['Disabled_ContrastEffect']),float(ColorEffects['Disabled_ContrastAmount']))

# backdrop
def bd(color):
    global ColorEffects

    if ColorEffects['Inactive_Enable'] == 'true':
        color = cF.intensityEffect(color, int(ColorEffects['Inactive_IntensityEffect']), float(ColorEffects['Inactive_IntensityAmount']))
        color = cF.colorEffect(color,ColorEffects['Inactive_Color'],int(ColorEffects['Inactive_ColorEffect']),float(ColorEffects['Inactive_ColorAmount']))
    return color

def bdAlpha(color):
    global Colors
    global ColorEffects

    if ColorEffects['Inactive_Enable'] == 'true':
        return cF.contrastEffect(Colors['Window_BackgroundNormal'],Colors['Window_ForegroundNormal'],color,int(ColorEffects['Inactive_ContrastEffect']),float(ColorEffects['Inactive_ContrastAmount']))
    else:
        return 1

def bdInsensitive(color):
    return bd(Insensitive(color))

def bdInsensitiveAlpha(color):
    return max(0,bdAlpha(color) + InsensitiveAlpha(color) - 2)

gtk2 = open('src/gtk2/gtkrc', 'w')
gtk2.write(
'# Theme:       Breeze-gtk\n'
'# Description: Breeze theme for GTK+2.0\n'
'\n'
'gtk-color-scheme = "text_color:' + Colors['View_ForegroundNormal'] + '"\n'
'gtk-color-scheme = "base_color:'+ Colors['View_BackgroundNormal'] + '"\n'
'gtk-color-scheme = "insensitive_base_color:'+ Insensitive(Colors['View_BackgroundNormal']) + '"\n'
'gtk-color-scheme = "fg_color:'+ Colors['Window_ForegroundNormal'] + '"\n'
'gtk-color-scheme = "bg_color:' + Colors['Window_BackgroundNormal'] + '"\n'
'gtk-color-scheme = "selected_fg_color:' + Colors['Selection_ForegroundNormal'] + '"\n'
'gtk-color-scheme = "selected_bg_color:' + Colors['Selection_BackgroundNormal'] + '"\n'
'gtk-color-scheme = "button_fg_color:' + Colors['Button_ForegroundNormal'] + '"\n'
'gtk-color-scheme = "tooltip_fg_color:' + Colors['Tooltip_ForegroundNormal'] + '"\n'
'gtk-color-scheme = "tooltip_bg_color:' + Colors['Tooltip_BackgroundNormal'] + '"\n'
'gtk-color-scheme = "insensitive_fg_color:' + cF.mixColor(Insensitive(Colors['Window_ForegroundNormal']),Colors['Window_BackgroundNormal'],InsensitiveAlpha(Colors['Window_ForegroundNormal'])) + '"\n'
'gtk-color-scheme = "insensitive_text_color:' + cF.mixColor(Insensitive(Colors['View_ForegroundNormal']),Colors['View_BackgroundNormal'],InsensitiveAlpha(Colors['View_ForegroundNormal'])) + '"\n'
'gtk-color-scheme = "button_insensitive_fg_color:' + cF.mixColor(Insensitive(Colors['Button_ForegroundNormal']),Colors['Button_BackgroundNormal'],InsensitiveAlpha(Colors['Button_ForegroundNormal'])) + '"\n'
'gtk-color-scheme = "border_color:' + border_color + '"\n'
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

#-------------------------------------------------------------------------------
# draw assets
#-------------------------------------------------------------------------------

# arrows
for i,j,k in zip(\
    [Colors['Button_ForegroundNormal'],Colors['Button_ForegroundNormal'],Colors['Button_ForegroundNormal'],Insensitive(Colors['Button_ForegroundNormal'])],\
    ['','-hover','-active','-insensitive'],\
    [1,1,1,InsensitiveAlpha(Colors['Button_ForegroundNormal'])]):
    for l in ['-up','-right','-down','-left']:
        assets('arrow', color=i, state=j, alpha=k, suffix=l, w=12, h=12)
        assets('arrow-small', color=i, state=j, alpha=k, suffix=l, w=8, h=8)

assets('menu-arrow', color=Colors['Window_ForegroundNormal'], w=12, h=12)
assets('menu-arrow', color=Colors['Selection_ForegroundNormal'], w=12, h=12, prefix='selected-')
assets('menu-arrow', color=Insensitive(Colors['Window_ForegroundNormal']),w=12, h=12, state='-insensitive', alpha=InsensitiveAlpha(Colors['Window_ForegroundNormal']))

# buttons
for i,j,k,l in zip(\
    [Colors['Button_BackgroundNormal'],Colors['Button_BackgroundNormal'],Colors['Button_DecorationHover'],Insensitive(Colors['Button_BackgroundNormal'])],\
    [border_color,Colors['Button_DecorationHover'],'none',Insensitive(border_color)],\
    ['','-hover','-active','-insensitive'],\
    [1,1,1,InsensitiveAlpha(border_color)]):
    assets('button', color=i, color2=j, state=k, alpha=l)

# spinbutton
for i,j,k,l in zip(\
    [Colors['View_BackgroundNormal'], Insensitive(Colors['View_BackgroundNormal'])],\
    [entry_border,Insensitive(entry_border)],\
    ['','-insensitive'],\
    [1,InsensitiveAlpha(entry_border)]):
    for m in ['-up','-down']:
        assets('spinbutton', color=i, color2=j, state=k, alpha=l, suffix=m)

# toolbutton
for i,j,k in zip(\
    ['none',Colors['Window_BackgroundNormal'],Colors['Button_DecorationHover'],border_color],\
    ['none',Colors['Button_DecorationHover'],'none','none'],\
    ['','-hover','-active', '-toggled']):
    assets('toolbutton', color=i, color2=j, state=k)

# checkbox
for i,j in zip(\
    [check_border, Colors['Button_DecorationFocus']],\
    ['-unchecked', '-checked']):
    assets('checkbox',suffix=j,color=i)
    assets('radio',suffix=j,color=i)


for i,j,k in zip(\
    ['-hover','-active','-selected','-insensitive'],\
    [Colors['Button_DecorationHover'], Colors['Button_DecorationFocus'], Colors['Selection_ForegroundNormal'], insensitive_check_border],\
    [1,1,1,InsensitiveAlpha(insensitive_check_border)]):
    for l in ['-unchecked', '-checked']:
        assets('checkbox',suffix=l,state=i,color=j,alpha=k)
        assets('radio',suffix=l,state=i,color=j,alpha=k)

# entry
for i,j,k,l in zip(\
    [Colors['View_BackgroundNormal'],Colors['View_BackgroundNormal'],Insensitive(Colors['View_BackgroundNormal'])],
    [entry_border, Colors['View_DecorationFocus'], Insensitive(entry_border)],\
    ['','-active','-insensitive'],\
    [1,1,InsensitiveAlpha(entry_border)]):
    assets('entry', color=Colors['Window_BackgroundNormal'], color2=j, color3=i, state=k, alpha=l)

# notebook
for i,j,k,l in zip(\
    [Colors['Window_ForegroundNormal'],menu_color],\
    ['none', border_color],\
    ['-inactive','-active'],\
    [0.2,1]):
    for m in ['-top','-right','-bottom','-left']:
        assets('tab', color=i, color2=j, state=k, alpha=l, suffix=m)

assets('notebook-gap', color=menu_color, w=4, h=2, suffix='-horizontal')
assets('notebook-gap', color=menu_color, w=2, h=4, suffix='-vertical')
assets('notebook',color=menu_color,color2=border_color)

# progressbar
assets('progressbar',color=cF.mixColor(Colors['Button_ForegroundNormal'],Colors['Window_BackgroundNormal'],0.3),w=10,h=10,suffix='-trough')
assets('progressbar',color=Colors['Selection_BackgroundNormal'],w=10,h=10,suffix='-bar')

# Gtk-Scale
for i,j,k in zip(\
    [Colors['Button_BackgroundNormal'],Colors['Button_BackgroundNormal'],cF.mixColor(Insensitive(Colors['Button_BackgroundNormal']),Colors['Window_BackgroundNormal'],InsensitiveAlpha(Colors['Button_BackgroundNormal']))], \
    [border_color,Colors['Button_DecorationHover'],Insensitive(border_color)],\
    ['','-active','-insensitive']):\
    assets('scale-slider',color=i, color2=j, state=k)

for i in ['-horizontal', '-vertical']:
    assets('scale-trough', color=entry_border, suffix=i)

# scrollbar
for i,j,k in zip(\
    [Colors['View_ForegroundNormal'],Colors['Button_DecorationHover'],Colors['Button_DecorationFocus'],Insensitive(Colors['View_ForegroundNormal'])],\
    ['','-hover','-active','-insensitive'],\
    [0.5,1,1,max(0,0.5 - 1 + InsensitiveAlpha(Colors['View_ForegroundNormal']))]):
    for l,m,n in zip(['-horizontal','-vertical'],[30,10],[10,30]):
        assets('scrollbar-slider', color=i, state=j, w=m, h=n,alpha=k, suffix=l)

for i,j,k in zip(['-horizontal', '-vertical'],[56,20],[20,56]):
    assets('scrollbar-trough', color=Colors['Window_ForegroundNormal'], w=j, h=k, alpha=0.3, suffix=i)

# expanders
assets('plus', color=Colors['View_ForegroundNormal'], w=12, h=12)
assets('minus', color=Colors['View_ForegroundNormal'], w=12, h=12)

# handles
assets('handle', color=Colors['Window_BackgroundNormal'], w=20, h=2, suffix='-h')
assets('handle', color=Colors['Window_BackgroundNormal'], w=2, h=20, suffix='-v')

# lines
assets('line', color=border_color, w=8, h=2, suffix='-h')
assets('line', color=border_color, w=2, h=8, suffix='-v')
assets('line', color=border_color, w=8, h=1, prefix='menu-')

# others
assets('null')
assets('menubar-button', color=Colors['Selection_BackgroundNormal'])
assets('tree-header', color=Colors['Button_BackgroundNormal'], color2=border_color)
assets('frame', color=menu_color, color2=border_color, prefix='menu-')
assets('frame', color=Colors['Window_BackgroundNormal'], color2=border_color)
assets('frame-gap',color=border_color, w=2, h=1, suffix='-start')
assets('frame-gap',color=border_color, w=2, h=1, suffix='-end')
assets('toolbar-background', color=Colors['Window_BackgroundNormal'])

#-------------------------------------------------------------------------------
# draw gtk3 assets
#-------------------------------------------------------------------------------

# check and radio
for i,j,k in zip(\
    [check_border, Colors['Button_DecorationFocus'], Colors['Button_DecorationFocus'],bd(check_border), bd(Colors['Button_DecorationFocus']), bd(Colors['Button_DecorationFocus'])],\
    ['-unchecked', '-checked', '-mixed','-unchecked-backdrop', '-checked-backdrop', '-mixed-backdrop'],\
    [1,1,1,bdAlpha(check_border), bdAlpha(Colors['Button_DecorationFocus']), bdAlpha(border_color)]):
    assets('checkbox',suffix=j, color=i, alpha=k, gtk_version='gtk3')
    assets('radio',suffix=j, color=i, alpha=k, gtk_version='gtk3')

for i,j,k in zip(\
    ['-hover','-active','-insensitive','-backdrop','-backdrop-insensitive'],\
    [Colors['Button_DecorationHover'], Colors['Button_DecorationFocus'], insensitive_check_border,bd(check_border),bd(insensitive_check_border)],\
    [1,1,InsensitiveAlpha(insensitive_check_border),bdAlpha(check_border),bdInsensitiveAlpha(insensitive_check_border)]):
    for l in ['-unchecked', '-checked', '-mixed']:
        assets('checkbox',suffix=l,state=i,color=j,alpha=k, gtk_version='gtk3')
        assets('radio',suffix=l,state=i,color=j,alpha=k, gtk_version='gtk3')

for i in ['-unchecked', '-checked', '-mixed']:
    assets('checkbox',suffix=i,prefix='selected-',color=Colors['Selection_ForegroundNormal'], gtk_version='gtk3')
    assets('radio',suffix=i,prefix='selected-',color=Colors['Selection_ForegroundNormal'], gtk_version='gtk3')

for i,j in zip(\
    [check_border, Colors['Button_DecorationFocus']],\
    ['-unchecked', '-checked']):
    assets('checkbox-selectionmode', color2=Colors['Window_BackgroundNormal'], color=i, w=40,h=40, suffix=j, gtk_version='gtk3')

for i,j,k in zip(\
    [Colors['Button_DecorationHover'], Colors['Button_DecorationFocus'],bd(check_border)],\
    ['-hover','-active','-backdrop'],\
    [1,1,bdAlpha(check_border)]):
    for l in ['-unchecked','-checked']:
        assets('checkbox-selectionmode', color2=Colors['Window_BackgroundNormal'], color=i, w=40,h=40, state=j, alpha=k, suffix=l, gtk_version='gtk3')

# titlebuttons
for i,j,k in zip(\
    ['','-hover','-active','-backdrop'],\
    [Colors['WM_activeForeground'],cF.closeHover(Colors['View_ForegroundNegative']),Colors['View_ForegroundNegative'],Colors['WM_inactiveForeground']],\
    [Colors['WM_activeBackground'],Colors['WM_activeBackground'],Colors['WM_activeBackground'],Colors['WM_inactiveBackground']]):
    assets('titlebutton', color=j, color2=k, state=i, w=18, h=18, suffix='-close', gtk_version='gtk3')

for i,j,k in zip(\
    ['','-hover','-active','-backdrop'],\
    [Colors['WM_activeBackground'],Colors['WM_activeForeground'],cF.mixColor(Colors['WM_activeBackground'],Colors['WM_activeForeground'], 0.3),Colors['WM_inactiveBackground']],\
    [Colors['WM_activeForeground'],Colors['WM_activeBackground'],Colors['WM_activeBackground'],Colors['WM_inactiveForeground']]):
    assets('titlebutton', color=j, color2=k, state=i, w=18, h=18, suffix='-minimize', gtk_version='gtk3')
    assets('titlebutton', color=j, color2=k, state=i, w=18, h=18, suffix='-maximize', gtk_version='gtk3')
    assets('titlebutton', color=j, color2=k, state=i, w=18, h=18, suffix='-maximize-maximized', gtk_version='gtk3')

# scrollbar
for i,j,k in zip(\
    [Colors['View_ForegroundNormal'],Colors['Button_DecorationHover'],Colors['Button_DecorationFocus'],Insensitive(Colors['View_ForegroundNormal']),bd(Colors['View_ForegroundNormal']),bd(Insensitive(Colors['View_ForegroundNormal']))],\
    ['','-hover','-active','-insensitive','-backdrop','-backdrop-insensitive'],\
    [0.5,1,1,max(0,0.5 - 1 + InsensitiveAlpha(Colors['View_ForegroundNormal'])),max(0,0.5 - 1 + bdAlpha(Colors['View_ForegroundNormal'])),max(0,0.5 - 1 + bdInsensitiveAlpha(Colors['View_ForegroundNormal']))]):
    for l,m,n in zip(['-horizontal','-vertical'],[28,20],[20,28]):
        assets('scrollbar-slider', color=i, w=m, h=n, state=j, alpha=k, suffix=l, gtk_version='gtk3')

for i,j,k in zip(['-horizontal', '-vertical'],[56,20],[20,56]):
    assets('scrollbar-trough', color=Colors['Window_ForegroundNormal'], w=j, h=k, alpha=0.3, suffix=i, gtk_version='gtk3')
    assets('scrollbar-trough', state='-backdrop', color=bd(Colors['Window_ForegroundNormal']), w=j, h=k, alpha=max(0,0.3 - 1 + bdAlpha(Colors['Window_ForegroundNormal'])), suffix=i, gtk_version='gtk3')
