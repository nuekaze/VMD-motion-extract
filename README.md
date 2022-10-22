# VMD motion extract

<p>A simple tool to convert VMD motion data for Miku Miku Dance into a CSV file and back again. I have noticed that some data is lost or changed when just converting from vmd to CSV and then back. But the files still works and I can not see any difference in the motion in MMD.</p>
<p>
Names are now able to be decoded correctly. Interpolation data is still saved as hex because I can not decode it. It is probably just a curve in binary or something.
</p>
<p>
Have fun!
</p>

# Usage

<p>
<code>
Usage: unpack.py input.vmd [output.csv] [OPTIONS]
</code>
</p>
<p>
<code>
Usage: repack.py input.csv [output.vmd] [OPTIONS]
</code>
</p>
<p>
Do <code>--help</code> for list of options.
</p>  

# File structure

<p>First line if the file contains some meta data. Don't change this one or it will break.<br/>
  <code>
    #MMD Version;Model name;number of motion frames(int);number of face frames(int);number of camera frames(int);model name encoding;bone name encoding
  </code></p>
<p>Motion data<br />
<code>
Frame number(int);Bone name;X-position(float);Y-position(float);Z-position(float);X-rotation(float);Y-rotation(float);Z-rotation(float);Interpolation data(hex)
</code></p>
<p>
Face data<br />
<code>
Frame number(int);Blendshape;Value(float)
</code></p>
<p>
Camera data<br />
<code>
Frame number(int);Length(float);X-position(float);Y-position(float);Z-position(float);X-rotation(float);Y-rotation(float);Z-rotation(float);Interpolation data(hex);FOV(int);Perspective(byte)
</code></p>
