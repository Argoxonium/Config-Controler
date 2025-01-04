"""
This package manages the application configuration settings. It ensures that configuration management is centralized 
through the ConfigManager class which implements the Singleton pattern to maintain a single instance.

It includes functionalities to:
- Read and write configuration settings.
- Automatically determine and handle redirects for configuration file locations.

The `config` instance created in this package is meant to be imported and used across the application.
"""
from .ConfigManager import ConfigManager, check_redirect

config = ConfigManager(check_redirect())

__all__ = ['config']
