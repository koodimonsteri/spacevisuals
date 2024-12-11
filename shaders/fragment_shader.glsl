#version 330 core
#include "shaders/lygia/generative/snoise.glsl"
in vec2 texCoords;
out vec4 fragColor;

uniform sampler2D noiseTexture;

void main() {
    vec3 color = texture(noiseTexture, texCoords).rgb;
    fragColor = vec4(color, 1.0);
}