import pyglet
from pyglet.gl import *
import random
import pyrr
import OpenGL.GL.shaders
import ctypes
import OpenGL
import math

int_size = 4
float_size = 4


def matrix_to_single_dim(m):
    return [y for x in m for y in x]


class Tree:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.width = 1
        self.height = 1
        self.size = 1
        self.rot = 0

    def draw(self):
        scale_transform = pyrr.matrix44.create_from_scale([self.size, self.size, self.size])
        rotation_transform = pyrr.matrix44.create_from_y_rotation(self.rot)
        position_transform = pyrr.matrix44.create_from_translation([self.x, self.y, self.z])
        compound_transform = pyrr.matrix44.multiply(pyrr.matrix44.multiply(scale_transform, rotation_transform),
                                                    position_transform)

        # Tree body
        glBindTexture(GL_TEXTURE_2D, texture_bark)
        glBindVertexArray(vao)
        qt1 = pyrr.matrix44.create_from_translation([0, -0.5, 0])
        qt2 = pyrr.matrix44.create_from_scale([1, 5, 1])
        t = pyrr.matrix44.multiply(pyrr.matrix44.multiply(qt2, qt1), compound_transform)
        v = matrix_to_single_dim(t)
        glUniformMatrix4fv(transform_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))
        glUniform2f(tex_scale, 1.0, 1.0)
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, 0)

        # Tree Leaves
        glBindTexture(GL_TEXTURE_2D, texture_leaf)
        glBindVertexArray(vao)
        qt1 = pyrr.matrix44.create_from_translation([0, 2.5, 0])
        qt2 = pyrr.matrix44.create_from_scale([3, 3, 3])
        t = pyrr.matrix44.multiply(pyrr.matrix44.multiply(qt2, qt1), compound_transform)
        v = matrix_to_single_dim(t)
        glUniformMatrix4fv(transform_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))
        glUniform2f(tex_scale, 1.0, 1.0)
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, 0)


tree_list = []
for i in range(20):
    t = Tree()
    t.x = random.randint(-20, 20)
    t.y = 0
    t.z = random.randint(-20, 20)
    tree_list.append(t)

vert_shader = """
  #version 330
  in layout (location = 0) vec3 position;
  in layout (location = 1) vec3 color;
  in layout (location = 2) vec2 tex_coord;
  in layout (location = 3) vec3 normal;

  out vec3 fragNormal;
  out vec3 fragPos;
  out vec3 fragColor;
  out vec2 fragTex;

  uniform mat4 transform;
  uniform mat4 projection;
  uniform mat4 view;

  void main()
  {
      gl_Position = projection * view * transform * vec4(position, 1.0f);
      fragNormal = normalize(vec3(transform * vec4(normal, 0.0)));
      fragPos = vec3(transform * vec4(position, 1.0f));
      fragColor = color;
      fragTex = tex_coord;
  }
"""

frag_shader = """
 #version 330
 out vec4 outColor;
 in vec3 fragNormal;
 in vec3 fragPos;
 in vec3 fragColor;
 in vec2 fragTex;


 uniform vec3 light_position;
 uniform vec3 camera_position;
 uniform vec3 ambient_color;
 uniform vec3 diffuse_color;
 uniform vec3 specular_color;
 uniform float shininess;

 uniform float constant;
 uniform float linear;
 uniform float quadratic;

 uniform vec2 tex_scale;

 void main()
 {
        vec3 lightDirection = normalize(light_position - fragPos);
        vec3 viewDir = normalize(camera_position - fragPos);
        vec3 reflectDir = reflect(-lightDirection , fragNormal);

        vec3 ambient_light = ambient_color;
        vec3 diffuse_light = diffuse_color * max(dot(fragNormal, lightDirection), 0.0);
        vec3 specular_light = specular_color * pow(max(dot(viewDir, reflectDir), 0.0), shininess);

        float distance = length(light_position - fragPos);
        float attenuation = 1.0 / (constant + linear * distance + quadratic * distance * distance);

        vec3 light = ambient_light + (diffuse_light + specular_light) * attenuation;

        outColor = vec4(light, 1.0f);

 }
"""

window = pyglet.window.Window(width=1280, height=800)

shader = OpenGL.GL.shaders.compileProgram(
    OpenGL.GL.shaders.compileShader(vert_shader, GL_VERTEX_SHADER),
    OpenGL.GL.shaders.compileShader(frag_shader, GL_FRAGMENT_SHADER))

glUseProgram(shader)

transform_matrix = glGetUniformLocation(shader, b'transform')
projection_matrix = glGetUniformLocation(shader, b'projection')
view_matrix = glGetUniformLocation(shader, b'view')
light_position = glGetUniformLocation(shader, b'light_position')
camera_position = glGetUniformLocation(shader, b'camera_position')
ambient_color = glGetUniformLocation(shader, b'ambient_color')
diffuse_color = glGetUniformLocation(shader, b'diffuse_color')
specular_color = glGetUniformLocation(shader, b'specular_color')
shininess = glGetUniformLocation(shader, b'shininess')
tex_scale = glGetUniformLocation(shader, b'tex_scale')
constant = glGetUniformLocation(shader, b'constant')
linear = glGetUniformLocation(shader, b'linear')
quadratic = glGetUniformLocation(shader, b'quadratic')

