from lexer import TokenType, Token

class ASTNode:
    def __repr__(self) -> str:
        return f"{type(self).__name__}({', '.join(f'{field}={getattr(self, field)}' for field in self.__dict__)})"

class Program(ASTNode):
    def __init__(self, statements: list[ASTNode]):
        self.statements = statements

class VariableDecl(ASTNode):
    def __init__(self, name: str, type: str, value: ASTNode):
        self.name = name
        self.type = type
        self.value = value

class WhileLoop(ASTNode):
    def __init__(self, condition: ASTNode, body: list[ASTNode]):
        self.condition = condition
        self.body = body

class IfStatement(ASTNode):
    def __init__(self, condition: ASTNode, if_body: list[ASTNode], else_if_list: list['IfStatement']):
        self.condition = condition
        self.if_body = if_body
        self.else_if_list = else_if_list

class ElseStatement(ASTNode):
    def __init__(self, body: list[ASTNode]):
        self.body = body

class BreakStatement(ASTNode):
    pass

class PrintStatement(ASTNode):
    def __init__(self, expr: ASTNode):
        self.expr = expr

class AssignmentStmt(ASTNode):
    def __init__(self, name: str, value: ASTNode):
        self.name = name
        self.value = value

class UnaryOp(ASTNode):
    def __init__(self, operator: TokenType, operand: ASTNode):
        self.operator = operator
        self.operand = operand

class BinaryOp(ASTNode):
    def __init__(self, left: ASTNode, operator: TokenType, right: ASTNode):
        self.left = left
        self.operator = operator
        self.right = right

class Identifier(ASTNode):
    def __init__(self, name: str):
        self.name = name

