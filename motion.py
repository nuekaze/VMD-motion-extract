"""
Author: Nue-class Destroyer
License: BSD-2 Simplified
"""
import struct, sys

def help():
    print('Usage: motion.py input.vmd [output.txt] [OPTIONS]\n')
    print('\n'.join([
        'List of options:',
        '    -m, --motion: Process motion data.',
        '    -f, --face:   Process face data.',
        '    -c, --camera: Process camera data.',
        '',
        '    -h, --help:   Show this help message.',
        '    -d, --debug:  Enable debugging.',
    ]))

"""
Process arguments
"""
skip = 0
motion = 0
face = 0
camera = 0
if '-h' in sys.argv  or '--help' in sys.argv:
    help()
    exit()
if '-m' in sys.argv or '--motion' in sys.argv:
    skip = 1
    motion = 1
if '-f' in sys.argv or '--face' in sys.argv:
    skip = 1
    face = 1
if '-c' in sys.argv or '--camera' in sys.argv:
    skip = 1
    camera = 1

try:
    if sys.argv[1][0] == '-':
        print('Input file is required. Exiting.')
        exit()

except IndexError:
    help()
    exit()

if not skip:
    motion = input('Include motion data? [y/N]: ')
    if motion == 'y' or motion == 'Y':
        motion = 1
    face = input('Include face data? [y/N]: ')
    if face == 'y' or face == 'Y':
        face = 1
    camera = input('Include camera data? [y/N]: ')
    if camera == 'y' or camera == 'Y':
        camera = 1

debug = 0
if '-d' in sys.argv or '--debug' in sys.argv:
    print('Debugging.')
    debug = 1
    from pprint import pprint

# Enter motion file here or use argument.
motion_file = 'input.vmd'
output_file = 'output.txt'
try:
    if sys.argv[1] and sys.argv[1][0] != '-':
        motion_file = sys.argv[1]
except IndexError:
    pass


"""
Begin real work
"""
# Load VMD file
raw = None
try:
    with open(motion_file, 'rb') as f:
        print('Using %s\nLoading VMD file...' % motion_file)
        raw = f.read()
except FileNotFoundError:
    print('%s was not found.')
    exit()

# This line is UTF-8, Program version
version = raw[0:30].decode('utf-8')
print('MMD version: %s' % version)

# Sometimes the character model uses UTF-8 and sometimes UTF-16
try:
    model = raw[30:50].replace(b'\x00', b'').decode('utf-8')
except UnicodeDecodeError:
    try:
        model = raw[30:50].replace(b'\x00', b'').decode('utf-16')
    except UnicodeDecodeError:
        print('No model is present. This is probably camera data.\nWill try to process camera data only.')
        motion = 0
        face = 0
        camera = 2

k_frames = struct.unpack('i', raw[50:54])[0] # Unsigned int, Number of keyframes
k_data = raw[54:]

try:
    print('MMD model: %s' % model)
except NameError:
    pass

if camera != 2:
    # Process motion data.
    motion_keyframes = []
    if motion:
        print('Processing motion data. This may take a few seconds...')
        for i in range(k_frames):
            # Bone name, I don't know how to decode this shit
            bone = k_data[0:15].replace(b'\x00', b'').hex()
            # Frame number
            frame = struct.unpack('i', k_data[15:19])[0]

            # Motion relative to default position
            xc = struct.unpack('f', k_data[19:23])[0]
            yc = struct.unpack('f', k_data[23:27])[0]
            zc = struct.unpack('f', k_data[27:31])[0]
            xr = struct.unpack('f', k_data[31:35])[0]
            yr = struct.unpack('f', k_data[35:39])[0]
            zr = struct.unpack('f', k_data[39:43])[0]

            # Interpolation data
            i_data = k_data[43:111].hex()
            # Add keyframe to list of keyframes
            motion_keyframes.append((bone, frame, xc, yc, zc, xr, yr, zr, i_data))
            # jump to next frame
            k_data = k_data[111:]
    else:
        k_data = k_data[111*k_frames:]

    if motion:
        print('Done.')
        if debug:
            pprint(motion_keyframes)

    # Process face data. Same process as motion data so I will skip comments.
    face_keyframes = []
    if face:
        print('Processing face data. This may take a few seconds...')
        k_frames = struct.unpack('i', k_data[0:4])[0]
        k_data = k_data[4:]
        for i in range(k_frames):
            bone = k_data[0:15].replace(b'\x00', b'').hex()
            frame = struct.unpack('i', k_data[15:19])[0]
            value = struct.unpack('f', k_data[19:23])[0]
            face_keyframes.append((bone, frame, value))
            k_data = k_data[23:]
    else:
        k_data = k_data[111*k_frames:]

    if face:
        print('Done.')
        if debug:
            pprint(face_keyframes)

# Process camera data. Same process as face data.
camera_keyframes = []
if camera:
    print('Processing camera data. This may take a few seconds...')
    k_frames = struct.unpack('i', k_data[0:4])[0]
    k_data = k_data[4:]
    for i in range(k_frames):
        if camera:
            frame = struct.unpack('i', k_data[0:4])[0]
            length = struct.unpack('f', k_data[4:8])[0]
            xc = struct.unpack('f', k_data[8:12])[0]
            yc = struct.unpack('f', k_data[12:16])[0]
            zc = struct.unpack('f', k_data[16:20])[0]
            xr = struct.unpack('f', k_data[24:28])[0]
            yr = struct.unpack('f', k_data[32:36])[0]
            zr = struct.unpack('f', k_data[36:40])[0]
            i_data = k_data[40:64].hex()
            fov = struct.unpack('i', k_data[68:72])[0]
            perspective = struct.unpack('i', k_data[72])[0]
            camera_keyframes.append((frame, length, xc, yc, zc, xr, yr, zr, i_data, fov, perspective))
        k_data = k_data[73:]
    if camera:
        print('Done.')
        if debug:
            pprint(camera_keyframes)

try:
    if sys.argv[2] and sys.argv[2][0] != '-':
        output_file = sys.argv[2]
except IndexError:
    pass

with open(output_file, 'w') as f:
    print('Writing data to %s.' % output_file)
    if motion:
        f.write('\n'.join('%s, %i, %f, %f, %f, %f, %f, %f, %s' % x for x in motion_keyframes))
    if face:
        f.write('\n'.join('%s, %i, %f' % x for x in face_keyframes))
    if camera:
        f.write('\n'.join('%i, %f, %f, %f, %f, %f, %f, %f, %s, %i, %i' % x for x in camera_keyframes))
print('Done. Exiting.')