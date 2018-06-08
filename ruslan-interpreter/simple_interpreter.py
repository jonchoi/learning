# Exercises
# - [x] multiple integers
# - [x] whitespace
# - [x] minus

# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF',

class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, EOF
        self.type = type
        # token value: 0, 1, 2, ... 9, '+' or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(Integer, 3)
            Token(Plus, '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    # why?
    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    # object to text mapping?
    def __init__(self, text):
        # client string input "3+5"
        self.text = text
        # self.pos is index of text
        self.pos = 0
        # current token instance
        self.current_token = None
        # self.current_int_string = ''
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None    # done
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        if self.current_char.isspace() and self.current_char is not None:
            self.advance()

    def get_integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence apart into tokens.
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()

            if self.current_char.isdigit():
                return Token(INTEGER, self.get_integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            self.error()

        return Token(EOF, None)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """ integer plus integer """
        self.current_token = self.get_next_token()

        left = self.current_token
        self.eat(INTEGER)

        op = self.current_token
        if op.type == PLUS:
            self.eat(PLUS)
        elif op.type == MINUS:
            self.eat(MINUS)
        else:
            self.error()

        right = self.current_token
        self.eat(INTEGER)

        if op.type == PLUS:
            result = left.value + right.value
        elif op.type == MINUS:
            result = left.value - right.value
        else:
            self.error()
        return result

def main():
    while True:
        try:
            text = raw_input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

# python bootstrap?
if __name__ == '__main__':
    main()



""" Check your knowledge

What is an interpreter?
- interpreter takes source code and targets another language
What is a compiler?
- compiler takes source code and targets machine code
Whats the difference between an interpreter and a compiler?
- interpreter goes to another language, compiler down to machine language
What is a token?
- representation of a syntactic unit of the written representation of code
What is the name of the process that breaks input apart into tokens?
- lexical analysis
What is the part of the interpreter that does lexical analysis called?
- lexer
What are the other common names for that part of an interpreter or a compiler?
- tokenizer, scanner


I, Jon Choi, of being sound mind and body, do hereby pledge to commit to studying
interpreters and compilers starting today and to get to a point where I know 100% 
how they work.

https://ruslanspivak.com/lsbasi-part1/

"""

