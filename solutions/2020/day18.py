from utils.abstract import FileReaderSolution


class Day18:
    def solve(self, input_data: str) -> int:
        result = 0
        for equation in input_data.splitlines():
            while not equation.isnumeric():
                groups = list(self.parenthetic_contents(equation))
                if len(groups) == 0:
                    break

                group = groups.pop(0)[1]
                equation = equation.replace('(' + group + ')', str(self.solve_expression(group)))

            result += self.solve_expression(equation)

        return result

    @staticmethod
    def execute_operator(operand_a, operand_b, operator):
        if operator == '+':
            return operand_a + operand_b

        if operator == '*':
            return operand_a * operand_b

        raise ValueError(f"Operator: {operator} unknown")

    @staticmethod
    def find_next_operator(operators, start_pos, expression):
        for i in range(start_pos + 1, len(expression)):
            if expression[i] in operators:
                return i

        return -1

    @staticmethod
    def find_previous_operator(operators, start_pos, expression):
        for i in range(start_pos-1, 0, -1):
            if expression[i] in operators:
                return i

        return -1

    @staticmethod
    def parenthetic_contents(string):
        """Generate parenthesized contents in string as pairs (level, contents)."""
        stack = []
        for i, c in enumerate(string):
            if c == '(':
                stack.append(i)
            elif c == ')' and stack:
                start = stack.pop()
                yield len(stack), string[start + 1: i]

    def solve_expression(self, expression):
        raise NotImplementedError

    def solve_equation(self, expression, operators, operator_pos):
        operator = expression[operator_pos]
        previous_operator_pos = self.find_previous_operator(operators, operator_pos, expression)
        next_operator_pos = self.find_next_operator(operators, operator_pos, expression)

        if previous_operator_pos == -1:
            operand_a = int(expression[0:operator_pos])
        else:
            operand_a = int(expression[previous_operator_pos + 1:operator_pos])

        if next_operator_pos == -1:
            operand_b = int(expression[operator_pos + 1:])
        else:
            operand_b = int(expression[operator_pos + 1:next_operator_pos - 1])

        result = self.execute_operator(int(operand_a), int(operand_b), operator)
        expression = expression.replace(f"{str(operand_a)} {operator} {str(operand_b)}", str(result), 1)

        return self.solve_expression(expression)


class Day18PartA(Day18, FileReaderSolution):
    def solve_expression(self, expression):
        operators = ['+', '*']

        for i in range(0, len(expression)):
            if expression[i] in operators:
                return self.solve_equation(expression, operators, i)

        return int(expression)


class Day18PartB(Day18, FileReaderSolution):
    def solve_expression(self, expression):
        operators = ['+', '*']

        for operator in operators:
            while (operator_pos := expression.find(operator)) != -1:
                return self.solve_equation(expression, operators, operator_pos)

        return int(expression)
