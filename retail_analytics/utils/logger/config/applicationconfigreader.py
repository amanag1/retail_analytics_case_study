import configparser
from pathlib import Path


class ApplicationConfigReader:

    # Reads configuration details pertaining to store from the application configuration file

    def __init__(self):
        self.storeConfig = configparser.ConfigParser()
        cwd = Path(__file__).parent
        ini_file_path = cwd / "applicationconfig.ini"
        self.storeConfig.read(ini_file_path)

    def getValue(self, key: str, section='LOG'):
        return (self.storeConfig[section][key])
