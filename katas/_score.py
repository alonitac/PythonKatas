import unittest
import xmlrunner

# Discover and run tests in the 'katas/test' directory
if __name__ == "__main__":
    test_suite = unittest.defaultTestLoader.discover('test')
    with open('results.xml', 'wb') as output:
        xmlrunner.XMLTestRunner(output=output).run(test_suite)

