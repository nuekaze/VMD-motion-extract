import struct
import sys
from pprint import pprint

try:
    if sys.argv[1] == '-h' || sys.argv[1] == '--help':
        print('Usage: motion.py [input.vmd [output.txt]] | [-h|--help]')
        exit()

except IndexError:
    pass

# Enter motion file here or use argument.
motion_file = 'motion.vmd'
output_file = 'result.txt'
try:
    if sys.argv[1]:
        motion_file = sys.argv[1]
except IndexError:
    pass

raw = None
try:
    with open(motion_file, 'rb') as f:
        print('Using %s\nLoading model...' % motion_file)
        raw = f.read()
except FileNotFoundError:
    print('%s was not found.' % motion_file)
    exit()

version = raw[0:30].decode('utf-8') # This line is UTF-8, Program version

# Sometimes the character model uses UTF-8 and sometimes UTF-16
try:
    model = raw[30:50].replace(b'\x00', b'').decode('utf-8')
except:
     model = raw[30:50].replace(b'\x00', b'').decode('utf-16')


k_frames = struct.unpack('i', raw[50:54])[0] # Unsigned int, Number of keyframes
k_data = raw[54:]
keyframes = []

print('MMD version: %s' % version)
print('MMD model: %s' % model)

# Go through all frames for motion
print('Processing motion. This may take a few seconds...')
for i in range(k_frames):
    bone = k_data[0:15] # Bone name, I don't know  how to decode this shit
    frame = struct.unpack('i', k_data[15:19])[0] # Frame number

    # Motion relative to default position
    xc = struct.unpack('f', k_data[19:23])[0]
    yc = struct.unpack('f', k_data[23:27])[0]
    zc = struct.unpack('f', k_data[27:31])[0]
    xr = struct.unpack('f', k_data[31:35])[0]
    yr = struct.unpack('f', k_data[35:39])[0]
    zr = struct.unpack('f', k_data[39:43])[0]

    i_data = k_data[43:111] # Interpolation data
    keyframes.append((bone, frame, xc, yc, zc, xr, yr, zr, i_data)) # Add keyframe to list of keyframes
    k_data = k_data[111:] # jump to next frame

print('Done.')
#print('\n'.join('%s, %i, %f, %f, %f, %f, %f, %f, %s' % x for x in keyframes))

try:
    if sys.argv[2]:
        output_file = sys.argv[2]
except IndexError:
    pass

with open(output_file, 'w') as f:
    print('Writing data to file.')
    f.write('\n'.join('%s, %i, %f, %f, %f, %f, %f, %f, %s' % x for x in keyframes))
print('Done. Exiting.')
