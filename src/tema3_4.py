import flet as ft
from typing import List, Callable

from formulas_estadísticas import (
    media, mediana, moda, media_agrupada, mediana_agrupada, moda_agrupada,
    cuartil, decil, percentil, rango_intercuartil, cuartil_agrupado,
    varianza, desviacion_estandar, rango, percentil_agrupado, decil_agrupado,
    coeficiente_variacion
)

class CalculadoraEstadistica:
    def __init__(self, page: ft.Page = None):
        self.page = page
        self.container = None
        self.initialize_controls()
        self.create_tabs()

    def initialize_controls(self):
        self.title = ft.Text(
            value="Medidas de tendencia central, de posición y de dispersión",
            theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
            text_align=ft.TextAlign.CENTER
        )

        self.data_type_switch = ft.Switch(
            label="Datos Agrupados",
            value=False,
        )

        self.values_input = ft.TextField(
            label="Ingrese límites inferiores de clase",
            width=420,
            hint_text="Ejemplo: 10,20,30,40,50",
            visible=False,
        )
        
        self.frequencies_input = ft.TextField(
            label="Ingrese frecuencias",
            width=420,
            hint_text="Ejemplo: 1,2,3,4,5",
            visible=False,
        )
        
        self.numbers_input = ft.TextField(
            label="Ingrese números",
            width=420,
            hint_text="Ejemplo: 1,2,3,4,5",
            visible=True,
            prefix_icon=ft.icons.FORMAT_LIST_NUMBERED,
        )

        self.calculate_button = ft.ElevatedButton("Calcular")
        self.calculate_position_button = ft.ElevatedButton("Calcular Posiciones")
        self.calcular_coeficiente_button = ft.ElevatedButton("Calcular Coeficiente")

    def build(self) -> ft.Container:
        if not self.container:
            input_container = ft.Container(
                content=ft.Column(
                    controls=[
                        self.data_type_switch,
                        self.values_input,
                        self.frequencies_input,
                        self.numbers_input,
                        self.calculate_button,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                padding=ft.padding.only(bottom=20),
            )

            self.container = ft.Container(
                content=ft.Column(
                    controls=[
                        self.title,
                        input_container,
                        self.tab,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
                expand=True  # Permite que el contenedor se expanda para llenar el espacio disponible
            )

        return self.container

    def setup_page(self):
        self.page.title = "Calculadora Estadística"
        self.page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.page.theme_mode = ft.ThemeMode.LIGHT

    def set_page(self, page: ft.Page):
        self.page = page
        if page:
            self.page.update()

    def update(self):
        if self.page:
            self.page.update()
        elif self.container:
            self.container.update()

    def parse_input(self, input_str: str) -> List[float]:
        try:
            return [float(x.strip()) for x in input_str.split(',') if x.strip()]
        except ValueError:
            return []

    def create_validate_input_function(self) -> Callable:
        def validate_input(control, e):
            try:
                if control.value:
                    nums = [float(x.strip()) for x in control.value.split(",")]
                    control.error_text = None
                else:
                    control.error_text = None
            except ValueError:
                control.error_text = "Ingrese solo números separados por comas"
            self.update()
        return validate_input

    def initialize_controls(self):
        self.title = ft.Text(
            value="Medidas de tendencia central, de posición y de dispersión",
            theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
            text_align=ft.TextAlign.CENTER
        )

        validar_entrada = self.create_validate_input_function()

        self.data_type_switch = ft.Switch(
            label="Datos Agrupados",
            value=False,
            on_change=lambda e: self.update_input_hint(e)
        )

        self.values_input = ft.TextField(
            label="Ingrese límites inferiores de clase",
            width=420,
            hint_text="Ejemplo: 10,20,30,40,50",
            visible=False,
            on_change=lambda e: validar_entrada(self.values_input, e)
        )
        self.frequencies_input = ft.TextField(
            label="Ingrese frecuencias",
            width=420,
            hint_text="Ejemplo: 1,2,3,4,5",
            visible=False,
            on_change=lambda e: validar_entrada(self.frequencies_input, e)
        )
        self.numbers_input = ft.TextField(
            label="Ingrese números",
            width=420,
            hint_text="Ejemplo: 1,2,3,4,5",
            visible=True,
            prefix_icon=ft.icons.FORMAT_LIST_NUMBERED,
            on_change=lambda e: validar_entrada(self.numbers_input, e)
        )

        self.decile_input = ft.TextField(
            label="Posición Decil (1-9)",
            width=210,
            hint_text="Ejemplo: 3",
        )
        self.percentile_input = ft.TextField(
            label="Posición Percentil (1-99)",
            width=210,
            hint_text="Ejemplo: 85",
        )

        self.media_input = ft.TextField(
            label="Valor de la media",
            width=210,
            hint_text="Ejemplo: 50.5",
        )
        self.desviacion_input = ft.TextField(
            label="Valor de desviacion",
            width=210,
            hint_text="Ejemplo: 25.7",
        )

        self.initialize_result_texts()

        self.calculate_button = ft.ElevatedButton("Calcular", on_click=lambda _: self.calcular_medidas())
        self.calculate_position_button = ft.ElevatedButton("Calcular Posiciones", on_click=self.calcular_medidas_de_posición)
        self.calcular_coeficiente_button = ft.ElevatedButton("Calcular Coeficiente", on_click=self.calcular_coeficiente)

    def initialize_result_texts(self):
        self.mean_result = ft.Text("Media: ")
        self.median_result = ft.Text("Mediana: ")
        self.mode_result = ft.Text("Moda: ")

        self.q1_result = ft.Text("Q1 (25%): ")
        self.q2_result = ft.Text("Q2 (50%): ")
        self.q3_result = ft.Text("Q3 (75%): ")

        self.decile_result = ft.Text("Decil: ")
        self.percentile_result = ft.Text("Percentil: ")
        self.iqr_result = ft.Text("Rango Intercuartil: ")

        self.variance_result = ft.Text("Varianza: ")
        self.std_dev_result = ft.Text("Desviación estándar: ")
        self.range_result = ft.Text("Rango: ")
        self.coeficiente = ft.Text("Coeficiente de variación: ", visible=False)

        self.coeficiente_result = ft.Text("Coeficiente de variación: ")

    def create_tabs(self):
        self.tab = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            indicator_color=ft.colors.GREEN_200,
            tabs=[
                self.create_tendencia_central_tab(),
                self.create_posicion_tab(),
                self.create_posicion_adicional_tab(),
                self.create_dispersion_tab()
            ],
            expand=1
        )

        self.t_coeficiente_variacion = self.create_coeficiente_variacion_tab()

    def create_tendencia_central_tab(self):
        return ft.Tab(
            text="Tendencia Central",
            icon=ft.icons.CENTER_FOCUS_WEAK,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        self.mean_result,
                        self.median_result,
                        self.mode_result,
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
            ),
        )

    def create_posicion_tab(self):
        return ft.Tab(
            text="Posición",
            icon=ft.icons.POLICY_SHARP,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        self.q1_result,
                        self.q2_result,
                        self.q3_result,
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
            ),
        )

    def create_posicion_adicional_tab(self):
        return ft.Tab(
            text="Posición Adicional",
            icon=ft.icons.ANALYTICS_OUTLINED,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                self.decile_input,
                                self.percentile_input,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        self.calculate_position_button,
                        self.decile_result,
                        self.percentile_result,
                        self.iqr_result,
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
            ),
        )

    def create_dispersion_tab(self):
        return ft.Tab(
            text="Dispersión",
            icon=ft.icons.DEBLUR_SHARP,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        self.variance_result,
                        self.std_dev_result,
                        self.range_result,
                        self.coeficiente,
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
            ),
        )

    def create_coeficiente_variacion_tab(self):
        return ft.Tab(
            text="Coeficiente de Variacion",
            icon=ft.icons.EQUALIZER,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                self.media_input,
                                self.desviacion_input,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        self.calcular_coeficiente_button,
                        self.coeficiente_result,
                    ],
                    spacing=20,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
            ),
        )

    def setup_layout(self):
        input_container = ft.Container(
            content=ft.Column(
                controls=[
                    self.data_type_switch,
                    self.values_input,
                    self.frequencies_input,
                    self.numbers_input,
                    self.calculate_button,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=ft.padding.only(bottom=20),
        )

        self.page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        self.title,
                        input_container,
                        self.tab,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
            )
        )

    def update_input_hint(self, e):
        if self.data_type_switch.value:
            self.values_input.visible = True
            self.frequencies_input.visible = True
            self.numbers_input.visible = False
            self.coeficiente.visible = True
            self.tab.tabs.append(self.t_coeficiente_variacion)
        else:
            self.values_input.visible = False
            self.frequencies_input.visible = False
            self.numbers_input.visible = True
            self.coeficiente.visible = False
            if self.t_coeficiente_variacion in self.tab.tabs:
                self.tab.tabs.remove(self.t_coeficiente_variacion)

        self.reset_results()
        self.page.update()

    def reset_results(self):
        self.mean_result.value = "Media: "
        self.median_result.value = "Mediana: "
        self.mode_result.value = "Moda: "
        self.q1_result.value = "Q1 (25%): "
        self.q2_result.value = "Q2 (50%): "
        self.q3_result.value = "Q3 (75%): "
        self.decile_result.value = "Decil: "
        self.percentile_result.value = "Percentil: "
        self.iqr_result.value = "Rango Intercuartil: "
        self.variance_result.value = "Varianza: "
        self.std_dev_result.value = "Desviación estándar: "
        self.range_result.value = "Rango: "
        self.coeficiente.value = "Coeficiente de variación: "
        self.decile_input.value = ""
        self.percentile_input.value = ""
        self.media_input.value = ""
        self.desviacion_input.value = ""
        self.coeficiente_result.value = "Coeficiente de variación: "

    def calcular_medidas_de_posición(self, e):
        try:
            if self.data_type_switch.value:  # Datos agrupados
                limites = self.parse_input(self.values_input.value)
                frecuencias = self.parse_input(self.frequencies_input.value)
                
                if not limites or not frecuencias or len(limites) != len(frecuencias):
                    raise ValueError("Datos inválidos o incompletos")

                self.calcular_decil_percentil_agrupados(limites, frecuencias)
                self.calcular_rango_intercuartil_agrupados(limites, frecuencias)

            else:  # Datos individuales
                datos = self.parse_input(self.numbers_input.value)
                if not datos:
                    raise ValueError("Por favor ingrese datos válidos")

                self.calcular_decil_percentil_individuales(datos)
                self.calcular_rango_intercuartil_individuales(datos)

            self.page.update()

        except Exception as e:
            self.mostrar_error(str(e))

    def calcular_decil_percentil_agrupados(self, limites, frecuencias):
        if self.decile_input.value:
            try:
                pos_decil = int(self.decile_input.value)
                if 1 <= pos_decil <= 9:
                    decil_val = decil_agrupado(pos_decil, limites, frecuencias)
                    self.decile_result.value = f"Decil {pos_decil}: {decil_val:.2f}"
                else:
                    self.decile_result.value = "Error: Posición del decil debe estar entre 1 y 9"
            except ValueError:
                self.decile_result.value = "Error: Ingrese un número válido para el decil"

        if self.percentile_input.value:
            try:
                pos_percentil = int(self.percentile_input.value)
                if 1 <= pos_percentil <= 99:
                    percentil_val = percentil_agrupado(pos_percentil, limites, frecuencias)
                    self.percentile_result.value = f"Percentil {pos_percentil}: {percentil_val:.2f}"
                else:
                    self.percentile_result.value = "Error: Posición del percentil debe estar entre 1 y 99"
            except ValueError:
                self.percentile_result.value = "Error: Ingrese un número válido para el percentil"

    def calcular_decil_percentil_individuales(self, datos):
        if self.decile_input.value:
            try:
                pos_decil = int(self.decile_input.value)
                if 1 <= pos_decil <= 9:
                    decil_val = decil(datos, pos_decil)
                    self.decile_result.value = f"Decil {pos_decil}: {decil_val:.2f}"
                else:
                    self.decile_result.value = "Error: Posición del decil debe estar entre 1 y 9"
            except ValueError:
                self.decile_result.value = "Error: Ingrese un número válido para el decil"

        if self.percentile_input.value:
            try:
                pos_percentil = int(self.percentile_input.value)
                if 1 <= pos_percentil <= 99:
                    percentil_val = percentil(datos, pos_percentil)
                    self.percentile_result.value = f"Percentil {pos_percentil}: {percentil_val:.2f}"
                else:
                    self.percentile_result.value = "Error: Posición del percentil debe estar entre 1 y 99"
            except ValueError:
                self.percentile_result.value = "Error: Ingrese un número válido para el percentil"

    def calcular_rango_intercuartil_agrupados(self, limites, frecuencias):
        q1 = cuartil_agrupado(1, limites, frecuencias)
        q3 = cuartil_agrupado(3, limites, frecuencias)
        iqr = q3 - q1
        self.iqr_result.value = f"Rango Intercuartil: {iqr:.2f}"

    def calcular_rango_intercuartil_individuales(self, datos):
        iqr = rango_intercuartil(datos)
        self.iqr_result.value = f"Rango Intercuartil: {iqr:.2f}"

    def calcular_medidas(self):
        try:
            if self.data_type_switch.value:  # Datos agrupados
                self.calcular_medidas_agrupadas()
            else:  # Datos individuales
                self.calcular_medidas_individuales()

            self.page.update()

        except Exception as e:
            self.mostrar_error(str(e))

    def calcular_medidas_agrupadas(self):
        limites = self.parse_input(self.values_input.value)
        frecuencias = self.parse_input(self.frequencies_input.value)
        
        if not limites or not frecuencias or len(limites) != len(frecuencias):
            raise ValueError("Datos inválidos o incompletos")

        ancho_clase = limites[1] - limites[0]
        marcas_clase = [li + (ancho_clase/2) for li in limites]
        
        self.calcular_tendencia_central_agrupada(marcas_clase, frecuencias, limites)
        
        self.calcular_posicion_agrupada(limites, frecuencias)
        
        self.calcular_dispersion_agrupada(marcas_clase, frecuencias, limites)

    def calcular_tendencia_central_agrupada(self, marcas_clase, frecuencias, limites):
        mean_val = sum(m * f for m, f in zip(marcas_clase, frecuencias)) / sum(frecuencias)
        self.mean_result.value = f"Media: {mean_val:.2f}"
        
        try:
            median_val = mediana_agrupada(limites, frecuencias)
            self.median_result.value = f"Mediana: {median_val:.2f}"
        except Exception as e:
            self.median_result.value = "Mediana: Error en el cálculo"
            print(f"Error en mediana: {str(e)}")

        try:
            mode_val = moda_agrupada(limites, frecuencias)
            self.mode_result.value = f"Moda: {mode_val:.2f}"
        except Exception as e:
            self.mode_result.value = "Moda: Error en el cálculo"
            print(f"Error en moda: {str(e)}")

    def calcular_posicion_agrupada(self, limites, frecuencias):
        try:
            q1 = cuartil_agrupado(1, limites, frecuencias)
            q2 = cuartil_agrupado(2, limites, frecuencias)
            q3 = cuartil_agrupado(3, limites, frecuencias)
            
            self.q1_result.value = f"Q1 (25%): {q1:.2f}"
            self.q2_result.value = f"Q2 (50%): {q2:.2f}"
            self.q3_result.value = f"Q3 (75%): {q3:.2f}"
        except Exception as e:
            self.q1_result.value = "Q1: Error en el cálculo"
            self.q2_result.value = "Q2: Error en el cálculo"
            self.q3_result.value = "Q3: Error en el cálculo"
            print(f"Error en cuartiles: {str(e)}")

    def calcular_dispersion_agrupada(self, marcas_clase, frecuencias, limites):
        try:
            mean_val = sum(m * f for m, f in zip(marcas_clase, frecuencias)) / sum(frecuencias)
            
            var_p = sum(frecuencias[i] * (marcas_clase[i] - mean_val) ** 2 for i in range(len(frecuencias))) / sum(frecuencias)
            var_m = sum(frecuencias[i] * (marcas_clase[i] - mean_val) ** 2 for i in range(len(frecuencias))) / (sum(frecuencias) - 1)
            
            desv_est_p = var_p ** 0.5
            desv_est_m = var_m ** 0.5
            
            coeficiente_p = coeficiente_variacion(desv_est_p, mean_val)
            coeficiente_m = coeficiente_variacion(desv_est_m, mean_val)
            
            self.variance_result.value = f"Varianza (Poblacional): {var_p:.2f}\nVarianza (Muestral): {var_m:.2f}"
            self.std_dev_result.value = f"Desviación estándar (Poblacional): {desv_est_p:.2f}\nDesviación estándar (Muestral): {desv_est_m:.2f}"
            self.range_result.value = f"Rango: {max(limites) - min(limites):.2f}"
            self.coeficiente.value = f"Coeficiente de variación (Poblacional): {coeficiente_p:.2f}%\nCoeficiente de variación (Muestral): {coeficiente_m:.2f}%"
        except Exception as e:
            self.variance_result.value = "Varianza: Error en el cálculo"
            self.std_dev_result.value = "Desviación estándar: Error en el cálculo"
            self.range_result.value = "Rango: Error en el cálculo"
            print(f"Error en medidas de dispersión: {str(e)}")

    def calcular_medidas_individuales(self):
        datos = self.parse_input(self.numbers_input.value)
        if not datos:
            raise ValueError("Por favor ingrese datos válidos")

        mean_val = media(datos)
        median_val = mediana(datos)
        mode_val = moda(datos)
        
        self.mean_result.value = f"Media: {mean_val:.2f}"
        self.median_result.value = f"Mediana: {median_val:.2f}"
        self.mode_result.value = f"Moda: {', '.join(map(str, mode_val)) if mode_val else 'No hay moda'}"

        q1_val = cuartil(datos, 1)
        q2_val = cuartil(datos, 2)
        q3_val = cuartil(datos, 3)
        
        self.q1_result.value = f"Q1 (25%): {q1_val:.2f}"
        self.q2_result.value = f"Q2 (50%): {q2_val:.2f}"
        self.q3_result.value = f"Q3 (75%): {q3_val:.2f}"

        var_p = varianza(datos, "p")
        var_m = varianza(datos, "m")
        desv_est_p = desviacion_estandar(datos, "p")
        desv_est_m = desviacion_estandar(datos, "m")
        rango_val = rango(datos)
        
        self.variance_result.value = f"Varianza (Poblacional): {var_p:.2f}\nVarianza (Muestral): {var_m:.2f}"
        self.std_dev_result.value = f"Desviación estándar (Poblacional): {desv_est_p:.2f}\nDesviación estándar (Muestral): {desv_est_m:.2f}"
        self.range_result.value = f"Rango: {rango_val:.2f}"

    def calcular_coeficiente(self, e):
        try:
            if not self.media_input.value or not self.desviacion_input.value:
                raise ValueError("Ingrese valores para la media y desviacion estandar")
            
            try:
                media_v = float(self.media_input.value)
                desviacion_v = float(self.desviacion_input.value)

                coeficiente_valor = coeficiente_variacion(desviacion_v, media_v)
                estimacion = self.get_estimacion_precision(coeficiente_valor)

                self.coeficiente_result.value = f"Coeficiente de variación: {coeficiente_valor:.2f}%\nLas estimaciones se consideran {estimacion}"
            except ValueError:
                self.coeficiente_result.value = "Error: Ingrese numeros validos"
        
            self.page.update()

        except Exception as e:
            self.mostrar_error(str(e))

    def get_estimacion_precision(self, coeficiente_valor: float) -> str:
        if coeficiente_valor <= 7:
            return "precisas"
        elif 8 <= coeficiente_valor <= 14:
            return "aceptables"
        elif 15 <= coeficiente_valor <= 20:
            return "regulares"
        else:
            return "poco precisas"

    def mostrar_error(self, mensaje: str):
        if self.page:
            self.page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Error: {mensaje}")))
        self.update()