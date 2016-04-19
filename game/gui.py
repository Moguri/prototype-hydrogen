import yaml
import direct.gui.DirectGui as dgui
import panda3d.core as p3d


DGG = dgui.DGG


class Error(RuntimeError):
    pass


class ParameterError(Error):
    pass


global_theme = None


class Theme(object):
    def __init__(self):
        self.props = {}

    def has_style(self, style):
        return style in self.props

    def get_property(self, style, prop):
        return self.props[style][prop]

    def has_property(self, style, prop):
        if style not in self.props:
            return False

        if prop not in self.props[style]:
            return False

        return True

    def set_property(self, style, prop, value):
        self.props[style][prop] = value

    @classmethod
    def from_dictionary(cls, dictionary):
        theme = cls()
        theme.props = dictionary

        return theme

    @classmethod
    def from_file(cls, filepath):
        print("Loading from file", filepath)
        with open(filepath) as f:
            return cls.from_dictionary(yaml.load(f))


class Widget(object):
    _direct_param_map = {
        'text': 'text',
        'text_bg': 'text_bg',
        'text_fg': 'text_fg',
        'text_pos': 'text_pos',
        'text_roll': 'text_roll',
        'text_scale': 'text_scale',
        'text_align': 'text_align',
        'frame_size': 'frameSize',
        'frame_visible_scale': 'frameVisibleScale',
        'frame_color': 'frameColor',
        'relief': 'relief',
        'inverted_frames': 'invertedFrames',
        'border_width': 'borderWidth',
        'image': 'image',
        'image_pos': 'image_pos',
        'image_hpr': 'image_hpr',
        'image_scale': 'image_scale',
        'geom': 'geom',
        'geom_pos': 'geom_pos',
        'geom_hpr': 'geom_hpr',
        'geom_scale': 'geom_scale',
        'parent': 'parent',
        'pos': 'pos',
        'hpr': 'hpr',
        'scale': 'scale',
        'pad': 'pad',
        'state': 'state',
        'frame_texture': 'frameTexture',
        'enable_edit': 'enableEdit',
        'suppress_keys': 'suppressKeys',
        'suppress_mouse': 'suppressMouse',
        'sort_order': 'sortOrder',
        'text_may_change': 'textMayChange',
    }

    def __init__(self, dgui_widget, parent, style=None, theme=None, **params):
        if isinstance(parent, Widget):
            parent = parent._dgui_widget
        self._dgui_widget = dgui_widget(parent=parent)

        if theme is None:
            theme = global_theme

        if style is None:
            theme = None

        if theme is not None and not theme.has_style(style):
            print("Warning: style not found in current theme: {}".format(style))
            theme = None

        if theme is not None:
            theme_params = {
                i: theme.get_property(style, i)
                for i in self._direct_param_map
                if theme.has_property(style, i) and i not in params
            }
        else:
            theme_params = {}

        theme_params.update(params)
        params = theme_params

        for param in sorted(params.keys()):
            if not hasattr(self, param):
                raise ParameterError("Unknown parameter: {}".format(param))

            setattr(self, param, params[param])

    def __getattr__(self, attr):
        if attr == 'pos':
            return self._dgui_widget.get_pos()
        elif attr == 'hpr':
            return self._dgui_widget.get_hpr()
        elif attr == 'parent':
            return self._dgui_widget.get_parent()
        elif attr == 'text_align':
            #TODO: hack to avoid issues since OnScreenText has no getAlign
            return ''
        elif attr == 'text_fg':
            #TODO: hack to avoid issues since OnScreenText has no getFg
            return ''
        elif attr == 'text_shadow':
            #TODO: hack to avoid issues since OnScreenText has no getFg
            return ''
        elif attr in self._direct_param_map:
            try:
                return self._dgui_widget[self._direct_param_map[attr]]
            except AttributeError as e:
                raise ParameterError(e)
        else:
            raise AttributeError("%r object has no attribute %r" % (self.__class__.__name__, attr))

        if attr.split('_')[0] in ('image', 'text', 'geom'):
            self._dgui_widget.resetFrameSize()

    def __setattr__(self, attr, value):
        #print(self.__class__.__name__, attr, value, type(value))
        if attr == 'pos':
            self._dgui_widget.set_pos(value)
        elif attr == 'hpr':
            self._dgui_widget.set_hpr(value)
        elif attr == 'parent':
            self._dgui_widget.set_parent(value)
        elif attr in self._direct_param_map:
            if attr == 'text_scale':
                value = tuple(value)
            elif attr == 'text_align' and isinstance(value, str):
                value = getattr(p3d.TextNode, value)
            elif attr == 'relief' and isinstance(value, str):
                value = getattr(DGG, value.upper())
            self._dgui_widget[self._direct_param_map[attr]] = value
        else:
            super().__setattr__(attr, value)

    def destroy(self):
        self._dgui_widget.destroy()


class Frame(Widget):
    _direct_param_map = dict(Widget._direct_param_map, **{
    })

    def __init__(self, parent, style=None, theme=None, **params):
        super().__init__(dgui.DirectFrame, parent, style, theme, **params)


class Button(Widget):
    _direct_param_map = dict(Widget._direct_param_map, **{
        'command': 'command',
        'extra_args': 'extraArgs',
        'commmand_buttons': 'commandButtons',
        'rollover_sound': 'rolloverSound',
        'click_sound': 'clickSound',
        'press_effect': 'pressEffect',
        'state': 'state',
    })

    def __init__(self, parent, style=None, theme=None, **params):
        super().__init__(dgui.DirectButton, parent, style, theme, **params)


class WaitBar(Widget):
    _direct_param_map = dict(Widget._direct_param_map, **{
        'value': 'value',
        'range': 'range',
        'bar_color': 'barColor',
        'bar_texture': 'barTexture',
        'bar_relief': 'barRelief',
        'bar_border_width': 'barBorderWidth',
    })

    def __init__(self, parent, style=None, theme=None, **params):
        super().__init__(dgui.DirectWaitBar, parent, style, theme, **params)


class Label(Widget):
    _direct_param_map = dict(Widget._direct_param_map, **{
        'active_state': 'activeState',
    })

    def __init__(self, parent, style=None, theme=None, **params):
        super().__init__(dgui.DirectLabel, parent, style, theme, **params)


