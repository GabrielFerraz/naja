import sys
from operator import itemgetter

#------------------------{ HELPERS }------------------------
def filtra_escopo(pilha):
    to_return = [0]
    for item in pilha:
        try:
            if item.value in ["se","def", "para"]:
                to_return.append(item.lexpos)
            elif item.value in ["senaose", "senao", "fim"]:
                to_return.pop()
                to_return.append(item.lexpos)
            
        except:
            pass
    return to_return

def verifica_tipo(varnome, vartype, pilha):
    varcodigo = get_codigo(varnome,pilha)
        
    if not varcodigo:
        return -1
    else:
        if vartype != get_tipo(names[varcodigo]):
            return -2
    return True

def get_codigo(varnome, pilha):
    
    for name in names:
        if varnome == names[name]['valor']:
            for item in reversed(filtra_escopo(pilha)):
                if names[name]['codigo'] == item:
                    return name
    return None

def get_tipo(valor):
    if valor in ["int", "crt", "bool", "real"]:
        return valor
    else:
        try:
            return valor['tipo']
        except:
            pass

#------------------------------------------------



if sys.version_info[0] >= 3:
    raw_input = input

entrada = ""
arquivo = open(sys.argv[1], "r")
a = arquivo.readlines()
saida = open(sys.argv[1].split('.')[0]+'.c','w')


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
	r'\d*\.\d+'
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
buffer = ""
bufferValor = []

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
	global buffer
	if buffer:
		saida.write(buffer)
		buffer = ''
	
def p_controle(p):
	'''controle : se 
                | enquanto 
                | para'''

def p_declaracao(p):
	'''declaracao : TIPO ID '''
	global buffer
	escopo = 0
	codigo = 0
	for a in p.stack:
		try:
			if a.value in ["def","se","senao","senaose","para","enquanto"]:
				codigo = a.lexpos
				if a.value not in ["senao","senaose"]:
					escopo += 1
		except:
			pass
			
	for name in names:
		if names[name]['valor'] == p[2] and names[name]['codigo'] == codigo:
			erro_semantico("Redefinicao de nome: '"+ p[2] +"'")
			
	names[p.lexpos(2)] = {"valor":p[2],"tipo":p[1],"escopo":escopo,'codigo':codigo}
	p[0] = p.lexpos(2)
	if p[1] == 'crt':
		buffer += 'char '
	elif p[1] == 'real':
		buffer += 'float '
	else:
		buffer += 'int '
	buffer += p[2]+';\n'
		
def p_empty(p):
	'empty : '
	pass

def p_senaosemais(p):
    '''senaosemais : senaose senaosemais
                   | empty '''

def p_senaose(p):
	'''senaose : SENAOSE expressao ':' suite '''
	if p[2] != "bool":
		erro_semantico("Expressao apos o Se invalida")
		
def p_senao(p):
    '''senao : SENAO ':' suite 
             | empty '''

def p_se(p):
	"se : SE expressao ':' suite senaosemais senao FIM "
	if p[2] != "bool":
		erro_semantico("Expressao apos o Se invalida")
		
def p_enquanto(p):
	"enquanto : ENQUANTO expressao ':' suite FIM "
	if p[2] != "bool":
		erro_semantico("Expressao apos o Se invalida")

def p_intid(p):
	'''intid : INT 
			 | ID '''
	if not isinstance(p[1], type(1)):
		erro = verifica_tipo(p[1], "int", p.stack);
		if erro == -1:
			erro_semantico("Variavel '"+ str(p[1]) +"' nao encontrada")
		 
		if erro == -2:
			erro_semantico("Loop ilegal:  'int' esperado, mas '"+ names[get_codigo(p[1], p.stack)]['tipo'] +"' encontrado")
			
			
def p_para(p):
	'''para : PARA ID DE intid ATE intid ':' suite FIM '''
	erro = verifica_tipo(p[2], "int", p.stack)

