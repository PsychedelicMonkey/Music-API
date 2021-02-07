import os
import click

def register(app):
    @app.cli.command()
    @click.argument('test_names', nargs=-1)
    def test(test_names):
        """Run all unit tests."""
        import unittest
        if test_names:
            tests = unittest.TestLoader().loadTestsFromNames(test_names)
        else:
            tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner(verbosity=2).run(tests)