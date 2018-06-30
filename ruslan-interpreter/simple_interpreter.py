# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, EOF = 'INTEGER', 'EOF'
PLUS, MINUS, MULTIPLY, DIVIDE = 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE'


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
        self.current_token = None
        self.current_char = self.text[self.pos]
        self.phrase = []

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

    def get_operator(self, char):
        if char == '+':
            self.advance()
            return Token(PLUS, '+')

        if char == '-':
            self.advance()
            return Token(MINUS, '-')

        if char == '*':
            self.advance()
            return Token(MULTIPLY, '*')

        if char == '/':
            self.advance()
            return Token(DIVIDE, '/')

        print 'ain\'t no operarator here'
        self.error()

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence apart into tokens.
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.get_integer())

            return self.get_operator(self.current_char)

        return Token(EOF, None)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def parse(self):
        self.current_token = self.get_next_token()
        self.phrase.append(self.current_token)
        while self.current_token.type is not EOF:
            self.current_token = self.get_next_token()
            self.phrase.append(self.current_token)
        return self.phrase

    def find_mult_div(self, phrase):
        # for idx, token in phrase:
        for token in phrase:
            if token.type == MULTIPLY or token.type == DIVIDE:
                print token
                # return idx
        return None

    def find_plus_minus(self, phrase):
        for idx, token in phrase:
            if token.type == PLUS or token.type == MINUS:
                return idx
        return None

    def apply_operator(self, op1, token, op2):
        if token.type is not INTEGER and token.type is not EOF:
            if token.type == PLUS:
                result = op1.value + op2.value
            elif token.type == MINUS:
                result = op1.value - op2.value
            elif token.type == MULTIPLY:
                result = op1.value * op2.value
            elif token.type == DIVIDE:
                result = op1.value / op2.value
            else:
                self.error()
        return result

    def calc_and_update_phrase(self, phrase, idx):
        cache_phrase = []
        cache_phrase = phrase

        # find result
        operator = cache_phrase[idx]
        op1 = cache_phrase[idx-1]
        op2 = cache_phrase[idx+1]
        new_operand = Token(INTEGER, self.apply_operator(op1, operator, op2))

        # update phrase with result
        cache_phrase.pop(idx-1)
        cache_phrase.pop(idx)
        cache_phrase.pop(idx+1)
        cache_phrase.insert(idx-1, new_operand)

        return cache_phrase

    def apply_mult_div(self):
        # add checks for integers, indices etc.

        cache_phrase = self.phrase
        idx = self.find_mult_div(cache_phrase)  # index of mult/div

        while idx is not None:  # there are mult/div ops left
            cache_phrase = self.calc_and_update_phrase(cache_phrase, idx)

        # update phrase post mult/div
        self.phrase = cache_phrase

    def apply_plus_minus(self):
        cache_phrase = self.phrase
        idx = self.find_plus_minus(cache_phrase)  # index of plus/minus

        while idx is not None:  # there are mult/div ops left
            cache_phrase = self.calc_and_update_phrase(cache_phrase, idx)

        # update phrase post plus_minus
        self.phrase = cache_phrase

    def calculate(self, phrase):
        self.parse()
        self.apply_mult_div()
        self.apply_plus_minus()
        return self.phrase.value

    def expr(self):
        self.parse()  # stores to global
        return self.calculate(self.phrase)


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

# Part 1 Notes
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


I, Jon Choi, of being sound mind and body, do hereby pledge to commit to
studying interpreters and compilers starting today and to get to a point
where I know 100% how they work.

https://ruslanspivak.com/lsbasi-part1/


# Part 2 Notes
Lexer - strings into tokens
Parser - recognizing a phrase in a stream of tokens
Lexeme - sequence of characters that form a token
"""

# Exercises
# Part 1
# - [x] multiple integers
# - [x] whitespace
# - [x] minus

# Part 2
# - [x] multiplication
# - [x] division
# - [ ] more number of operations
