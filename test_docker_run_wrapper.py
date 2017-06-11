import os
import unittest

from docker_run_wrapper import parse, correct_format, construct_command, with_volumepath


class TestDrw(unittest.TestCase):

    def test_parse(self):
        line = 'python = "python:3"'
        expected = ['python', 'python:3']
        actual = parse(line)
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
        params = ['-mdoctest', 'example.py']
        expected = 'docker run --rm -it -v $(pwd):/drw/ python:latest python -mdoctest example.py'
        actual = construct_command(image, command_name, params)
        self.assertEqual(expected, actual)


    def test_filepath_with_volumepath(self):
        param = 'test_docker_run_wrapper.py'
        expected = '/drw/test_docker_run_wrapper.py'
        actual = with_volumepath(param)
        self.assertEqual(expected, actual)


    def test_dirpath_with_volumepath(self):
        param = 'sample'
        os.mkdir(param)
        expected = '/drw/sample'
        actual = with_volumepath(param)
        self.assertEqual(expected, actual)
        os.rmdir(param)


    def test_not_filepath_with_volumepath(self):
        param = 'not_filepath'
        expected = 'not_filepath'
        actual = with_volumepath(param)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
