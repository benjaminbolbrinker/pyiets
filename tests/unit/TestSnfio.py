import unittest
import sys
sys.path.insert(0, "../../")

from pyiets.io.snfio import SnfParser


class TestStringMethods(unittest.TestCase):
    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


if __name__ == '__main__':
    # unittest.main()
    parser = SnfParser()
    # parser.get_mode(6)
    parser.get_modes()
