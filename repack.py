"""
Author: Nue-class Destroyer
License: BSD 2-Clause "Simplified" License
"""
import struct, sys

def help():
    print('Usage: repack.py input.txt [output.vmd] [OPTIONS]\n')
    print('\n'.join([
        'List of options',
        '    -m, --motion:   Process motion data.',
        '    -f, --face:     Process face data.',
        '    -c, --camera:   Process camera data.',
        '',
        '    -h, --help:     Show this help message.',
        '    -v, --verbose:  Show some more info.',
        '    -d, --debug:    Enable debugging.',
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
verbose = 0
if '-d' in sys.argv or '--debug' in sys.argv:
    print('Debugging.')
    debug = 1
    from pprint import pprint

if '-v' in sys.argv or '--verbose' in sys.argv:
    verbose = 1
# Enter motion file here or use argument.
motion_file = 'input.txt'
output_file = 'output.vmd'
try:
    if sys.argv[1] and sys.argv[1][0] != '-':
        motion_file = sys.argv[1]
except IndexError:
    pass


"""
Begin real work
"""
# Load TXT file
try:
    with open(motion_file, 'r') as f:
        if debug or verbose:
            print('Using %s\nLoading TXT file...' % motion_file)
        raw = f.readlines()
except FileNotFoundError:
    print('%s was not found.')
    exit()

# Get meta data
meta = raw[0].split(',')
version = bytes.fromhex(meta[0])
model = bytes.fromhex(meta[1])
motion_frames = int(meta[2])
face_frames = int(meta[3])
camera_frames = int(meta[4].strip('\n'))

# Show some info
if debug or verbose:
    print('MMD version: %s' % version.decode('utf-8'))
try:
    if debug or verbose:
        print('MMD model: %s' % model.replace(b'\x00', b'').decode('utf-8'))
except UnicodeDecodeError:
    try:
        if debug or verbose:
            print('MMD model: %s' % model.replace(b'\x00', b'').decode('utf-16'))
    except UnicodeDecodeError:
        if debug or verbose:
            print('No model is present. This is probably camera data.\nWill try to process camera data only.')
        motion = 0
        face = 0
        camera = 2

# Process motion keyframes
motion_keyframes = []
if debug or verbose:
    print('Motion frames: %i' % motion_frames)
for kf in raw[1:1+motion_frames]:
    try:
        kf = kf.strip('\n').split(',')
        bone = bytes.fromhex(kf[0])
        frame = bytes(struct.pack('I', int(kf[1])))
        xc = bytes(struct.pack('f', float(kf[2])))
        yc = bytes(struct.pack('f', float(kf[3])))
        zc = bytes(struct.pack('f', float(kf[4])))
        xr = bytes(struct.pack('f', float(kf[5])))
        yr = bytes(struct.pack('f', float(kf[6])))
        zr = bytes(struct.pack('f', float(kf[7])))
        i_data = bytes.fromhex(kf[8])
        motion_keyframes.append((bone, frame, xc, yc, zc, xr, yr, zr, i_data))
    except ValueError:
        print(kf)
        exit()

if debug:
    pprint(motion_keyframes)

# Process face keyframes
face_keyframes = []
if debug or verbose:
    print('Face frames: %i' % face_frames)
for kf in raw[1+motion_frames:1+motion_frames+face_frames]:
    kf = kf.split(',')
    bone =  bytes.fromhex(kf[0])
    frame = bytes(struct.pack('I', int(kf[1])))
    value = bytes(struct.pack('f', float(kf[2])))
    face_keyframes.append((bone, frame, value))

if debug:
    pprint(face_keyframes)

# Process camera keyframes
camera_keyframes = []
if debug or verbose:
    print('Camera frames: %i' % camera_frames)
for kf in raw[1+motion_frames+face_frames:1+motion_frames+face_frames+camera_frames]:
    kf = kf.split(',')
    frame = bytes(struct.pack('I', int(kf[0])))
    length = bytes(struct.pack('f', float(kf[1])))
    xc = bytes(struct.pack('f', float(kf[2])))
    yc = bytes(struct.pack('f', float(kf[3])))
    zc = bytes(struct.pack('f', float(kf[4])))
    xr = bytes(struct.pack('f', float(kf[5])))
    yr = bytes(struct.pack('f', float(kf[6])))
    zr = bytes(struct.pack('f', float(kf[7])))
    i_data = bytes.fromhex(kf[8])
    fov = bytes(struct.pack('I', int(kf[9])))
    perspective = bytes(struct.pack('B', int(kf[10])))
    camera_keyframes.append((frame, length, xc, yc, zc, xr, yr, zr, i_data, fov, perspective))

if debug:
    pprint(camera_keyframes)

"""
Save file
"""
ready_data = [version, model, bytes(struct.pack('I', motion_frames))]
if motion:
    for i in motion_keyframes:
        ready_data.append(b''.join(i))

ready_data.append(bytes(struct.pack('I', face_frames)))
if face:
    for i in face_keyframes:
        ready_data.append(b''.join(i))

ready_data.append(bytes(struct.pack('I', camera_frames)))
if camera:
    for i in camera_keyframes:
        ready_data.append(b''.join(i))

try:
    if sys.argv[2] and sys.argv[2][0] != '-':
        output_file = sys.argv[2]
except IndexError:
    pass

with open(output_file, 'wb') as f:
    if debug or verbose:
        print('Writing data to %s.' % output_file)
        f.write(b''.join(ready_data))
if debug or verbose:
    print('Done. Exiting.')