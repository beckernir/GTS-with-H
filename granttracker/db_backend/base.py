"""
Custom MySQL database backend that bypasses MariaDB version check
"""
from django.db.backends.mysql.base import DatabaseWrapper as MySQLDatabaseWrapper
from django.db.backends.mysql.base import DatabaseFeatures as MySQLDatabaseFeatures
from django.db.backends.mysql.base import DatabaseOperations as MySQLDatabaseOperations
from django.db.backends.mysql.base import DatabaseClient as MySQLDatabaseClient
from django.db.backends.mysql.base import DatabaseCreation as MySQLDatabaseCreation
from django.db.backends.mysql.base import DatabaseIntrospection as MySQLDatabaseIntrospection
from django.db.backends.mysql.base import DatabaseValidation as MySQLDatabaseValidation


class DatabaseFeatures(MySQLDatabaseFeatures):
    """Custom database features that bypass version checks"""
    
    def __init__(self, connection):
        super().__init__(connection)
    
    @property
    def supports_returning_columns(self):
        """Disable RETURNING clause support for MariaDB 10.4 compatibility"""
        return False


class DatabaseOperations(MySQLDatabaseOperations):
    """Custom database operations"""
    
    def __init__(self, connection):
        super().__init__(connection)


class DatabaseWrapper(MySQLDatabaseWrapper):
    """Custom database wrapper that uses our modified features"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.features = DatabaseFeatures(self)
        self.ops = DatabaseOperations(self)


# Export the wrapper class
DatabaseWrapper = DatabaseWrapper

# Export the required classes
DatabaseClient = MySQLDatabaseClient
DatabaseCreation = MySQLDatabaseCreation
DatabaseIntrospection = MySQLDatabaseIntrospection
DatabaseValidation = MySQLDatabaseValidation 