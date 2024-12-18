import re
import sys
import argparse
import operator
import tomli_w

TOKEN_REGEX = {
    'DICT_PAIR': r'[a-z]+\s*:\s*',
    'DICT_START': r'\$\[',
    'LIST_START': r'list\(',
    'FUNCTION': r'max\(\)',
    'IDENTIFIER': r'[a-z]+',
    'STRING': r'"[^"]*"',
    'NUMBER': r'\d+',
    'COMMA': r',',
    'CLOSE': r'\)',
    'CLOSE_DICT': r'\]',
    'ASSIGN': r'<-',
    'EXPR_START': r'#\{',
    'EXPR_END': r'\}',
    'OPERATOR': r'[+\-*/]',
    'SEMICOLON': r';',
}

TOKEN_PATTERN = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_REGEX.items())

def lex(input_text):
    tokens = []
    for match in re.finditer(TOKEN_PATTERN, input_text):
        token_type = match.lastgroup
        token_value = match.group(token_type)
        tokens.append((token_type, token_value))
    return tokens

def evaluate_expression(expression_tokens, constants):
    operations = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    stack = []

    for token in expression_tokens:
        if token[0] == 'NUMBER':
            stack.append(int(token[1]))
        elif token[0] == 'IDENTIFIER':
            if token[1] in constants:
                stack.append(constants[token[1]])
            else:
                raise ValueError(f"Unknown identifier: {token[1]}")
        elif token[0] == 'OPERATOR':
            if len(stack) < 2:
                raise ValueError("Insufficient operands for operation")
            b = stack.pop()
            a = stack.pop()
            stack.append(operations[token[1]](a, b))
        elif token[0] == 'FUNCTION':
            if token[1] == 'max()':
                if len(stack) < 2:
                    raise ValueError("Function 'max()' requires at least two operands")
                b = stack.pop()
                a = stack.pop()
                stack.append(max(a, b))
        else:
            raise ValueError(f"Unexpected token in expression: {token}")

    if len(stack) != 1:
        raise ValueError("Expression did not evaluate to a single result")

    return stack[0]

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.assignments = {}

    def peek(self) -> tuple[str | None, str | None]:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def consume(self, expected_type=None) -> tuple[str | None, str | None]:
        token = self.peek()
        if expected_type and token[0] != expected_type:
            raise ValueError(f"Expected {expected_type}, but got {token[0]}")
        self.pos += 1
        return token

    def parse_value(self):
        token_type, token_value = self.peek()
        if token_type == 'NUMBER':
            self.consume('NUMBER')
            return int(token_value)
        elif token_type == 'STRING':
            self.consume('STRING')
            return token_value.strip('"')
        elif token_type == 'LIST_START':
            return self.parse_list()
        elif token_type == 'DICT_START':
            return self.parse_dict()
        elif token_type == 'EXPR_START':
            return self.parse_expression()
        else:
            raise ValueError(f"Unexpected token {token_type}")

    def parse_expression(self):
        self.consume('EXPR_START')
        expression_tokens = []
        while self.peek()[0] != 'EXPR_END':
            expression_tokens.append(self.consume())
        self.consume('EXPR_END')
        return evaluate_expression(expression_tokens, self.assignments)

    def parse_list(self):
        self.consume('LIST_START')
        elements = []
        while self.peek()[0] != 'CLOSE':
            elements.append(self.parse_value())
            if self.peek()[0] == 'COMMA':
                self.consume('COMMA')
        self.consume('CLOSE')
        return elements

    def parse_dict(self):
        self.consume('DICT_START')
        elements = {}
        while self.peek()[0] != 'CLOSE_DICT':
            key = self.consume('DICT_PAIR')[1].split(':', 1)[0].strip()
            value = self.parse_value()
            elements[key] = value
            if self.peek()[0] == 'COMMA':
                self.consume('COMMA')
        self.consume('CLOSE_DICT')
        return elements

    def parse_assignment(self):
        key = self.consume('IDENTIFIER')[1]
        self.consume('ASSIGN')
        value = self.parse_value()
        self.consume('SEMICOLON')
        return key, value

    def parse(self):
        self.assignments = {}
        while self.pos < len(self.tokens):
            key, value = self.parse_assignment()
            self.assignments[key] = value
        return self.assignments

def main():
    parser = argparse.ArgumentParser(description="Транслятор в TOML")
    parser.add_argument("--output", help="Путь к выходному файлу")
    args = parser.parse_args()

    input_text = sys.stdin.read()
    tokens = lex(input_text)

    parser = Parser(tokens)
    data = parser.parse()

    with open(args.output, "wb") as toml_file:
        tomli_w.dump(data, toml_file)

if __name__ == "__main__":
    main()
