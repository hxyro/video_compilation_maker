from moviepy.editor import VideoFileClip

def box_blur(video_path, output_dir):

    box_blur_output_video_path = f'{output_dir}/output_box_blur.mp4'
    try:
        with VideoFileClip(video_path) as video:
            video.write_videofile(box_blur_output_video_path, ffmpeg_params=['-lavfi', '[0:v]scale=ih*16/9:-1,boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,ch)/20:chroma_power=1[bg];[bg][0:v]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16'], threads=8,audio_fps=44100)

    except Exception as e:
        print(e, f'failed to load {video_path}')

    return box_blur_output_video_path
