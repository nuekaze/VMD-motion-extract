# motion.py

A simple tool to convert VMD motion data for Miku Miku Dance into a text file.

<code>Usage: motion.py [input.vmd [output.txt]] | [-h|--help]</code>

The data are sequenced as follows.<br />
Bone name(hex), Frame number(int), X-position(float), Y-position(float), Z-position(float), X-rotation(float), Y-rotation(float), Z-rotation(float), Interpolation data(hex)<br />
Because I cannot decode the bone names or interpolation data I just wrote them as hex code. Not that it matters what their names are anyway.

There are some issues still with decoding some names. Especially the bone names. I cant manage to decode them so I will just leave it as is for the moment.
The interpolation data is also untouched because I could not find any documentation on it. Not that I looked for very long.

Have fun!
