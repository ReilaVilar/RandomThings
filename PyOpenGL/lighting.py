from pyglet.gl import *
import random
import OpenGL.GL.shaders
import ctypes
import math
import pyrr

int_size = 4
float_size = 4

rotating = True


def matrix_to_single_dim(m):
    return [y for x in m for y in x]


vert_shader = """
  #version 330
  in layout (location = 0) vec3 position;
  in layout (location = 1) vec3 normal;

  uniform mat4 transform;
  uniform mat4 projection;
  uniform mat4 view;

  uniform vec3 light_direction;
  uniform vec3 ambient_color;
  uniform vec3 diffuse_color;

  out vec3 color;

  void main()
  {

      gl_Position = projection * view * transform * vec4(position, 1.0f);

      vec3 norm = normalize(vec3(transform * vec4(normal, 0.0)));
      vec3 lightDirection = normalize(light_direction);

      vec3 ambient_light = ambient_color;
      vec3 diffuse_light = diffuse_color * max(dot(norm, lightDirection), (0.0));

      color = ambient_light + diffuse_light;

  }
"""

frag_shader = """
 #version 330
 out vec4 outColor;
 in vec3 color;

 void main()
 {
    outColor = vec4(color, 1.0);
 }
"""

window = pyglet.window.Window(width=800, height=600)

shader = OpenGL.GL.shaders.compileProgram(
    OpenGL.GL.shaders.compileShader(vert_shader, GL_VERTEX_SHADER),
    OpenGL.GL.shaders.compileShader(frag_shader, GL_FRAGMENT_SHADER))

glUseProgram(shader)

transform_matrix = glGetUniformLocation(shader, b'transform')
projection_matrix = glGetUniformLocation(shader, b'projection')
view_matrix = glGetUniformLocation(shader, b'view')
light_direction = glGetUniformLocation(shader, b'light_direction')
ambient_color = glGetUniformLocation(shader, b'ambient_color')
diffuse_color = glGetUniformLocation(shader, b'diffuse_color')

sphere_vertex_data = []
sphere_indices = []
sphere_num_sectors = 10
sphere_num_stacks = 10

delta_alpha = math.pi / sphere_num_stacks
delta_beta = 2.0 * math.pi / sphere_num_sectors
index_number = 0


def get_sphere_position(stack, sector):
    alpha = (-math.pi / 2.0) + stack * delta_alpha
    beta = -math.pi + sector * delta_beta

    x = 0.5 * math.cos(alpha) * math.cos(beta)
    y = 0.5 * math.cos(alpha) * math.sin(beta)
    z = 0.5 * math.sin(alpha)

    return [x, y, z]


def get_normal(p1, p2, p3):
    u = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
    v = (p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2])

    x = u[1] * v[2] - u[2] * v[1]
    y = u[2] * v[0] - u[0] * v[2]
    z = u[0] * v[1] - u[1] * v[0]

    return [x, y, z]


def push_vertex(position, normal):
    sphere_vertex_data.append(position[0])
    sphere_vertex_data.append(position[1])
    sphere_vertex_data.append(position[2])
    sphere_vertex_data.append(normal[0])
    sphere_vertex_data.append(normal[1])
    sphere_vertex_data.append(normal[2])


for i in range(sphere_num_stacks):
    for j in range(sphere_num_sectors):
        p1 = get_sphere_position(i, j)
        p2 = get_sphere_position(i, j + 1)
        p3 = get_sphere_position(i + 1, j)
        p4 = get_sphere_position(i + 1, j + 1)

        normal_1 = get_normal(p1, p2, p3)
        normal_2 = get_normal(p2, p3, p4)

        normal_2[0] = -normal_2[0]
        normal_2[1] = -normal_2[1]
        normal_2[2] = -normal_2[2]

        push_vertex(p1, normal_1)
        push_vertex(p2, normal_1)
        push_vertex(p3, normal_1)

        push_vertex(p2, normal_2)
        push_vertex(p3, normal_2)
        push_vertex(p4, normal_2)

        sphere_indices.append(index_number)
        sphere_indices.append(index_number + 1)
        sphere_indices.append(index_number + 2)
        sphere_indices.append(index_number + 3)
        sphere_indices.append(index_number + 4)
        sphere_indices.append(index_number + 5)

        index_number = index_number + 6

