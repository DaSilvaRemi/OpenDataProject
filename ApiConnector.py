import json
import requests


class Api:
    def __init__(self, url: str) -> None:
        """
        Constructeur de la classe API

        Args:
            url: L'URL de l'Api
        """
        self.api_url = url
        self.http_response: requests.Response = None

    def open(self) -> None:
        """
        Emet une requête vers l'API et récupère sa réponse HTTP
        """
        # Catch JSON data
        self.http_response = requests.get(self.api_url)

    def close(self) -> None:
        """
        Ferme la requête de l'API
        """
        self.http_response.close()

    def read(self) -> object:
        """
        Récupère la réponse JSON de la requête vers l'API

        Returns:
            Les données JSON
        """
        self.open()
        if self.http_response.status_code != 200:
            self.http_response.raise_for_status()

        return self.http_response.json()

    def print_json_datas(self) -> None:
        """
        Affiche les données JSON formatées
        """
        print(json.dumps(self.read(), indent=2))
