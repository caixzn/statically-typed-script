from lexer import TokenType
from parser import (
    ASTNode,
    Program,
    VariableDecl,
    WhileLoop,
    IfStatement,
    AssignmentStmt,
    BinaryOp,
    UnaryOp,
    Identifier,
    Literal,
    BreakStatement,
    PrintStatement,
    ElseStatement
)
from sam_vm import Opcode, Instruction

class CodeGenerator:
    def __init__(self):
        self.instructions = []
        self.symbol_table = {}
        self.label_counter = 0
        self.loop_end_labels = []

    def generate(self, ast: Program):
        self.visit(ast)
        self.emit(Opcode.HALT)
        return self.instructions

    def visit(self, node: ASTNode):
        method_name = f"visit_{type(node).__name__}"
        visit_method = getattr(self, method_name, self.generic_visit)
        return visit_method(node)

    def generic_visit(self, node: ASTNode):
        raise Exception(f"No visit method for {type(node).__name__}")

    def emit(self, opcode: Opcode, operand=None):
        self.instructions.append(Instruction(opcode, operand))
    
    def emit_label(self, label: str):
        self.instructions.append(label)

    def create_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"

    def visit_Program(self, node: Program):
        for statement in node.statements:
            self.visit(statement)

    def visit_VariableDecl(self, node: VariableDecl):
        self.visit(node.value)
        self.symbol_table[node.name] = len(self.symbol_table)
        self.emit(Opcode.STORE, self.symbol_table[node.name])

    def visit_WhileLoop(self, node: WhileLoop):
        start_label = self.create_label()
        end_label = self.create_label()

        self.loop_end_labels.append(end_label)
        
        self.current_end_label = end_label
        self.emit(Opcode.JMP, start_label)
        self.emit_label(start_label + ":")
        self.visit(node.condition)
        self.emit(Opcode.JZ, end_label)

        for statement in node.body:
            self.visit(statement)

        self.emit(Opcode.JMP, start_label)
        self.emit_label(end_label + ":")

        self.loop_end_labels.pop()
    
    def visit_IfStatement(self, node: IfStatement):
        end_label = self.create_label()
        self.visit(node.condition)
        next_label = self.create_label()
        self.emit(Opcode.JZ, next_label)
        
        for statement in node.if_body:
            self.visit(statement)
        self.emit(Opcode.JMP, end_label)
        
        self.emit_label(next_label + ":")
        
        for else_if in node.else_if_list:
            if isinstance(else_if, ElseStatement):  # This is the final 'else'
                for statement in else_if.body:
                    self.visit(statement)
            else:
                next_label = self.create_label()
                self.visit(else_if.condition)
                self.emit(Opcode.JZ, next_label)
                
                for statement in else_if.if_body:
                    self.visit(statement)
                self.emit(Opcode.JMP, end_label)
                
                self.emit_label(next_label + ":")
        
        self.emit_label(end_label + ":")

    def visit_AssignmentStmt(self, node: AssignmentStmt):
        self.visit(node.value)
        self.emit(Opcode.STORE, self.symbol_table[node.name])

    def visit_BinaryOp(self, node: BinaryOp):
        self.visit(node.left)
        self.visit(node.right)
        if node.operator == TokenType.PLUS:
            self.emit(Opcode.ADD)
        elif node.operator == TokenType.MINUS:
            self.emit(Opcode.SUB)
        elif node.operator == TokenType.MULTIPLY:
            self.emit(Opcode.MUL)
        elif node.operator == TokenType.DIVIDE:
            self.emit(Opcode.DIV)
        elif node.operator == TokenType.LESS_THAN:
            self.emit(Opcode.LT)
        elif node.operator == TokenType.GREATER_THAN:
            self.emit(Opcode.GT)
        elif node.operator == TokenType.EQUAL_EQUAL:
            self.emit(Opcode.EQ)
        elif node.operator == TokenType.AND:
            self.emit(Opcode.AND)
        elif node.operator == TokenType.OR:
            self.emit(Opcode.OR)
        elif node.operator == TokenType.LESS_EQUAL:
            self.emit(Opcode.PUSH, 1)
            self.emit(Opcode.ADD)
            self.emit(Opcode.LT)
        elif node.operator == TokenType.GREATER_EQUAL:
            self.emit(Opcode.PUSH, 1)
            self.emit(Opcode.SUB)
            self.emit(Opcode.GT)
            

    def visit_UnaryOp(self, node: UnaryOp):
        self.visit(node.operand)
        if node.operator == TokenType.MINUS:
            self.emit(Opcode.PUSH, 0)
            self.emit(Opcode.SWAP)
            self.emit(Opcode.SUB)
        elif node.operator == TokenType.NOT:
            self.emit(Opcode.NOT)

    def visit_Identifier(self, node: Identifier):
        self.emit(Opcode.LOAD, self.symbol_table[node.name])

    def visit_Literal(self, node: Literal):
        self.emit(Opcode.PUSH, node.value)

    def visit_BreakStatement(self, node: BreakStatement):
        if not self.loop_end_labels:
            raise Exception("Break statement outside of loop")
        self.emit(Opcode.JMP, self.loop_end_labels[-1])
    
    def visit_PrintStatement(self, node: PrintStatement):
        self.visit(node.expr)
        self.emit(Opcode.PRINT)

