import Image
import ImageDraw
im = Image.open("test2.jpg")
transparent_area = (50,50,100,100)

mask=Image.new('L', im.size, color=255)
draw=ImageDraw.Draw(mask)
draw.rectangle(transparent_area, fill=0)
im.putalpha(mask)
im.save('/tmp/output.png')

draw.text()