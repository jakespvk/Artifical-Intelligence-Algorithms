#version 330
in vec3 Normal;
in vec2 TexCoord;
in vec3 FragPos;

// This is the proper way to set the color of the fragment, NOT using gl_FragColor.
layout (location=0) out vec4 FragColor;

uniform sampler2D ourTexture;
// Lighting parameters for ambient light, and a single point light w/ no attenuation.
uniform vec3 ambientColor;
uniform vec3 pointPosition;
uniform vec3 pointColor;
uniform vec3 viewVector;
uniform vec4 coefficients;

void main() {
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(pointPosition - FragPos);  
    float cosineLight = max(dot(norm, lightDir), 0.0);

    // Compute the ambient and diffuse components.
    vec3 ambient = ambientColor;
    vec3 diffuse = cosineLight * pointColor;

    // Compute specular
    vec3 R = reflect(-lightDir, norm);
    vec3 V = normalize(viewVector - FragPos);
    float cosine = dot(V, R);
    float shininess = coefficients[3];
    vec3 specularColor = vec3(1.0, 1.0, 1.0); 
    float specularCoefficient = pow(max(cosine, 0.0), shininess);
    vec3 specular = specularCoefficient * specularColor;

    // Assemble the final fragment color.
    FragColor = vec4(diffuse * coefficients[0] +
                    ambient * coefficients[1] + 
                    specular * coefficients[2], 1) * 
                    texture(ourTexture, TexCoord);
}
