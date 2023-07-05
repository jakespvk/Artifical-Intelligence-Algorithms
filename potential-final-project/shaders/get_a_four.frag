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
uniform vec3 direction;
uniform vec3 pointColor;
uniform vec3 viewVector;
uniform vec4 coefficients;
uniform vec3 pointLightArgs;
uniform vec3 spotlightPos;
uniform vec3 spotlightDir;
uniform float spotlightCutoff;

vec4 calcDirectional(vec3 direction, vec3 pointColor, vec3 viewVector, vec4 coefficients) {
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(-direction);  
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
    return vec4(diffuse * coefficients[0] +
                    ambient * coefficients[1] + 
                    specular * coefficients[2], 1) * 
                    texture(ourTexture, TexCoord);
}

vec4 calcPointWithAtten(vec3 pointPosition, vec3 pointColor, vec3 viewVector, vec4 coefficients) {
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

    // point light
    float constant = pointLightArgs[0];
    float linear = pointLightArgs[1];
    float quadratic = pointLightArgs[2];
    float distance = length(pointPosition - FragPos);
    float attenuation = 1.0 / (constant + linear * distance + quadratic * (distance * distance));

    ambient *= attenuation;
    diffuse *= attenuation;
    specular *= attenuation;

    // Assemble the final fragment color.
    return vec4(diffuse * coefficients[0] +
                    ambient * coefficients[1] + 
                    specular * coefficients[2], 1) * 
                    texture(ourTexture, TexCoord);
}

vec4 calcSpotlight(vec3 spotlightDir, vec3 spotlightPos, float spotlightCutoff, vec4 coefficients) {

    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(spotlightPos - FragPos);  
    // changed lightDir to spotlightDir for debugging
    float cosineLight = max(dot(norm, spotlightDir), 0.0);
    // spotlight
    float theta = dot(spotlightDir, normalize(-spotlightDir));

    // Compute the ambient and diffuse components.
    vec3 ambient = ambientColor;
    if (theta > spotlightCutoff) {
        

        // Compute the ambient and diffuse components.
        vec3 diffuse = cosineLight * pointColor;

        // Compute specular
        vec3 R = reflect(-spotlightDir, norm);
        vec3 V = normalize(viewVector - FragPos);
        float cosine = dot(V, R);
        float shininess = coefficients[3];
        vec3 specularColor = vec3(1.0, 1.0, 1.0); 
        float specularCoefficient = pow(max(cosine, 0.0), shininess);
        vec3 specular = specularCoefficient * specularColor;

        // Assemble the final fragment color.
        return vec4(diffuse * coefficients[0] +
                ambient * coefficients[1] + 
                specular * coefficients[2], 1) * 
            texture(ourTexture, TexCoord);

    } else {
        return vec4(ambient * vec3(texture(ourTexture, TexCoord)), 1.0);
    }
}

void main() {
    // Assemble the final fragment color.
    FragColor = calcDirectional(direction, pointColor, viewVector, coefficients) +
                calcPointWithAtten(pointPosition, pointColor, viewVector, coefficients) +
                calcSpotlight(spotlightDir, spotlightPos, spotlightCutoff, coefficients);
    //FragColor = calcSpotlight(spotlightDir, spotlightPos, spotlightCutoff, coefficients);



}
