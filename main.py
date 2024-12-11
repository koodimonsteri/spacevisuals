import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import noise

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


def generate_noise_texture(width, height, scale, time):
    """Generate a 2D Perlin noise texture."""
    texture = np.zeros((width, height, 3), dtype=np.float32)
    for x in range(width):
        for y in range(height):
            value = noise.pnoise3(
                x / scale, y / scale, time, octaves=6, persistence=0.5, lacunarity=2.0
            )
            value = (value + 1) / 2  # Normalize to 0-1
            texture[x][y] = [
                value * 0.5,  # Red channel
                value * 0.8 * (1 - value),  # Green channel
                value * 0.3  # Blue channel
            ]
    return texture


def create_texture(texture_data):
    """Create an OpenGL texture from numpy array."""
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture_data.shape[0], texture_data.shape[1], 0, GL_RGB, GL_FLOAT, texture_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture_id


def create_quad_vao():
    """Create a VAO for a full-screen quad."""
    vertices = np.array([
        -1.0, -1.0,
         1.0, -1.0,
         1.0,  1.0,
        -1.0,  1.0
    ], dtype=np.float32)

    indices = np.array([
        0, 1, 2,
        2, 3, 0
    ], dtype=np.uint32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * vertices.itemsize, None)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return vao


def main():
    pygame.init()
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)

    vertex_shader = open("shaders/vertex_shader.glsl", "r").read()
    fragment_shader = open("shaders/fragment_shader.glsl", "r").read()
    shader = compileProgram(
        compileShader(vertex_shader, GL_VERTEX_SHADER),
        compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    )

    glUseProgram(shader)

    quad_vao = create_quad_vao()
    glEnable(GL_TEXTURE_2D)

    clock = pygame.time.Clock()
    time = 0.0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        noise_texture = generate_noise_texture(256, 256, 200.0, time)
        texture_id = create_texture(noise_texture)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glBindVertexArray(quad_vao)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        pygame.display.flip()

        glDeleteTextures([texture_id])

        time += 0.005  # Slower animation
        clock.tick(60)

if __name__ == "__main__":
    main()
