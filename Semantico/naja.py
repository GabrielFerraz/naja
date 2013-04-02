import sys
from operator import itemgetter

if sys.version_info[0] >= 3:
    raw_input = input

entrada = ""
arquivo = open(sys.argv[1], "r")
a = arquivo.readlines()

reserved = {"enquanto": "ENQUANTO",
	"continua": "CONTINUA",
	"retorna": "RETORNA",
	"Verdade": "CONSTANTE",
	"senaose": "SENAOSE",
	"imprime": "IMPRIME",
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

literals = ['=','+','-','*','/', '(',')','[', ']', '%', '!', '<', '>', ':', ',']

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
    print str(t.lineno)+": "+a[t.lineno-1]
    t.lexer.skip(1)
    sys.exit(0)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

#precedence = (
#    ('left','+','-'),
#    ('left','*','/'),
#    ('right','UMINUS'),
#    )

# dictionary of names
names = { }
pilha = []
qtd_params = 0

def p_program(p):
    ''' program : primario 
                | primario program 
                | NOVALINHA'''

def p_primario(p):
	'''primario : controle 
	            | declaracao 
	            | definicao 
	            | atribuicao 
	            | chamada 
	            | defsubfuncao
	            | NOVALINHA primario '''
	
def p_controle(p):
	'''controle : se 
                | enquanto 
                | para'''

def p_declaracao(p):
	'''declaracao : TIPO ID '''
	escopo = 0
	codigo = 0
	for a in p.stack:
		try:
			if a.value in ["def","se","senao","senaose","para","enquanto"]:
				if a.value not in ["senao","senaose"]:
					escopo += 1
		except:
			pass
	names[p.lexpos(2)] = {"valor":p[2],"tipo":p[1],"escopo":escopo,'codigo':codigo}
	p[0] = p.lexpos(2)
		



def p_empty(p):
	'empty : '
	pass

def p_senaosemais(p):
    '''senaosemais : senaose senaosemais
                   | empty '''

def p_senaose(p):
    '''senaose : SENAOSE expressao ':' suite '''

def p_senao(p):
    '''senao : SENAO ':' suite 
             | empty '''

def p_se(p):
	"se : SE expressao ':' suite senaosemais senao FIM "

def p_enquanto(p):
    "enquanto : ENQUANTO expressao ':' suite FIM "

def p_intid(p):
    '''intid : INT 
             | ID '''

def p_para(p):
    '''para : PARA ID DE intid ATE intid ':' suite FIM '''

def p_definicao(p):
	'''definicao : DEF TIPO ID '(' params ')' ':' suite_sem_retorno retorna FIM
                 | DEF TIPO ID '(' params ')' ':' suite_sem_retorno retorna novalinha FIM'''
	if not p[5]:
		p[5] = []
	names[p.lexpos(3)] = {"valor":p[3],"tipo":p[2], "params":len(p[5]), "codigo":-1}
	for i in p[5]:
		names[i]["codigo"] = p.lexpos(3)

def p_novalinha(p):
    '''novalinha : NOVALINHA
                | NOVALINHA novalinha'''
    
def p_defsubfuncao(p):
    '''defsubfuncao : DEF VAZIO ID '(' params ')' ':' suite FIM '''
    
def p_atribuicao_vetor(p):
    "atribuicao : ID '[' INT ']' '=' valor "
    
def p_atribuicao(p):
    "atribuicao : ID '=' valor "
	
    
def p_valorvalor(p):
	'''valorvalor : ',' valor valorvalor
                | empty '''
	if len(p) > 2:
		if not p[3]:
			p[3] = []
		p[0] = p[2] + p[3]


def p_chamada(p):
	'''chamada : ID '(' valor valorvalor ')'
			   | ID '(' ')' '''
	p[0] = p[1]
	print p[3]
	if len(p) >4: 
		print p[4]
	if len(p) > 4:
		if not p[4]:
			p[4] = 0
	chamada = busca_nome(p[1])
	parametros = []
	pos = []
	for i in names:
		if names[i]['codigo'] == chamada:
			parametros.append((i,names[i]['tipo']))
	parametros = sorted(parametros, key = itemgetter(0))
	if len(p) > 4 and names[chamada]["params"] == len(p[3]+p[4]):
		
		for w in p[3]+p[4]:
			if w in ['int','real','crt']:
				if w != parametros[0][1]:
					erro_semantico("argumento do tipo "+w+". "+parametros[0][1]+" esperado")
			else:
				n = busca_nome(w)
				if names[n]['tipo'] != parametros[0][1]:
					erro_semantico(names[n]["valor"]+" do tipo "+names[n]['tipo']+". "+parametros[0][1]+" esperado")
			parametros.pop(0)
	else:
		erro_semantico(p[1]+'() precisa de '+str(names[chamada]["params"])+' argumentos ('+str(len(p[3]+p[4]))+' passados)')

def p_valor(p):
	'''valor : ID 
		| literal 
		| chamada 
		| CONSTANTE'''
	p[0] = [p[1]]
	print p[1]
        
def p_expressao(p):
    'expressao :  exp_ou' 

def p_comparacao(p):
    '''comparacao : valor
                  | valor operador_comp valor '''
    
def p_operador_comp(p):
    '''operador_comp : '<' 
                     | '>' 
                     | IGUIG 
                     | MAIORIG 
                     | MENORIG 
                     | DIF '''
           
def p_exponenciacao(p):
    '''exponenciacao : comparacao
                   | comparacao EXP exp_u '''

def p_exp_u(p):
    '''exp_u : exponenciacao 
             | "-" exp_u
             | "+" exp_u '''
    
def p_param(p):
	'param : declaracao'
	p[0] = [p[1]]

def p_params(p):
	'''params : param ',' params
			  | param 
			  | empty '''
	if len(p) > 2:
		if not p[3]:
			p[3] = []
		if p[2] == ',':
			p[0] = p[1] + p[3]
	else:
		if not p[1]:
			p[1] = []
		else:
			p[0] = p[1]
def p_retorna(p):
    'retorna : RETORNA expressao'

def p_imprime(p):
    'imprime : IMPRIME expressao'

def p_op_aum(p):
    '''op_aum : MAISIG 
              | MENOSIG 
              | MULTIG 
              | DIVIG 
              | MODIG 
              | EXPIG '''

def p_exp_m(p):
	'''exp_m : exp_u 
	         | exp_m '*' exp_u 
	         | exp_m DIVINT exp_u 
	         | exp_m '/' exp_u'''

def p_exp_a(p):
	'''exp_a : exp_m 
	         | exp_a '+' exp_m 
	         | exp_a '-' exp_m'''

def p_exp_ou(p):
	'''exp_ou : exp_e 
	          | exp_ou OU exp_e'''

def p_exp_e(p):
	'''exp_e : exp_nao 
	         | exp_e E exp_nao'''

def p_exp_nao(p):
	'''exp_nao : exp_a 
               | '!' exp_nao'''
               
def p_suite(p):
	'''suite : afirmacao
	         | afirmacao NOVALINHA suite
	         | NOVALINHA suite
	         | empty'''
	         
def p_suite_sem_retorno(p):
	'''suite_sem_retorno : afirmacao_sem_retorno
	         | afirmacao_sem_retorno NOVALINHA suite_sem_retorno
	         | NOVALINHA suite_sem_retorno
	         | empty'''
	         
def p_afirmacao(p):
	'''afirmacao : afirm_simples 
	             | afirm_composto'''
	             
def p_afirmacao_sem_retorno(p):
	'''afirmacao_sem_retorno : afirm_simples_sem_retorno 
	             | afirm_composto'''

def p_afirm_simples(p):
	'''afirm_simples : atribuicao 
                     | atribuicao_aumentada 
                     | imprime 
                     | retorna 
		     | declaracao
                     | QUEBRA 
                     | CONTINUA'''
                     
def p_afirm_simples_sem_retorno(p):
	'''afirm_simples_sem_retorno : atribuicao 
                     | atribuicao_aumentada 
                     | imprime 
		     | declaracao
                     | QUEBRA 
                     | CONTINUA'''

def p_afirm_composto(p):
	'''afirm_composto : se 
	                  | enquanto 
	                  | para'''

def p_atribuicao_aumentada(p):
    'atribuicao_aumentada : ID op_aum valor'

def p_literal(p):
	'''literal : PALAVRA 
			   | INT 
			   | REAL'''
	if isinstance(p[1],type(1)):
		p[0] = 'int'
	elif isinstance(p[1],type(1.1)):
		p[0] = 'real'
	elif isinstance(p[1],type('bla')):
		p[0] = 'crt'
	

def p_error(p):
    if p:
        print("Erro de Sintaxe: '%s' encontrado" % p.value)
        print str(p.lineno)+": "+a[p.lineno-1]
        sys.exit(0)
    else:
        print("Syntax error at EOF")

def erro_semantico(string):
	print(string)
	sys.exit(0)
	
def busca_nome(string):
	for n in names:
		if string == names[n]['valor']:
			return n
			
	erro_semantico("nome "+string+" nao definido")
import ply.yacc as yacc
yacc.yacc()

for linha in a:
	entrada += linha

yacc.parse(entrada)
lexer.input(entrada)
print("Programa sem erros")
print names
#print pilha
#print lexer.token()
#while True:
#    tok = lexer.token()
#    if not tok: break      # No more input
#    print tok
