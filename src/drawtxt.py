from PIL import Image, ImageDraw, ImageFont
# get an image
base = Image.open('logo.png').convert('RGBA')

# make a blank image for the text, initialized to transparent text color
txt = Image.new('RGBA', base.size, (255,255,255,0))

# get a font
# fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)
# get a drawing context
d = ImageDraw.Draw(txt)

# draw text, half opacity
d.text((10,10), "Hello", fill=(255,255,255,128))
# draw text, full opacity
d.text((10,60), "World", fill=(255,255,255,255))
w = txt.rotate(25)
out = Image.alpha_composite(base, w)

out.show()
