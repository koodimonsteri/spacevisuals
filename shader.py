import logging
from pathlib import Path

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

logger = logging.getLogger(__name__)

def read_shader_file(file_path: Path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return ""


def compile_shader(shader_type, shader_code):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, shader_code)
    glCompileShader(shader)
    
    compile_status = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if not compile_status:
        error_message = glGetShaderInfoLog(shader)
        print(f"Shader compile failed: {error_message}")
        sys.exit(1)
    
    return shader


def create_shader_program(vertex_shader_code, fragment_shader_code):
    vertex_shader = compile_shader(GL_VERTEX_SHADER, vertex_shader_code)
    fragment_shader = compile_shader(GL_FRAGMENT_SHADER, fragment_shader_code)
    
    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)
    
    link_status = glGetProgramiv(shader_program, GL_LINK_STATUS)
    if not link_status:
        error_message = glGetProgramInfoLog(shader_program)
        print(f"Shader program link failed: {error_message}")
        sys.exit(1)
    
    return shader_program


def preprocess_shader(shader_path):
    """Preprocesses the shader, resolving #include statements."""
    shader_code = read_shader_file(shader_path)
    
    while "#include" in shader_code:
        include_start = shader_code.find("#include")

        start_quote = shader_code.find('"', include_start) + 1
        end_quote = shader_code.find('"', start_quote)

        include_file = shader_code[start_quote:end_quote]
        
        #include_path = Path(shader_path) / include_file
        include_path = Path(include_file)
        include_code = read_shader_file(include_path)
        
        shader_code = shader_code[:include_start] + include_code + shader_code[end_quote + 1:]

    return shader_code


def check_shader_compile(shader, shader_type):
    compile_status = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if not compile_status:
        error_message = glGetShaderInfoLog(shader).decode('utf-8')
        logger.error(f"Shader compile error ({shader_type}): {error_message}")
    else:
        logger.info(f"{shader_type} compiled successfully!")

def check_program_link(program):
    link_status = glGetProgramiv(program, GL_LINK_STATUS)
    if not link_status:
        error_message = glGetProgramInfoLog(program).decode('utf-8')
        logger.error(f"Program link error: {error_message}")
    else:
        logger.info("Program linked successfully!")


if __name__ == '__main__':
    #sh = preprocess_shader('shaders/vertex_shader.glsl')
    sh = preprocess_shader("shaders/lygia/generative/pnoise.glsl")
    print(sh)