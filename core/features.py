from core.libraries import *

class HEX():
    
    def __init__(self, str_code: str):
        self.code = str_code

class RGB():
    
    def __init__(self, tuple_code: tuple):
        self.code = tuple_code
        self.r = tuple_code[0]
        self.g = tuple_code[1]
        self.b = tuple_code[2]

class HSV():

    def __init__(self, tuple_code: tuple):
        self.code = tuple_code
        self.h = tuple_code[0]
        self.s = tuple_code[1]
        self.v = tuple_code[2]

class HSL():

    def __init__(self, tuple_code: tuple):
        self.code = tuple_code
        self.h = tuple_code[0]
        self.s = tuple_code[1]
        self.l = tuple_code[2]

class YIQ():

    def __init__(self, tuple_code: tuple):
        self.code = tuple_code
        self.y = tuple_code[0]
        self.i = tuple_code[1]
        self.q = tuple_code[2]

class Color():

    def __init__(self, dict_data: dict = None, name: str = None, hex: HEX = None, rgb: RGB = None, hsv: HSV = None, hsl: HSL = None, yiq: YIQ = None):
        self.name = dict_data['name'] if (dict_data != None) else name
        self.hex = HEX(dict_data['hex']) if (dict_data != None) else hex
        self.rgb = RGB((dict_data['rgb']['r'], dict_data['rgb']['g'], dict_data['rgb']['b'])) if (dict_data != None) else rgb
        self.hsv = HSV((dict_data['hsv']['h'], dict_data['hsv']['s'], dict_data['hsv']['v'])) if (dict_data != None) else hsv
        self.hsl = HSL((dict_data['hsl']['h'], dict_data['hsl']['s'], dict_data['hsl']['l'])) if (dict_data != None) else hsl
        self.yiq = YIQ((dict_data['yiq']['y'], dict_data['yiq']['i'], dict_data['yiq']['q'])) if (dict_data != None) else yiq

class ColorsDatabase():

    def __init__(self, list_data: list):
        self.colors = []
        for colVar in list_data:
            self.colors.append(Color(colVar))
    
    def get_ColorsNames(self) -> list[str]:
        return [col.name for col in self.colors]
    
    def get_ColorsHex(self) -> list[HEX]:
        return [col.hex for col in self.colors]

    def get_ColorsRgb(self) -> list[RGB]:
        return [col.rgb for col in self.colors]
    
    def get_ColorsHsv(self) -> list[HSV]:
        return [col.hsv for col in self.colors]
    
    def get_ColorsHsl(self) -> list[HSL]:
        return [col.hsl for col in self.colors]
    
    def get_ColorsYiq(self) -> list[YIQ]:
        return [col.yiq for col in self.colors]

    def get_ColorsHexCodes(self) -> list[str]:
        return [col.hex.code for col in self.colors]
    
    def get_ColorsRgbCodes(self) -> list[str]:
        return [col.rgb.code for col in self.colors]
    
    def get_ColorsHsvCodes(self) -> list[str]:
        return [col.hsv.code for col in self.colors]
    
    def get_ColorsHslCodes(self) -> list[str]:
        return [col.hsl.code for col in self.colors]
    
    def get_ColorsYiqCodes(self) -> list[str]:
        return [col.yiq.code for col in self.colors]

    def get_byName(self, name) -> Color | None:
        for col in self.colors:
            if (col.name == name):
                return col
    
    def get_byHex(self, hex: HEX) -> Color:
        for col in self.colors:
            if (col.hex == hex):
                return col
    
    def get_byRgb(self, rgb: RGB) -> Color:
        for col in self.colors:
            if (col.rgb == rgb):
                return col
    
    def get_byHsv(self, hsv: HSV) -> Color:
        for col in self.colors:
            if (col.hsv == hsv):
                return col
    
    def get_byHsl(self, hsl: HSL) -> Color:
        for col in self.colors:
            if (col.hsl == hsl):
                return col
    
    def get_byYiq(self, yiq: YIQ) -> Color:
        for col in self.colors:
            if (col.yiq == yiq):
                return col

