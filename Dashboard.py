import branca
import dash
import dash_core_components as dcc
import dash.dependencies as dpd
import dash_html_components as html
import folium
import numpy as np
import pandas
import plotly_express as px
from typing import Tuple

from WeatherDataFrame import WeatherDataFrame

class Dashboard:
    def __init__(self, weather_data_frame: WeatherDataFrame, map_file_name: str = 'map.html') -> None:
        """
        Constructeur de la classe Dashboard

        Parameters
        -------
            weather_data_frame: DataFrame contenant les données météo
        """
        self.app: dash.Dash = dash.Dash(__name__)
        self.map_file_name: str = map_file_name
        self.fig_data_frame: pandas.DataFrame = None
        self.map_data_frame: pandas.DataFrame = None
        self.get_map_dataframe(weather_data_frame)

    def get_map_dataframe(self, weather_data_frame: WeatherDataFrame) -> pandas.DataFrame:
        """
        Formate la weather DataFrame pour récupérer une DataFrame formatée pour la carte météo

        Parameters
        -------
            weather_data_frame: DataFrame contenant les données météo

        Returns
        -------
            La DataFrame pour la carte météo
        """

        weather_data_frame.format_data_frame()
        self.fig_data_frame = weather_data_frame.data_frame
        weather_data_frame.format_data_frame_groupby_commune()
        self.map_data_frame = weather_data_frame.data_frame
        return self.map_data_frame

    def create_map(self) -> None:
        """
        Créer une carte à partir de la DataFrame formatée pour la carte. Sauvegarde la map crée dans un fichier HTML.
        """

        latitude_values = self.map_data_frame['latitude'].values
        longitude_values = self.map_data_frame['longitude'].values
        temp_moy_values = self.map_data_frame['temp_C'].round(2).values
        city_values = self.map_data_frame['commune_name'].values

        # Cordonnées du centre de la France
        center_cord = (46.539758, 2.430331)
        weather_map = folium.Map(location=center_cord, zoom_start=6)

        color_map = branca.colormap.LinearColormap(colors=['blue', 'red'], vmin=min(temp_moy_values),
                                                   vmax=max(temp_moy_values))
        weather_map.add_child(color_map)

        for latitude, longitude, city, size, color in zip(latitude_values, longitude_values, city_values,
                                                          temp_moy_values, temp_moy_values):
            folium.CircleMarker(
                location=[latitude, longitude],
                radius=size,
                color=color_map(color),
                fill=True,
                fill_color=color_map(color),
                fill_opacity=0.6,
                popup=city + " " + str(size)
            ).add_to(weather_map)

        weather_map.save(outfile=self.map_file_name)

    def create_histogramme_fig(self) -> object:
        """
        Créer un histogramme de la moyenne de température dans l'intervalle [-8; 41[

        Returns
        -------
            Un NumPy Histogram avec les données formaté dans un plotly bar
        """

        counts_city, bins = np.histogram(self.map_data_frame["temp_C"], [-8, 0, 6, 11, 16, 21, 26, 31, 36, 41])
        bins = 0.5 * (bins[:-1] + bins[1:])

        return px.bar(self.map_data_frame,
                      title='Histogramme du nombre de villes dans un intervalle de température',
                      x=bins,
                      y=counts_city,
                      labels={'x': 'Température moyenne annuelle', 'y': 'Nombres de villes'}
                      )

    def create_bubble_graph(self, month_limit: Tuple[str, str] = ('1', '12')) -> object:
        """
        Créer un graphe à bulle montrant l'évolution des températures

        Parameters
        ----------
        month_limit : Tuple[str, str]
            La limite de mois du graph généré, par défaut elle est définie entre [1, 12]

        Returns
        -------
            Un Plotly Express Scatter avec les données formaté
        """

        tmp_data_frame = self.fig_data_frame.query('mois >= ' + month_limit[0] +
                                                   ' and mois <=' + month_limit[1])

        tmp_data_frame = tmp_data_frame.groupby(['commune_code', 'commune_name', 'region_name',
                                                 'nom_dept', 'longitude', 'latitude', 'mois'],
                                                as_index=False).temp_C.mean()
        tmp_data_frame['size'] = tmp_data_frame['temp_C'].abs()

        return px.scatter(tmp_data_frame,
                          x='nom_dept',
                          y='temp_C',
                          color='region_name',
                          size='size',
                          hover_name='commune_name',
                          hover_data=['longitude', 'latitude', 'mois'],
                          labels={'temp_C': 'Température moyenne', 'nom_dept': 'Nom département'}
                          )

    def create_dash(self, histogramme_fig: object, scatter_fig: object) -> None:
        """
        Créer un dashboard/application web à partir d'une map et d'un histogramme

        Parameters
        ----------
        histogramme_fig : object
            La figure plotly représentant l'histogramme

        scatter_fig : object
            La figure plotly représentant le scatter groupé par region
        """
        month_drop_down_option = [
            {'label': 'Janvier', 'value': '1'},
            {'label': 'Février', 'value': '2'},
            {'label': 'Mars', 'value': '3'},
            {'label': 'Avril', 'value': '4'},
            {'label': 'Mai', 'value': '5'},
            {'label': 'Juin', 'value': '6'},
            {'label': 'Juillet', 'value': '7'},
            {'label': 'Août', 'value': '8'},
            {'label': 'Septembre', 'value': '9'},
            {'label': 'Octobre', 'value': '10'},
            {'label': 'Novembre', 'value': '11'},
            {'label': 'Décembre', 'value': '12'}
        ]

        self.app.layout = html.Div(
            children=[
                html.Div(
                    children=[
                        html.H1(
                            children=f'Projet Météo Open Data par Rémi DA SILVA et Chang GAO',
                            style={'textAlign': 'center', 'color': '#7FDBFF'}
                        ),

                        html.Div(
                            children=f'''Ce projet à pour but de montrer la température moyenne en France,
                                     afin d'en tirer des conclusions climatiques'''
                        ),
                    ]),

                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H2(
                                    children=f'''L'histogramme du nombre de ville sur un intervalle de température
                                                         définie sur un an''',
                                    style={'textAlign': 'center', 'color': '#7FDBFF'}
                                ),
                            ]),

                        dcc.Graph(
                            id='Histogramme',
                            figure=histogramme_fig
                        ),

                        html.P(
                            children=f'''L'histogramme çi-dessus montre le nombre de villes qui sont concerné
                                    par un intervalle de température.
                                    Cela nous permet d'en déduire les moyennes et tendances de températures en France.
                                    '''
                        )
                    ]),

                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H2(
                                    children=f'Evolution des températures des villes par régions sur une année',
                                    style={'textAlign': 'center', 'color': '#7FDBFF'}),

                                html.P(
                                    children=f'''Le graphe çi-dessous est le graphe de l'évolution de la température sur une année''')
                            ]),

                        dcc.Dropdown(
                            id='start_month_dropdown',
                            options=month_drop_down_option,
                            value='1'
                        ),

                        dcc.Dropdown(
                            id='end_month_dropdown',
                            options=month_drop_down_option,
                            value='1'
                        ),

                        dcc.Graph(
                            id='Scatter graph',
                            figure=scatter_fig
                        )
                    ]),

                html.Div(
                    className='container',
                    children=[
                        html.H1(children=f'Carte géolocalisée',
                                style={'textAlign': 'center', 'color': '#7FDBFF'}),

                        html.Iframe(
                            id='map',
                            srcDoc=open(self.map_file_name, 'r').read(),
                            width='100%',
                            height='600'
                        )
                    ]),

            ]
        )

    def run_dash(self):
        """
        Exécute le dashboard
        """
        # RUN APP
        self.app.run_server(debug=True)

    def show_dash(self) -> None:
        """
        Affiche le dashboard en créant la carte, l'histogramme et le dashboard
        """
        self.create_map()
        self.create_dash(self.create_histogramme_fig(), self.create_bubble_graph())
        self.run_dash()
