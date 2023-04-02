from PIL import Image
from moviepy.editor import VideoFileClip

def snapshots(video_files, thumbnail_cache_dir):
    for a in video_files:
        try:
            video = VideoFileClip(a)
            interval = video.duration * 0.81
            video.save_frame(f"{thumbnail_cache_dir}/{a.split('.')[-2].split('/')[-1]}.png", t=interval)
        except Exception as e:
            print(e, f' failed to load video: {a}')
            continue

def thumbnail(img, output_dir):

    images = []
    for image in img:
        images.append(Image.open(image))
    
    total_width = 1688
    total_height = 950
    new_image = Image.new('RGB', (total_width, total_height))
    x_offset = 0
    sub_x = int(total_width/3)
    sub_y = total_height

    for image in images:
        x_image,y_image = image.size
        center_x = x_image/2.0
        center_y = y_image/2.0
        left = int(center_x - sub_x/2.0)
        top = int(center_y - sub_y/2.0)
        right = int(center_x + sub_x/2.0)
        bottom = int(center_y + sub_y/2.0)
        im1 = image.crop((left, top, right, bottom))
        newsize = (sub_x, sub_y)
        im1 = im1.resize(newsize)
        new_image.paste(im1, (x_offset,0))
        x_offset += sub_x

    whole_image = Image.new('RGB', (total_width, total_height))
    whole_image.paste(new_image)
    whole_image.save(f'{output_dir}/thumbnail.png')
