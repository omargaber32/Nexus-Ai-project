#please run "pip install -r requirements.txt" in the terminal before running the code
from config import Config, summary_table
from gui import launch_gui

config1 = Config(5, 8, 6, 3)
config2 = Config(1, 2, 2, 1)
config3 = Config(-1, 15, 99, 8)
config4 = Config(1,6,9,4)

summary_table()

launch_gui()
