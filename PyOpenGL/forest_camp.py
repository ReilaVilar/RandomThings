from pyglet.gl import *
import random
import pyrr
import OpenGL.GL.shaders
import ctypes
import OpenGL
import math

player_x = 0
player_y = 1
player_z = -10
player_y_angle = 90
player_x_angle = 90

int_size = 4
float_size = 4
lightOn_1 = True
lightOn_2 = True
sky_move_on = True
skyLight_on = True
ambient = 0.5


def matrix_to_single_dim(m):
    return [y for x in m for y in x]


class Tree:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.width = 1
        self.height = 1
        self.size = 3 / random.randint(1, 5)
        self.rotation = random.randint(0, 90)

    def draw(self):
        scale_transform = pyrr.matrix44.create_from_scale([self.size, self.size, self.size])
        rotation_transform = pyrr.matrix44.create_from_y_rotation(self.rotation)
        position_transform = pyrr.matrix44.create_from_translation([self.x, self.y, self.z])
        compound_transform = pyrr.matrix44.multiply(pyrr.matrix44.multiply(scale_transform, rotation_transform),
                                                    position_transform)

        glUniform1i(useTexture, True)
        # Tree body
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture_bark)
        glBindVertexArray(vao)
        qt1 = pyrr.matrix44.create_from_translation([0, -0.5 - 1 + self.size, 0])
        qt2 = pyrr.matrix44.create_from_scale([1, 5, 1])
        t = pyrr.matrix44.multiply(pyrr.matrix44.multiply(qt2, qt1), compound_transform)
        v = matrix_to_single_dim(t)
        glUniformMatrix4fv(transform_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))
        glUniform2f(tex_scale, 1.0, 2.0)
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, 0)

        # Tree Leaves
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture_leaf)
        glBindVertexArray(vao)
        qt1 = pyrr.matrix44.create_from_translation([0, 2.5 - 1 + self.size, 0])
        qt2 = pyrr.matrix44.create_from_scale([3, 3, 3])
        t = pyrr.matrix44.multiply(pyrr.matrix44.multiply(qt2, qt1), compound_transform)
        v = matrix_to_single_dim(t)
        glUniformMatrix4fv(transform_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))
        glUniform2f(tex_scale, 1.0, 1.0)
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, 0)


tree_list = []
for i in range(15):
    t = Tree(random.randint(-75, 75), 0, random.randint(-75, 75))
    tree_list.append(t)


class Cloud:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def draw(self):
        position_transform = pyrr.matrix44.create_from_translation([self.x, self.y, self.z])
        glUniform3f(ambient_color, ambient * 0.7, ambient * 0.7, ambient * 0.7)
        glUniform4f(object_color, 1, 1, 1, 0.4)
        glUniform1i(useTexture, False)
        glEnable(GL_BLEND)
        glBindVertexArray(vao)
        qt1 = pyrr.matrix44.create_from_translation([0, 0.5, 0])
        qt2 = pyrr.matrix44.create_from_scale([2, 1, 3])
        t = pyrr.matrix44.multiply(pyrr.matrix44.multiply(qt2, qt1), position_transform)
        v = matrix_to_single_dim(t)
        glUniformMatrix4fv(transform_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, 0)

        glBindVertexArray(vao)
        qt1 = pyrr.matrix44.create_from_translation([0, -0.5, 2])
        qt2 = pyrr.matrix44.create_from_scale([2, 1, 2])
        t = pyrr.matrix44.multiply(pyrr.matrix44.multiply(qt2, qt1), position_transform)
        v = matrix_to_single_dim(t)
        glUniformMatrix4fv(transform_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, 0)

        glBindVertexArray(vao)
        qt1 = pyrr.matrix44.create_from_translation([0, -0.5, -2])
        qt2 = pyrr.matrix44.create_from_scale([2, 1, 2])
        t = pyrr.matrix44.multiply(pyrr.matrix44.multiply(qt2, qt1), position_transform)
        v = matrix_to_single_dim(t)
        glUniformMatrix4fv(transform_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, 0)
        glDisable(GL_BLEND)


cloud_list = []
for i in range(20):
    c = Cloud(random.randint(-75, 75), random.randint(18, 23), random.randint(-75, 75))
    cloud_list.append(c)