def p_definicao(p):
	'''definicao : DEF TIPO ID '(' params ')' ':' suite_sem_retorno retorna FIM
                 | DEF TIPO ID '(' params ')' ':' suite_sem_retorno retorna novalinha FIM'''
	if not p[5]:
		p[5] = []
	names[p.lexpos(3)] = {"valor":p[3],"tipo":p[2], "params":len(p[5]), "codigo":-1}
	for i in p[5]:
		names[i]["codigo"] = p.lexpos(3)
	if p[2] != p[9]:
		erro_semantico("Funcao retornando "+p[9]+". "+p[2]+" esperado")

def p_novalinha(p):
    '''novalinha : NOVALINHA
                | NOVALINHA novalinha'''
    
def p_defsubfuncao(p):
    '''defsubfuncao : DEF VAZIO ID '(' params ')' ':' suite FIM '''
    
def p_atribuicao_vetor(p):
    "atribuicao : ID '[' INT ']' '=' valor "
    
def p_atribuicao(p):
	"atribuicao : ID '=' valor "
	erro = verifica_tipo(p[1], get_tipo(p[3][0]), p.stack)
	if erro == -1:
		erro_semantico("Variavel '"+ p[1] +"' nao encontrada!")
	elif erro == -2:
		erro_semantico("Atribuicao ilegal: '"+ get_tipo(names[get_codigo(p[1], p.stack)]) +"' esperado, mas '"+get_tipo(p[3][0])+"' encontrado!")
	buffer = p[1]+" = "
    
def p_valorvalor(p):
	'''valorvalor : ',' valor valorvalor
				| empty '''
	if len(p) > 2:
		p[0] = p[2] + p[3]
	else:
		p[0] = []


def p_chamada(p):
	'''chamada : ID '(' valor valorvalor ')'
			   | ID '(' ')' '''
	p[0] = p[1]
	#	if len(p) > 4:
	#		if not p[4]:
	#			p[4] = 0
	chamada = busca_nome(p[1])
	parametros = []

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
				n = get_codigo(w,p.stack)
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
	if p[1] in ["Verdadeiro", "Falso"]:
		p[1] = 'bool'
	p[0] = [p[1]]
	bufferValor.append(p[1])
def p_comparacao(p):
	'''comparacao : valor
				  | valor operador_comp valor '''
	global buffer
	if len(p)>2:
		if p[1][0] in ['int','real','crt','bool']:
			v1 = p[1][0]
		else:
			v1 = names[busca_nome(p[1][0])]['tipo']
		if p[3][0] in ['int','real','crt','bool']:
			v2 = p[3][0]
		else:
			v2 = names[busca_nome(p[3][0])]['tipo']
		if p[2] in ['>=','<=']:
			if "crt" in [v1,v2]:
				erro_semantico('comparacao ilegal de caracteres')
		if v1 != v2:
			erro_semantico("Comparacao ilegal de "+v1+" com "+v2)
			
		p[0] = 'bool'
		buffer += bufferValor.pop(-2)+' '+p[2]+' '+bufferValor.pop()
	else:
		p[0] = p[1][0]
	
	
	
def p_operador_comp(p):
	'''operador_comp : '<' 
                     | '>' 
                     | IGUIG 
                     | MAIORIG 
                     | MENORIG 
                     | DIF '''
	p[0] = p[1]
	
def p_exponenciacao(p):
	'''exponenciacao : comparacao
					| comparacao EXP exp_u '''

	if len(p) > 2:
		if p[1] not in ['int', 'real'] or p[2] != 'int':
			erro_semantico("Operacao ilegal com exponenciacao.")

	p[0] = p[1]

def p_exp_u(p):
	'''exp_u : exponenciacao 
			 | "-" exp_u
			 | "+" exp_u '''

	if len(p) > 2:
		if p[2] not in ['int', 'real']:
			erro_semantico("Operacao ilegal com sinais")
		p[0] = p[2]
	else:
		p[0] = p[1]
	
