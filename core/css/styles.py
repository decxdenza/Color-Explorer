from core.libraries import *

@dataclass
class Shadows():

    top_bar_drag_area_text = flet.BoxShadow(
        0, 50,
        flet.Colors.TEAL_300,
        blur_style=flet.ShadowBlurStyle.OUTER
    )
    
    grid_view_add_new_container = flet.BoxShadow(
        0, 50,
        flet.Colors.TEAL_300,
        blur_style=flet.ShadowBlurStyle.OUTER
    )

    search_bar_nothing_found_text = flet.BoxShadow(
        0, 50,
        flet.Colors.TEAL_300,
        blur_style=flet.ShadowBlurStyle.OUTER
    )
    
    mdl_about_view_credits_container = flet.BoxShadow(
        0, 10,
        flet.Colors.RED,
        blur_style=flet.ShadowBlurStyle.OUTER
    )

@dataclass
class Colors():

    top_bar_search_bar_icon = flet.Colors.TEAL_300
    top_bar_search_bar_shadow = flet.Colors.TEAL_300

    top_bar_drag_area_text = flet.Colors.TEAL_300
    top_bar_drag_area_settings_icon_button = flet.Colors.TEAL_300
    top_bar_drag_area_about_icon_button = flet.Colors.TEAL_300

    top_bar_close_cross_icon_button = flet.Colors.RED

    top_bar_to_night_theme_icon_button = flet.Colors.TEAL_300
    top_bar_to_light_theme_icon_button = flet.Colors.TEAL_300
    top_bar_view_filter_list_icon_button = flet.Colors.TEAL_300
    top_bar_view_filter_grid_icon_button = flet.Colors.TEAL_300

    grid_view_item_bright_text = flet.Colors.BLACK
    grid_view_item_dark_text = flet.Colors.WHITE

    grid_view_add_new_bg_container = flet.Colors.TEAL_300
    grid_view_add_new_icon = flet.Colors.WHITE

    list_view_add_new_bg_icon_button = flet.Colors.TEAL_300
    list_view_add_new_button = flet.Colors.TEAL_300
    
    mdl_about_view_description_item_border_side = flet.Colors.YELLOW
    mdl_about_view_references_item_border_side = flet.Colors.ORANGE
    mdl_about_view_credits_item_border_side = flet.Colors.RED

    list_view_item_delete_trailing_action_text = flet.Colors.RED

    mdl_add_new_required_field_text = flet.Colors.RED
    mdl_add_new_cancel_button = flet.Colors.RED

    mdl_color_view_delete_icon_button = flet.Colors.RED
    
    mdl_settings_view_close_button = flet.Colors.RED
    mdl_settings_view_close_text_button = flet.Colors.RED

@dataclass
class BorderRadiuses():

    grid_view_item_container = flet.border_radius.all(10)

    grid_view_add_new_container = flet.border_radius.all(10)
    
    list_view_item_container = flet.border_radius.all(10)

    mdl_about_view_container = flet.border_radius.all(10)

    mdl_color_view_container = flet.border_radius.all(10)

@dataclass
class Icons():

    top_bar_search_bar = flet.Icons.SEARCH

    top_bar_drag_area_settings_icon_button = flet.Icons.SETTINGS
    top_bar_drag_area_about_icon_button = flet.Icons.HELP_OUTLINE

    top_bar_close_cross_icon_button = flet.Icons.CLOSE

    top_bar_to_night_theme_icon_button = flet.Icons.NIGHTLIGHT
    top_bar_to_light_theme_icon_button = flet.Icons.SUNNY
    top_bar_view_filter_list_icon_button = flet.Icons.LIST
    top_bar_view_filter_grid_icon_button = flet.Icons.GRID_VIEW

    grid_view_add_new = flet.Icons.ADD

    grid_view_item_copy_trailing_action = flet.Icons.COPY
    grid_view_item_delete_trailing_action = flet.Icons.DELETE

    list_view_item_trailing = flet.Icons.MORE_VERT
    list_view_item_copy_trailing_action = flet.Icons.COPY
    list_view_item_delete_trailing_action = flet.Icons.DELETE

    list_view_add_new = flet.Icons.ADD

    mdl_about_view_item_leading = flet.Icons.API
    mdl_about_view_item_trailing = flet.Icons.MORE_VERT
    mdl_about_view_item_docs_trailing_action = flet.Icons.OPEN_IN_BROWSER
    mdl_about_view_item_install_trailing_action = flet.Icons.INSTALL_DESKTOP
    mdl_about_view_item_credits_trailing_action = flet.Icons.PERSON

    mdl_color_view_copy_action_button = flet.Icons.COPY
    mdl_color_view_delete_icon_button = flet.Icons.DELETE

    mdl_add_new_save_button = flet.Icons.SAVE
    mdl_add_new_cancel_button = flet.Icons.CANCEL

    mdl_settings_view_languagelab_reset_button = flet.Icons.RESTORE
    mdl_settings_view_languagelab_reload_button = flet.Icons.REFRESH
    mdl_settings_view_languagelab_open_dir_button = flet.Icons.FOLDER_OPEN
    mdl_settings_view_languagelab_help = flet.Icons.INFO
    mdl_settings_view_colormanager_dropdown_help = flet.Icons.INFO

@dataclass
class TextStyling():

    top_bar_drag_area_text = flet.TextStyle(
        shadow=Shadows.top_bar_drag_area_text
    )

@dataclass
class ButtonStyling():

    list_view_add_new_button = flet.ButtonStyle(
        shadow_color=Colors.list_view_add_new_button
    )