class Literal(ASTNode):
    def __init__(self, value, type: str):
        self.value = value
        self.type = type

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Program:
        return self.program()

    def program(self) -> Program:
        return Program(self.statement_list())

    def statement_list(self) -> list[ASTNode]:
        statements = []
        while not self.is_at_end() and not self.check(TokenType.RBRACE):
            statements.append(self.statement())
        return statements

    def statement(self) -> ASTNode:
        if self.match(TokenType.LET):
            return self.variable_declaration()
        elif self.match(TokenType.WHILE):
            return self.while_loop()
        elif self.match(TokenType.IF):
            return self.if_statement()
        elif self.match(TokenType.BREAK):
            return self.break_statement()
        elif self.match(TokenType.PRINT):
            return self.print_statement()
        elif self.check(TokenType.IDENTIFIER):
            return self.assignment_statement()
        else:
            raise Exception(f"Unexpected token: {self.peek()}")

    def variable_declaration(self) -> VariableDecl:
        name = self.consume(TokenType.IDENTIFIER, "Expected variable name").value
        self.consume(TokenType.COLON, "Expected ':' after variable name")
        type = self.consume(TokenType.TYPE, "Expected type after ':'").value
        self.consume(TokenType.EQUALS, "Expected '=' after type")
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after variable declaration")
        return VariableDecl(name, type, value)

    def while_loop(self) -> WhileLoop:
        self.consume(TokenType.LPAREN, "Expected '(' after 'while'")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after while condition")
        body = self.block()
        return WhileLoop(condition, body)

    def if_statement(self) -> IfStatement:
        self.consume(TokenType.LPAREN, "Expected '(' after 'if'")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after if condition")
        if_body = self.block()
        else_if_list = self.else_if_list()
        return IfStatement(condition, if_body, else_if_list)

    def else_if_list(self) -> list[IfStatement]:
        else_if_statements = []
        while self.match(TokenType.ELSE):
            if self.match(TokenType.IF):
                self.consume(TokenType.LPAREN, "Expected '(' after 'else if'")
                condition = self.expression()
                self.consume(TokenType.RPAREN, "Expected ')' after else if condition")
                if_body = self.block()
                else_if_statements.append(IfStatement(condition, if_body, []))
            else:
                else_body = self.block()
                else_if_statements.append(ElseStatement(else_body))
                break
        return else_if_statements

    def break_statement(self) -> BreakStatement:
        self.consume(TokenType.SEMICOLON, "Expected ';' after 'break'")
        return BreakStatement()
    
    def print_statement(self) -> PrintStatement:
        self.consume(TokenType.LPAREN, "Expected '(' after 'print'")
        expr = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after print expression")
        self.consume(TokenType.SEMICOLON, "Expected ';' after print statement")
        return PrintStatement(expr)

    def assignment_statement(self) -> AssignmentStmt:
        name = self.consume(TokenType.IDENTIFIER, "Expected variable name").value
        self.consume(TokenType.EQUALS, "Expected '=' in assignment")
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after assignment")
        return AssignmentStmt(name, value)

    def block(self) -> list[ASTNode]:
        self.consume(TokenType.LBRACE, "Expected '{' before block")
        statements = self.statement_list()
        self.consume(TokenType.RBRACE, "Expected '}' after block")
        return statements

    def expression(self) -> ASTNode:
        return self.or_expr()

    def or_expr(self) -> ASTNode:
        expr = self.and_expr()
        while self.match(TokenType.OR):
            right = self.and_expr()
            expr = BinaryOp(expr, TokenType.OR, right)
        return expr

    def and_expr(self) -> ASTNode:
        expr = self.equality()
        while self.match(TokenType.AND):
            right = self.equality()
            expr = BinaryOp(expr, TokenType.AND, right)
        return expr

    def equality(self) -> ASTNode:
        expr = self.relational()
        while self.match(TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL):
            operator = self.previous().type
            right = self.relational()
            expr = BinaryOp(expr, operator, right)
        return expr

    def relational(self) -> ASTNode:
        expr = self.additive()
        while self.match(TokenType.LESS_THAN, TokenType.GREATER_THAN, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            operator = self.previous().type
            right = self.additive()
            expr = BinaryOp(expr, operator, right)
        return expr

    def additive(self) -> ASTNode:
        expr = self.multiplicative()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous().type
            right = self.multiplicative()
            expr = BinaryOp(expr, operator, right)
        return expr

    def multiplicative(self) -> ASTNode:
        expr = self.unary()
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self.previous().type
            right = self.unary()
            expr = BinaryOp(expr, operator, right)
        return expr

    def unary(self) -> ASTNode:
        if self.match(TokenType.MINUS, TokenType.NOT):
            operator = self.previous().type
            right = self.unary()
            return UnaryOp(operator, right)
        return self.primary()

    def primary(self) -> ASTNode:
        if self.match(TokenType.INT_LITERAL):
            return Literal(int(self.previous().value), 'int')
        if self.match(TokenType.FLOAT_LITERAL):
            return Literal(float(self.previous().value), 'float')
        if self.match(TokenType.BOOL_LITERAL):
            return Literal(self.previous().value == 'true', 'bool')
        if self.match(TokenType.IDENTIFIER):
            return Identifier(self.previous().value)
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr
        raise Exception(f"Unexpected token: {self.peek()}")

    def match(self, *types) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def consume(self, type: TokenType, message: str) -> Token:
        if self.check(type):
            return self.advance()
        raise Exception(f"{message} at {self.peek()}")

    def check(self, type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

class SemanticAnalyzer:
    def __init__(self):
        self.scopes: list[dict[str, str]] = [{}]  # Stack of scopes
        self.current_function: str | None = None
        self.loop_depth: int = 0

    def analyze(self, ast: Program):
        for statement in ast.statements:
            self.visit(statement)

    def visit(self, node: ASTNode):
        method_name = f"visit_{type(node).__name__}"
        visit_method = getattr(self, method_name, self.generic_visit)
        return visit_method(node)

    def generic_visit(self, node: ASTNode):
        raise Exception(f"No visit method for {type(node).__name__}")

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def declare(self, name: str, type: str):
        if name in self.scopes[-1]:
            raise Exception(f"Variable '{name}' already declared in this scope")
        self.scopes[-1][name] = type

    def lookup(self, name: str) -> str | None:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def visit_Program(self, node: Program):
        for statement in node.statements:
            self.visit(statement)

    def visit_VariableDecl(self, node: VariableDecl):
        value_type = self.visit(node.value)
        if value_type != node.type:
            raise Exception(f"Type mismatch: expected {node.type}, got {value_type}")
        self.declare(node.name, node.type)

    def visit_WhileLoop(self, node: WhileLoop):
        condition_type = self.visit(node.condition)
        if condition_type != 'bool':
            raise Exception(f"While condition must be boolean, got {condition_type}")
        self.loop_depth += 1
        self.enter_scope()
        for statement in node.body:
            self.visit(statement)
        self.exit_scope()
        self.loop_depth -= 1

    def visit_IfStatement(self, node: IfStatement):
        condition_type = self.visit(node.condition)
        if condition_type != 'bool':
            raise Exception(f"If condition must be boolean, got {condition_type}")
        self.enter_scope()
        for statement in node.if_body:
            self.visit(statement)
        self.exit_scope()
        for statement in node.else_if_list:
            self.visit(statement)
    
    def visit_ElseStatement(self, node: ElseStatement):
        self.enter_scope()
        for statement in node.body:
            self.visit(statement)
        self.exit_scope()

    def visit_AssignmentStmt(self, node: AssignmentStmt):
        var_type = self.lookup(node.name)
        if var_type is None:
            raise Exception(f"Variable '{node.name}' not declared")
        value_type = self.visit(node.value)
        
        if var_type != value_type:
            raise Exception(f"Type mismatch in assignment: variable '{node.name}' is {var_type}, trying to assign {value_type}")

    def visit_BreakStatement(self, node: BreakStatement):
        if self.loop_depth == 0:
            raise Exception("Break statement outside of loop")
    
    def visit_PrintStatement(self, node: PrintStatement):
        pass


    def visit_BinaryOp(self, node: BinaryOp):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        if left_type != right_type:
            raise Exception(f"Type mismatch in binary operation: {left_type} {node.operator} {right_type}")
        if node.operator in [TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, TokenType.DIVIDE]:
            if left_type not in ['int', 'float']:
                raise Exception(f"Invalid type for arithmetic operation: {left_type}")
            return left_type
        elif node.operator in [TokenType.LESS_THAN, TokenType.GREATER_THAN, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL]:
            if left_type not in ['int', 'float']:
                raise Exception(f"Invalid type for comparison: {left_type}")
            return 'bool'
        elif node.operator in [TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL]:
            return 'bool'
        elif node.operator in [TokenType.AND, TokenType.OR]:
            if left_type != 'bool':
                raise Exception(f"Logical operations require boolean operands, got {left_type}")
            return 'bool'
        else:
            raise Exception(f"Unknown binary operator: {node.operator}")

    def visit_UnaryOp(self, node: UnaryOp):
        operand_type = self.visit(node.operand)
        if node.operator == TokenType.MINUS:
            if operand_type not in ['int', 'float']:
                raise Exception(f"Invalid type for negation: {operand_type}")
            return operand_type
        elif node.operator == TokenType.NOT:
            if operand_type != 'bool':
                raise Exception(f"Logical NOT requires boolean operand, got {operand_type}")
            return 'bool'
        else:
            raise Exception(f"Unknown unary operator: {node.operator}")

    def visit_Identifier(self, node: Identifier):
        var_type = self.lookup(node.name)
        if var_type is None:
            raise Exception(f"Variable '{node.name}' not declared")
        return var_type

    def visit_Literal(self, node: Literal):
        return node.type
