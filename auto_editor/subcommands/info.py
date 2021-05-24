'''subcommands/info.py'''

import os
import sys

from auto_editor.usefulFunctions import cleanList

def info_options(parser):
    parser.add_argument('--fast', action='store_true',
        help='skip information that is very slow to get.')
    parser.add_argument('--my_ffmpeg', action='store_true',
        help='use your ffmpeg and other binaries instead of the ones packaged.')
    parser.add_argument('(input)', nargs='*',
        help='the path to a file you want inspected.')
    return parser

def removeZeroes(inp: float) -> str:
    return '{0:.8f}'.format(inp).rstrip('0').rstrip('.')

def aspectRatio(w, h) -> str:

    def gcd(a, b) -> int:
        while b:
            a, b = b, a % b
        return a

    w = int(w)
    h = int(h)

    if(h == 0):
        return ''

    c = gcd(w, h)

    return '{}:{}'.format(int(w / c), int(h / c))

def info(files, ffmpeg, ffprobe, fast, log):

    if(len(files) == 0):
        print('info: subcommand for inspecting media contents.')
        print('Add a file to inspect. Example:')
        print('    auto-editor info example.mp4')
        sys.exit()

    for file in files:
        if(os.path.exists(file)):
            print('file: {}'.format(file))
        else:
            log.error('Could not find file: {}'.format(file))

        hasVid = len(ffprobe.pipe(['-show_streams', '-select_streams', 'v', file])) > 5
        hasAud = len(ffprobe.pipe(['-show_streams', '-select_streams', 'a', file])) > 5

        # Detect if subtitles are present.
        sub_text = ffprobe.pipe(['-show_streams', '-select_streams', 's', file])
        hasSub = len(sub_text) > 5 and 'Invalid data' not in sub_text

        if(hasVid):
            print(f' - fps: {ffprobe.getFrameRate(file)}')

            dur = ffprobe.getDuration(file)
            if(dur == 'N/A'):
                dur = ffprobe.pipe(['-show_entries', 'format=duration', '-of',
                    'default=noprint_wrappers=1:nokey=1', file]).strip()
                dur = removeZeroes(float(dur))
                print(f' - duration: {dur} (container)')
            else:
                dur = removeZeroes(float(dur))
                print(f' - duration: {dur}')

            res = ffprobe.getResolution(file)
            width, height = res.split('x')
            print(f' - resolution: {res} ({aspectRatio(width, height)})')

            print(f' - video codec: {ffprobe.getVideoCodec(file)}')

            vbit = ffprobe.getPrettyBitrate(file, 'v', track=0)
            print(' - video bitrate: {}'.format(vbit))

            if(hasAud):
                tracks = ffprobe.getAudioTracks(file)
                print(f' - audio tracks: {tracks}')

                for track in range(tracks):
                    print(f'   - Track #{track}')
                    print(f'     - codec: {ffprobe.getAudioCodec(file, track)}')
                    print(f'     - samplerate: {ffprobe.getPrettySampleRate(file, track)}')

                    abit = ffprobe.getPrettyBitrate(file, 'a', track)
                    print(f'     - bitrate: {abit}')
            else:
                print(' - audio tracks: 0')

            if(hasSub):
                tracks = ffprobe.getSubtitleTracks(file)
                print(f' - subtitle tracks: {tracks}')
                for track in range(tracks):
                    print(f'   - Track #{track}')
                    print(f'     - lang: {ffprobe.getLang(file, track)}')

            if(not fast):
                fps_mode = ffmpeg.pipe(['-i', file, '-hide_banner', '-vf', 'vfrdet',
                    '-an', '-f', 'null', '-'])
                fps_mode = cleanList(fps_mode.split('\n'), '\r\t')
                fps_mode = fps_mode.pop()

                if('VFR:' in fps_mode):
                    fps_mode = (fps_mode[fps_mode.index('VFR:'):]).strip()

                print(' - {}'.format(fps_mode))

        elif(hasAud):
            print(f' - duration: {ffprobe.getAudioDuration(file)}')
            print(f' - codec: {ffprobe.getAudioCodec(file, track=0)}')
            print(f' - samplerate: {ffprobe.getPrettySampleRate(file, track=0)}')
            abit = ffprobe.getPrettyBitrate(file, 'a', track=0)
            print(f' - bitrate: {abit}')
        else:
            print('Invalid media.')
    print('')