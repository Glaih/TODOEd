# TODOEd
Simple TODO list management application with auth using Flask and SQLite.
  
    api/ - app root
        app.py - api
        run_tests.py - test runner with error reporting in stderr
    
        db/ - databases
            auth.db - api authentication db
            test_auth.db - db for testing purpose
    
        func/ - api modules
            registation.py - module for hashing password, striping mail of spaces and writing them to AUTH_DB
            validation.py - module for validation of password and mail
    
        static/ - dir for static files
    
        templates/ - dir for templates
    
        test/ - autotests and utils
            clear_db.py - module for clearing test base
            create_db.py - module for creating db with specifyed name
            test_app.py - autotests
