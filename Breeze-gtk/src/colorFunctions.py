import grapefruit as gft

def htmlColor(color):
    return gft.Color.NewFromRgb(float(color.split(',')[0])/255,float(color.split(',')[1])/255,float(color.split(',')[2])/255).html

def buttongradient(color, state=''):
    r,g,b = gft.Color.HtmlToRgb(color)
    if state == '-active':
        h,s,l = gft.Color.RgbToHsl(r,g,b)
        stop1 = gft.Color.NewFromHsl(h, s, l).ColorWithLightness(1.03*l).html
        stop2 = gft.Color.NewFromHsl(h, s, l).ColorWithLightness(l/1.10).html
    else:
        h,s,l = gft.Color.RgbToHsl(r,g,b)
        stop1 = gft.Color.NewFromHsl(h, s, l).ColorWithLightness(1.01*l).html
        stop2 = gft.Color.NewFromHsl(h, s, l).ColorWithLightness(l/1.03).html
    return (stop1, stop2)

def mixColor(color1,color2,amount):
    r1,g1,b1 = gft.Color.HtmlToRgb(color1)
    r2,g2,b2 = gft.Color.HtmlToRgb(color2)
    color1 = gft.Color.NewFromRgb(r1,g1,b1)
    color2 = gft.Color.NewFromRgb(r2,g2,b2)
    return color1.Blend(color2, amount).html

def closeHover(color):
    r,g,b = gft.Color.HtmlToRgb(color)
    h,s,l = gft.Color.RgbToHsl(r,g,b)
    return gft.Color.NewFromHsl(h, s, l).ColorWithLightness(l*1.5).html

def readColors(input_file, output_file):
    Colors = {}
    with open(input_file, 'r') as colors:
        for widget in ['Button', 'Selection', 'Tooltip', 'View', 'Window', 'WM']:
            for line in colors:
                if line.strip().split(':')[-1].strip('[]') == widget:
                    break
            for line in colors:
                if line == '\n':
                    break
                color = line.strip().split('=')[0]
                if color == 'activeFont':
                    continue
                value = htmlColor(line.strip().split('=')[1])
                Colors['{0}_{1}'.format(widget,color)] = value
                with open(output_file, 'a') as gtk3:
                    gtk3.write('${0}_{1}:{2};\n'.format(widget,color,value))
    return Colors

def readColorEffects(input_file, output_file):
    ColorEffects = {}
    with open(input_file, 'r') as colors:
        for state in ['Disabled', 'Inactive']:
            for line in colors:
                if line.strip().split(':')[-1].strip('[]') == state:
                    break
            for line in colors:
                if line == '\n':
                    break
                effect = line.strip().split('=')[0]
                value = line.strip().split('=')[1]
                if effect == 'Color':
                    value = htmlColor(value)
                ColorEffects['{0}_{1}'.format(state,effect)] = value
                with open(output_file, 'a') as gtk3:
                    gtk3.write('${0}_{1}:{2};\n'.format(state,effect,value))
    return ColorEffects

def colorEffect(color,effect_color, effect, amount):
    r,g,b = gft.Color.HtmlToRgb(color)
    h,s,l = gft.Color.RgbToHsl(r,g,b)
    if effect == 1:
        if amount >= 0:
            return gft.Color.NewFromHsl(h, s, l).Desaturate(amount).html
        else:
            return gft.Color.NewFromHsl(h, s, l).Saturate(abs(amount)).html
    elif effect == 2 or effect == 3: # don't really know what they do, tinting should be mixing with white
        return mixColor(effect_color,color, amount)
    else:
        return color

def intensityEffect(color, effect, amount):
    r,g,b = gft.Color.HtmlToRgb(color)
    h,s,l = gft.Color.RgbToHsl(r,g,b)
    if effect == 1:
        if amount >= 0:
            return mixColor('white',color,amount)
        else:
            return mixColor('black',color,amount)
    elif effect == 2:
        if amount >= 0:
            return gft.Color.NewFromHsl(h, s, l).DarkerColor(amount).html
        else:
            return gft.Color.NewFromHsl(h, s, l).ColorWithLightness(l*(1+abs(amount))).html
    elif effect == 3:
        if amount >= 0:
            return gft.Color.NewFromHsl(h, s, l).LighterColor(amount).html
        else:
            return gft.Color.NewFromHsl(h, s, l).ColorWithLightness(l/(1+abs(amount))).html
    else:
        return color

def contrastEffect(bg_color, fg_color, color, effect, amount):
    r1,g1,b1 = gft.Color.HtmlToRgb(bg_color)
    h1,s1,l1 = gft.Color.RgbToHsl(r1,g1,b1)
    r2,g2,b2 = gft.Color.HtmlToRgb(fg_color)
    h2,s2,l2 = gft.Color.RgbToHsl(r2,g2,b2)
    r3,g3,b3 = gft.Color.HtmlToRgb(color)
    h3,s3,l3 = gft.Color.RgbToHsl(r3,g3,b3)
    if effect == 1 or effect == 2:  # can't see any difference
        if l1 > l2 and l1 > l3:
            return 1-amount
        elif l1 < l2 and l1 < l3:
            return 1-amount
        else:
            return 1