cube_vertex_positions = [-0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, -1.0,
                         +0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, -1.0,
                         +0.5, +0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, -1.0,
                         -0.5, +0.5, -0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, -1.0,

                         -0.5, -0.5, +0.5, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, +1.0,
                         +0.5, -0.5, +0.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, +1.0,
                         +0.5, +0.5, +0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, +1.0,
                         -0.5, +0.5, +0.5, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, +1.0,

                         -0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, -1.0, 0.0,
                         +0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0, 0.0,
                         -0.5, -0.5, +0.5, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, -1.0, 0.0,
                         +0.5, -0.5, +0.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, -1.0, 0.0,

                         -0.5, +0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, +1.0, 0.0,
                         +0.5, +0.5, -0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, +1.0, 0.0,
                         -0.5, +0.5, +0.5, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, +1.0, 0.0,
                         +0.5, +0.5, +0.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, +1.0, 0.0,

                         -0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 0.0, -1.0, 0.0, 0.0,
                         -0.5, +0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 1.0, -1.0, 0.0, 0.0,
                         -0.5, -0.5, +0.5, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0, 0.0, 0.0,
                         -0.5, +0.5, +0.5, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, 0.0, 0.0,

                         +0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 1.0, 0.0, +1.0, 0.0, 0.0,
                         +0.5, +0.5, -0.5, 1.0, 1.0, 1.0, 1.0, 1.0, +1.0, 0.0, 0.0,
                         +0.5, -0.5, +0.5, 1.0, 1.0, 1.0, 0.0, 0.0, +1.0, 0.0, 0.0,
                         +0.5, +0.5, +0.5, 1.0, 1.0, 1.0, 0.0, 1.0, +1.0, 0.0, 0.0]

cube_indices = [0, 1, 2, 0, 2, 3,
                4, 5, 6, 4, 6, 7,
                8, 11, 9, 8, 11, 10,
                12, 15, 13, 12, 15, 14,
                16, 17, 18, 17, 18, 19,
                20, 22, 21, 21, 23, 22]

vao = GLuint(0)
glGenVertexArrays(1, vao)
glBindVertexArray(vao)

vbo = GLuint(0)
glGenBuffers(1, vbo)

glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, len(cube_vertex_positions) * float_size,
             (GLfloat * len(cube_vertex_positions))(*cube_vertex_positions), GL_STATIC_DRAW)

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 11 * 4, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)

glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 11 * 4, ctypes.c_void_p(12))
glEnableVertexAttribArray(1)

glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 11 * 4, ctypes.c_void_p(24))
glEnableVertexAttribArray(2)

glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, 11 * 4, ctypes.c_void_p(32))
glEnableVertexAttribArray(3)

ibo = GLuint(0)
glGenBuffers(1, ibo)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(cube_indices) * int_size,
             (GLuint * len(cube_indices))(*cube_indices), GL_STATIC_DRAW)

qvao = GLuint(0)
glGenVertexArrays(1, qvao)
glBindVertexArray(qvao)

quad_vertex_positions = [-0.5, -0.0, -0.5, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0,
                         +0.5, -0.0, -0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0,
                         +0.5, -0.0, +0.5, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0,
                         -0.5, -0.0, +0.5, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0]

quad_indices = [0, 1, 2, 0, 2, 3]

qvbo = GLuint(0)
glGenBuffers(1, qvbo)
glBindBuffer(GL_ARRAY_BUFFER, qvbo)
glBufferData(GL_ARRAY_BUFFER, len(quad_vertex_positions) * float_size,
             (GLfloat * len(quad_vertex_positions))(*quad_vertex_positions), GL_STATIC_DRAW)

qibo = GLuint(0)
glGenBuffers(1, qibo)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, qibo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(quad_indices) * int_size, (GLuint * len(quad_indices))(*quad_indices),
             GL_STATIC_DRAW)

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 11 * 4, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)

glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 11 * 4, ctypes.c_void_p(20))
glEnableVertexAttribArray(1)

glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 11 * 4, ctypes.c_void_p(12))
glEnableVertexAttribArray(2)

glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, 11 * 4, ctypes.c_void_p(32))
glEnableVertexAttribArray(3)

glEnable(GL_TEXTURE_2D)

grass_image = pyglet.image.load('grass.jpg')
texture_grass = grass_image.get_texture().id
bark_image = pyglet.image.load('bark.jpg')
texture_bark = bark_image.get_texture().id
leaf_image = pyglet.image.load('leaf.jpg')
texture_leaf = leaf_image.get_texture().id