class Settings():

    def __init__(self, dict_data: dict):
        self.view_mode = dict_data['view_mode']
        self.theme_mode = dict_data['theme_mode']
        self._round = dict_data['_round']
        self.color_database = ColorsDatabase(dict_data['color_database'])
        self.dict = dict_data

class ColorContextMenu(flet.CupertinoContextMenu):

    def __init__(self, col: Color, clk, content, actions, enable_haptic_feedback = None, ref = None, disabled = None, visible = None, data = None, adaptive = False):
        super().__init__(content, actions, enable_haptic_feedback, ref, disabled, visible, data, adaptive)
        self.color = col

class ColorPopupMenu(flet.PopupMenuButton):

    def __init__(self, color: Color, content = None, items = None, icon = None, bgcolor = None, icon_color = None, shadow_color = None, surface_tint_color = None, icon_size = None, splash_radius = None, elevation = None, menu_position = None, clip_behavior = None, enable_feedback = None, shape = None, padding = None, menu_padding = None, style = None, popup_animation_style = None, size_constraints = None, on_cancelled = None, on_open = None, on_cancel = None, on_select = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, tooltip = None, visible = None, disabled = None, data = None):
        super().__init__(content, items, icon, bgcolor, icon_color, shadow_color, surface_tint_color, icon_size, splash_radius, elevation, menu_position, clip_behavior, enable_feedback, shape, padding, menu_padding, style, popup_animation_style, size_constraints, on_cancelled, on_open, on_cancel, on_select, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, visible, disabled, data)
        self.color = color

class ColorContainer(flet.Container):

    def __init__(self, color: Color, content = None, padding = None, margin = None, alignment = None, bgcolor = None, gradient = None, blend_mode = None, border = None, border_radius = None, image_src = None, image_src_base64 = None, image_repeat = None, image_fit = None, image_opacity = None, shape = None, clip_behavior = None, ink = None, image = None, ink_color = None, animate = None, blur = None, shadow = None, url = None, url_target = None, theme = None, theme_mode = None, color_filter = None, ignore_interactions = None, foreground_decoration = None, on_click = None, on_tap_down = None, on_long_press = None, on_hover = None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, tooltip = None, badge = None, visible = None, disabled = None, data = None, rtl = None, adaptive = None):
        super().__init__(content, padding, margin, alignment, bgcolor, gradient, blend_mode, border, border_radius, image_src, image_src_base64, image_repeat, image_fit, image_opacity, shape, clip_behavior, ink, image, ink_color, animate, blur, shadow, url, url_target, theme, theme_mode, color_filter, ignore_interactions, foreground_decoration, on_click, on_tap_down, on_long_press, on_hover, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, badge, visible, disabled, data, rtl, adaptive)
        self.color = color

class ColorListTile(flet.ListTile):

    def __init__(self, color: Color, content_padding = None, bgcolor = None, bgcolor_activated = None, hover_color = None, leading = None, title = None, subtitle = None, trailing = None, is_three_line = None, selected = None, dense = None, autofocus = None, toggle_inputs = None, selected_color = None, selected_tile_color = None, style = None, enable_feedback = None, horizontal_spacing = None, min_leading_width = None, min_vertical_padding = None, url = None, url_target = None, title_alignment = None, icon_color = None, text_color = None, shape = None, visual_density = None, mouse_cursor = None, title_text_style = None, subtitle_text_style = None, leading_and_trailing_text_style = None, min_height = None, on_click=None, on_long_press=None, ref = None, key = None, width = None, height = None, left = None, top = None, right = None, bottom = None, expand = None, expand_loose = None, col = None, opacity = None, rotate = None, scale = None, offset = None, aspect_ratio = None, animate_opacity = None, animate_size = None, animate_position = None, animate_rotation = None, animate_scale = None, animate_offset = None, on_animation_end = None, tooltip = None, badge = None, visible = None, disabled = None, data = None, adaptive = None):
        super().__init__(content_padding, bgcolor, bgcolor_activated, hover_color, leading, title, subtitle, trailing, is_three_line, selected, dense, autofocus, toggle_inputs, selected_color, selected_tile_color, style, enable_feedback, horizontal_spacing, min_leading_width, min_vertical_padding, url, url_target, title_alignment, icon_color, text_color, shape, visual_density, mouse_cursor, title_text_style, subtitle_text_style, leading_and_trailing_text_style, min_height, on_click, on_long_press, ref, key, width, height, left, top, right, bottom, expand, expand_loose, col, opacity, rotate, scale, offset, aspect_ratio, animate_opacity, animate_size, animate_position, animate_rotation, animate_scale, animate_offset, on_animation_end, tooltip, badge, visible, disabled, data, adaptive)
        self.color = color

