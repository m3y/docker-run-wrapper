import os
import unittest

from docker_run_wrapper import (
    parse,
    correct_format,
    construct_command,
    create_command_fragment,
    is_shell_mode
    )


class TestDrw(unittest.TestCase):

    def test_parse(self):
        line = 'python = "python:3"'
        expected = ['python', 'python:3']
        actual = parse(line)
        self.assertEqual(expected, actual)

    def test_correct_format(self):
        lines = ['python', 'python:3']
        expected = True
        actual = correct_format(lines)
        self.assertEqual(expected, actual)

    def test_correct_format_empty_value(self):
        lines = ['python', '']
        expected = False
        actual = correct_format(lines)
        self.assertEqual(expected, actual)

    def test_correct_format_not_enough(self):
        lines = ['python']
        expected = False
        actual = correct_format(lines)
        self.assertEqual(expected, actual)

    def test_construct_command(self):
        image = 'python:latest'
        command_name = 'python'
        params = '-mdoctest example.py'
        expected = 'docker run --rm -it -w /drw/ -v $(pwd):/drw/' + \
                   ' python:latest python -mdoctest example.py'
        actual = construct_command(image, command_name, params)
        self.assertEqual(expected, actual)

    def test_create_command_fragment(self):
        input_params = ['mysql', '-h', 'HOST', '-u', 'USER', '-p', 'DATABASE']
        config = {'mysql': 'mysql:5.7'}
        expected = ('mysql:5.7', 'mysql', '-h HOST -u USER -p DATABASE')
        actual = create_command_fragment(input_params, config)
        self.assertEqual(expected, actual)

    def test_create_command_fragment_using_shell(self):
        input_params = ['ghc --make helloworld.hs && ./helloworld']
        config = {'ghc': 'haskell:latest'}
        expected = (
            'haskell:latest',
            '/bin/sh',
            "-c 'ghc --make helloworld.hs && ./helloworld'"
            )
        actual = create_command_fragment(input_params, config)
        self.assertEqual(expected, actual)

    def test_create_command_fragment_unknown_command(self):
        input_params = ['ipython']
        config = {'python': 'python:3'}
        with self.assertRaises(ValueError):
            create_command_fragment(input_params, config)

    def test_is_shell_mode_using(self):
        param_head = "ghc --make helloworld.hs"
        self.assertEqual(True, is_shell_mode(param_head))

    def test_is_shell_mode(self):
        param_head = "mysql"
        self.assertEqual(False, is_shell_mode(param_head))


if __name__ == "__main__":
    unittest.main()
