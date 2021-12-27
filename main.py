from Dashboard import Dashboard
from WeatherDataFrame import WeatherDataFrame
import warnings, os

warnings.simplefilter("ignore") # Change the filter in this process
os.environ["PYTHONWARNINGS"] = "ignore" # Also affect subprocesses
weather_data_frame = WeatherDataFrame('donnees-synop-2021.csv')
map_file_name = 'map.html'
dashboard = Dashboard(weather_data_frame, map_file_name)
dashboard.show_dash()