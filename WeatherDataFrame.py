import pandas as pd


def rename_date_frame_rows(data_frame: pd.DataFrame) -> None:
    """
    Renomme les noms de colonnes de la DataFrame
    """
    return data_frame.rename(
        columns={"communes (code)": "commune_code", "communes (name)": "commune_name",
                 "region (name)": "region_name", "department (name)": "nom_dept", "Longitude": "longitude",
                 "Latitude": "latitude", "Date": "date", "Température (°C)": "temp_C", "mois_de_l_annee": "mois"},
        inplace=True)


def format_data_frame(data_frame: pd.DataFrame) -> None:
    """
        Renomme les colonnes, supprime les valeurs à null et sélectionne uniquement les colonnes nécessaires :
        -commune-code
        -commune-name
        -region_name
        -nom_dept
        -date
        -longitude
        -latitude
        -temp_C
        -mois
        """
    rename_date_frame_rows(data_frame)
    return data_frame[['commune_code', 'commune_name', 'region_name', 'nom_dept', 'date',
                       'longitude', 'latitude', 'temp_C', 'mois']].dropna()


class WeatherDataFrame:
    def __init__(self, csv_file_name: str) -> None:
        """
        Constructeur de WeatherDataFrame
        """
        self.csv_file_name: str = csv_file_name
        self.data_frame: pd.DataFrame = pd.read_csv(self.csv_file_name, sep=";", encoding='utf-8')

    def rename_date_frame_rows(self) -> None:
        """
        Renomme les noms de colonnes de la DataFrame
        """
        self.data_frame.rename(
            columns={"communes (code)": "commune_code", "communes (name)": "commune_name",
                     "region (name)": "region_name", "department (name)": "nom_dept", "Longitude": "longitude",
                     "Latitude": "latitude", "Date": "date", "Température (°C)": "temp_C", "mois_de_l_annee": "mois"},
            inplace=True)

    def format_data_frame(self) -> None:
        """
        Renomme les colonnes, supprime les valeurs à null et sélectionne uniquement les colonnes nécessaires : 
        -commune-code
        -commune-name
        -region_name
        -nom_dept
        -date
        -longitude
        -latitude
        -temp_C
        -mois
        """
        self.rename_date_frame_rows()
        self.data_frame = self.data_frame[['commune_code', 'commune_name', 'region_name', 'nom_dept', 'date',
                                           'longitude', 'latitude', 'temp_C', 'mois']].dropna()

    def format_data_frame(self) -> None:
        """
        Renomme les colonnes, supprime les valeurs à null et sélectionne uniquement les colonnes nécessaires :
        -commune-code
        -commune-name
        -region_name
        -nom_dept
        -date
        -longitude
        -latitude
        -temp_C
        -mois
        """
        self.rename_date_frame_rows()
        self.data_frame = self.data_frame[['commune_code', 'commune_name', 'region_name', 'nom_dept', 'date',
                                           'longitude', 'latitude', 'temp_C', 'mois']].dropna()

    def format_data_frame_groupby_commune(self) -> None:
        """
        Formate la DataFrame en regroupant les données selon leur code de commune
        """
        self.format_data_frame()
        self.data_frame = self.data_frame.groupby(['commune_code', 'commune_name', 'region_name', 'nom_dept',
                                                   'longitude', 'latitude'], as_index=False).temp_C.mean()

    def format_data_frame_groupby_mois(self) -> None:
        """
        Formate la DataFrame en regroupant les données selon leur code de commune
        """
        self.format_data_frame()
        self.data_frame = self.data_frame.groupby(['commune_code', 'commune_name', 'region_name',
                                                   'nom_dept', 'longitude', 'latitude', 'mois'],
                                                  as_index=False).temp_C.mean()