class StreetLight:
    def __init__(self, x, z):
        self.x = x
        self.y = 4
        self.z = z
        self.lightOn = True
        self.lightPosition = 0

    def draw(self):
        position_transform = pyrr.matrix44.create_from_translation([self.x, self.y, self.z])

        glUniform3f(self.lightPosition, self.x, self.y, self.z)
        glUniform1i(useTexture, False)
        glUniform3f(ambient_color, 1, 1, 1)

        if self.lightOn:
            glUniform4f(object_color, 1, 1, 0.5, 1)
        else:
            glUniform4f(object_color, 0.3, 0.3, 0.1, 1)

        glBindVertexArray(vao)
        qt1 = pyrr.matrix44.create_from_translation([0, 0, 0])
        qt2 = pyrr.matrix44.create_from_scale([1, 1.4, 1])
        t = pyrr.matrix44.multiply(pyrr.matrix44.multiply(qt2, qt1), position_transform)
        v = matrix_to_single_dim(t)
        glUniformMatrix4fv(transform_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, 0)

        # top decor
        glUniform4f(object_color, 0.4, 0.3, 0.2, 1)
        glBindVertexArray(vao)
        qt1 = pyrr.matrix44.create_from_translation([0, 0.7, 0])
        qt2 = pyrr.matrix44.create_from_scale([1.4, 0.2, 1.4])
        t = pyrr.matrix44.multiply(pyrr.matrix44.multiply(qt2, qt1), position_transform)
        v = matrix_to_single_dim(t)
        glUniformMatrix4fv(transform_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, 0)

        # lamp stick
        glUniform4f(object_color, 0.3, 0.2, 0.1, 1)
        glBindVertexArray(vao)
        qt1 = pyrr.matrix44.create_from_translation([0, -4, 0])
        qt2 = pyrr.matrix44.create_from_scale([0.3, 8, 0.3])
        t = pyrr.matrix44.multiply(pyrr.matrix44.multiply(qt2, qt1), position_transform)
        v = matrix_to_single_dim(t)
        glUniformMatrix4fv(transform_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, 0)

    def update(self, u):
        self.lightOn = u


street_light_list = []
sl = StreetLight(-15, 20)
sl.lightOn = lightOn_1
street_light_list.append(sl)
sl2 = StreetLight(-5, 0)
sl2.lightOn = lightOn_2
street_light_list.append(sl2)


class SunMoon:
    def __init__(self):
        self.x = 0
        self.y = 90
        self.z = 0
        self.speed = 0.4
        self.sun_angle = 0

    def draw(self):
        global player_x
        glUniform1i(useTexture, False)
        glUniform3f(ambient_color, 1, 1, 1)

        # Sun
        glUniform4f(object_color, 1, 0.9, 0.4, 1)
        glBindVertexArray(svao)
        qt1 = pyrr.matrix44.create_from_translation([self.x, self.y, self.z])
        qtr = pyrr.matrix44.create_from_x_rotation(-math.pi / 2.0)
        qt2 = pyrr.matrix44.create_from_scale([5, 5, 5])
        t = pyrr.matrix44.multiply(pyrr.matrix44.multiply(qt2, qtr), qt1)
        v = matrix_to_single_dim(t)
        glUniformMatrix4fv(transform_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))
        glDrawElements(GL_TRIANGLES, len(sphere_indices), GL_UNSIGNED_INT, 0)

        # Moon
        glUniform4f(object_color, 0.6, 0.6, 0.55, 1)
        glBindVertexArray(svao)
        qt1 = pyrr.matrix44.create_from_translation([-self.x, -self.y, self.z])
        qtr = pyrr.matrix44.create_from_x_rotation(-math.pi / 2.0)
        qt2 = pyrr.matrix44.create_from_scale([5, 5, 5])
        t = pyrr.matrix44.multiply(pyrr.matrix44.multiply(qt2, qtr), qt1)
        v = matrix_to_single_dim(t)
        glUniformMatrix4fv(transform_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))
        glDrawElements(GL_TRIANGLES, len(sphere_indices), GL_UNSIGNED_INT, 0)

    def update(self, dt):
        global skyLight_on, ambient
        rotation_radius = 150
        center_x = 0
        center_y = 0

        if not skyLight_on:
            glUniform1i(sky_light_on, False)
            glUniform1i(sun_light_on, False)
        elif self.y >= 0:
            glUniform1i(sky_light_on, True)
            glUniform1i(sun_light_on, True)
        elif self.y <= 0:
            glUniform1i(sky_light_on, True)
            glUniform1i(sun_light_on, False)

        if sky_move_on:
            self.sun_angle = self.sun_angle + self.speed * dt
            self.x = center_x + rotation_radius * math.cos(self.sun_angle)
            self.y = center_y + rotation_radius * math.sin(self.sun_angle)

            if self.y >= 0:
                if self.x >= 0:
                    ambient = ambient + dt * 0.4
                if self.x <= 0:
                    ambient = ambient - dt * 0.4
            if self.y <= 0:
                if self.x >= 0:
                    ambient = ambient - dt * 0.1
                if self.x <= 0:
                    ambient = ambient + dt * 0.1
        glUniform3f(ambient_color, ambient * 0.1, ambient * 0.1, ambient * 0.1)
        glUniform3f(sun_light_direction, (self.x - player_x) * 10, self.y * 10, player_z)


