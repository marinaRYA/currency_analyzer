import flet as ft
import time
import currency

ETH = currency.getdata('ETH')
BTC = currency.getdata('BTC')

#ETH = [(1, 100), (2, 120), (3, 110), (4, 130)]
#BTC = [(1, 50000), (2, 52000), (3, 51000), (4, 53000)]

class RealTimeChart(ft.UserControl):
    def __init__(self):
        self.y_labels: list = []
        self.data_points: list = []
        self.points: list = ETH

        self.chart = ft.LineChart(
            tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.WHITE),
            min_y=int(min(self.points, key=lambda y: y[1])[1]),
            max_y=int(max(self.points, key=lambda y: y[1])[1]),
            min_x=int(min(self.points, key=lambda x: x[0])[0]),
            max_x=int(max(self.points, key=lambda x: x[0])[0]),
            expand=True,
            left_axis=ft.ChartAxis(labels_size=50),
            bottom_axis=ft.ChartAxis(labels_interval=1, labels_size=40),
        )

        self.line_chart = ft.LineChartData(
            color=ft.colors.GREEN,
            stroke_width=2,
            curved=True,
            stroke_cap_round=True,
            below_line_gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[
                    ft.colors.with_opacity(0.25, ft.colors.GREEN),
                    "transparent",
                ],
            ),
        )

        super().__init__()

    def create_data_point(self, x, y):
        return ft.LineChartDataPoint(
            x,
            y,
            selected_below_line=ft.ChartPointLine(
                width=0.5, color="white54", dash_pattern=[2, 4]
            ),
            selected_point=ft.ChartCirclePoint(stroke_width=1),
        )

    def get_data_points(self):
        for x, y in self.points:
            self.data_points.append(self.create_data_point(x, y))
            self.chart.update()
            time.sleep(0.05)

    def test_click(self, e):
        # switch the list
        self.switch_list(e)
        #
        self.chart.data_series = [self.line_chart]
        # get the new data points
        self.get_data_points()

    def switch_list(self, e):
        if e.control.data == "eth":
            self.points = ETH
        if e.control.data == "btc":
            self.points = BTC

        self.data_points = []
        self.chart.data_series = []
        self.line_chart.data_points = self.data_points

        self.chart.min_y = int(min(self.points, key=lambda y: y[1])[1])
        self.chart.max_y = int(max(self.points, key=lambda y: y[1])[1])
        self.chart.min_x = int(min(self.points, key=lambda x: x[0])[0])
        self.chart.max_x = int(max(self.points, key=lambda x: x[0])[0])
        self.chart.update()
        time.sleep(0.5)

    def get_data_buttons(self, btn_name, data):
        return ft.ElevatedButton(
            btn_name,
            width=140,
            height=40,
            style=ft.ButtonStyle(
                shape={"": ft.RoundedRectangleBorder(radius=6)},
            ),
            bgcolor="teal600",
            color="black",
            data=data,
            on_click=lambda e: self.test_click(e),
        )

    def build(self):

        self.line_chart.data_points = self.data_points
        self.chart.data_series = [self.line_chart]

        return ft.Column(
            horizontal_alignment="center",
            controls=[
                ft.Text(
                    "Historical Prices for cryptocurrencies",
                    size=16,
                    weight="bold",
                ),
                self.chart,
            ],
        )


def main(page: ft.Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    chart = RealTimeChart()
    page.add(
        ft.Column(
            expand=True,
            alignment="center",
            horizontal_alignment="center",
            controls=[
                ft.Text(
                    currency.get_month_and_year(),
                    size=14,
                    weight="bold",
                ),
                ft.Container(
                    expand=1,
                    border_radius=6,
                    bgcolor=ft.colors.with_opacity(0.005, ft.colors.WHITE10),
                    content=ft.Row(
                        alignment="center",
                        controls=[
                            chart.get_data_buttons("Ethereum", "eth"),
                            chart.get_data_buttons("Bitcoin", "btc"),
                        ],
                    ),
                ),
                ft.Container(
                    expand=4,
                    content=chart,
                    padding=20,
                    border_radius=6,
                    bgcolor=ft.colors.with_opacity(0.005, ft.colors.WHITE10),
                ),
            ],
        ),
    )
    page.update()
    time.sleep(1)
    chart.get_data_points()


ft.app(main)
