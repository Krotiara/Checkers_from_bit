import unittest
import pep8


class AdditionForTests:
    @staticmethod
    def open_file(filename):
        errors = []
        with open(filename, mode='r', encoding='utf-8-sig') as f:
            text = f.readlines()
            for line in text:
                new_line = line.replace('\n', '')
                errors.append(new_line)
        return errors


class InfoPep8:
    @staticmethod
    def get_info(code, errors):
        validator = pep8.PepValidator()
        gotten_errors = validator.check_all_text(code)
        addition = AdditionForTests()
        needed_errors = addition.open_file(errors)
        return gotten_errors, needed_errors


class TestMethods(unittest.TestCase):

    def test_small_code(self):
        information = InfoPep8()
        comparison = information.get_info('example1.txt', 'errors1.txt')

        self.assertListEqual(*comparison)

    def test_stylistic(self):
        information = InfoPep8()
        comparison = information.get_info('example2.txt', 'errors2.txt')

        self.assertListEqual(*comparison)

    def test_pep8(self):
        information = InfoPep8()
        comparison = information.get_info('pep8.py', 'empty1.txt')

        self.assertListEqual(*comparison)

    def test_pep8_console(self):
        information = InfoPep8()
        comparison = information.get_info('pep8_console.py', 'empty.txt')

        self.assertListEqual(*comparison)

    def test_pep8_tests(self):
        information = InfoPep8()
        comparison = information.get_info('pep8_tests.py', 'empty.txt')

        self.assertListEqual(*comparison)


if __name__ == '__main__':
    unittest.main()