sunMoon = SunMoon()


def legs(x, z, width, height, breadth, legsize):
    scale_transform = pyrr.matrix44.create_from_scale([width / 2, height, breadth / 2])
    position_transform = pyrr.matrix44.create_from_translation([x, -height / 2, z])
    compound_transform = pyrr.matrix44.multiply(scale_transform, position_transform)

    glUniform1i(useTexture, True)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture_bark)
    glBindVertexArray(vao)
    qt1 = pyrr.matrix44.create_from_translation([width / 2, 0, breadth / 2])
    qt2 = pyrr.matrix44.create_from_scale([legsize, height, legsize])
    t = pyrr.matrix44.multiply(pyrr.matrix44.multiply(qt2, qt1), compound_transform)
    v = matrix_to_single_dim(t)
    glUniformMatrix4fv(transform_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))
    glUniform2f(tex_scale, 0.3, 0.4)
    glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, 0)

    glBindVertexArray(vao)
    qt1 = pyrr.matrix44.create_from_translation([-width / 2, 0, breadth / 2])
    qt2 = pyrr.matrix44.create_from_scale([legsize, height, legsize])
    t = pyrr.matrix44.multiply(pyrr.matrix44.multiply(qt2, qt1), compound_transform)
    v = matrix_to_single_dim(t)
    glUniformMatrix4fv(transform_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))
    glUniform2f(tex_scale, 0.3, 0.4)
    glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, 0)

    glBindVertexArray(vao)
    qt1 = pyrr.matrix44.create_from_translation([width / 2, 0, -breadth / 2])
    qt2 = pyrr.matrix44.create_from_scale([legsize, height, legsize])
    t = pyrr.matrix44.multiply(pyrr.matrix44.multiply(qt2, qt1), compound_transform)
    v = matrix_to_single_dim(t)
    glUniformMatrix4fv(transform_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))
    glUniform2f(tex_scale, 0.3, 0.4)
    glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, 0)

    glBindVertexArray(vao)
    qt1 = pyrr.matrix44.create_from_translation([-width / 2, 0, -breadth / 2])
    qt2 = pyrr.matrix44.create_from_scale([legsize, height, legsize])
    t = pyrr.matrix44.multiply(pyrr.matrix44.multiply(qt2, qt1), compound_transform)
    v = matrix_to_single_dim(t)
    glUniformMatrix4fv(transform_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))
    glUniform2f(tex_scale, 0.3, 0.4)
    glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, 0)

def table(x, y, z, width, breadth):
    position_transform = pyrr.matrix44.create_from_translation([x, y, z])

    glUniform1i(useTexture, True)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture_bark)
    glBindVertexArray(vao)
    qt1 = pyrr.matrix44.create_from_translation([0, 0, 0])
    qt2 = pyrr.matrix44.create_from_scale([width, 0.5, breadth])
    t = pyrr.matrix44.multiply(pyrr.matrix44.multiply(qt2, qt1), position_transform)
    v = matrix_to_single_dim(t)
    glUniformMatrix4fv(transform_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))
    glUniform2f(tex_scale, 1.0, 1.0)
    glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, 0)


vert_shader = """
  #version 330
  in layout (location = 0) vec3 position;
  in layout (location = 1) vec3 color;
  in layout (location = 2) vec2 tC;
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
      fragTex = tC;
  }
"""

