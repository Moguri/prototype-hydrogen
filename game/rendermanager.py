import panda3d.core as p3d


class HydrogenRenderManager:
    def __init__(self, base):

        self.base = base
        self.base.render.set_shader_auto()


def get_plugin():
    return HydrogenRenderManager

