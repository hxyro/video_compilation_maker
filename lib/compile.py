from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, concatenate_audioclips

def compile(video_files, audio_files, output_dir,thumbnail_cache_dir, ncs, mute):
    # Define the path of the output video file
    output_video_path = f"{output_dir}/output.mp4"

    # Initialize an empty list to store the video clips
    videos = []

    # Initialize the frame rate to a very high value
    frame_rate = 999999999

    # Loop through all video and audio files
    for video_file, audio_file in zip(video_files, audio_files):
        try:
            # Load the video clip
            video = VideoFileClip(video_file)

            # Add NCS audio
            if ncs:
                # Load the audio clip
                audio = AudioFileClip(audio_file)

                # Calculate the number of times to repeat the audio clip to match the length of the video clip
                repeat_times = int(video.duration/audio.duration + 1)

                # Concatenate the audio clips to match the length of the video clip
                audio = concatenate_audioclips([audio] * repeat_times)

                # Trim the audio clip to match the length of the video clip
                audio = audio.subclip(0, video.duration)

                # Set the audio component of the video clip to the concatenated audio clip
                video = video.set_audio(audio)

            # Mute the audio component of the video clip
            elif mute:
                video = video.without_audio()

            # Save a single frame of the video for thumbnail
            video.save_frame(f"{thumbnail_cache_dir}/{video_file.split('.')[-2].split('/')[-1]}.png", t=(video.duration * 0.81))

        except Exception as e:
            print(e, f' failed to load {video_file} or {audio_file}')
            continue

        # Update the frame rate to the minimum value among all video clips
        if video.fps < frame_rate:
            frame_rate = video.fps

        # Add the video clip to the list of video clips
        videos.append(video)

    # Concatenate all video clips into a single video clip
    output_video = concatenate_videoclips(videos, method='compose')

    # Write the concatenated video clip to the output video file
    output_video.write_videofile(output_video_path, fps=frame_rate, threads=8,audio_fps=44100)

    return output_video_path

