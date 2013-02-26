# -----------------------------------------------------------------------------
# naja.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

reserved = {"enquanto": "ENQUANTO",
	"continua": "CONTINUA",
	"retorna": "RETORNA",
	"Verdade": "CONSTANTE",
	"senaose": "SENAOSE",
	"imprime": "FUNCINT",
	"quebra": "QUEBRA",
	"Falso": "CONSTANTE",
	"vazio": "VAZIO",
	"senao": "SENAO",
	"para": "PARA",
	"ate": "ATE",
	"def": "DEF",
	"fim": "FIM",
	"se": "SE",
	"de": "DE",
	"bool": "TIPO",
	"real": "TIPO",
	"int": "TIPO",
	"crt": "TIPO"}

tokens = [
    'ID','INT','REAL','HEXA', 'MAISIG', 'MENOSIG', 'MULTIG', 'DIVIG', 'MODIG', 'EXPIG', 'EXP',
    'DIVINT', 'E', 'OU', 'MENORIG', 'MAIORIG', 'IGUIG', 'DIF'
    ] + list(reserved.values())

literals = ['=','+','-','*','/', '(',')','[', ']', '%', '!', '<', '>']

t_MAISIG = r'\+='
t_MENOSIG = r'-='
t_MULTIG = r'\*='
t_DIVIG = r'/='
t_MODIG = r'%='
t_EXPIG = r'\*\*='
t_EXP = r'\*\*'
t_DIVINT = r'//'
t_E = r'&&'
t_OU = r'\|\|'
t_MENORIG = r'<='
t_MAIORIG = r'>='
t_IGUIG = r'=='
t_DIF = r'!='

# Tokens

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	t.type = reserved.get(t.value,'ID')
	return t


def t_INT(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_REAL(t):
	r'\d*.\d+'
	t.value = float(t.value)
	return t

def t_HEXA(t):
	r'0[xX][0-9a-fA-F]+'
	t.value = hex(t.value)
	return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Caracter Ilegal '%s'" % t.value[0])
    print "Linha "+str(t.lineno)
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules

#precedence = (
#    ('left','+','-'),
#    ('left','*','/'),
#    ('right','UMINUS'),
#    )

# dictionary of names
names = { }

def p_primario_decl(p):
	'primario : declaracao'
	print "funfou"

def p_declaracao(p):
    'declaracao : TIPO ID'
	

#def p_statement_assign(p):
#    'statement : NAME "=" expression'
#    names[p[1]] = p[3]

#def p_statement_expr(p):
#    'statement : expression'
#    print(p[1])

#def p_expression_binop(p):
#    '''expression : expression '+' expression
#                  | expression '-' expression
#                  | expression '*' expression
#                  | expression '/' expression'''
#    if p[2] == '+'  : p[0] = p[1] + p[3]
#    elif p[2] == '-': p[0] = p[1] - p[3]
#    elif p[2] == '*': p[0] = p[1] * p[3]
#    elif p[2] == '/': p[0] = p[1] / p[3]

#def p_expression_uminus(p):
#    "expression : '-' expression %prec UMINUS"
#    p[0] = -p[2]

#def p_expression_group(p):
#    "expression : '(' expression ')'"
#    p[0] = p[2]

#def p_expression_number(p):
#    "expression : NUMBER"
#    p[0] = p[1]

#def p_expression_name(p):
#    "expression : NAME"
#    try:
#        p[0] = names[p[1]]
#    except LookupError:
#        print("Undefined name '%s'" % p[1])
#        p[0] = 0

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc()

while 1:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s: continue
    yacc.parse(s)
