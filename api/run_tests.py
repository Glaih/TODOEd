if __name__ == '__main__':
    import unittest

    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if result.wasSuccessful():
        exit(0)
    exit(1)
