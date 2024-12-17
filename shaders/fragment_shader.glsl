#version 330 core
#include "shaders/lygia/generative/snoise.glsl"
in vec2 texCoords;
out vec4 fragColor;

uniform float u_time;

void main() {
    float rep = 60.0; // total time
    float time_scale = 0.02;
    float time = mod(u_time, rep) * time_scale; // Keeps time within [0, rep]
    float noise_scale = 3.0;
    vec2 uv = texCoords * noise_scale; // Increase scale

    // base noise
    float n = snoise(vec3(uv, time));

    // detailed noise
    float detail = snoise(vec3(uv * 2.5, time * 0.5)) * 0.4;
    n += detail;
    n = clamp(n, 0.0, 1.0);  // Ensure noise stays in [0, 1]

    // nebula colors
    vec3 purple = vec3(0.4, 0.1, 0.6);  // Deep purple
    vec3 blue = vec3(0.1, 0.2, 0.5);    // Deep blue
    vec3 pink = vec3(0.7, 0.3, 0.5);    // Pink highlight
    vec3 teal = vec3(0.1, 0.5, 0.4);    // Subtle teal

    // Blend colors based on noise intensity
    //vec3 baseColor = mix(purple, blue, n);
    vec3 baseColor = mix(purple, blue, smoothstep(0.0, 0.4, n)); 
    baseColor = mix(baseColor, pink, smoothstep(0.3, 0.7, n));
    baseColor = mix(baseColor, teal, smoothstep(0.5, 1.0, n));

    float vignette = 1.0 - dot(texCoords - 0.5, texCoords - 0.5) * 2.0;
    vignette = clamp(vignette, 0.0, 1.0);
    baseColor *= vignette;

    // Mix with black space
    vec3 finalColor = mix(vec3(0.0), baseColor, smoothstep(0.2, 0.7, n));

    fragColor = vec4(finalColor, 1.0);
}