frag_shader = """
 #version 330
 out vec4 outColor;
 in vec3 fragNormal;
 in vec3 fragPos;
 in vec3 fragColor;
 in vec2 fragTex;

 uniform vec3 camera_position;
 uniform vec3 ambient_color;
 uniform float shininess;

 struct Light{
    vec3 position;
    vec3 diffuse_color;
    vec3 specular_color;
    bool on;
 };

 uniform Light light_1;
 uniform Light light_2;

 uniform float constant;
 uniform float linear;
 uniform float quadratic;


 uniform vec2 tex_scale;
 uniform sampler2D tex;
 uniform bool useTexture;
 uniform vec4 object_color;


 uniform vec3 sky_ambient_color;
 uniform vec3 sky_color;

 uniform vec3 sun_light_direction;
 uniform vec3 sun_diffuse_color;
 uniform vec3 moon_diffuse_color;

 uniform bool sun_light_on;
 uniform bool sky_light_on;

 void main()
 {
        vec3 light_1_lightDirection = normalize(light_1.position - fragPos);
        vec3 viewDir = normalize(camera_position - fragPos);
        vec3 light_1_reflectDir = reflect(-light_1_lightDirection , fragNormal);

        vec3 ambient_light = ambient_color;
        vec3 light_1_diffuse_light = light_1.diffuse_color * max(dot(fragNormal, light_1_lightDirection), 0.0);
        vec3 light_1_specular_light = light_1.specular_color * pow(max(dot(viewDir, light_1_reflectDir), 0.0), shininess);

        float light_1_distance = length(light_1.position - fragPos);
        float light_1_attenuation = 1.0 / (constant + linear * light_1_distance + quadratic * light_1_distance * light_1_distance);

        vec3 l1;

        vec3 light_2_lightDirection = normalize(light_2.position - fragPos);
        vec3 light_2_reflectDir = reflect(-light_2_lightDirection , fragNormal);

        vec3 light_2_diffuse_light = light_2.diffuse_color * max(dot(fragNormal, light_2_lightDirection), 0.0);
        vec3 light_2_specular_light = light_2.specular_color * pow(max(dot(viewDir, light_2_reflectDir), 0.0), shininess);

        float light_2_distance = length(light_2.position - fragPos);
        float light_2_attenuation = 1.0 / (constant + linear * light_2_distance + quadratic * light_2_distance * light_2_distance);

        vec3 l2;
        vec3 yellow = vec3(1.2, 1.2, 1);
        l1 = vec3(l1 * yellow);
        vec3 red = vec3(1.4, 1, 1);
        l2 = vec3(l2 * red);

        if(light_1.on)
        {
             l1 = ambient_light + (light_1_diffuse_light + light_1_specular_light) * light_1_attenuation;
        }
        else
        {
             l1 = ambient_light;
        }
        if(light_2.on)
        {
             l2 = ambient_light + (light_2_diffuse_light + light_2_specular_light) * light_2_attenuation;
        }
        else
        {
             l2 = ambient_light;
        }

        vec3 street_light = l1 + l2;

        // Sky 
        vec3 sky_lightDirection = normalize(sun_light_direction - fragPos);
        vec3 sky_diffuse_light = sun_diffuse_color * max(dot(fragNormal, sky_lightDirection), (0.0));
        vec3 sky_light = vec3(0.8, 0.8, 0.6);

        // Moon
        vec3 moon_lightDirection = -sky_lightDirection;
        vec3 moon_diffuse_light = moon_diffuse_color * max(dot(fragNormal, moon_lightDirection), (0.0));
        vec3 moon_light_color = vec3(0.7, 0.7, 1);

        if(sun_light_on && sky_light_on)
        {
             sky_light = ambient_light + sky_diffuse_light;
        }
        else if(!sun_light_on && sky_light_on)
        {
             sky_light = ambient_light + vec3(moon_diffuse_light * moon_light_color);
        }
        else
        {
             sky_light = ambient_light;
        }


        if(useTexture)
        {
            outColor = texture(tex, fragTex * tex_scale) * vec4(sky_light + street_light, 1.0f);
        }
        else
        {
            outColor = vec4(object_color) * vec4(sky_light * street_light, 1.0f);
        }

 }
"""

window = pyglet.window.Window(width=1240, height=800)