vao = GLuint(0)
glGenVertexArrays(1, vao)
glBindVertexArray(vao)

vbo = GLuint(0)
glGenBuffers(1, vbo)

glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, len(sphere_vertex_data) * float_size,
             (GLfloat * len(sphere_vertex_data))(*sphere_vertex_data), GL_STATIC_DRAW)

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)

glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
glEnableVertexAttribArray(1)

ibo = GLuint(0)
glGenBuffers(1, ibo)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(sphere_indices) * int_size,
             (GLuint * len(sphere_indices))(*sphere_indices), GL_STATIC_DRAW)

cube_vertex_positions = [-0.5, -0.5, -0.5, 0, 0, -1,
                         +0.5, -0.5, -0.5, 0, 0, -1,
                         +0.5, +0.5, -0.5, 0, 0, -1,
                         -0.5, +0.5, -0.5, 0, 0, -1,

                         -0.5, -0.5, +0.5, 0, 0, 1,
                         +0.5, -0.5, +0.5, 0, 0, 1,
                         +0.5, +0.5, +0.5, 0, 0, 1,
                         -0.5, +0.5, +0.5, 0, 0, 1,

                         -0.5, -0.5, -0.5, 0, -1, 0,
                         +0.5, -0.5, -0.5, 0, -1, 0,
                         -0.5, -0.5, +0.5, 0, -1, 0,
                         +0.5, -0.5, +0.5, 0, -1, 0,

                         -0.5, +0.5, -0.5, 0, 1, 0,
                         +0.5, +0.5, -0.5, 0, 1, 0,
                         -0.5, +0.5, +0.5, 0, 1, 0,
                         +0.5, +0.5, +0.5, 0, 1, 0,

                         -0.5, -0.5, -0.5, -1, 0, 0,
                         -0.5, +0.5, -0.5, -1, 0, 0,
                         -0.5, -0.5, +0.5, -1, 0, 0,
                         -0.5, +0.5, +0.5, -1, 0, 0,

                         +0.5, -0.5, -0.5, 1, 0, 0,
                         +0.5, +0.5, -0.5, 1, 0, 0,
                         +0.5, -0.5, +0.5, 1, 0, 0,
                         +0.5, +0.5, +0.5, 1, 0, 0,
                         ]

cube_indices = [0, 1, 2, 0, 2, 3,
                4, 5, 6, 4, 6, 7,
                8, 11, 9, 8, 11, 10,
                12, 15, 13, 12, 15, 14,
                16, 17, 18, 17, 18, 19,
                20, 22, 21, 21, 23, 22
                ]

qvao = GLuint(0)
glGenVertexArrays(1, qvao)
glBindVertexArray(qvao)

qvbo = GLuint(0)
glGenBuffers(1, qvbo)

glBindBuffer(GL_ARRAY_BUFFER, qvbo)
glBufferData(GL_ARRAY_BUFFER, len(cube_vertex_positions) * float_size,
             (GLfloat * len(cube_vertex_positions))(*cube_vertex_positions), GL_STATIC_DRAW)

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)

glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
glEnableVertexAttribArray(1)

qibo = GLuint(0)
glGenBuffers(1, qibo)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, qibo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(cube_indices) * int_size,
             (GLuint * len(cube_indices))(*cube_indices), GL_STATIC_DRAW)

once = True
sphere_angle = 0
angle_x = 0
angle_y = 90
angle_z = 0
eye_x = 0
eye_y = 0
eye_z = -10
w_pressed = False
a_pressed = False
s_pressed = False
d_pressed = False


