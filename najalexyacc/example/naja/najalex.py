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
    'ID','REAL','INT', 'MAISIG', 'MENOSIG', 'MULTIG', 'DIVIG', 'MODIG', 'EXPIG', 'EXP',
    'DIVINT', 'E', 'OU', 'MENORIG', 'MAIORIG', 'IGUIG', 'DIF', 'PALAVRA', 'NOVALINHA'
    ] + list(reserved.values())

literals = ['=','+','-','*','/', '(',')','[', ']', '%', '!', '<', '>', ':',',']

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
	r'[a-zA-Z_]\w*'
	t.type = reserved.get(t.value,'ID')
	return t

def t_COMENTARIO(t):
    r'\#[^\n]*'

def t_REAL(t):
	r'\d*.\d+'
	t.value = float(t.value)
	return t

def t_INT(t):
	r'\d+'
	t.value = int(t.value)
	return t
	
def t_PALAVRA(t):
    r'\"[^\"]*\"'
    t.value = t.value[1:-1]
    return t
    
t_ignore = " \t"    

def t_NOVALINHA(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    return t
    
def t_error(t):
    print("Caracter Ilegal '%s'" % t.value[0])
    print "Linha "+str(t.lineno)
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Test it out
data = '''
def int calculadora(int operacao, int v1, int v2):
    se operacao == 1:
        retorna v1 + v2
    senaose operacao == 2:
        retorna v1 - v2
    senaose operacao == 3:
        retorna v1 * v2
    senao:
        retorna v1 / v2
    fim

    retorna 0 
fim

int resultado
resultado = calculadora(soma, 3, 6) 
    
'''  

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print tok
