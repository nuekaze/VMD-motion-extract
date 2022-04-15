# VMD motion extract

<p>A simple tool to convert VMD motion data for Miku Miku Dance into a text file and back again. I have noticed that some data is lost or changed when just converting from vmd to txt and then back. But the files still works and I can not see any difference in the motion in MMD.</p>
<p>
Because I cannot decode the some names or interpolation data I just wrote them as hex code. Not that it matters what their names are anyway.</p>
<p>
There are some issues still with decoding some names. Especially the bone names. I cant manage to decode them so I will just leave it as is for the moment.
The interpolation data is also untouched because I could not find any documentation on it. Not that I looked for very long.</p>
<p>
Have fun!
</p>

# Usage

<p>
<code>
Usage: unpack.py input.vmd [output.txt] [OPTIONS]
</code>
</p>
<p>
<code>
Usage: repack.py input.txt [output.vmd] [OPTIONS]
</code>
</p>
<p>
Do <code>--help</code> for list of options.
</p>  

# File structure

<p>First line if the file contains some meta data.<br/>
  <code>
    MMD Version(hex), Model name(hex), number of motion frames(int), number of face frames(int), number of camera frames(int)
  </code></p>
<p>Motion data<br />
<code>
Bone name(hex), Frame number(int), X-position(float), Y-position(float), Z-position(float), X-rotation(float), Y-rotation(float), Z-rotation(float), Interpolation data(hex)
</code></p>
<p>
Face data<br />
<code>
Part name(hex), frame number(int), Value(float)
</code></p>
<p>
Camera data<br />
<code>
Frame number(int), Length(float), X-position(float), Y-position(float), Z-position(float), X-rotation(float), Y-rotation(float), Z-rotation(float), Interpolation data(hex), FOV(int), Perspective(byte)
</code></p>
