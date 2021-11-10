import pep8
import argparse
import os
import mimetypes
import sys


class Pep8Console:
    def __init__(self):
        self.validator = pep8.PepValidator()
        self.errors = []
        self.without_error = []

    @staticmethod
    def create_parser():
        parser = argparse.ArgumentParser(prog="Pep8 валидатор.",
                                        description="""Данная программа
                                        проверяет искомый код по
                                        стандартам Pep-8. Выполнила:
                                        Самарина А.С. Группа: КН-202""")
        parser.add_argument('--filename',
                            '-f',
                            type=str,
                            help="""Имя файла расширения py""")
        parser.add_argument('--directory',
                            '-d',
                            help="""Директория, в которой хранятся те или
                            иные файлы для проверки по стандартам Pep-8""")
        parser.add_argument('--somefiles',
                            '-s',
                            nargs='*',
                            action='append',
                            help="""Несколько файлов или директорий,
                            которые нужны для проверки по
                            стандарту Pep-8""")
        parser.add_argument('--ignoreerrors',
                            '-i',
                            nargs='*',
                            action='append',
                            help="""Ошибки, которые вы хотите
                            игнорировать""")
        return parser

    def open_file(self, file):
        for error in self.validator.check_all_text(file):
            self.errors.append(error)
        self.validator.list_of_errors = []

    def open_directory(self, directory):
        directory_list = os.listdir(directory)
        for direct in directory_list:
            if 'text' in str(mimetypes.guess_type(direct)[0]):
                for error in self.validator.check_all_text(direct):
                    self.errors.append(error)
                self.validator.list_of_errors = []

    def delete_error(self, error):
        for element in self.errors:
            if error in element:
                self.without_error.append(element)

    def validator_checking(self):
        if namespace.filename:
            self.open_file(namespace.filename)
        if namespace.directory:
            self.open_directory(namespace.directory)
        if namespace.somefiles:
            for arg in namespace.somefiles[0]:
                if os.path.isfile(arg):
                    self.open_file(arg)
                elif os.path.isdir(arg):
                    self.open_directory(arg)
        if namespace.ignoreerrors:
            for error in namespace.ignoreerrors[0]:
                self.delete_error(error)
            if len(set(self.errors).difference(set(self.without_error))) == 0:
                print('Ok')
            else:
                new_list = list(set(self.errors).difference(
                    set(self.without_error)))
                for elem in new_list:
                    print(elem)
        else:
            if len(self.errors) == 0:
                print('Ok')
            else:
                for err in self.errors:
                    print(err)
        if not sys.argv[1]:
            print('Oh, well, no args, no problems.')


if __name__ == "__main__":
    a = Pep8Console()
    namespace = a.create_parser().parse_args()
    a.validator_checking()
