
"""
This module initializes the application's configuration management by leveraging the ConfigManager class,
which adheres to the Singleton design pattern to ensure a single instance manages the configuration across the application.

The module performs an initial setup by determining the appropriate configuration file location using the `check_redirect` function.
It then creates and configures a single instance of `ConfigManager` using the identified configuration path.
This instance is made available for import throughout the application, ensuring all configuration reads and writes are centralized.

Usage:
    Import the `config` instance from this module to access and manage application settings throughout the project.

Example:
    from your_module_name import config
    database_path = config.get('Database', 'path')

Attributes:
    config (ConfigManager): A globally available configuration manager instance initialized with the correct configuration path.

Functions:
    check_redirect(): Determines the effective configuration file path, either directly or via a redirect.

Assumptions:
    This module assumes that it is located in the same package as the `ConfigManager` and that `check_redirect`
    is defined either within the same module or is correctly imported from an external module.
    It should be imported once at the start of the application to set up the configuration management properly.
"""

import os
from .ConfigManager import ConfigManager, check_redirect

config:ConfigManager = ConfigManager(check_redirect()) #when inporting inport config.
