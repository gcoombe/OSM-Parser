#!/usr/bin/env python3

import unittest


def main():
    loader = unittest.TestLoader()
    test_suite = loader.discover('.')

    test_runner = unittest.runner.TextTestRunner(verbosity=1)
    test_runner.run(test_suite)

if __name__ == '__main__':
    main()
