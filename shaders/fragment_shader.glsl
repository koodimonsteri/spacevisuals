#version 330 core
#include "shaders/lygia/generative/snoise.glsl"
in vec2 texCoords;
out vec4 fragColor;

uniform float u_time;

vec3 getNebulaClouds(vec2 _uv, float time) {
    // base noise
    vec2 uv = _uv * 2.0;
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

    return finalColor;
}

float random(vec2 uv) {
    return fract(sin(dot(uv, vec2(12.9898, 78.233))) * 43758.5453123);
}

// Star appearance over time
float starBlink(float time, float seed) {
    float cycle = mod(time + seed, 5.0); // 5-second blinking cycle
    return smoothstep(0.0, 1.0, sin(cycle * 3.14159)); // Fade in/out
}

// Star intensity and shape
float getStar(vec2 uv, vec2 position, float size, float brightness) {
    float dist = length(uv - position);
    float starShape = exp(-dist * size); // Star size and falloff
    return starShape * brightness;
}

vec3 getStars(vec2 uv, float time) {
    vec3 starColor = vec3(1.0); // Bright white for stars
    vec3 stars = vec3(0.0);     // Initialize stars to black (background)

    // Generate dynamic positions and properties for stars
    for (int i = 0; i < 10; i++) {  // Adjust the number of stars
        vec2 seed = vec2(float(i), float(i + 1)); // Unique seed for each star
        
        // Use noise to create dynamic positions
        vec2 starPos = vec2(
            0.5 * (snoise(vec3(seed.x, seed.y, time * 0.5)) + 1.0), // Remap to [0, 1]
            0.5 * (snoise(vec3(seed.y, seed.x, time * 0.5)) + 1.0)  // Remap to [0, 1]
        );

        // Star size and brightness
        float size = snoise(vec3(seed, 1.0)) * 20.0 + 20.0; // Random size via noise
        float brightness = snoise(vec3(seed + 2.0, 1.0)) * 0.7 + 0.3; // Random brightness via noise
        float blink = starBlink(time, float(i)); // Blinking effect

        // Add star contribution
        stars += starColor * getStar(uv, starPos, size, blink * brightness);
    }

    return stars;
}

void main() {
    float rep = 600.0; // total time
    float time_scale = 0.02;
    float time = mod(u_time, rep) * time_scale; // Keeps time within [0, rep]
    float noise_scale = 1.0;
    vec2 uv = texCoords * noise_scale; // Increase scale

    // get nebula clouds effect
    vec3 nebulaColor = getNebulaClouds(uv, time);

    // get blinking stars effect
    vec3 blinkingStarColor = getStars(uv, time);

    vec3 finalColor = nebulaColor + blinkingStarColor;

    fragColor = vec4(finalColor, 1.0);
}
