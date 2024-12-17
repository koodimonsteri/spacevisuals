import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
#import noise
import time
import logging


from shader import check_program_link, check_shader_compile, preprocess_shader

logger = logging.getLogger(__name__)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


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

    vertex_shader = preprocess_shader("shaders/vertex_shader.glsl")
    fragment_shader = preprocess_shader("shaders/fragment_shader.glsl")
    print(fragment_shader)
    vertex_shader_obj = compileShader(vertex_shader, GL_VERTEX_SHADER)
    fragment_shader_obj = compileShader(fragment_shader, GL_FRAGMENT_SHADER)

    check_shader_compile(vertex_shader_obj, "Vertex Shader")
    check_shader_compile(fragment_shader_obj, "Fragment Shader")

    shader = compileProgram(vertex_shader_obj, fragment_shader_obj)
    check_program_link(shader)

    glUseProgram(shader)

    quad_vao = create_quad_vao()

    clock = pygame.time.Clock()
    frame_count = 0
    start_time = time.time()
    fps_time = start_time
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        current_time = time.time()
        delta = current_time - start_time
        time_location = glGetUniformLocation(shader, "u_time")
        if time_location == -1:
            logger.error("Uniform 'u_time' not found in shader.")
        else:
            glUniform1f(time_location, delta)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBindVertexArray(quad_vao)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        pygame.display.flip()

        frame_count += 1
        elapsed_time = time.time() - fps_time
        if elapsed_time >= 1.0:
            fps = frame_count / elapsed_time
            logger.info("FPS: %.2f}", fps)
            logger.info('current time: %s', current_time)
            frame_count = 0
            fps_time = time.time()
        
        clock.tick(60)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
