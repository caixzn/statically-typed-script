from grammar import Grammar
from ll1_check import is_ll1
from predict import predict_algorithm


def print_grammar(G: Grammar) -> None:
    print(f"Terminais:\n{'\n'.join([x for x in G.terminals()])}")
    print(f"Não-terminais:\n{'\n'.join([X for X in G.nonterminals()])}")
    print(f"Produções:\n{'\n'.join(
        ['id: ' + str(p) + ' ' + str(G.lhs(p)) + '->' + str(G.rhs(p)) for p in G.productions()])}")


if __name__ == "__main__":
    G = Grammar()

    G.add_nonterminal("Program")
    G.add_production("Program", ["StatementList"])

    G.add_nonterminal("StatementList")
    G.add_production("StatementList", ["Statement", "StatementList"])
    G.add_production("StatementList", [])  # epsilon

    G.add_nonterminal("Statement")
    G.add_production("Statement", ["VariableDecl"])
    G.add_production("Statement", ["WhileLoop"])
    G.add_production("Statement", ["IfStatement"])
    G.add_production("Statement", ["AssignmentStmt"])
    G.add_production("Statement", ["break", ";"])

    G.add_terminal("break")
    G.add_terminal(";")

    G.add_nonterminal("VariableDecl")
    G.add_production("VariableDecl", ["let", "Identifier", ":", "Type", "=", "Expression", ";"])
    G.add_terminal("let")
    G.add_terminal(":")
    G.add_terminal("=")

    G.add_nonterminal("Type")
    G.add_production("Type", ["int"])
    G.add_production("Type", ["float"])
    G.add_production("Type", ["bool"])
    G.add_terminal("int")
    G.add_terminal("float")
    G.add_terminal("bool")

    G.add_nonterminal("WhileLoop")
    G.add_production("WhileLoop", ["while", "(", "Expression", ")", "Block"])
    G.add_terminal("while")
    G.add_terminal("(")
    G.add_terminal(")")

    G.add_nonterminal("IfStatement")
    G.add_production("IfStatement", ["if", "(", "Expression", ")", "Block", "ElseIfList"])
    G.add_terminal("if")

    G.add_nonterminal("ElseIfList")
    G.add_production("ElseIfList", ["else", "ElseIfPart"])
    G.add_production("ElseIfList", [])  # epsilon
    G.add_terminal("else")

    G.add_nonterminal("ElseIfPart")
    G.add_production("ElseIfPart", ["IfStatement"])
    G.add_production("ElseIfPart", ["Block"])

    G.add_nonterminal("Block")
    G.add_production("Block", ["{", "StatementList", "}"])
    G.add_terminal("{")
    G.add_terminal("}")

    G.add_nonterminal("AssignmentStmt")
    G.add_production("AssignmentStmt", ["Identifier", "=", "Expression", ";"])

    G.add_nonterminal("Expression")
    G.add_production("Expression", ["OrExpr"])

    G.add_nonterminal("OrExpr")
    G.add_production("OrExpr", ["AndExpr", "OrExprTail"])

    G.add_nonterminal("OrExprTail")
    G.add_production("OrExprTail", ["||", "AndExpr", "OrExprTail"])
    G.add_production("OrExprTail", [])  # epsilon
    G.add_terminal("||")

    G.add_nonterminal("AndExpr")
    G.add_production("AndExpr", ["EqualityExpr", "AndExprTail"])

    G.add_nonterminal("AndExprTail")
    G.add_production("AndExprTail", ["&&", "EqualityExpr", "AndExprTail"])
    G.add_production("AndExprTail", [])  # epsilon
    G.add_terminal("&&")

    G.add_nonterminal("EqualityExpr")
    G.add_production("EqualityExpr", ["RelationalExpr", "EqualityExprTail"])

    G.add_nonterminal("EqualityExprTail")
    G.add_production("EqualityExprTail", ["EqualityOp", "RelationalExpr", "EqualityExprTail"])
    G.add_production("EqualityExprTail", [])  # epsilon

    G.add_nonterminal("EqualityOp")
    G.add_production("EqualityOp", ["=="])
    G.add_production("EqualityOp", ["!="])
    G.add_terminal("==")
    G.add_terminal("!=")

    G.add_nonterminal("RelationalExpr")
    G.add_production("RelationalExpr", ["AdditiveExpr", "RelationalExprTail"])

    G.add_nonterminal("RelationalExprTail")
    G.add_production("RelationalExprTail", ["RelationalOp", "AdditiveExpr", "RelationalExprTail"])
    G.add_production("RelationalExprTail", [])  # epsilon

    G.add_nonterminal("RelationalOp")
    G.add_production("RelationalOp", ["<"])
    G.add_production("RelationalOp", [">"])
    G.add_production("RelationalOp", ["<="])
    G.add_production("RelationalOp", [">="])
    G.add_terminal("<")
    G.add_terminal(">")
    G.add_terminal("<=")
    G.add_terminal(">=")

    G.add_nonterminal("AdditiveExpr")
    G.add_production("AdditiveExpr", ["MultiplicativeExpr", "AdditiveExprTail"])

    G.add_nonterminal("AdditiveExprTail")
    G.add_production("AdditiveExprTail", ["AdditiveOp", "MultiplicativeExpr", "AdditiveExprTail"])
    G.add_production("AdditiveExprTail", [])  # epsilon

    G.add_nonterminal("AdditiveOp")
    G.add_production("AdditiveOp", ["+"])
    G.add_production("AdditiveOp", ["-"])
    G.add_terminal("+")
    G.add_terminal("-")

    G.add_nonterminal("MultiplicativeExpr")
    G.add_production("MultiplicativeExpr", ["UnaryExpr", "MultiplicativeExprTail"])

    G.add_nonterminal("MultiplicativeExprTail")
    G.add_production("MultiplicativeExprTail", ["MultiplicativeOp", "UnaryExpr", "MultiplicativeExprTail"])
    G.add_production("MultiplicativeExprTail", [])  # epsilon

    G.add_nonterminal("MultiplicativeOp")
    G.add_production("MultiplicativeOp", ["*"])
    G.add_production("MultiplicativeOp", ["/"])
    G.add_terminal("*")
    G.add_terminal("/")

    G.add_nonterminal("UnaryExpr")
    G.add_production("UnaryExpr", ["UnaryOp", "PrimaryExpr"])
    G.add_production("UnaryExpr", ["PrimaryExpr"])

    G.add_nonterminal("UnaryOp")
    G.add_production("UnaryOp", ["-"])
    G.add_production("UnaryOp", ["!"])
    G.add_terminal("-")
    G.add_terminal("!")

    G.add_nonterminal("PrimaryExpr")
    G.add_production("PrimaryExpr", ["Identifier"])
    G.add_production("PrimaryExpr", ["IntLiteral"])
    G.add_production("PrimaryExpr", ["FloatLiteral"])
    G.add_production("PrimaryExpr", ["BoolLiteral"])
    G.add_production("PrimaryExpr", ["(", "Expression", ")"])

    G.add_terminal("Identifier")
    G.add_terminal("IntLiteral")
    G.add_terminal("FloatLiteral")
    G.add_nonterminal("BoolLiteral")

    G.add_production("BoolLiteral", ["true"])
    G.add_production("BoolLiteral", ["false"])
    G.add_terminal("true")
    G.add_terminal("false")

    G.add_production("Statement", ["print", "(", "Expression", ")", ";"])
    G.add_terminal("print")

    print_grammar(G)
    print("Imprimindo terminais")
    for x in G.terminals():
        print(x)
    print("Imprimindo não-terminais")
    for x in G.nonterminals():
        print(x)
    print("Imprimindo produções")
    for x in G.productions():
        print(x)

    pred_alg = predict_algorithm(G)
    ll1 = is_ll1(G, pred_alg)
    if ll1:
        print("É LL(1)")
    else:
        print("Não é LL(1)")