def p_exp_m(p):
	'''exp_m : exp_u 
			 | exp_m '*' exp_u 
			 | exp_m DIVINT exp_u 
			 | exp_m '/' exp_u'''
			 
	if len(p) > 2:
		if p[1] not in ['real', 'int'] or p[3] not in ['real', 'int']:
			erro_semantico("Operacao aritmetica ilegal.") # <------------------------------- MUDAR ISSO AQUI!
			
		if p[2] == '//':
			p[0] = 'int'
		else:
			if "real" in [p[1],p[3]]:
				p[0] = "real"
			else:
				p[0] = "int"
	else:
		p[0] = p[1]
		
def p_exp_a(p):
	'''exp_a : exp_m 
			 | exp_a '+' exp_m 
			 | exp_a '-' exp_m'''
	if len(p) > 2:
		if p[1] not in ['real', 'int'] or p[3] not in ['real', 'int']:
			erro_semantico("Operacao aritmetica ilegal.") # <------------------------------- MUDAR ISSO AQUI!
		else:
			if "real" in [p[1],p[3]]:
				p[0] = "real"
			else:
				p[0] = "int"
	else:
		p[0] = p[1]
	
def p_exp_nao(p):
	'''exp_nao : exp_a 
			   | '!' exp_nao'''
	if p[1] == '!' and p[2] != "bool":
			erro_semantico("Operacao logica ilegal.") # <------------------------------- MUDAR ISSO AQUI!
	else:
		p[0] = p[1]

def p_exp_e(p):
	'''exp_e : exp_nao 
			 | exp_e E exp_nao'''
	if len(p) > 2:
		if p[1] != "bool" or p[3] != "bool":
			erro_semantico("Operacao logica ilegal.") # <------------------------------- MUDAR ISSO AQUI!
	else:
		p[0] = p[1]

def p_exp_e(p):
	'''exp_e : exp_nao 
			 | exp_e E exp_nao'''
	if len(p) > 2:
		if p[1] != "bool" or p[3] != "bool":
			erro_semantico("Operacao logica ilegal.") # <------------------------------- MUDAR ISSO AQUI!
	else:
		p[0] = p[1]

def p_exp_ou(p):
	'''exp_ou : exp_e 
			  | exp_ou OU exp_e'''
	if len(p) > 2:
		if p[1] != "bool" or p[3] != "bool":
			erro_semantico("Operacao logica ilegal.") # <------------------------------- MUDAR ISSO AQUI!
	else:
		p[0] = p[1]
		
def p_expressao(p):
	'expressao :  exp_ou' 
	p[0] = p[1]

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
	if p[2] not in ['int','real','crt','bool']:
			p[0] = names[busca_nome(p[2])]['tipo']
	else:
		p[0] = p[2]

def p_imprime(p):
    'imprime : IMPRIME expressao'

def p_op_aum(p):
    '''op_aum : MAISIG 
              | MENOSIG 
              | MULTIG 
              | DIVIG 
              | MODIG 
              | EXPIG '''

def p_atribuicao_aumentada(p):
	"atribuicao_aumentada : ID op_aum valor"
	if get_tipo(names[get_codigo(p[1], p.stack)]) in ['real', 'int']:
		erro = verifica_tipo(p[1], get_tipo(p[3][0]), p.stack)
		if erro == -1:
			erro_semantico("Variavel '"+ p[1] +"' nao encontrada!")
		elif erro == -2:
			erro_semantico("Atribuicao ilegal: '"+ get_tipo(names[get_codigo(p[1], p.stack)]) +"' esperado, mas '"+get_tipo(p[3][0])+"' encontrado!")
	else:
		erro_semantico("Atribuicao ilegal. Variavel do tipo "+get_tipo(names[get_codigo(p[1], p.stack)]))
		
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
print buffer
#print pilha
#print lexer.token()
#while True:
#    tok = lexer.token()
#    if not tok: break      # No more input
#    print tok
