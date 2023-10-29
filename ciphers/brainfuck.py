import traceback

"""
    author: Samarth Tankasali
    date: 29.10.2023
    class: Brainfuck Cipher

    This class implements the BF-cipher algorithm and provides
    some useful methods for interpreting instructions

    Description:
    Brainfuck is an esoteric programming language created in 1993 by Urban Müller.

    Notable for its extreme minimalism, the language consists of only eight simple commands, a data pointer and an instruction pointer. While it is fully Turing complete, it is not intended for practical use, but to challenge and amuse programmers. Brainfuck requires one to break commands into microscopic steps.

    The language's name is a reference to the slang term brainfuck, which refers to things so complicated or unusual that they exceed the limits of one's understanding, as it was not meant or made for designing actual software but to challenge the boundaries of computer programming.
"""


class BFCipher:
    """
    Brainfuck Interpreter.

    BFCipher class processes the brainfuck instruction and returns the output after compilation.

    Args:
        instruction (str): A string of the BFCipher code.

    Examples:
        >>> # Code to add 5 + 2
        >>> instruction = "++>+++++[<+>-]++++++++[<++++++>-]<."
        >>> print(BFCipher(instruction).compile())
        7
        >>> # Code to print "Hello World!"
        >>> instruction = "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
        >>> print(BFCipher(instruction).compile(), end = "")
        Hello World!
    """

    def __init__(self, instruction: str) -> None:
        """
        BFCipher constructor

        Args:
            instruction (str): A string of the BFCipher code.
        """
        self.main_arr: list = [0]*30000
        self.instruction_ptr: int = 0
        self.data_ptr: int = 0
        self.user_input: list = []
        self.loop_table: dict = {}
        self.output: str = ""
        if not isinstance(instruction, str):
            raise TypeError("Instruction must be a string")
        else:
            self.instruction: str = instruction

    def __syntax_check(self):
        """
        Performs a syntax check of the instruction and generates the `loop_table`.
        """
        checker_ptr: int = self.instruction_ptr
        bracket_stack = []
        while checker_ptr < len(self.instruction):
            if self.instruction[checker_ptr] == '[':
                bracket_stack.append(checker_ptr)
            elif self.instruction[checker_ptr] == ']':
                if len(bracket_stack) == 0:
                    raise SyntaxError(
                        f"Incomplete closure of bracket for instruction {checker_ptr}")
                loop_beginning_index = bracket_stack.pop()
                self.loop_table[loop_beginning_index] = checker_ptr
                self.loop_table[checker_ptr] = loop_beginning_index
            checker_ptr += 1
        if len(bracket_stack) > 0:
            raise SyntaxError(
                f"Incomplete closure of bracket for instruction {checker_ptr}")

    def __increment_data_ptr(self):
        """
        Increment the data pointer by one (to point to the next cell to the right).
        """
        self.data_ptr += 1
        if self.data_ptr > 30000:
            raise ValueError(
                "NullValue Reference: Data pointer referencing null.")

    def __decrement_data_ptr(self):
        """
        Decrement the data pointer by one (to point to the next cell to the left).
        """
        self.data_ptr -= 1
        if self.data_ptr < 0:
            raise ValueError(
                "NullValue Reference: Data pointer referencing null.")

    def __increment_data_value(self):
        """
        Increment the byte at the data pointer by one.
        """
        self.main_arr[self.data_ptr] += 1
        self.main_arr[self.data_ptr] = self.main_arr[self.data_ptr] & 0xFF

    def __decrement_data_value(self):
        """
        Decrement the byte at the data pointer by one.
        """
        self.main_arr[self.data_ptr] -= 1
        self.main_arr[self.data_ptr] = self.main_arr[self.data_ptr] & 0xFF

    def __append_bracket(self):
        """
        If the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next command, jump it forward to the command after the matching `]` command.
        """
        if self.main_arr[self.data_ptr] == 0:
            self.instruction_ptr = self.loop_table[self.instruction_ptr]

    def __pop_bracket(self):
        """
        If the byte at the data pointer is nonzero, then instead of moving the instruction pointer forward to the next command, jump it back to the command after the matching `[` command.
        """
        if self.main_arr[self.data_ptr] != 0:
            self.instruction_ptr = self.loop_table[self.instruction_ptr]

    def __print_output(self):
        """
        Output the byte at the data pointer.
        """
        self.output += chr(self.main_arr[self.data_ptr])

    def __take_input(self):
        """
        Accept one byte of input, storing its value in the byte at the data pointer.
        """
        if self.user_input == []:
            user_input = list(input() + "\n")
        self.main_arr[self.data_ptr] = ord(user_input.pop(0))

    def compile(self) -> str:
        """
        Executes the brainfuck instructions and returns appropriate output after compilation.

        Returns:
            `str`: A string representing the output of the BF instructions.
        """
        try:
            self.__syntax_check()
            while self.instruction_ptr < len(self.instruction):
                if self.instruction[self.instruction_ptr] == '>':
                    self.__increment_data_ptr()
                elif self.instruction[self.instruction_ptr] == '<':
                    self.__decrement_data_ptr()
                elif self.instruction[self.instruction_ptr] == '+':
                    self.__increment_data_value()
                elif self.instruction[self.instruction_ptr] == '-':
                    self.__decrement_data_value()
                elif self.instruction[self.instruction_ptr] == '[':
                    self.__append_bracket()
                elif self.instruction[self.instruction_ptr] == ']':
                    self.__pop_bracket()
                elif self.instruction[self.instruction_ptr] == '.':
                    self.__print_output()
                elif self.instruction[self.instruction_ptr] == ',':
                    self.__take_input()
                self.instruction_ptr += 1
            return self.output
        except ValueError:
            print(traceback.format_exc(), end="")
        except SyntaxError:
            print(traceback.format_exc(), end="")


if __name__ == "__main__":
    inputs = ["testcode1.bf", "testcode2.bf"] # Add path of testcodes here
    outputs = ["7", "Hello World!\n"] # Add expected outputs here
    passed = failed = 0
    for input, expected_ouput in zip(inputs, outputs):
        file = open(f"tests_BFCipher/{input}", "r")
        instruction = file.read()
        output = BFCipher(instruction).compile()
        if output == expected_ouput:
            passed+=1
        else:
            failed+=1
        file.close()
    print(f"Passed : {passed}\nFailed : {failed}")
    if failed == 0:
        print("All testcases passed :)")
    else:
        print(f"{failed} testcases failed :(")
