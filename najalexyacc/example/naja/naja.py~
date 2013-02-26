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
    'DIVINT', 'E', 'OU', 'MENORIG', 'MAIORIG', 'IGUIG', 'DIF', 'STRING'
    ] + list(reserved.values())

literals = ['=','+','-','*','/', '(',')','[', ']', '%', '!', '<', '>', ':']

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
t_NOVALINHA = r'\n+'

# Tokens

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	t.type = reserved.get(t.value,'ID')
	return t


def t_REAL(t):
	r'\d*.\d+'
	t.value = float(t.value)
	return t

def t_INT(t):
	r'\d+'
	t.value = int(t.value)
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

def p_primario(p):
	'''primario : controle | declaracao | definicao | atribuicao | chamada | defsubfuncao | NOVALINHA'''
	
def p_controle(p):
    'controle : se | enquanto | para'

def p_declaracao(p):
    'declaracao : TIPO ID'
    
def p_se(p):
    '''se : SE expressao ':'
        suite
        (SENAOSE expressao ':' suite)*
        [SENAO ':' suite]
        FIM '''

def p_enquanto(p):
    'enquanto : ENQUANTO expressao : suite FIM'

def p_para(p):
    '''para : PARA ID DE (INT | ID) ATE (INT | ID) :  
        suite
        FIM'''

def p_definicao(p):
    '''definicao : DEF TIPO ID '('[params]')' : 
        suite 
        retorna
        FIM'''

def p_defsubfuncao(p):
    '''defsubfuncao : DEF VAZIO ID '('[params]')' :
        suite
        FIM'''

def p_atribuicao(p):
    "atribuicao : ID ['['INT']'] '=' valor"
    
def p_chamada(p):
    "chamada : ID '(' [valor (,valor)*] ')'"

def p_valor(p)
    '''valor : ID 
        | literal 
        | chamada'''
def p_expressao(p):
    'expressao :  exp_ou' 

def p_comparacao(p):
    'comparacao : valor [operador_comp valor]'
    
def p_param(p):

    'param : declaracao'

def p_params(p):

    'params : param(,param)*'

def p_retorna(p):

    'retorna : RETORNA expressao'

def p_imprime(p):

    'imprime : IMPRIME expressao'

def p_op_aum(p):

    'op_aum : MAISIG | MENOSIG | MULTIG | DIVIG | MODIG | EXPIG'

def p_atribuicao_aumentada(p):
    'atribuicao_aumentada : ID op_aum valor'

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