@window.event
def on_draw():
    global once, tree_list
    window.clear()

    if once:
        glClearColor(0, 0.25, 0.5, 1)
        glEnable(GL_DEPTH_TEST)
        pm = pyrr.matrix44.create_perspective_projection(45.0, 800.0 / 600.0, 0.1, 100.0)
        projection_vector = matrix_to_single_dim(pm)
        glUniformMatrix4fv(projection_matrix, 1, GL_FALSE, (GLfloat * len(projection_vector))(*projection_vector))

        glUniform3f(ambient_color, 0.2, 0.2, 0.2)
        glUniform3f(diffuse_color, 0.4, 0.4, 0.4)

        once = False

    t = pyrr.matrix44.create_look_at([0, 0, 0], [0, 0, 1], [0, 1, 0])
    v = matrix_to_single_dim(t)
    glUniformMatrix4fv(view_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))

    # floor
    glBindVertexArray(vao)
    qt1 = pyrr.matrix44.create_from_translation([1.5, 0, 5])
    qtr = pyrr.matrix44.create_from_x_rotation(-math.pi / 2.0)
    qtr2 = pyrr.matrix44.create_from_y_rotation(sphere_angle / 180.0 * math.pi)
    qt2 = pyrr.matrix44.create_from_scale([2, 2, 2])
    t = pyrr.matrix44.multiply(pyrr.matrix44.multiply(pyrr.matrix44.multiply(qt2, qtr), qtr2), qt1)
    v = matrix_to_single_dim(t)
    glUniformMatrix4fv(transform_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))
    glDrawElements(GL_TRIANGLES, len(sphere_indices), GL_UNSIGNED_INT, 0)


    #cube
    glBindVertexArray(qvao)
    qt1 = pyrr.matrix44.create_from_translation([-1.5, 0, 5])
    qtr = pyrr.matrix44.create_from_x_rotation(-math.pi / 2.0)
    qtr2 = pyrr.matrix44.create_from_y_rotation(sphere_angle / 180.0 * math.pi)
    qt2 = pyrr.matrix44.create_from_scale([1.5, 1.5, 1.5])
    t = pyrr.matrix44.multiply(pyrr.matrix44.multiply(pyrr.matrix44.multiply(qt2, qtr), qtr2), qt1)
    v = matrix_to_single_dim(t)
    glUniformMatrix4fv(transform_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))
    glDrawElements(GL_TRIANGLES, len(cube_indices), GL_UNSIGNED_INT, 0)


@window.event
def on_key_press(key, modifiers):
    global w_pressed, a_pressed, s_pressed, d_pressed, rotating
    if key == pyglet.window.key.W:
        w_pressed = True
    if key == pyglet.window.key.A:
        a_pressed = True
    if key == pyglet.window.key.S:
        s_pressed = True
    if key == pyglet.window.key.D:
        d_pressed = True
    if key == pyglet.window.key.SPACE:
        rotating = not rotating


@window.event
def on_key_release(key, modifiers):
    global w_pressed, a_pressed, s_pressed, d_pressed
    if key == pyglet.window.key.W:
        w_pressed = False
    if key == pyglet.window.key.A:
        a_pressed = False
    if key == pyglet.window.key.S:
        s_pressed = False
    if key == pyglet.window.key.D:
        d_pressed = False


@window.event
def on_mouse_motion(x, y, dx, dy):
    global angle_x, angle_y

    angle_y = angle_y - 1 * dx
    angle_x = angle_x + 0.4 * dy

    if angle_x > 40:
        angle_x = 40
    elif angle_x < -40:
        angle_x = -40


@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)


def sinDegree(degree):
    return math.sin(math.radians(degree))


def cosDegree(degree):
    return math.cos(math.radians(degree))


def update(dt):
    global angle_y, eye_x, eye_z, angle_y, rotating, sphere_angle
    global w_pressed, a_pressed, s_pressed, d_pressed

    if rotating:
        sphere_angle = sphere_angle + 30 * dt

    glUniform3f(light_direction, 1, 0, -0.5)
    if w_pressed:
        eye_x = eye_x + 1 * math.sin(math.radians(angle_y))
        eye_z = eye_z + 1 * math.cos(math.radians(angle_y))
    if s_pressed:
        eye_x = eye_x - 1 * math.sin(math.radians(angle_y))
        eye_z = eye_z - 1 * math.cos(math.radians(angle_y))
    if a_pressed:
        eye_x = eye_x + 1 * math.sin(math.radians(angle_y + 90))
        eye_z = eye_z + 1 * math.cos(math.radians(angle_y + 90))
    if d_pressed:
        eye_x = eye_x - 1 * math.sin(math.radians(angle_y + 90))
        eye_z = eye_z - 1 * math.cos(math.radians(angle_y + 90))


pyglet.clock.schedule_interval(update, 1 / 120.0)
pyglet.app.run()
