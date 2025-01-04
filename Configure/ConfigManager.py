import os
import configparser



class Singleton(type):
    """
    A metaclass that ensures a class has only one instance throughout the execution of a program. It implements the Singleton pattern
    which is beneficial for managing resources like configuration settings, where exactly one object is needed to coordinate actions across 
    the system. It uses a dictionary to store instances of the classes it creates, preventing multiple instantiations.

    Attributes:
    _instances (dict): A dictionary mapping class types to their instantiated objects.

    Usage:
    To apply, define a class and set its metaclass to Singleton. Any subsequent instantiations will return the same instance.
    """
    #create a global class variable to 
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Call method that manages the instantiation of classes and ensures only one instance per class.
        If the class does not exist in the instances dictionary, it creates a new instance and stores it.
        Subsequent calls return the stored instance.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The single instance of the class.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class ConfigManager(metaclass=Singleton):
    """
    Manages application configurations, providing a centralized interface to access and modify settings.
    This class leverages the Singleton pattern to ensure only one configuration manager instance manages the config file
    operations throughout the application lifecycle, promoting consistency and preventing conflicts.

    Attributes:
        config (ConfigParser): An instance of ConfigParser to read and write to the configuration file.
        config_path (str): Path to the configuration file.

    Methods:
        get(section, option): Retrieves the value for the given section and option.
        get_all(): Returns a dictionary of all configuration sections and their key/value pairs.
    """
    def __init__(self, config_path = None):
        """
        Initializes the ConfigManager with the specified configuration path.

        Args:
            config_path (str): The path to the configuration file to be managed. If None, defaults to 'config.ini'.
        """
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
        
