

class BaseWebPackagerError(Exception):
    """Base for all app exceptions"""
    pass


class DuplicatedWebConfigName(BaseWebPackagerError):
    """Two webconfigs with the same name were found"""
    pass


class InvalidWebConfigPath(BaseWebPackagerError):
    """The specified webconfig path doesn't exist"""
    pass


class InexistentWebConfig(BaseWebPackagerError):
    """App config name doesn't exist"""
    pass


class WebconfigCreationError(BaseWebPackagerError):
    """Some OS error was thrown"""
