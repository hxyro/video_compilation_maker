from functools import cache
import os
import sys
import random
import argparse

from lib.compile import compile
from lib.thumbnail import thumbnail, snapshots
from lib.score_images import score_images
from lib.filters import box_blur

def main():
    parser = argparse.ArgumentParser(description='Process a compilation of TikTok videos.')
    parser.add_argument('-i', '--input', type=str, required=True, help='Path to the input directory containing TikTok videos.')
    parser.add_argument('-o', '--output', type=str, required=True, help='Path to the output directory where the processed videos will be saved.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--ncs', action='store_true', help='Replace the audio with a royalty-free NCS track.')
    group.add_argument('-m', '--mute', action='store_true', help='Remove the audio from the output video.')
    parser.add_argument('-b', '--blur', action='store_true', help='Add a blur effect to the output video.')
    parser.add_argument('-t', '--thumbnail', action='store_true', help='Generate a thumbnail image for output video.')
    parser.add_argument('-c', '--cache', action='store_true', help='Keep the cache files')
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    input_dir = os.path.abspath(args.input)
    output_dir = os.path.abspath(args.output)
    audio_dir = os.path.abspath('audio/ncs/')
    model_path = os.path.abspath('model/model-resnet50.pth')


    if args.ncs and args.mute:
        print('Error: The -a and -m flags cannot be used at the same time.', file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    if not os.path.isdir(args.input):
        print(f'error: the input directory "{args.input}" does not exist or is not a directory.', file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    if not os.path.isdir(args.output):
        print(f'error: the output directory "{args.output}" does not exist or is not a directory.', file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    cache_dir = f"{output_dir}/cache"
    for dir in ["thumbnail", "audio", "video"]:
        os.makedirs(os.path.join(cache_dir, dir), exist_ok=True)
    thumbnail_cache_dir = cache_dir+'/thumbnail'

    video_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir)]

    all_audio_files = os.listdir(audio_dir)
    random.shuffle(all_audio_files)

    audio_files = [os.path.join(audio_dir, f) for f in all_audio_files[:len(video_files)]]

    output_video_path = compile(video_files, audio_files, output_dir,thumbnail_cache_dir, ncs=args.ncs, mute=args.mute)

    if args.blur:
       box_blur_output_video_path = box_blur(output_video_path, output_dir=args.output)

    if args.thumbnail:
        thumbnail(score_images(model_path, thumbnail_cache_dir), output_dir)

    if not args.cache: os.system("rm -rf {}".format(cache_dir))

if __name__ == '__main__':
    main()

