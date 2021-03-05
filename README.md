# TODOEd
Simple TODOlist management application with auth using Flask and SQLite.
  
    api/ - app root
        app.py - api
        run_tests.py - test runner with error reporting in stderr
        config.py - configuration file for app
    
        db/ - databases
            users.db - api db
            test_users.db - db for testing purpose
    
        func/ - api modules
            __init__.py - app factory
            database.py - model(flask_sqlalchemy)
            blueprints.py - flask blueprints
    
        migrations/ - db migration(flask-migrate)
        
        static/ - dir for static files
    
        templates/ - dir for templates
    
        test/ - autotests and utils
            clear_db.py - module for clearing test base
            create_db.py - module for creating db with specifyed name
            test_app.py - autotests


For app to work properly, environment variables ['SECRET'] for SECRET_KEY and ['JWT_SECRET'] for JWT_SECRET_KEY must be set.
