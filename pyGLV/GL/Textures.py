import OpenGL.GL as gl
from PIL import Image

class Texture:
    """
    This Class is used for initializing simple textures
    """

    def __init__(self,filepath):
        img = Image.open(filepath)
        image_data = img.convert("RGBA").tobytes()
        image_width = img.width
        image_height = img.height

        self._texture = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D,self._texture)
        gl.glTexParameteri(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_WRAP_S,gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_WRAP_T,gl.GL_REPEAT)
        gl.glTexParameteri(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_MIN_FILTER,gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D,gl.GL_TEXTURE_MAG_FILTER,gl.GL_LINEAR)
        gl.glTexImage2D(gl.GL_TEXTURE_2D,0,gl.GL_RGBA,image_width,image_height,0,gl.GL_RGBA,gl.GL_UNSIGNED_BYTE,image_data)
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