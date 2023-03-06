import OpenGL.GL as gl
import numpy as np
from PIL import Image

class Texture:
    """
    This Class is used for initializing simple textures
    """

    CUBE_TEX_COORDINATES = np.array([
    [0.0, 0.0],
    [1.0, 0.0],
    [1.0, 1.0],
    [0.0, 0.0],
    [1.0, 1.0],
    [0.0, 1.0],
    [0.0, 0.0],
    [1.0, 0.0],
    [1.0, 1.0],
    [0.0, 0.0],
    [1.0, 1.0],
    [0.0, 1.0],
    [0.0, 0.0],
    [1.0, 0.0],
    [1.0, 1.0],
    [0.0, 0.0],
    [1.0, 1.0],
    [0.0, 1.0],
    [0.0, 0.0],
    [1.0, 0.0],
    [1.0, 1.0],
    [0.0, 0.0],
    [1.0, 1.0],
    [0.0, 1.0],
    [0.0, 0.0],
    [1.0, 0.0],
    [1.0, 1.0],
    [0.0, 0.0],
    [1.0, 1.0],
    [0.0, 1.0],
    [0.0, 0.0],
    [1.0, 0.0],
    [1.0, 1.0],
    [0.0, 0.0],
    [1.0, 1.0],
    [0.0, 1.0],
    [0.0, 0.0],
    [1.0, 0.0],
    [1.0, 1.0],
    [0.0, 0.0],
    [1.0, 1.0],
    [0.0, 1.0],
],dtype=np.float32)

    def __init__(self,filepath):
        angle = -90

        img = Image.open(filepath)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img = img.rotate(angle) #need to rotate by 90 degrees 
        image_data = img.convert("RGBA").tobytes()

        self._texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D,self._texture)
        
        #gl.glTexParameteri(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_WRAP_S,gl.GL_MIRRORED_REPEAT)
        #gl.glTexParameteri(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_WRAP_T,gl.GL_MIRRORED_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_WRAP_S,gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_WRAP_T,gl.GL_REPEAT)

        gl.glTexParameteri(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_MIN_FILTER,gl.GL_LINEAR)
        gl.glTexParameteri(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_MAG_FILTER,gl.GL_LINEAR)

        gl.glTexImage2D(gl.GL_TEXTURE_2D,0,gl.GL_RGBA,img.width,img.height,0,gl.GL_RGBA,gl.GL_UNSIGNED_BYTE,image_data)
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)
    
    """
    Bind and Activate texture
    """
    def bind(self):
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D,self._texture)

    """
        unbind texture
    """
    def unbind(self):
        gl.glDeleteTextures(1,self._texture)