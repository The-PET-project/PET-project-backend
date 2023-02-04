import os


class ConfigLoader:

    @staticmethod
    def get_config():
        return {
            'DB_SCHEME': os.environ.get('DB_SCHEME', 'mysql'),
            'DB_USERNAME': os.environ.get('DB_USERNAME', 'root'),
            'DB_PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'DB_HOST': os.environ.get('DB_HOST', '127.0.0.1'),
            'DB_PORT': os.environ.get('DB_PORT', '3306'),
            'DB_DATABASE_SCHEMA': os.environ.get('DB_DATABASE_SCHEMA', 'petproject')
        }
