import os
import configparser

class Singleton(type):
    """
    This class is a metaclass addition to any class to force the creation of one instance of a class within a program. This is key
    for the ConfigManager since it config gets imported 
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class ConfigManager(metaclass=Singleton):
    """
    Manages the config, allowing you to pull information and get info when needed. In addition save information when needed to the
    config file.
    """
    def __init__(self, config_path = None):
        self.config = configparser.ConfigParser() #need to call and not inharent because metalass and subclass are already in Configparser.
        self.config_path = config_path
        self.config.read(config_path)

    def __str__(self):
        return f"🔍 ConfigManager loaded from: {self.config_path}"

    def get(self, section: str, option: str):
        try:
            return self.config.get(section, option)
        except configparser.NoOptionError:
            return None

    def get_all(self):
        return {section: dict(self.config.items(section)) for section in self.config.sections()}

def check_redirect() -> str:
    """
    Check for configuration file locations, either 'config.ini' or '_redirect.ini'.
    If 'config.ini' exists, return its path.
    If '_redirect.ini' exists, check for a redirection path inside and validate it.

    :return: The valid configuration file path.
    :rtype: str
    :raises FileNotFoundError: If neither file exists or the redirection path is invalid.
    """
    # Get the current directory where this script is located
    current_folder = os.path.dirname(os.path.abspath(__file__))

    # Define file paths
    config_file = os.path.join(current_folder, "config.ini")
    redirect_file = os.path.join(current_folder, "_redirect.ini")

    # Check for config.ini first
    if check_path(config_file):
        print(f"✅ Config file found: {config_file}") #\u2705
        return config_file

    # Check for _redirect.ini next
    if check_path(redirect_file):
        print(f"🔄 Redirect file found: {redirect_file}") # \U0001F504

        # Parse the redirect file
        parser = configparser.ConfigParser()
        parser.read(redirect_file)

        # Check if redirect path exists
        if parser.has_section("Redirect") and parser.has_option("Redirect", "config_location"):
            redirect_path = parser.get("Redirect", "config_location")

            # Expand ~ if present and validate the path
            expanded_redirect_path = os.path.expanduser(redirect_path)
            
            if check_path(expanded_redirect_path):
                print(f"✅ Redirected config found: {expanded_redirect_path}")
                return expanded_redirect_path
            else:
                raise FileNotFoundError(f"❌ Redirect path not found: {expanded_redirect_path}") #\u274C
        
        else:
            raise ValueError("❌ Redirect file exists but contains no valid 'config_location'.")
    
    # Raise an error if no files were found
    raise FileNotFoundError("❌ No valid config or redirect file found in the current folder.")

def check_path(path: str) -> bool:
    """Check if the path exists"""
    return os.path.isfile(path)
        
