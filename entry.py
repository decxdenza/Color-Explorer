from core.libraries import *

@dataclass
class BuildInfo():

    ver = '1.1.4'

class ColorExplorer():

    def __init__(self, page: flet.Page):
        self.gui = page
        self.gui.window.title_bar_hidden = True
        self.gui.window.title_bar_buttons_hidden = True
        self.gui.window.maximizable = False
        self.gui.window.resizable = False
        self.gui.window.height = 700
        self.gui.window.width = 1000
        self.gui.title = f'Color Explorer [v{BuildInfo.ver}]'

        self.encoder = json.JSONEncoder()
        self.decoder = json.JSONDecoder()

        self.paths_validate()

        self.settings = None
        self.langlab = None
        self.load_settings()
        self.load_lang()

        self.search_bar = flet.SearchBar(
            bar_shadow_color=Colors.top_bar_search_bar_shadow, 
            bar_hint_text=self.langlab.EU_search_bar_hint_text.value, 
            bar_leading=flet.Icon(
                Icons.top_bar_search_bar, 
                Colors.top_bar_search_bar_icon
            ), 
            view_elevation=100,
            on_change=self.search_colors
        )
        self.mdl = flet.AlertDialog()
        self.grid_view = flet.GridView(
            controls=[], 
            expand=1, 
            runs_count=5, 
            max_extent=150, 
            child_aspect_ratio=1.0, 
            spacing=50, 
            run_spacing=30,
        )
        self.list_view = flet.Column(
            controls=[],
            expand=True,
            scroll=flet.ScrollMode.ALWAYS
        )
        self.snackbar = flet.SnackBar(
            content=flet.Text()
        )
        self.drag_area = flet.WindowDragArea(
            maximizable=False,
            content=flet.Row(
                controls=[
                    flet.Text(
                        "Color Explorer",
                        size=21,
                        color=Colors.top_bar_drag_area_text,
                        style=TextStyling.top_bar_drag_area_text
                    ),
                    flet.IconButton(
                        Icons.top_bar_drag_area_settings_icon_button,
                        Colors.top_bar_drag_area_settings_icon_button,
                        opacity=0.8,
                        on_click=self.open_settings_view
                    ),
                    flet.IconButton(
                        Icons.top_bar_drag_area_about_icon_button,
                        Colors.top_bar_drag_area_about_icon_button,
                        opacity=0.8,
                        on_click=self.open_about
                    )
                ]
            ), 
            width=self.gui.window.width-180
        )
        self.close_cross = flet.IconButton(
            Icons.top_bar_close_cross_icon_button,
            Colors.top_bar_close_cross_icon_button,
            on_click=self.close
        )
        self.theme_btn = flet.IconButton(
            Icons.top_bar_to_night_theme_icon_button, 
            Colors.top_bar_to_night_theme_icon_button,
            on_click=self.theme_change
        )
        self.view_mode_filter = flet.IconButton(
            Icons.top_bar_view_filter_list_icon_button,
            Colors.top_bar_view_filter_list_icon_button,
            on_click=self.view_mode_change
        )
        self.top_bar = flet.Row(
            controls=[
                self.drag_area,
                self.close_cross
            ]
        )
        self.load_ring = flet.ProgressRing(width=50, height=50, stroke_width=1.5)

        self.gui.overlay.append(self.snackbar)

        self.mainWindow = flet.Column(
            controls=[
                self.top_bar,
                self.search_bar
            ],
            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
            alignment=flet.MainAxisAlignment.CENTER,
            scroll=flet.ScrollMode.ADAPTIVE
        )

        try:
            self.gui.theme_mode = self.settings.theme_mode
        except:
            self.gui.theme_mode = 'dark'
        self.gui.update()
        
        self.theme_btn.icon = Icons.top_bar_to_night_theme_icon_button if (self.settings.theme_mode == 'light') else Icons.top_bar_to_light_theme_icon_button
        self.theme_btn.icon_color = Colors.top_bar_to_night_theme_icon_button if (self.settings.theme_mode == 'light') else Colors.top_bar_to_light_theme_icon_button
        self.theme_btn.tooltip = self.langlab.EU_theme_button_to_night_theme_tooltip.value if (self.settings.theme_mode == 'light') else self.langlab.EU_theme_button_to_light_theme_tooltip.value
        self.mainWindow.controls[0].controls.insert(1, self.theme_btn)

        self.view_mode_filter.icon = Icons.top_bar_view_filter_list_icon_button if (self.settings.view_mode == ViewMode.Grid) else Icons.top_bar_view_filter_grid_icon_button
        self.view_mode_filter.icon_color = Colors.top_bar_view_filter_list_icon_button if (self.settings.view_mode == ViewMode.Grid) else Colors.top_bar_view_filter_grid_icon_button
        self.view_mode_filter.tooltip = self.langlab.EU_view_mode_filter_to_list_tooltip.value if (self.settings.view_mode == ViewMode.Grid) else self.langlab.EU_view_mode_filter_to_grid_tooltip.value
        self.mainWindow.controls[0].controls.insert(2, self.view_mode_filter)
        
        self.gui.add(self.mainWindow)
        self.gui.update()
        self.validate_colors()
    
    def close(self, e) -> None:
        self.gui.window.destroy()
        exit(0)
    
    def int_message(self, message = None) -> None:
        self.snackbar.content.value = message
        self.snackbar.open = True
        self.gui.update()
    
    def must_reboot(self) -> None:
        self.int_message(self.langlab.EU_must_reboot.value)

    def reload(self) -> None:
        if (len(self.gui.controls)>1):
            if (self.grid_view in self.gui.controls):
                self.gui.remove(self.grid_view)
            elif (self.list_view in self.gui.controls):
                self.gui.remove(self.list_view)
        if (self.settings.view_mode == ViewMode.Grid):
            self.gui.add(self.grid_view)
        elif (self.settings.view_mode == ViewMode.List):
            self.gui.add(self.list_view)
        self.gui.update()
    
    def update_all(self) -> None:
        try:
            self.search_bar.update()
        except:
            pass
        try:
            self.mdl.update()
        except:
            pass
        try:
            self.grid_view.update()
        except:
            pass
        try:
            self.list_view.update()
        except:
            pass
        try:
            self.snackbar.update()
        except:
            pass
        try:
            self.drag_area.update()
        except:
            pass
        try:
            self.close_cross.update()
        except:
            pass
        try:
            self.theme_btn.update()
        except:
            pass
        try:
            self.view_mode_filter.update()
        except:
            pass
        try:
            self.top_bar.update()
        except:
            pass
        try:
            self.mainWindow.update()
        except:
            pass
    
    def view_mode_change(self, e):
        self.search_bar.value = ''
        self.settings.view_mode = ViewMode.List if (self.settings.view_mode == ViewMode.Grid) else ViewMode.Grid
        self.settings.dict['view_mode'] = self.settings.view_mode
        self.view_mode_filter.icon = Icons.top_bar_view_filter_list_icon_button if (self.settings.view_mode == ViewMode.Grid) else Icons.top_bar_view_filter_grid_icon_button
        self.view_mode_filter.icon_color = Colors.top_bar_view_filter_list_icon_button if (self.settings.view_mode == ViewMode.Grid) else Colors.top_bar_view_filter_grid_icon_button
        self.view_mode_filter.tooltip = self.langlab.EU_view_mode_filter_to_list_tooltip.value if (self.settings.view_mode == ViewMode.Grid) else self.langlab.EU_view_mode_filter_to_grid_tooltip.value
        self.save_settings()
        self.validate_colors()
    
    def theme_change(self, e):
        self.theme_btn.icon = Icons.top_bar_to_night_theme_icon_button if (self.settings.theme_mode == 'dark') else Icons.top_bar_to_light_theme_icon_button
        self.theme_btn.icon_color = Colors.top_bar_to_night_theme_icon_button if (self.settings.theme_mode == 'dark') else Colors.top_bar_to_light_theme_icon_button
        self.theme_btn.tooltip = self.langlab.EU_theme_button_to_night_theme_tooltip.value if (self.settings.theme_mode == 'dark') else self.langlab.EU_theme_button_to_light_theme_tooltip.value
        self.settings.theme_mode = 'light' if (self.settings.theme_mode == 'dark') else 'dark'
        self.settings.dict['theme_mode'] = self.settings.theme_mode
        self.gui.theme_mode = self.settings.theme_mode
        self.save_settings()
        self.gui.update()
    
    def round_change(self, e):
        self.settings._round = e.control.value
        self.settings.dict['_round'] = e.control.value
        self.save_settings()
    
    def paths_validate(self) -> None:
        if (not os.path.exists(Dirs.main)):
            os.mkdir(Dirs.main)
        if (not os.path.exists(Dirs.assets)):
            os.mkdir(Dirs.assets)
        if (not os.path.exists(Dirs.configs)):
            os.mkdir(Dirs.configs)
        if (not os.path.exists(Dirs.logs)):
            os.mkdir(Dirs.logs)
        if (not os.path.exists(Dirs.labs)):
            os.mkdir(Dirs.labs)
        if (not os.path.exists(Files.data)):
            expl_setts = { 'view_mode': 'grid', 'theme_mode': 'dark', '_round': 'all', 'color_database': [] }
            with open(Files.data, 'w+', -1, 'utf-8') as f:
                json.dump(expl_setts, f, indent=4)
                f.flush()
                f.close()
        if (not os.path.exists(Files.langlab)):
            pass
    
    def search_colors(self, e):
        if (e.control.value != '' and e.control.value != ' ' and e.control.value != None):
            clr_names = self.settings.color_database.get_ColorsNames()
            close_matches = Sequencer.get_matches_lstw(e.control.value, clr_names)
            if (len(close_matches)>=1):
                if (self.settings.view_mode == ViewMode.Grid):
                    self.grid_view.controls.clear()
                    for mtch in close_matches:
                        try:
                            self.add_to_grid(self.settings.color_database.get_byName(mtch))
                        except:
                            pass
                elif (self.settings.view_mode == ViewMode.List):
                    self.list_view.controls.clear()
                    for mtch in close_matches:
                        try:
                            self.add_to_list(self.settings.color_database.get_byName(mtch))
                        except:
                            pass
            else:
                if (self.settings.view_mode == ViewMode.Grid):
                    self.grid_view.controls.clear()
                    self.grid_view.expand = True
                    self.grid_view.controls.append(
                        flet.Row(
                            controls=[
                                flet.Text(
                                    self.langlab.EU_colors_not_found.value,
                                    opacity=0.3, 
                                    size=30,
                                    style=TextStyling.top_bar_drag_area_text
                                )
                            ],
                            expand=True,
                            alignment=flet.MainAxisAlignment.CENTER
                        )
                    )
                elif (self.settings.view_mode == ViewMode.List):
                    self.list_view.controls.clear()
                    self.list_view.expand = True
                    self.list_view.controls.append(
                        flet.Column(
                            controls=[
                                flet.Text(
                                    self.langlab.EU_colors_not_found.value,
                                    opacity=0.3,
                                    size=30,
                                    style=TextStyling.top_bar_drag_area_text
                                )
                            ],
                            expand=True,
                            horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                            alignment=flet.MainAxisAlignment.CENTER
                        )
                    )
        else:
            self.validate_colors_after_search()
        self.gui.update()

    def add_to_grid(self, color: Color) -> None:
        self.grid_view.controls.append(
            flet.Stack(
                controls=[
                    ColorContainer(
                        color,
                        content=flet.Text(
                            color.rgb.code,
                            text_align=flet.TextAlign.CENTER,
                            color=Colors.grid_view_item_bright_text if (ColorManager.bright(color.rgb)) else Colors.grid_view_item_dark_text
                        ),
                        bgcolor=color.hex.code,
                        shadow=flet.BoxShadow(
                            0, 50,
                            color.hex.code,
                            blur_style=flet.ShadowBlurStyle.OUTER
                        ),
                        border_radius=BorderRadiuses.grid_view_item_container,
                        height=180, 
                        width=100,
                        tooltip=color.name,
                        on_click=self.open_color_view
                    )
                ]
            )
        )
    
    def add_to_list(self, color: Color) -> None:
        self.list_view.controls.append(
            ColorListTile(
                color=color,
                leading=flet.Container(
                    bgcolor=color.hex.code,
                    shadow=flet.BoxShadow(
                        0, 50,
                        color.hex.code,
                        blur_style=flet.ShadowBlurStyle.OUTER
                    ),
                    border_radius=BorderRadiuses.list_view_item_container,
                    height=70,
                    width=100,
                    on_click=self.open_color_view
                ),
                title=flet.Text(color.name),
                subtitle=flet.Text(color.rgb.code),
                trailing=ColorPopupMenu(
                    color=color,
                    icon=Icons.list_view_item_trailing,
                    items=[
                        flet.PopupMenuItem(
                            'HEX {0}'.format(color.hex.code),
                            icon=Icons.list_view_item_copy_trailing_action,
                            on_click=self.color_f_click
                        ),
                        flet.PopupMenuItem(
                            'RGB {0}'.format(color.rgb.code),
                            icon=Icons.list_view_item_copy_trailing_action,
                            on_click=self.color_f_click
                        ),
                        flet.PopupMenuItem(
                            'HSV {0}'.format(color.hsv.code),
                            icon=Icons.list_view_item_copy_trailing_action,
                            on_click=self.color_f_click
                        ),
                        flet.PopupMenuItem(
                            'HSL {0}'.format(color.hsl.code),
                            icon=Icons.list_view_item_copy_trailing_action,
                            on_click=self.color_f_click
                        ),
                        flet.PopupMenuItem(
                            'YIQ {0}'.format(color.yiq.code),
                            icon=Icons.list_view_item_copy_trailing_action,
                            on_click=self.color_f_click
                        ),
                        flet.PopupMenuItem(
                            content=flet.Text(
                                self.langlab.EU_list_item_delete_action_text.value, 
                                color=Colors.list_view_item_delete_trailing_action_text),
                            icon=Icons.list_view_item_delete_trailing_action,
                            on_click=self.delete_color
                        )
                    ]
                ),
                on_click=self.open_color_view
            )
        )

    def validate_colors(self) -> None:
        if (self.settings.view_mode == ViewMode.Grid):
            self.grid_view.controls.clear()
            for col in self.settings.color_database.colors:
                self.add_to_grid(col)
            self.grid_view.controls.append(
                flet.Stack(
                    controls=[
                        flet.Container(
                            content=flet.Icon(
                                Icons.grid_view_add_new,
                                color=Colors.grid_view_add_new_icon
                            ),
                            bgcolor=Colors.grid_view_add_new_bg_container,
                            shadow=Shadows.grid_view_add_new_container,
                            border_radius=BorderRadiuses.grid_view_add_new_container,
                            height=180, 
                            width=100,
                            on_click=self.new_color_open
                        ),
                    ]
                )
            )
            self.reload()
        elif (self.settings.view_mode == ViewMode.List):
            self.list_view.controls.clear()
            for col in self.settings.color_database.colors:
                self.add_to_list(col)
            self.list_view.controls.append(
                flet.FilledButton(
                    ' ',
                    style=ButtonStyling.list_view_add_new_button,
                    icon=Icons.list_view_add_new,
                    bgcolor=Colors.list_view_add_new_bg_icon_button,
                    width=self.gui.width-50,
                    height=70,
                    on_click=self.new_color_open
                )
            )
            self.reload()
        self.gui.update()
    
    def validate_colors_after_search(self) -> None:
        if (self.settings.view_mode == ViewMode.Grid):
            self.grid_view.controls.clear()
            for col in self.settings.color_database.colors:
                self.add_to_grid(col)
            self.grid_view.controls.append(
                flet.Stack(
                    controls=[
                        flet.Container(
                            content=flet.Icon(
                                Icons.grid_view_add_new,
                                color=Colors.grid_view_add_new_icon
                            ),
                            bgcolor=Colors.grid_view_add_new_bg_container,
                            shadow=Shadows.grid_view_add_new_container,
                            border_radius=BorderRadiuses.grid_view_add_new_container,
                            height=180, 
                            width=100,
                            on_click=self.new_color_open
                        ),
                    ]
                )
            )
        elif (self.settings.view_mode == ViewMode.List):
            self.list_view.controls.clear()
            for col in self.settings.color_database.colors:
                self.add_to_list(col)
            self.list_view.controls.append(
                flet.IconButton(
                    Icons.list_view_add_new,
                    bgcolor=Colors.list_view_add_new_bg_icon_button,
                    width=self.gui.width-50,
                    height=70,
                    on_click=self.new_color_open
                )
            )
        self.gui.update()

    def create_reference_view_item(self, name: str, desc: str, docs_url: str, pip: bool = False, width_1: float = 5, width_2: float = 51) -> flet.Container:
        def to_docs(e):
            webbrowser.open_new_tab(e.control.tooltip)
        def pip_install(e):
            try:
                os.system(f'pip install {e.control.data}')
            except:
                pass
        return flet.Container(
            width=330,
            height=70,
            shape=flet.RoundedRectangleBorder(),
            border_radius=BorderRadiuses.mdl_about_view_container,
            border=flet.Border(
                flet.BorderSide(2, Colors.mdl_about_view_references_item_border_side),
                flet.BorderSide(2, Colors.mdl_about_view_references_item_border_side),
                flet.BorderSide(2, Colors.mdl_about_view_references_item_border_side),
                flet.BorderSide(2, Colors.mdl_about_view_references_item_border_side)
            ),
            shadow=Shadows.mdl_about_view_references_container,
            content=flet.Row(
                tight=True,
                controls=[
                    flet.Row(width=width_1),
                    flet.Icon(Icons.mdl_about_view_item_leading),
                    flet.Column(
                        tight=True,
                        spacing=0.1,
                        controls=[
                            flet.Text(name),
                            flet.Text(desc, opacity=0.85)
                        ]
                    ),
                    flet.Row(width=width_2),
                    flet.PopupMenuButton(
                        icon=flet.Icons.MORE_VERT,
                        items=[
                            flet.PopupMenuItem(
                                self.langlab.EU_about_view_item_docs.value,
                                Icons.mdl_about_view_item_docs_trailing_action,
                                tooltip=docs_url,
                                on_click=to_docs
                                ),
                            flet.PopupMenuItem(
                                self.langlab.EU_about_view_item_cannot_be_installed.value if (pip == False) else self.langlab.EU_about_view_item_install.value,
                                Icons.mdl_about_view_item_install_trailing_action,
                                data=name,
                                disabled=True if (pip == False) else False,
                                on_click=pip_install
                            )
                        ]
                    )
                ]
            )
        )

    def create_credits_view_item(self, name: str, w: str, git_url: str, width_1: float = 5, width_2: float = 51) -> flet.Container:
        def to_git(e):
            webbrowser.open_new_tab(e.control.tooltip)
        return flet.Container(
            width=330,
            height=70,
            shape=flet.RoundedRectangleBorder(),
            border_radius=BorderRadiuses.mdl_about_view_container,
            border=flet.Border(
                flet.BorderSide(2, Colors.mdl_about_view_credits_item_border_side),
                flet.BorderSide(2, Colors.mdl_about_view_credits_item_border_side),
                flet.BorderSide(2, Colors.mdl_about_view_credits_item_border_side),
                flet.BorderSide(2, Colors.mdl_about_view_credits_item_border_side)
            ),
            shadow=Shadows.mdl_about_view_credits_container,
            content=flet.Row(
                tight=True,
                controls=[
                    flet.Row(width=width_1),
                    flet.Icon(Icons.mdl_about_view_item_credits_trailing_action),
                    flet.Column(
                        tight=True,
                        spacing=0.1,
                        controls=[
                            flet.Text(w),
                            flet.Text(f'by {name}', opacity=0.85)
                        ]
                    ),
                    flet.Row(width=width_2),
                    flet.PopupMenuButton(
                        icon=flet.Icons.MORE_VERT,
                        items=[
                            flet.PopupMenuItem(
                                self.langlab.EU_about_view_item_credits_action_text.value,
                                Icons.mdl_about_view_item_credits_trailing_action,
                                tooltip=git_url,
                                on_click=to_git
                            )
                        ]
                    )
                ]
            )
        )
    
    def open_logger(self, e):
        pass
    
    def open_about(self, e):
        def to_docs(e):
            webbrowser.open_new_tab(e.control.tooltip)
        def pip_install(e):
            try:
                os.system(f'pip install {e.control.data}')
            except:
                pass
        self.mdl = flet.AlertDialog(
            scrollable=True,
            title=flet.Text('About'),
            content=flet.Column(
                tight=True,
                controls=[
                    flet.Row(
                        controls=[
                            flet.Text('Description', size=16)
                        ], alignment=flet.MainAxisAlignment.CENTER
                    ),
                    flet.Container(
                        width=330,
                        height=85,
                        shape=flet.RoundedRectangleBorder(),
                        border_radius=BorderRadiuses.mdl_about_view_container,
                        border=flet.Border(
                            flet.BorderSide(2, Colors.mdl_about_view_description_item_border_side),
                            flet.BorderSide(2, Colors.mdl_about_view_description_item_border_side),
                            flet.BorderSide(2, Colors.mdl_about_view_description_item_border_side),
                            flet.BorderSide(2, Colors.mdl_about_view_description_item_border_side)
                        ),
                        shadow=Shadows.mdl_about_view_description_container,
                        content=flet.Row(
                            tight=True,
                            controls=[
                                flet.TextField(
                                    'Desktop application for maintaining your own color palette.',
                                    width=325,
                                    height=70,
                                    read_only=True,
                                    multiline=True
                                )
                            ]
                        )
                    ),
                    flet.Row(
                        controls=[
                            flet.Text('References', size=16)
                        ], alignment=flet.MainAxisAlignment.CENTER
                    ),
                    self.create_reference_view_item('flet', 'UI library', 'https://flet.dev/docs/', True, width_2=154),
                    self.create_reference_view_item('os', 'Interaction with OS', 'https://docs.python.org/3/library/os.html', width_2=90),
                    self.create_reference_view_item('json', 'Interaction with json files', 'https://docs.python.org/3/library/json.html', width_2=54),
                    self.create_reference_view_item('math', 'Mathematical functions', 'https://docs.python.org/3/library/math.html', width_2=65),
                    self.create_reference_view_item('pyperclip', 'Interaction with clipboard', 'https://pyperclip.readthedocs.io/en/latest/', True),
                    self.create_reference_view_item('subprocess', 'Subprocess management', 'https://docs.python.org/3/library/subprocess.html', width_2=55),
                    self.create_reference_view_item('webbrowser', 'Interaction with web-browser', 'https://docs.python.org/3/library/webbrowser.html', width_2=30),
                    flet.Row(
                        controls=[
                            flet.Text('Credits', size=16)
                        ], alignment=flet.MainAxisAlignment.CENTER
                    ),
                    self.create_credits_view_item('denza', 'Code', 'https://github.com/decxdenza', width_2=161),
                    self.create_credits_view_item('KiriX', 'Mathematical calculations', 'https://github.com/K1r1X', width_2=53)
                ], alignment=flet.MainAxisAlignment.CENTER
            )
        )
        self.gui.open(self.mdl)
    
    def open_color_view(self, e):
        def copy_name(e):
            pyperclip.copy(e.control.value)
            self.int_message(self.langlab.EU_name_clip_copy.value)
        def copy_hex(e):
            pyperclip.copy(e.control.value)
            self.int_message(self.langlab.EU_hex_clip_copy.value)
        def copy_rgb(e):
            pyperclip.copy(e.control.parent.controls[0].controls[0].color.rgb.code)
            self.int_message(self.langlab.EU_rgb_clip_copy.value)
        def copy_hsv(e):
            pyperclip.copy(e.control.parent.controls[0].controls[0].color.hsv.code)
            self.int_message(self.langlab.EU_hsv_clip_copy.value)
        def copy_hsl(e):
            pyperclip.copy(e.control.parent.controls[0].controls[0].color.hsl.code)
            self.int_message(self.langlab.EU_hsl_clip_copy.value)
        def copy_yiq(e):
            pyperclip.copy(e.control.parent.controls[0].controls[0].color.yiq.code)
            self.int_message(self.langlab.EU_yiq_clip_copy.value)
        def part_copy(e):
            match(e.control.key):
                case 'RGB':
                    match(e.control.label):
                        case 'R':
                            pyperclip.copy(e.control.value)
                            self.int_message(self.langlab.EU_rgb_r_clip_copy.value)
                        case 'G':
                            pyperclip.copy(e.control.value)
                            self.int_message(self.langlab.EU_rgb_g_clip_copy.value)
                        case 'B':
                            pyperclip.copy(e.control.value)
                            self.int_message(self.langlab.EU_rgb_b_clip_copy.value)
                case 'HSV':
                    match(e.control.label):
                        case 'H':
                            pyperclip.copy(e.control.value)
                            self.int_message(self.langlab.EU_hsv_h_clip_copy.value)
                        case 'S':
                            pyperclip.copy(e.control.value)
                            self.int_message(self.langlab.EU_hsv_s_clip_copy.value)
                        case 'V':
                            pyperclip.copy(e.control.value)
                            self.int_message(self.langlab.EU_hsv_v_clip_copy.value)
                case 'HSL':
                    match(e.control.label):
                        case 'H':
                            pyperclip.copy(e.control.value)
                            self.int_message(self.langlab.EU_hsl_h_clip_copy.value)
                        case 'S':
                            pyperclip.copy(e.control.value)
                            self.int_message(self.langlab.EU_hsl_s_clip_copy.value)
                        case 'L':
                            pyperclip.copy(e.control.value)
                            self.int_message(self.langlab.EU_hsl_l_clip_copy.value)
                case 'YIQ':
                    match(e.control.label):
                        case 'Y':
                            pyperclip.copy(e.control.value)
                            self.int_message(self.langlab.EU_yiq_y_clip_copy.value)
                        case 'I':
                            pyperclip.copy(e.control.value)
                            self.int_message(self.langlab.EU_yiq_i_clip_copy.value)
                        case 'Q':
                            pyperclip.copy(e.control.value)
                            self.int_message(self.langlab.EU_yiq_q_clip_copy.value)
        if (type(e.control) == ColorContainer):
            self.mdl = flet.AlertDialog(
                title=flet.Row(
                    controls=[
                        flet.Text(self.langlab.EU_color_view_modal_title_text.value),
                        flet.IconButton(
                            Icons.mdl_color_view_delete_icon_button,
                            Colors.mdl_color_view_delete_icon_button,
                            on_click=self.delete_color
                        )
                    ]
                ),
                content=flet.Column(
                    tight=True,
                    controls=[
                        flet.Stack(
                            controls=[
                                ColorContainer(
                                    e.control.color,
                                    height=50,
                                    width=240,
                                    shadow=flet.BoxShadow(
                                        0, 50,
                                        e.control.color.hex.code,
                                        blur_style=flet.ShadowBlurStyle.OUTER
                                    ),
                                    bgcolor=e.control.color.hex.code,
                                    border_radius=BorderRadiuses.mdl_color_view_container,
                                )
                            ]
                        ),
                        flet.TextField(e.control.color.name, text_size=12, tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label=self.langlab.EU_color_view_modal_item_color_name_label_text.value, on_click=copy_name, read_only=True),
                        flet.TextField(e.control.color.hex.code, text_size=12, tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='HEX', on_click=copy_hex, read_only=True),
                        flet.Row(
                            controls=[
                                flet.TextField(e.control.color.rgb.r, text_size=12, key='RGB', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='R', height=40, width=73, on_click=part_copy, read_only=True),
                                flet.TextField(e.control.color.rgb.g, text_size=12, key='RGB', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='G', height=40, width=73, on_click=part_copy, read_only=True),
                                flet.TextField(e.control.color.rgb.b, text_size=12, key='RGB', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='B', height=40, width=73, on_click=part_copy, read_only=True)
                            ]
                        ),
                        flet.ElevatedButton(self.langlab.EU_color_view_modal_item_rgb_copy_button_text.value, Icons.mdl_color_view_copy_action_button, on_click=copy_rgb, width=240),
                        flet.Row(
                            controls=[
                                flet.TextField(e.control.color.hsv.h, text_size=12, key='HSV', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='H', height=40, width=73, on_click=part_copy, read_only=True),
                                flet.TextField(e.control.color.hsv.s, text_size=12, key='HSV', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='S', height=40, width=73, on_click=part_copy, read_only=True),
                                flet.TextField(e.control.color.hsv.v, text_size=12, key='HSV', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='V', height=40, width=73, on_click=part_copy, read_only=True)
                            ]
                        ),
                        flet.ElevatedButton(self.langlab.EU_color_view_modal_item_hsv_copy_button_text.value, Icons.mdl_color_view_copy_action_button, on_click=copy_hsv, width=240),
                        flet.Row(
                            controls=[
                                flet.TextField(e.control.color.hsl.h, text_size=12, key='HSL', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='H', height=40, width=73, on_click=part_copy, read_only=True),
                                flet.TextField(e.control.color.hsl.s, text_size=12, key='HSL', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='S', height=40, width=73, on_click=part_copy, read_only=True),
                                flet.TextField(e.control.color.hsl.l, text_size=12, key='HSL', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='L', height=40, width=73, on_click=part_copy, read_only=True)
                            ]
                        ),
                        flet.ElevatedButton(self.langlab.EU_color_view_modal_item_hsl_copy_button_text.value, Icons.mdl_color_view_copy_action_button, on_click=copy_hsl, width=240),
                        flet.Row(
                            controls=[
                                flet.TextField(e.control.color.yiq.y, text_size=12, key='YIQ', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='Y', height=40, width=73, on_click=part_copy, read_only=True),
                                flet.TextField(e.control.color.yiq.i, text_size=12, key='YIQ', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='I', height=40, width=73, on_click=part_copy, read_only=True),
                                flet.TextField(e.control.color.yiq.q, text_size=12, key='YIQ', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='Q', height=40, width=73, on_click=part_copy, read_only=True)
                            ]
                        ),
                        flet.ElevatedButton(self.langlab.EU_color_view_modal_item_yiq_copy_button_text.value, Icons.mdl_color_view_copy_action_button, on_click=copy_yiq, width=240),
                    ], alignment=flet.MainAxisAlignment.CENTER
                )
            )
        elif (type(e.control) == ColorListTile):
            self.mdl = flet.AlertDialog(
                title=flet.Row(
                    controls=[
                        flet.Text(self.langlab.EU_color_view_modal_title_text.value),
                        flet.IconButton(
                            Icons.mdl_color_view_delete_icon_button,
                            Colors.mdl_color_view_delete_icon_button,
                            on_click=self.delete_color
                        )
                    ]
                ),
                content=flet.Column(
                    tight=True,
                    controls=[
                        flet.Stack(
                            controls=[
                                ColorContainer(
                                    e.control.color,
                                    height=50,
                                    width=240,
                                    shadow=flet.BoxShadow(
                                        0, 50,
                                        e.control.color.hex.code,
                                        blur_style=flet.ShadowBlurStyle.OUTER
                                    ),
                                    bgcolor=e.control.color.hex.code,
                                    border_radius=BorderRadiuses.mdl_color_view_container,
                                )
                            ]
                        ),
                        flet.TextField(e.control.color.name, text_size=12, tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label=self.langlab.EU_color_view_modal_item_color_name_label_text.value, on_click=copy_name, read_only=True),
                        flet.TextField(e.control.color.hex.code, text_size=12, tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='HEX', on_click=copy_hex, read_only=True),
                        flet.Row(
                            controls=[
                                flet.TextField(e.control.color.rgb.r, text_size=12, key='RGB', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='R', height=40, width=73, on_click=part_copy, read_only=True),
                                flet.TextField(e.control.color.rgb.g, text_size=12, key='RGB', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='G', height=40, width=73, on_click=part_copy, read_only=True),
                                flet.TextField(e.control.color.rgb.b, text_size=12, key='RGB', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='B', height=40, width=73, on_click=part_copy, read_only=True)
                            ]
                        ),
                        flet.ElevatedButton(self.langlab.EU_color_view_modal_item_rgb_copy_button_text.value, Icons.mdl_color_view_copy_action_button, on_click=copy_rgb, width=240),
                        flet.Row(
                            controls=[
                                flet.TextField(e.control.color.hsv.h, text_size=12, key='HSV', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='H', height=40, width=73, on_click=part_copy, read_only=True),
                                flet.TextField(e.control.color.hsv.s, text_size=12, key='HSV', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='S', height=40, width=73, on_click=part_copy, read_only=True),
                                flet.TextField(e.control.color.hsv.v, text_size=12, key='HSV', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='V', height=40, width=73, on_click=part_copy, read_only=True)
                            ]
                        ),
                        flet.ElevatedButton(self.langlab.EU_color_view_modal_item_hsv_copy_button_text.value, Icons.mdl_color_view_copy_action_button, on_click=copy_hsv, width=240),
                        flet.Row(
                            controls=[
                                flet.TextField(e.control.color.hsl.h, text_size=12, key='HSL', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='H', height=40, width=73, on_click=part_copy, read_only=True),
                                flet.TextField(e.control.color.hsl.s, text_size=12, key='HSL', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='S', height=40, width=73, on_click=part_copy, read_only=True),
                                flet.TextField(e.control.color.hsl.l, text_size=12, key='HSL', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='L', height=40, width=73, on_click=part_copy, read_only=True)
                            ]
                        ),
                        flet.ElevatedButton(self.langlab.EU_color_view_modal_item_hsl_copy_button_text.value, Icons.mdl_color_view_copy_action_button, on_click=copy_hsl, width=240),
                        flet.Row(
                            controls=[
                                flet.TextField(e.control.color.yiq.y, text_size=12, key='YIQ', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='Y', height=40, width=73, on_click=part_copy, read_only=True),
                                flet.TextField(e.control.color.yiq.i, text_size=12, key='YIQ', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='I', height=40, width=73, on_click=part_copy, read_only=True),
                                flet.TextField(e.control.color.yiq.q, text_size=12, key='YIQ', tooltip=self.langlab.EU_color_view_modal_item_copy_tooltip.value, label='Q', height=40, width=73, on_click=part_copy, read_only=True)
                            ]
                        ),
                        flet.ElevatedButton(self.langlab.EU_color_view_modal_item_yiq_copy_button_text.value, Icons.mdl_color_view_copy_action_button, on_click=copy_yiq, width=240),
                    ], alignment=flet.MainAxisAlignment.CENTER
                )
            )
        self.gui.open(self.mdl)
        self.gui.update()
    
    def color_f_click(self, e):
        if ('HEX ' in e.control.text):
            pyperclip.copy(e.control.text.replace('HEX ', ''))
            self.int_message(self.langlab.EU_hex_clip_copy.value)
        elif ('RGB ' in e.control.text):
            pyperclip.copy(e.control.text.replace('RGB ', ''))
            self.int_message(self.langlab.EU_rgb_clip_copy.value)
        elif ('HSV ' in e.control.text):
            pyperclip.copy(e.control.text.replace('HSV ', ''))
            self.int_message(self.langlab.EU_hsv_clip_copy.value)
        elif ('HSL ' in e.control.text):
            pyperclip.copy(e.control.text.replace('HSL ', ''))
            self.int_message(self.langlab.EU_hsl_clip_copy.value)
        elif ('YIQ ' in e.control.text):
            pyperclip.copy(e.control.text.replace('YIQ ', ''))
            self.int_message(self.langlab.EU_yiq_clip_copy.value)
    
    def load_settings(self) -> None:
        if (os.path.exists(Files.data)):
            try:
                data = None
                with open(Files.data, 'r', -1, 'utf-8') as f:
                    data = json.load(f)
                    f.close()
                self.settings = Settings(dict(data))
            except:
                self.settings = Settings({ 'view_mode': 'grid', 'theme_mode': 'dark', '_round': 'all', 'color_database': [] })
        else:
            expl_setts = { 'view_mode': 'grid', 'theme_mode': 'dark', '_round': 'all', 'color_database': [] }
            with open(Files.data, 'w+', -1, 'utf-8') as f:
                try:
                    json.dump(expl_setts, f, indent=4)
                    f.flush()
                    f.close()
                except:
                    pass
            self.settings = Settings(expl_setts)
    
    def load_lang(self) -> None:
        if (self.langlab == None):
            self.langlab = LanguageLab()
        if (os.path.exists(Files.langlab)):
            try:
                self.fix_lang()
                data = None
                with open(Files.langlab, 'r', -1, 'utf-8') as r:
                    data = json.load(r)
                    r.close()
                for var in list(self.langlab.current_dict().keys()):
                    if (var in data):
                        self.langlab.__getattribute__(var).value = data[var]
            except:
                self.langlab = LanguageLab()
                self.fix_lang()
        else:
            with open(Files.langlab, 'w+', -1, 'utf-8') as w:
                json.dump(self.langlab.default_dict(), w, indent=4)
                w.flush()
                w.close()
    
    def save_settings(self) -> None:
        with open(Files.data, 'w+', -1, 'utf-8') as f:
            f.truncate(0)
            json.dump(self.settings.dict, f, indent=4)
            f.flush()
            f.close()
    
    def int_reset_lang(self) -> None:
        with open(Files.langlab, 'w+', -1, 'utf-8') as w:
            w.truncate(0)
            json.dump(self.langlab.default_dict(), w, indent=4)
            w.flush()
            w.close()
    
    def reset_lang(self) -> None:
        self.gui.close(self.mdl)
        self.gui.update()
        self.int_reset_lang()
        self.update_all()
        self.must_reboot()
    
    def fix_lang(self) -> None:
        data = None
        with open(Files.langlab, 'r+', -1, 'utf-8') as rw:
            data = json.load(rw)
            for key in list(self.langlab.default_dict().keys()):
                if (key not in list(dict(data).keys())):
                    data[key] = self.langlab.__getattribute__(key).default
            rw.seek(0)
            rw.truncate(0)
            json.dump(dict(data), rw, indent=4)
            rw.flush()
            rw.close()
    
    def append_lang(self) -> None:
        data = None
        with open(Files.langlab, 'r', -1, 'utf-8') as r:
            data = json.load(r)
            r.close()
        for key in list(self.langlab.default_dict().keys()):
            if (key not in list(dict(data).keys())):
                data[key] = self.langlab.default[key]
        with open(Files.langlab, 'w+', -1, 'utf-8') as w:
            w.truncate(0)
            json.dump(dict(data), w, indent=4)
            w.flush()
            w.close()
    
    def new_color_open(self, e):
        picker = ColorPicker()
        def close(e):
            self.gui.close(self.mdl)
            #self.reload()
            self.gui.update()
        def focus(e):
            e.control.border_color = None
            e.control.parent.controls[0].visible = False
            self.gui.update()
        self.mdl = flet.AlertDialog(
            title=flet.Text(self.langlab.EU_new_color_view_modal_title_text.value),
            content=flet.Column(
                tight=True,
                controls=[
                    flet.Text(
                        self.langlab.EU_new_color_view_modal_color_name_required_text.value,
                        color=Colors.mdl_add_new_required_field_text,
                        size=12,
                        visible=False
                    ),
                    flet.TextField(
                        label=self.langlab.EU_new_color_view_modal_color_name_label_text.value,
                        hint_text=self.langlab.EU_new_color_view_modal_color_name_hint_text.value,
                        on_focus=focus
                    ),
                    picker
                ],
                alignment=flet.MainAxisAlignment.CENTER
            ),
            actions=[
                flet.OutlinedButton(
                    self.langlab.EU_new_color_view_modal_save_button_text.value,
                    Icons.mdl_add_new_save_button,
                    scale=1.1,
                    on_click=self.save_new_color_mdl
                )
            ]
        )
        self.gui.open(self.mdl)
        self.gui.update()
    
    def save_new_color_mdl(self, e):
        if (e.control.parent.content.controls[1].value == '' or e.control.parent.content.controls[1].value == None):
            self.int_message(self.langlab.EU_color_name_not_entered.value)
            e.control.parent.content.controls[1].border_color = Colors.mdl_add_new_required_field_text
            e.control.parent.content.controls[0].visible = True
            self.gui.update()
            return
        self.gui.close(self.mdl)
        self.gui.update()
        hex = HEX(e.control.parent.content.controls[2].color)
        rgb = ColorManager.to_rgb(hex)
        hsv = ColorManager.to_hsv(rgb, True if (self.settings._round == 'all') else False)
        hsl = ColorManager.to_hsl(rgb, True if (self.settings._round == 'all') else False)
        yiq = ColorManager.to_yiq(rgb, True if (self.settings._round == 'all') else False)
        self.settings.color_database.colors.append(Color(None, e.control.parent.content.controls[1].value, hex, rgb, hsv, hsl, yiq))
        self.settings.dict['color_database'].append({ 'name': e.control.parent.content.controls[1].value, 'hex': hex.code, 'rgb': {'r': rgb.r, 'g': rgb.g, 'b': rgb.b}, 'hsv': {'h': hsv.h, 's': hsv.s, 'v': hsv.v}, 'hsl': {'h': hsl.h, 's': hsl.s, 'l': hsl.l}, 'yiq': {'y': yiq.y, 'i': yiq.i, 'q': yiq.q} })
        self.save_settings()
        self.validate_colors()
    
    def delete_color(self, e):
        if (type(e.control) == flet.IconButton):
            color = e.control.parent.parent.content.controls[0].controls[0].color
            try:
                self.gui.close(self.mdl)
                self.gui.update()
            except:
                pass
        else:
            color = e.control.parent.color
        self.settings.color_database.colors.remove(color)
        d = { 'name': color.name, 'hex': color.hex.code, 'rgb': {'r': color.rgb.r, 'g': color.rgb.g, 'b': color.rgb.b}, 'hsv': {'h': color.hsv.h, 's': color.hsv.s, 'v': color.hsv.v}, 'hsl': {'h': color.hsl.h, 's': color.hsl.s, 'l': color.hsl.l}, 'yiq': {'y': color.yiq.y, 'i': color.yiq.i, 'q': color.yiq.q} }
        self.settings.dict['color_database'].remove(d)
        self.save_settings()
        self.validate_colors()
    
    def open_settings_view(self, e):
        def view_info(e):
            self.int_message(e.control.tooltip)
        self.mdl = flet.AlertDialog(
            title=flet.Text(self.langlab.EU_settings_modal_title_text.value),
            content=flet.Column(
                tight=True,
                controls=[
                    flet.Text(self.langlab.EU_settings_languagelab_title_text.value, text_align=flet.TextAlign.END),
                    flet.Row(
                        controls=[
                            flet.Button(
                                self.langlab.EU_settings_languagelab_reset_button_text.value,
                                Icons.mdl_settings_view_languagelab_reset_button,
                                tooltip=self.langlab.EU_settings_languagelab_reset_tooltip.value,
                                width=110,
                                on_click=lambda _: self.reset_lang()
                            ),
                            flet.Button(
                                self.langlab.EU_settings_langlab_to_dir.value,
                                Icons.mdl_settings_view_languagelab_open_dir_button,
                                width=110,
                                on_click=lambda _: subprocess.run(['explorer.exe', Dirs.labs])
                            )
                        ]
                    ),
                    flet.Text(self.langlab.EU_settings_colormanager_title_text.value, text_align=flet.TextAlign.END),
                    flet.Row(
                        controls=[
                            flet.Dropdown(
                                label=self.langlab.EU_settings_colormanager_dropdown_title_text.value,
                                value='all',
                                width=195,
                                options=[
                                    flet.dropdown.Option(
                                        'all', 
                                        self.langlab.EU_settings_colormanager_dropdown_all_option_text.value
                                    ),
                                    flet.dropdown.Option(
                                        'half',
                                        self.langlab.EU_settings_colormanager_dropdown_half_option_text.value
                                    )
                                ],
                                on_change=self.round_change
                            ),
                            flet.IconButton(
                                Icons.mdl_settings_view_colormanager_dropdown_help,
                                on_click=view_info
                            )
                        ]
                    )
                ],
                alignment=flet.MainAxisAlignment.CENTER
            )
        )
        self.mdl.content.controls[3].controls[1].tooltip = f'{self.mdl.content.controls[3].controls[0].options[0].text}: {self.langlab.EU_settings_colormanager_dropdown_all.value} {self.mdl.content.controls[3].controls[0].options[1].text}: {self.langlab.EU_settings_colormanager_dropdown_half.value}'
        self.gui.open(self.mdl)
        self.gui.update()

if (__name__ == '__main__'):
    flet.app(ColorExplorer)
