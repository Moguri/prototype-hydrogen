import panda3d.core as p3d
from direct.filter.FilterManager import FilterManager

hdr_vert = """
#version 330

uniform mat4 p3d_ModelViewProjectionMatrix;

in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;

out vec2 texcoord;

void main() {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    texcoord = p3d_MultiTexCoord0;
}
"""

# GLSL version of Uncharted 2 operator taken from http://filmicgames.com/archives/75
hdr_frag = """
#version 330

uniform sampler2D tex;

in vec2 texcoord;

out vec4 o_color;

void main() {
    vec3 color = texture(tex, texcoord).rgb;

    color = max(vec3(0.0), color - vec3(0.004));
    color = (color * (vec3(6.2) * color + vec3(0.5))) / (color * (vec3(6.2) * color + vec3(1.7)) + vec3(0.06));

    o_color = vec4(color, 1.0);
}
"""


class HydrogenRenderManager:
    def __init__(self, base):

        base.render.set_shader_auto()
        base.render.set_attrib(p3d.LightRampAttrib.make_identity())

        manager = FilterManager(base.win, base.cam)
        tex = p3d.Texture()
        quad = manager.renderSceneInto(colortex=tex)
        quad.set_shader(p3d.Shader.make(p3d.Shader.SL_GLSL, hdr_vert, hdr_frag))
        quad.set_shader_input('tex', tex)


        self.base = base


def get_plugin():
    return HydrogenRenderManager