###### First Shader ######
shader = OpenGL.GL.shaders.compileProgram(
    OpenGL.GL.shaders.compileShader(vert_shader, GL_VERTEX_SHADER),
    OpenGL.GL.shaders.compileShader(frag_shader, GL_FRAGMENT_SHADER))

glUseProgram(shader)

transform_matrix = glGetUniformLocation(shader, b'transform')
projection_matrix = glGetUniformLocation(shader, b'projection')
view_matrix = glGetUniformLocation(shader, b'view')
tex_scale = glGetUniformLocation(shader, b'tex_scale')
tex = glGetUniformLocation(shader, b'tex')
glUniform1i(tex, 0)

useTexture = glGetUniformLocation(shader, b'useTexture')
glUniform1i(useTexture, True)
object_color = glGetUniformLocation(shader, b'object_color')
glUniform4f(object_color, 0, 0, 0, 1.0)

light_position1 = glGetUniformLocation(shader, b'light_1.position')
sl.lightPosition = light_position1
light_position2 = glGetUniformLocation(shader, b'light_2.position')
sl2.lightPosition = light_position2
camera_position = glGetUniformLocation(shader, b'camera_position')
ambient_color = glGetUniformLocation(shader, b'ambient_color')
diffuse_color1 = glGetUniformLocation(shader, b'light_1.diffuse_color')
specular_color1 = glGetUniformLocation(shader, b'light_1.specular_color')
diffuse_color2 = glGetUniformLocation(shader, b'light_2.diffuse_color')
specular_color2 = glGetUniformLocation(shader, b'light_2.specular_color')
shininess = glGetUniformLocation(shader, b'shininess')
constant = glGetUniformLocation(shader, b'constant')
linear = glGetUniformLocation(shader, b'linear')
quadratic = glGetUniformLocation(shader, b'quadratic')
light_on_1 = glGetUniformLocation(shader, b'light_1.on')
glUniform1i(light_on_1, True)
light_on_2 = glGetUniformLocation(shader, b'light_2.on')
glUniform1i(light_on_2, True)
# Directional Light - Sun&Moon
sun_light_direction = glGetUniformLocation(shader, b'sun_light_direction')
sun_diffuse_color = glGetUniformLocation(shader, b'sun_diffuse_color')
moon_diffuse_color = glGetUniformLocation(shader, b'moon_diffuse_color')
sun_light_on = glGetUniformLocation(shader, b'sun_light_on')
glUniform1i(sun_light_on, True)
sky_light_on = glGetUniformLocation(shader, b'sky_light_on')
glUniform1i(sky_light_on, True)

###### VAO for Sphere ######
sphere_vertex_data = []
sphere_indices = []
sphere_num_sectors = 100
sphere_num_stacks = 100

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


def push_vertex(position, normal):
    sphere_vertex_data.append(position[0])
    sphere_vertex_data.append(position[1])
    sphere_vertex_data.append(position[2])
    sphere_vertex_data.append(normal[0])
    sphere_vertex_data.append(normal[1])
    sphere_vertex_data.append(normal[2])


def get_normal(p1, p2, p3):
    u = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
    v = (p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2])

    x = u[1] * v[2] - u[2] * v[1]
    y = u[2] * v[0] - u[0] * v[2]
    z = u[0] * v[1] - u[1] * v[0]

    return [x, y, z]


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

svao = GLuint(0)
glGenVertexArrays(1, svao)
glBindVertexArray(svao)

svbo = GLuint(0)
glGenBuffers(1, svbo)

glBindBuffer(GL_ARRAY_BUFFER, svbo)
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

