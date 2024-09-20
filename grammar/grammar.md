# Grammar

[Voltar ao README](../README.md)

## Program structure

```ebnf
Program         ::= StatementList

StatementList   ::= Statement StatementList
                  | ε
```

## Statements

```ebnf
Statement       ::= VariableDecl
                  | WhileLoop
                  | IfStatement
                  | AssignmentStmt
                  | "break" ";"
```


## Variable declaration

```ebnf
VariableDecl    ::= "let" Identifier ":" Type "=" Expression ";"
```


## Types

```ebnf
Type            ::= "int8" | "int16" | "int32" | "int64"
                  | "uint8" | "uint16" | "uint32" | "uint64"
                  | "float32" | "float64" | "bool"
```


## While loop

```ebnf
WhileLoop       ::= "while" "(" Expression ")" Block
```


## If statement

```ebnf
IfStatement     ::= "if" "(" Expression ")" Block ElsePart

ElsePart        ::= "else" Block
                  | ε
```


## Block

```ebnf
Block           ::= "{" StatementList "}"
```


## Assignment

```ebnf
AssignmentStmt  ::= Identifier "=" Expression ";"
```


## Expressions

```ebnf
Expression      ::= OrExpr

OrExpr          ::= AndExpr OrExprTail
OrExprTail      ::= "||" AndExpr OrExprTail
                  | ε

AndExpr         ::= EqualityExpr AndExprTail
AndExprTail     ::= "&&" EqualityExpr AndExprTail
                  | ε

EqualityExpr    ::= RelationalExpr EqualityExprTail
EqualityExprTail ::= EqualityOp RelationalExpr EqualityExprTail
                   | ε
EqualityOp      ::= "==" | "!="

RelationalExpr  ::= AdditiveExpr RelationalExprTail
RelationalExprTail ::= RelationalOp AdditiveExpr RelationalExprTail
                     | ε
RelationalOp    ::= "<" | ">" | "<=" | ">="

AdditiveExpr    ::= MultiplicativeExpr AdditiveExprTail
AdditiveExprTail ::= AdditiveOp MultiplicativeExpr AdditiveExprTail
                   | ε
AdditiveOp      ::= "+" | "-"

MultiplicativeExpr ::= UnaryExpr MultiplicativeExprTail
MultiplicativeExprTail ::= MultiplicativeOp UnaryExpr MultiplicativeExprTail
                         | ε
MultiplicativeOp  ::= "*" | "/"

UnaryExpr       ::= UnaryOp PrimaryExpr
                  | PrimaryExpr
UnaryOp         ::= "-" | "!"

PrimaryExpr     ::= Identifier
                  | IntLiteral
                  | FloatLiteral
                  | BoolLiteral
                  | "(" Expression ")"
```


## Terminals

```ebnf
Identifier      ::= [a-zA-Z_][a-zA-Z0-9_]*
IntLiteral      ::= [0-9]+
FloatLiteral    ::= [0-9]+ "." [0-9]+
BoolLiteral     ::= "true" | "false"
```