class LangField():

    def __init__(self, value, default):
        self.value = value
        self.default = default

class LanguageLab():

    def __init__(self):
        
        self.EU_search_bar_hint_text = LangField('Enter color name here...', 'Enter color name here...')

        self.EU_grid_item_delete_action_text = LangField('Delete', 'Delete')

        self.EU_list_item_delete_action_text = LangField('Delete', 'Delete')

        self.EU_theme_button_to_night_theme_tooltip = LangField('Toggle night theme mode', 'Toggle night theme mode')
        self.EU_theme_button_to_light_theme_tooltip = LangField('Toggle light theme mode', 'Toggle light theme mode')

        self.EU_view_mode_filter_to_grid_tooltip = LangField('Toggle grid view mode', 'Toggle grid view mode')
        self.EU_view_mode_filter_to_list_tooltip = LangField('Toggle list view mode', 'Toggle list view mode')

        self.EU_color_view_modal_title_text = LangField('Color view', 'Color view')
        self.EU_color_view_modal_item_color_name_label_text = LangField('Color name', 'Color name')
        self.EU_color_view_modal_item_copy_tooltip = LangField('Click to copy', 'Click to copy')
        self.EU_color_view_modal_item_rgb_copy_button_text = LangField('Copy RGB', 'Copy RGB')
        self.EU_color_view_modal_item_hsv_copy_button_text = LangField('Copy HSV', 'Copy HSV')
        self.EU_color_view_modal_item_hsl_copy_button_text = LangField('Copy HSL', 'Copy HSL')
        self.EU_color_view_modal_item_yiq_copy_button_text = LangField('Copy YIQ', 'Copy YIQ')

        self.EU_new_color_view_modal_title_text = LangField('New color', 'New color')
        self.EU_new_color_view_modal_color_name_required_text = LangField('*required field', '*required field')
        self.EU_new_color_view_modal_color_name_label_text = LangField('Color name', 'Color name')
        self.EU_new_color_view_modal_color_name_hint_text = LangField('Enter color name here...', 'Enter color name here...')
        self.EU_new_color_view_modal_save_button_text = LangField('Save', 'Save')

        self.EU_about_view_item_docs = LangField('Docs', 'Docs')
        self.EU_about_view_item_install = LangField('Install (pip required)', 'Install (pip required)')
        self.EU_about_view_item_cannot_be_installed = LangField('Cannot be installed', 'Cannot be installed')
        self.EU_about_view_item_credits_action_text = LangField('Github', 'Github')

        self.EU_color_name_not_entered = LangField('Please, enter color name.', 'Please, enter color name.')

        self.EU_name_clip_copy = LangField('Color name has been copied to clipboard.', 'Color name has been copied to clipboard.')
        self.EU_hex_clip_copy = LangField('HEX color code has been copied to clipboard.', 'HEX color code has been copied to clipboard.')
        self.EU_rgb_clip_copy = LangField('RGB color code has been copied to clipboard.', 'RGB color code has been copied to clipboard.')
        self.EU_hsv_clip_copy = LangField('HSV color code has been copied to clipboard.', 'HSV color code has been copied to clipboard.')
        self.EU_hsl_clip_copy = LangField('HSL color code has been copied to clipboard.', 'HSL color code has been copied to clipboard.')
        self.EU_yiq_clip_copy = LangField('YIQ color code has been copied to clipboard.', 'YIQ color code has been copied to clipboard.')

        self.EU_rgb_r_clip_copy = LangField('Red of RGB color code has been copied to clipboard.', 'Red of RGB color code has been copied to clipboard.')
        self.EU_rgb_g_clip_copy = LangField('Green of RGB color code has been copied to clipboard.', 'Green of RGB color code has been copied to clipboard.')
        self.EU_rgb_b_clip_copy = LangField('Blue of RGB color code has been copied to clipboard.', 'Blue of RGB color code has been copied to clipboard.')

        self.EU_hsv_h_clip_copy = LangField('Hue of HSV color code has been copied to clipboard.', 'Hue of HSV color code has been copied to clipboard.')
        self.EU_hsv_s_clip_copy = LangField('Saturation of HSV color code has been copied to clipboard.', 'Saturation of HSV color code has been copied to clipboard.')
        self.EU_hsv_v_clip_copy = LangField('Value of HSV color code has been copied to clipboard.', 'Value of HSV color code has been copied to clipboard.')

        self.EU_hsl_h_clip_copy = LangField('Hue of HSL color code has been copied to clipboard.', 'Hue of HSL color code has been copied to clipboard.')
        self.EU_hsl_s_clip_copy = LangField('Saturation of HSL color code has been copied to clipboard.', 'Saturation of HSL color code has been copied to clipboard.')
        self.EU_hsl_l_clip_copy = LangField('Lightness of HSL color code has been copied to clipboard.', 'Lightness of HSL color code has been copied to clipboard.')
    
        self.EU_yiq_y_clip_copy = LangField('Luminosity (Y) of YIQ color code has been copied to clipboard.', 'Luminosity (Y) of YIQ color code has been copied to clipboard.')
        self.EU_yiq_i_clip_copy = LangField('\"In-phase\" of YIQ color code has been copied to clipboard.', '\"In-phase\" of YIQ color code has been copied to clipboard.')
        self.EU_yiq_q_clip_copy = LangField('Quadrature of YIQ color code has been copied to clipboard.', 'Quadrature of YIQ color code has been copied to clipboard.')
    
        self.EU_colors_not_found = LangField('Nothing found :(', 'Nothing found :(')

        self.EU_settings_modal_title_text = LangField('Settings', 'Settings')

        self.EU_settings_languagelab_title_text = LangField('LanguageLab', 'LanguageLab')
        self.EU_settings_languagelab_reset_button_text = LangField('Reset', 'Reset')
        self.EU_settings_languagelab_reset_tooltip = LangField('Sets the default settings.', 'Sets the default settings.')
        self.EU_settings_langlab_to_dir = LangField('Open directory', 'Open directory')

        self.EU_settings_colormanager_title_text = LangField('Color Manager', 'Color Manager')
        self.EU_settings_colormanager_dropdown_title_text = LangField('Round', 'Round')
        self.EU_settings_colormanager_dropdown_half = LangField('Only rounds RGB codes.', 'Only rounds RGB codes.')
        self.EU_settings_colormanager_dropdown_half_option_text = LangField('Half', 'Half')
        self.EU_settings_colormanager_dropdown_all = LangField('Round all formats (RGB, HSV, HSL, YIQ).', 'Round all formats (RGB, HSV, HSL, YIQ).')
        self.EU_settings_colormanager_dropdown_all_option_text = LangField('All', 'All')

        self.EU_must_reboot = LangField('Please, restart app.', 'Please, restart app.')
    
    def default_dict(self):
        return { var: self.__getattribute__(var).default for var in vars(self) }

    def current_dict(self):
        return { var: self.__getattribute__(var).value for var in vars(self) }

        