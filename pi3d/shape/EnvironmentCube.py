import os.path

from pi3d import *
from pi3d.Buffer import Buffer
from pi3d.shape.Shape import Shape
from pi3d.Texture import Texture

CUBE_PARTS = ['front', 'right', 'top', 'bottom', 'left', 'back']

def loadECfiles(path, fname, suffix='jpg', nobottom=False):
  # Helper for loading environment cube faces.
  #TODO this will scramble all the rest of the cube. It needs to substitute a blank (black) texture instead!
  # if nobottom set then only load five parts into array
  if nobottom:
    parts = [p for p in CUBE_PARTS if p != 'bottom']
  else:
    parts = CUBE_PARTS

  files = (os.path.join(path, '%s_%s.%s' % (fname, p, suffix)) for p in parts)
  return [Texture(f) for f in files]

class EnvironmentCube(Shape):
  def __init__(self,  camera, light, size=500.0, maptype="HALFCROSS", name="", x=0.0, y=0.0, z=0.0,
               rx=0.0, ry=0.0, rz=0.0, cx=0.0, cy=0.0, cz=0.0, nobottom=False):
    super(EnvironmentCube,self).__init__(camera, light, name, x, y, z, rx, ry, rz,
                                1.0, 1.0, 1.0, cx, cy, cz)

    if VERBOSE:
      print "Creating environment cube ..."

    self.width = size
    self.height = size
    self.depth = size
    self.ssize = 36
    self.ttype = GL_TRIANGLES
    self.nobottom = nobottom

    ww = size / 2.0
    hh = size / 2.0
    dd = size / 2.0

    #cuboid data - faces are separated out for texturing..

    self.vertices = ((-ww, hh, dd), (ww, hh, dd), (ww,-hh, dd), (-ww, -hh, dd),
        (ww, hh, dd),  (ww, hh, -dd),  (ww, -hh, -dd), (ww, -hh, dd),
        (-ww, hh, dd), (-ww, hh, -dd), (ww, hh, -dd),  (ww, hh, dd),
        (ww, -hh, dd), (ww, -hh, -dd), (-ww, -hh, -dd),(-ww, -hh, dd),
        (-ww, -hh, dd),(-ww, -hh, -dd),(-ww, hh, -dd), (-ww, hh, dd),
        (-ww, hh, -dd),(ww, hh, -dd),  (ww, -hh, -dd), (-ww,-hh,-dd))
    self.normals = ((0.0, 0.0, 1),    (0.0, 0.0, 1),   (0.0, 0.0, 1),  (0.0, 0.0, 1),
        (1, 0.0, 0),  (1, 0.0, 0),    (1, 0.0, 0),     (1, 0.0, 0),
        (0.0, 1, 0),  (0.0, 1, 0),    (0.0, 1, 0),     (0.0, 1, 0),
        (0.0, -1, 0), (0,- 1, 0),     (0.0, -1, 0),    (0.0, -1, 0),
        (-1, 0.0, 0),  (-1, 0.0, 0),  (-1, 0.0, 0),    (-1, 0.0, 0),
        (0.0, 0.0, -1),(0.0, 0.0, -1),(0.0, 0.0, -1),  (0.0, 0.0, -1))
    self.indices = ((3, 0, 1), (2, 3, 1), (7, 4, 5),  (6, 7, 5),
        (11, 8, 9),  (10, 11, 9), (15, 12, 13), (14, 15, 13),
        (17, 18, 19),(16, 17, 19),(22, 21, 20), (23, 22, 20))

    if maptype == "CROSS":
      self.tex_coords = ((1.0, 0.34), (0.75, 0.34), (0.75, 0.661), (1.0, 0.661), #front
        (0.75, 0.34), (0.5, 0.34), (0.5, 0.661), (0.75, 0.661), #right
        (0.251, 0.0), (0.251, 0.34), (0.498, 0.34), (0.498, 0.0), #top
        (0.498, 0.998), (0.498, 0.66), (0.251, 0.66), (0.251, 0.998), #bottom
        (0.0, 0.661), (0.25, 0.661), (0.25, 0.34), (0.0, 0.34), #left
        (0.25, 0.34), (0.5, 0.34), (0.5, 0.661), (0.25, 0.661)) #back

      self.buf = []
      self.buf.append(Buffer(self, self.vertices, self.tex_coords, self.indices, self.normals))

    elif maptype == "HALFCROSS":
      self.tex_coords = ((0.25,0.25), (0.25,0.75), (-0.25,0.75), (-0.25,0.25), #front
        (0.25,0.75), (0.75,0.75), (0.75,1.25), (0.25,1.25), #right
        (0.25,0.25), (0.75,0.25), (0.75,0.75), (0.25,0.75), #top
        (0,0), (1,0), (1,1), (0,1), #bottom
        (0.25,-0.25), (0.75,-0.25), (0.75,0.25), (0.25,0.25), #left
        (0.75,0.25), (0.75,0.75), (1.25,0.75), (1.25,0.25)) #back

      self.buf = []
      self.buf.append(Buffer(self, self.vertices, self.tex_coords, self.indices, self.normals))

    else:
      self.tex_coords = ((0.002,0.002), (0.998,0.002), (0.998,0.998),(0.002,0.998),
            (0.002,0.002), (0.998,0.002), (0.998,0.998), (0.002,0.998),
            (0.002,0.998), (0.002,0.002), (0.998,0.002), (0.998,0.998),
            (0.998,0.002), (0.998,0.998), (0.002,0.998), (0.002,0.002),
            (0.998,0.998), (0.002,0.998), (0.002,0.002), (0.998,0.002),
            (0.998,0.002), (0.002,0.002), (0.002,0.998), (0.998,0.998))

      self.buf = []
      self.buf.append(Buffer(self, self.vertices[0:4], self.tex_coords[0:4], ((3,0,1), (2,3,1)), self.normals[0:4])) #front
      self.buf.append(Buffer(self, self.vertices[4:8], self.tex_coords[4:8], ((3,0,1), (2,3,1)), self.normals[4:8])) #right
      self.buf.append(Buffer(self, self.vertices[8:12], self.tex_coords[8:12], ((3,0,1), (2,3,1)), self.normals[8:12])) #top
      self.buf.append(Buffer(self, self.vertices[12:16], self.tex_coords[12:16], ((3,0,1), (2,3,1)), self.normals[12:16])) #bottom
      self.buf.append(Buffer(self, self.vertices[16:20], self.tex_coords[16:20], ((3,0,1), (2,3,1)), self.normals[16:20])) #left
      self.buf.append(Buffer(self, self.vertices[20:24], self.tex_coords[20:24], ((3,1,0), (2,1,3)), self.normals[20:24])) #back
      
  def set_draw_details(self, shader, textures, ntiles=0.0, shiny=0.0):
    if not (type(textures) is list):
      texture_list = [textures]
    else:
      texture_list = textures
    for i, b in enumerate(self.buf):
      if self.nobottom and i > 2: j = i-1
      else: j = i
      b.set_draw_details(shader, [texture_list[j]], ntiles, shiny)

