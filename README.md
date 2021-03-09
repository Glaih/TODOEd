# TODOEd
Simple TODOlist management application with auth using Flask and PostgreSQL.
  
    api/ - app root
        app.py - api
        run_tests.py - test runner with error reporting in stderr
        config.py - configuration file for app

        func/ - api modules
            __init__.py - app factory
            database.py - model(flask_sqlalchemy)
            blueprints.py - flask blueprints
    
        migrations/ - db migration(flask-migrate)
        
        static/ - dir for static files
    
        templates/ - dir for templates
    
        test/ - autotests and utils
            clear_db.py - module for clearing test base
            create_db.py - module for creating db
            test_app.py - autotests


For app to work properly, environment variables ['SECRET'] for SECRET_KEY, ['JWT_SECRET'] for JWT_SECRET_KEY,
['DB_PASSWORD'] for DB_PASSWORD, ['DB_LOGIN'] for DB_LOGIN and ['DB_HOST'] for DB_HOST must be set.
