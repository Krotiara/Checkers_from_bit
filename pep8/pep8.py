import re


class PepValidator:
    def __init__(self):
        self.text = []
        self.numbered_text = []
        self.dict_of_errors = {}
        self.list_of_errors = []
        self.file = ''
        self.list_opportunity = [',', '(', '{', '[', '\\']

    def create_dict_of_error(self):
        self.dict_of_errors = {
            'E111': 'Indentation is not a multiple of four',
            'E101': 'Indentation contains mixed spaces and tabs',
            'E201': 'Whitespace after "("',
            'E202': 'Whitespace before ")"',
            'E203': 'Whitespace before ":"',
            'E401': 'Multiple imports on one line',
            'E501': 'Line is too long (maximum 79 characters)',
            'W191': 'Indentation contains tabs',
            'W292': 'No newline at end of file',
            'W293': 'Blank line contains whitespace',
            'StylisticError1': 'Function names should be lowercase',
            'StylisticError2': 'Class names should use CamelCase convention'
        }

    def open_file(self, filename):
        self.file = filename
        """utf-8-sig используется для удаления BOM в начале файла"""
        with open(filename, mode='r', encoding='utf-8-sig',
                  errors='ignore') as f:
            current_text = f.readlines()
        return current_text

    def number_of_line(self):
        for line_number, line in enumerate(self.text, 1):
            self.numbered_text.append([line_number, line])
        return self.numbered_text

    def find_line(self, line):
        for numbered_line in self.numbered_text:
            if line == numbered_line[1]:
                return numbered_line[0]

    def create_error(self, line_number, error_code):
        return "{} {} {} {}".format(self.file, line_number, error_code,
                                    self.dict_of_errors[error_code])

    # E1
    def find_opportunity(self, line):
        for opportunity in self.list_opportunity:
            print(self.text[self.find_line(line) - 2])
            print(self.text[self.find_line(line) - 2].endswith(opportunity))
            print(opportunity)
            if self.text[self.find_line(line) - 2].endswith(opportunity):
                print('m')
                return True
            return False

    def find_indentation(self, line):
        pattern = re.compile(r'^([ ]+)')
        result = pattern.match(line)
        if result is None or len(result.group()) % 4 == 0:
            return -1
        elif self.find_opportunity(line):
            return -1
        else:
            return self.find_line(line)

    def check_spaces_and_tabs(self, line):
        pattern = re.compile(r'^([' ',\t]+)')
        result = pattern.match(line)
        if result is not None:
            return self.find_line(line)
        return -1

    def check_indentation(self):
        for line in self.text:
            if self.find_indentation(line) != -1:
                self.list_of_errors.append(self.create_error(
                    self.find_indentation(line), 'E111'))
            elif self.check_spaces_and_tabs(line) != -1:
                self.list_of_errors.append(self.create_error(
                    self.check_spaces_and_tabs(line), 'E101'))

    # E2
    def find_symbol(self, line, symbol):
        if symbol in line:
            if symbol == '(':
                if line[line.find(symbol) + 1] == " ":
                    return self.find_line(line)
                return -1
            if symbol == ')':
                if line[line.find(symbol) - 1] == " ":
                    return self.find_line(line)
                return -1
            if symbol == ':':
                if line[line.find(symbol) - 1] == " ":
                    return self.find_line(line)
                return -1
        return -1

    def check_whitespaces(self):
        for line in self.text:
            if self.find_symbol(line, '(') != -1:
                self.list_of_errors.append(self.create_error(
                    self.find_symbol(line, '('), 'E201'))
            if self.find_symbol(line, ')') != -1:
                self.list_of_errors.append(self.create_error(
                    self.find_symbol(line, ')'), 'E202'))
            if self.find_symbol(line, ':') != -1:
                self.list_of_errors.append(self.create_error(
                    self.find_symbol(line, ':'), 'E203'))

    # E4
    def check_import(self, text):
        for line in text:
            if line.startswith('import') and ',' in line:
                line_number = self.find_line(line)
                self.list_of_errors.append(self.create_error(
                    line_number, 'E401'))

    # E5
    def check_line_length(self):
        for line in self.text:
            if len(line) > 79:
                line_number = self.find_line(line)
                self.list_of_errors.append(self.create_error(
                    line_number, 'E501'))

    # W1
    def find_only_tabs(self, line):
        pattern = re.compile(r'^(\t+)')
        result = pattern.match(line)
        if result is not None:
            return self.find_line(line)
        return -1

    def check_indentation_warning(self):
        for line in self.text:
            if self.find_only_tabs(line) != -1:
                self.list_of_errors.append(self.create_error(
                    self.find_only_tabs(line), 'W191'))

    # W2
    def check_whitespace_warning(self):
        if self.text[-1] == " ":
            line_number1 = self.find_line(self.text[-1])
            self.list_of_errors.append(self.create_error(
                line_number1, 'W293'))
        elif not self.text[-1].endswith('\n'):
            line_number = self.find_line(self.text[-1])
            return self.list_of_errors.append(self.create_error(
                line_number, 'W292'))

    # StylisticErrors
    @staticmethod
    def find_word(word, line):
        entry_number = line.find(word)
        start_next_word = entry_number + len(word) + 1
        return start_next_word

    def check_stylistic(self):
        for line in self.text:
            if 'def' in line:
                if line[self.find_word('def', line)].isupper():
                    line_number1 = self.find_line(line)
                    self.list_of_errors.append(self.create_error(
                        line_number1, 'StylisticError1'))
            elif 'class' in line:
                if line[self.find_word('class', line)].islower():
                    line_number2 = self.find_line(line)
                    self.list_of_errors.append(self.create_error(
                        line_number2, 'StylisticError2'))
        return self.list_of_errors

    def check_all_text(self, filename):
        self.create_dict_of_error()
        self.text = self.open_file(filename)
        self.number_of_line()
        self.check_indentation()
        self.check_whitespaces()
        self.check_import(self.text)
        self.check_line_length()
        self.check_whitespace_warning()
        self.check_indentation_warning()
        self.check_stylistic()
        return self.list_of_errors