glBindTexture(GL_TEXTURE_2D, texture_grass)

glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)

glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

once = True
amb_light = 0.2
diff_light = 0.4
spec_light = 0.4


@window.event
def on_draw():
    global once, tree_list
    window.clear()

    if once:
        glClearColor(0.25, 0.6, 1, 1)
        glEnable(GL_DEPTH_TEST)
        pm = pyrr.matrix44.create_perspective_projection(45.0, 1280.0 / 800.0, 0.1, 100.0)
        projection_vector = matrix_to_single_dim(pm)
        glUniformMatrix4fv(projection_matrix, 1, GL_FALSE, (GLfloat * len(projection_vector))(*projection_vector))

        once = False

    t = pyrr.matrix44.create_look_at([player_x, player_y, player_z],
                                     [player_x + cosDegree(angle_x), player_y - cosDegree(angle_y),
                                      player_z + sinDegree(angle_x)], [0, 1, 0])
    v = matrix_to_single_dim(t)
    glUniformMatrix4fv(view_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))

    # Render floor
    glBindVertexArray(qvao)
    qt1 = pyrr.matrix44.create_from_translation([0., -2, 50])
    qt2 = pyrr.matrix44.create_from_scale([200, 1, 200])
    t = pyrr.matrix44.multiply(qt2, qt1)
    v = matrix_to_single_dim(t)
    glUniformMatrix4fv(transform_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))
    glUniform2f(tex_scale, 25.0, 25.0)
    glDrawElements(GL_TRIANGLES, len(quad_indices), GL_UNSIGNED_INT, 0)

    for t in tree_list:
        t.draw()


@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)


def sinDegree(degree):
    return math.sin(math.radians(degree))


def cosDegree(degree):
    return math.cos(math.radians(degree))


angle_x = 0
angle_y = 0
player_x = 0
player_y = 0
player_z = -10
key_state_w = False
key_state_a = False
key_state_s = False
key_state_d = False

diffusePosition = [1, 0, 0]
total_time = 0


def update(dt):
    global player_x, player_y, player_z, angle_x
    global key_state_w, key_state_a, key_state_s, key_state_d
    global angle_x, angle_y
    global ambient_color, diffuseColor, diffuse_position
    global diffuse_color, diffusePosition, total_time, specularColor

    total_time = total_time + dt

    if key_state_w:
        player_x = player_x + math.cos(math.radians(angle_x)) * 10 * dt
        player_z = player_z + math.sin(math.radians(angle_x)) * 10 * dt
    if key_state_s:
        player_x = player_x - math.cos(math.radians(angle_x)) * 10 * dt
        player_z = player_z - math.sin(math.radians(angle_x)) * 10 * dt
    if key_state_a:
        player_x = player_x - math.cos(math.radians(angle_x + 90)) * 10 * dt
        player_z = player_z - math.sin(math.radians(angle_x + 90)) * 10 * dt
    if key_state_d:
        player_x = player_x - math.cos(math.radians(angle_x - 90)) * 10 * dt
        player_z = player_z - math.sin(math.radians(angle_x - 90)) * 10 * dt

    glUniform3f(camera_position, player_x, player_y, player_z)
    glUniform3f(ambient_color, 0.2, 0.2, 0.2)
    glUniform3f(diffuse_color, 0.4, 0.4, 0.4)
    glUniform3f(specular_color, 0.4, 0.4, 0.4)
    glUniform1f(shininess, 12)

    glUniform1f(constant, 1.0)
    glUniform1f(linear, 0.05)
    glUniform1f(constant, 0.032)


@window.event
def on_key_press(key, ups):
    global key_state_w, key_state_a, key_state_s, key_state_d
    global amb_light, diff_light, spec_light

    if key == pyglet.window.key.W:
        key_state_w = True
    if key == pyglet.window.key.A:
        key_state_a = True
    if key == pyglet.window.key.S:
        key_state_s = True
    if key == pyglet.window.key.D:
        key_state_d = True
    if key == pyglet.window.key._1:
        amb_light = 0.2 - amb_light
    if key == pyglet.window.key._2:
        diff_light = 0.4 - diff_light
    if key == pyglet.window.key._3:
        spec_light = 0.4 - spec_light


@window.event
def on_key_release(key, ups):
    global key_state_w, key_state_a, key_state_s, key_state_d
    if key == pyglet.window.key.W:
        key_state_w = False
    if key == pyglet.window.key.A:
        key_state_a = False
    if key == pyglet.window.key.S:
        key_state_s = False
    if key == pyglet.window.key.D:
        key_state_d = False


@window.event
def on_mouse_motion(x, y, dx, dy):
    global angle_x, angle_y
    angle_x = angle_x + dx * 0.5
    angle_y = angle_y + dy * 0.5

    if angle_y > 120:
        angle_y = 120
    elif angle_y < -10:
        angle_y = -10


pyglet.clock.schedule_interval(update, 1 / 120.0)
pyglet.app.run()
