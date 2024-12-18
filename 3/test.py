import unittest

import tomli

from main import *
import tomli_w

class MyTestCase(unittest.TestCase):
    def test_max(self):
        input_text = "name <- 5; sur <- #{name 2 max() };"
        tokens = lex(input_text)

        parser = Parser(tokens)
        data = parser.parse()

        self.assertEqual(
            tomli_w.dumps(tomli.loads(
                """
                name = 5
                sur = 5
                """)).strip(),
            tomli_w.dumps(data).strip()
        )

    def test_op(self):
        input_text = "name <- 5; sur <- #{name 2 + };"
        tokens = lex(input_text)

        parser = Parser(tokens)
        data = parser.parse()

        self.assertEqual(
            tomli_w.dumps(tomli.loads(
            """
            name = 5
            sur = 7
            """)).strip(),
            tomli_w.dumps(data).strip()
        )

    def test_1(self):
        input_text = "test <- $[ key: list(1, 2, $[ nestedkey: \"value\" ]) ];"

        tokens = lex(input_text)

        parser = Parser(tokens)
        data = parser.parse()

        self.assertEqual(
            tomli_w.dumps(tomli.loads(
            """
        [test]
        key = [1, 2,
        { nestedkey = "value"}]
        """)).strip(),
        tomli_w.dumps(data).strip()
    )

    def test_2(self):
        input_text = "name <- \"Example\"; values <- list(1, 2, 3);"

        tokens = lex(input_text)

        parser = Parser(tokens)
        data = parser.parse()

        self.assertEqual(
            tomli_w.dumps(tomli.loads(
            """
            name = "Example"
            values = [1, 2,  3]
        """)).strip(),
        tomli_w.dumps(data).strip()
    )

    def test_3(self):
        input_text = "data <- $[ keyone: 42, keytwo : list(1, 2, $[ nestedkey: \"value\" ]), keythree : $[innerone : 10, innertwo : \"string\"] ];"

        tokens = lex(input_text)

        parser = Parser(tokens)
        data = parser.parse()

        self.assertEqual(
            tomli_w.dumps(tomli.loads(
            """
            [data]
            keyone = 42
            keytwo = [1, 2,
            { nestedkey = "value"}
            ]
            keythree = { innerone  = 10, innertwo = "string" }
            """)).strip(),
            tomli_w.dumps(data).strip()
        )


if __name__ == '__main__':
    unittest.main()
