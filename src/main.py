import flet as ft
import matplotlib.pyplot as plt
import io
import base64
from collections import Counter
from Tema1_2 import tema1, tema2, tema3, tema4, tema5
from Tema5_6 import Tema5_6
from Tema7_8 import Tema7_8
from Tema10_11 import calcular_binomial, calcular_geometrica, calcular_hipergeometrica, calcular_multinomial, calcular_poisson, crear_barra_separacion, crear_pestana_binomial, crear_pestana_geometrica, crear_pestana_hipergeometrica, crear_pestana_multinomial, crear_pestana_poisson
from tema3_4 import CalculadoraEstadistica


class UI(ft.UserControl):

    def __init__(self, page):
        super().__init__(expand=True)
        self.page = page
        self.tema5_6 = Tema5_6()
        self.instanciaTab = Tema7_8()
        self.calculadora = CalculadoraEstadistica(page)
        self.calculadora.set_page(page)
        
        self.gradient_color = ft.LinearGradient(
            colors=["#007BFF", "#0066A2", "#003366"], 
            begin=ft.Alignment(0, 0),
            end=ft.Alignment(1, 0),
            stops=[0.0, 0.5, 1.0]
        )

        self.mode_switch = ft.Switch(
            value=True,
            on_change=self.switch_update,
            thumb_color="black",
            thumb_icon={  
                ft.ControlState.DEFAULT: ft.icons.LIGHT_MODE,
                ft.ControlState.SELECTED: ft.icons.DARK_MODE
            }
        )
        
        self.tema10_11_tabs = ft.Tabs(
            tabs=[
                ft.Tab(text="Tema 1: Binomial", content=crear_pestana_binomial(self.page)),
                ft.Tab(text="Tema 2: Multinomial", content=crear_pestana_multinomial(self.page)),
                ft.Tab(text="Tema 3: Hipergeométrica", content=crear_pestana_hipergeometrica(self.page)),
                ft.Tab(text="Tema 4: Geométrica", content=crear_pestana_geometrica(self.page)),
                ft.Tab(text="Tema 5: Poisson", content=crear_pestana_poisson(self.page)),
            ], 
            selected_index=0
        )        
        
        tema1_2_tabs = ft.Tabs(
            tabs=[
                ft.Tab(text="Tema 1: Tabla de Frecuencias", content=tema1(self.page)),
                ft.Tab(text="Tema 2: Gráfica de Barras", content=tema2(self.page)),
                ft.Tab(text="Tema 3: Gráfica de Pastel", content=tema3(self.page)),
                ft.Tab(text="Tema 4: Serie de Tiempo", content=tema4(self.page)),
                ft.Tab(text="Tema 5: Histograma", content=tema5(self.page)),
            ],
            selected_index=0
        )

        tema5_6_tabs = ft.Tabs(
            tabs=[
                self.tema5_6.tab_espacio_muestral(),
                self.tema5_6.tab_permutacion_normal(),
                self.tema5_6.tab_permutacion_repeticion(),
                self.tema5_6.tab_combinacion_normal(),
                self.tema5_6.tab_combinacion_repeticion(),
            ]
        )

        self.initial_container = ft.Container(
            bgcolor="#F0F0F0",
            border_radius=20,
            padding=20,
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Text("Tema 1 y 2", color="black"),
                    tema1_2_tabs,
                ],
                scroll="always", 
                expand=True,      
            ),
        )

        self.tema3_container = ft.Container(
            border_radius=20,
            padding=20,
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Text("Tema 3 y 4", color="black"),
                    self.calculadora.build()
                ],
                expand=True
            )
        )

        self.tema5_container = ft.Container(
            bgcolor="#F0F0F0",
            border_radius=20,
            padding=20,
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Text("Tema 5 y 6", color="black"),
                    tema5_6_tabs,
                ]
            )
        )

        tema7_8_tabs = ft.Tabs(
            tabs=[
                self.instanciaTab.tab_evento(),
                self.instanciaTab.tab_aditiva(),
                self.instanciaTab.tab_condicional(),
                self.instanciaTab.tab_independientes(),
                self.instanciaTab.tab_regla_multiplicativa(),
            ]
        )

        self.container = ft.Column(
            controls=[tema7_8_tabs],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True
        )

        self.tema9_container = ft.Container(
            bgcolor="#F0F0F0",
            border_radius=20,
            padding=20,
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Text("Tema 10 y 11", color="black"),
                    self.tema10_11_tabs,
                    ft.Container(border_radius=20)
                ]
            )
        )

        self.container_list = [
            self.initial_container, 
            self.tema3_container, 
            self.tema5_container, 
            self.container,
            self.tema9_container 
        ]

        self.container_1 = ft.Container(content=self.container_list[0], expand=True)

        self.navigation_container = ft.Container(
            col=1,
            gradient=self.gradient_color,
            border_radius=10,
            content=ft.Column(
                controls=[
                    ft.Container(
                        expand=True,
                        gradient=self.gradient_color, 
                        content=ft.NavigationRail(
                            bgcolor=ft.colors.TRANSPARENT,
                            expand=True,
                            on_change=self.change_page,
                            selected_index=0,
                            destinations=[
                                ft.NavigationBarDestination(icon=ft.icons.BAR_CHART),
                                ft.NavigationBarDestination(icon=ft.icons.SHOW_CHART),
                                ft.NavigationBarDestination(icon=ft.icons.CALCULATE),
                                ft.NavigationBarDestination(icon=ft.icons.PIE_CHART),
                                ft.NavigationBarDestination(icon=ft.icons.PERCENT),
                            ]
                        )
                    ),
                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            expand=True,
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                ft.IconButton(icon=ft.icons.OUTPUT),
                                self.mode_switch
                            ]
                        )
                    ),
                ]
            )
        )

        self.frame_2 = ft.Container(
            col=11,
            expand=True,
            content=self.container_1
        )

        self.container = ft.ResponsiveRow(
            controls=[self.navigation_container, self.frame_2]
        )

    def change_page(self, e):
        index = e.control.selected_index
        self.container_1.content = self.container_list[index]
        self.frame_2.content = self.container_1
        self.update()
        print(index)

    def switch_update(self, e):
        self.page.theme_mode = "dark" if e.control.value else "light"
        self.page.update()

    def build(self):
        return self.container
    
    def did_mount(self):
        self.calculadora.page = self.page
        self.update_event_handlers()

    def update_event_handlers(self):
        self.calculadora.calculate_button.on_click = lambda e: self.handle_calculate(e)
        self.calculadora.calculate_position_button.on_click = lambda e: self.handle_calculate_position(e)
        self.calculadora.calcular_coeficiente_button.on_click = lambda e: self.handle_calculate_coefficient(e)
        self.calculadora.data_type_switch.on_change = lambda e: self.handle_switch_change(e)
        validar_entrada = self.calculadora.create_validate_input_function()
        self.calculadora.values_input.on_change = lambda e: validar_entrada(self.calculadora.values_input, e)
        self.calculadora.frequencies_input.on_change = lambda e: validar_entrada(self.calculadora.frequencies_input, e)
        self.calculadora.numbers_input.on_change = lambda e: validar_entrada(self.calculadora.numbers_input, e)
        
        self.update()

    def handle_calculate(self, e):
        self.calculadora.calcular_medidas()
        self.update()

    def handle_calculate_position(self, e):
        self.calculadora.calcular_medidas_de_posición(e)
        self.update()

    def handle_calculate_coefficient(self, e):
        self.calculadora.calcular_coeficiente(e)
        self.update()

    def handle_switch_change(self, e):
        self.calculadora.update_input_hint(e)
        self.update()



def main(page: ft.Page):
    page.window.min_height = 820
    page.window.min_width = 510
    page.theme = ft.Theme(font_family="Open Sans")
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.add(UI(page))

ft.app(main)