###### VAO for Cube ######
cube_vertex_positions = [-0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, -1.0,  # Front Face, Bottom Left   (0)
                         +0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, -1.0,  # Front Face, Bottom Right  (1)
                         +0.5, +0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, -1.0,  # Front Face, Upper Right   (2)
                         -0.5, +0.5, -0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, -1.0,  # Front Face, Upper Left    (3)

                         -0.5, -0.5, +0.5, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, +1.0,  # Back Face, Bottom Left    (4)
                         +0.5, -0.5, +0.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, +1.0,  # Back Face, Bottom Right   (5)
                         +0.5, +0.5, +0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, +1.0,  # Back Face, Upper Right    (6)
                         -0.5, +0.5, +0.5, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, +1.0,  # Back Face, Upper Left     (7)

                         -0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, -1.0, 0.0,  # Front Face, Bottom Left   (8)
                         +0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0, 0.0,  # Front Face, Bottom Right  (9)
                         -0.5, -0.5, +0.5, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, -1.0, 0.0,  # Back Face, Bottom Left    (10)
                         +0.5, -0.5, +0.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, -1.0, 0.0,  # Back Face, Bottom Right   (11)

                         -0.5, +0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, +1.0, 0.0,  # Front Face, Upper Left    (12)
                         +0.5, +0.5, -0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, +1.0, 0.0,  # Front Face, Upper Right   (13)
                         -0.5, +0.5, +0.5, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, +1.0, 0.0,  # Back Face, Upper Left     (14)
                         +0.5, +0.5, +0.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, +1.0, 0.0,  # Back Face, Upper Right    (15)

                         -0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 0.0, -1.0, 0.0, 0.0,  # Front Face, Bottom Left   (16)
                         -0.5, +0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 1.0, -1.0, 0.0, 0.0,  # Front Face, Upper Left    (17)
                         -0.5, -0.5, +0.5, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0, 0.0, 0.0,  # Back Face, Bottom Left    (18)
                         -0.5, +0.5, +0.5, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, 0.0, 0.0,  # Back Face, Upper Left     (19)

                         +0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 1.0, 0.0, +1.0, 0.0, 0.0,  # Front Face, Bottom Right  (20)
                         +0.5, +0.5, -0.5, 1.0, 1.0, 1.0, 1.0, 1.0, +1.0, 0.0, 0.0,  # Front Face, Upper Right   (21)
                         +0.5, -0.5, +0.5, 1.0, 1.0, 1.0, 0.0, 0.0, +1.0, 0.0, 0.0,  # Back Face, Bottom Right   (22)
                         +0.5, +0.5, +0.5, 1.0, 1.0, 1.0, 0.0, 1.0, +1.0, 0.0, 0.0  # Back Face, Upper Right    (23)
                         ]

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

######  VAO for Quad ######
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
glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(quad_indices) * int_size,
             (GLuint * len(quad_indices))(*quad_indices), GL_STATIC_DRAW)

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 11 * 4, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)

glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 11 * 4, ctypes.c_void_p(20))
glEnableVertexAttribArray(1)

glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 11 * 4, ctypes.c_void_p(12))
glEnableVertexAttribArray(2)

glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, 11 * 4, ctypes.c_void_p(32))
glEnableVertexAttribArray(3)

######  Textures  ######
glEnable(GL_TEXTURE_2D)

grass_image = pyglet.image.load('grass.jpg')
texture_grass = grass_image.get_texture().id

bark_image = pyglet.image.load('bark.jpg')
texture_bark = bark_image.get_texture().id

leaf_image = pyglet.image.load('leaf.jpg')
texture_leaf = leaf_image.get_texture().id

glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)

glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

once = True


@window.event
def on_draw():
    global once
    window.clear()
    glUseProgram(shader)

    if once:
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        pm = pyrr.matrix44.create_perspective_projection(45.0, 1240.0 / 800.0, 0.1, 200.0)
        projection_vector = matrix_to_single_dim(pm)
        glUniformMatrix4fv(projection_matrix, 1, GL_FALSE, (GLfloat * len(projection_vector))(*projection_vector))
        once = False
    glDisable(GL_BLEND)

    t = pyrr.matrix44.create_look_at([player_x, player_y, player_z],
                                     [player_x + CosDegree(player_y_angle), SinDegree(player_x_angle),
                                      player_z + SinDegree(player_y_angle)],
                                     [0, 1, 0])
    v = matrix_to_single_dim(t)
    glUniformMatrix4fv(view_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))

    # Render ground
    glUniform1i(useTexture, True)
    glBindVertexArray(qvao)
    qt1 = pyrr.matrix44.create_from_translation([0, -2, 0])
    qt2 = pyrr.matrix44.create_from_scale([300, 1, 300])
    t = pyrr.matrix44.multiply(qt2, qt1)
    v = matrix_to_single_dim(t)
    glUniformMatrix4fv(transform_matrix, 1, GL_FALSE, (GLfloat * len(v))(*v))
    glUniform2f(tex_scale, 100.0, 100.0)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture_grass)
    glDrawElements(GL_TRIANGLES, len(quad_indices), GL_UNSIGNED_INT, 0)

    # Render trees
    for t in tree_list:
        t.draw()

    # Render Street Lights
    for sl in street_light_list:
        sl.draw()

    # Render decorations
    table(-10, 0.5, 10, 4, 8)
    legs(-10, 10, 2, 1.5, 4, 0.09)

    # Render clouds
    for c in cloud_list:
        c.draw()

    # Render Sun & Moon
    sunMoon.draw()


