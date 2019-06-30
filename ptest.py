from PIL import Image
image = Image.new('RGB', (240, 135))
image.save('thumbnail_does_not_exist.png')