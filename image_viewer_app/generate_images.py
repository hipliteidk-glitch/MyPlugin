#!/usr/bin/env python3
"""Generate sample images for the image viewer app"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_image(width, height, color1, color2, text, text_color='white'):
    """Create a gradient image with text overlay"""
    img = Image.new('RGB', (width, height), color1)
    draw = ImageDraw.Draw(img)
    
    # Draw gradient
    for i in range(height):
        ratio = i / height
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    # Draw text
    try:
        # Try to use a system font
        font = ImageFont.truetype("/system/fonts/Roboto-Regular.ttf", 60)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 60)
        except:
            font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    draw.text((x, y), text, font=font, fill=text_color)
    
    return img

# Ensure the drawable directory exists
os.makedirs('app/src/main/res/drawable', exist_ok=True)

# Generate images - EDIT THESE TO CHANGE YOUR APP'S IMAGES!
images_data = [
    ((255, 100, 100), (100, 50, 200), "Image 1", 'white'),
    ((100, 200, 100), (50, 100, 255), "Image 2", 'white'),
    ((255, 200, 50), (200, 50, 100), "Image 3", 'white'),
    ((100, 200, 255), (50, 50, 150), "Image 4", 'white'),
    ((255, 100, 200), (200, 50, 50), "Image 5", 'white'),
]

for i, (color1, color2, text, text_color) in enumerate(images_data, 1):
    img = create_image(512, 512, color1, color2, text, text_color)
    img.save(f'app/src/main/res/drawable/image{i}.png')
    print(f"Generated image{i}.png")

print("All images generated!")
print("Now you can:")
print("1. Edit the images_data list above to change colors/text")
print("2. Replace the generated PNGs with your own images")
print("3. Build the APK")