@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)


def SinDegree(degree):
    return math.sin(math.radians(degree))


def CosDegree(degree):
    return math.cos(math.radians(degree))


key_w = False
key_s = False
key_a = False
key_d = False


def update(dt):
    global player_x, player_y, player_z
    global key_w, key_s, key_a, key_d
    global player_x_angle, player_y_angle

    glClearColor(ambient * 0.2, ambient * 0.2, ambient * 0.5, 1)
    glUniform3f(ambient_color, 0.1, 0.1, 0.1)

    if key_w:
        player_x = player_x + 15 * dt * CosDegree(player_y_angle)
        player_z = player_z + 15 * dt * SinDegree(player_y_angle)
    if key_s:
        player_x = player_x - 15 * dt * CosDegree(player_y_angle)
        player_z = player_z - 15 * dt * SinDegree(player_y_angle)
    if key_a:
        player_x = player_x - 15 * dt * CosDegree(player_y_angle + 90)
        player_z = player_z - 15 * dt * SinDegree(player_y_angle + 90)
    if key_d:
        player_x = player_x - 15 * dt * CosDegree(player_y_angle - 90)
        player_z = player_z - 15 * dt * SinDegree(player_y_angle - 90)
    if player_x <= -100:
        player_x = -100
    if player_x >= 100:
        player_x = 100
    if player_z <= -100:
        player_z = -100
    if player_z >= 100:
        player_z = 100

    glUniform3f(camera_position, player_x, player_y, player_z)
    glUniform3f(diffuse_color1, 0.4, 0.4, 0.4)
    glUniform3f(specular_color1, 0.4, 0.4, 0.4)
    glUniform3f(diffuse_color2, 0.4, 0.4, 0.4)
    glUniform3f(specular_color2, 0.4, 0.4, 0.4)
    glUniform1f(shininess, 12)

    glUniform1f(constant, 1.0)
    glUniform1f(linear, 0.05)
    glUniform1f(constant, 0.032)

    sunMoon.update(dt)
    glUniform3f(sun_diffuse_color, 0.7, 0.7, 0.7)
    glUniform3f(moon_diffuse_color, 0.25, 0.25, 0.4)


@window.event
def on_key_press(key, e):
    global key_w, key_s, key_a, key_d
    global lightOn_1, lightOn_2, sky_move_on, skyLight_on
    if key == pyglet.window.key.W:
        key_w = True
    if key == pyglet.window.key.S:
        key_s = True
    if key == pyglet.window.key.A:
        key_a = True
    if key == pyglet.window.key.D:
        key_d = True
    if key == pyglet.window.key._1:
        if lightOn_1:
            lightOn_1 = False
            glUniform1i(light_on_1, False)
        else:
            lightOn_1 = True
            glUniform1i(light_on_1, True)
        sl.update(lightOn_1)
    if key == pyglet.window.key._2:
        if lightOn_2:
            lightOn_2 = False
            glUniform1i(light_on_2, False)
        else:
            lightOn_2 = True
            glUniform1i(light_on_2, True)
        sl2.update(lightOn_2)
    if key == pyglet.window.key._3:
        sky_move_on = not sky_move_on
    if key == pyglet.window.key._4:
        skyLight_on = not skyLight_on


@window.event
def on_key_release(key, e):
    global key_w, key_s, key_a, key_d
    if key == pyglet.window.key.W:
        key_w = False
    if key == pyglet.window.key.S:
        key_s = False
    if key == pyglet.window.key.A:
        key_a = False
    if key == pyglet.window.key.D:
        key_d = False


@window.event
def on_mouse_motion(x, y, dx, dy):
    global player_x_angle, player_y_angle
    player_x_angle = player_x_angle + dy
    player_y_angle = player_y_angle + dx

    if player_x_angle > 90:
        player_x_angle = 90
    elif player_x_angle < -90:
        player_x_angle = -90


pyglet.clock.schedule_interval(update, 1 / 120.0)
pyglet.app.run()
