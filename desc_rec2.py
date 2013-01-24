from gramatica import m

entrada = [('tipo', 'int'), ('identificador', 'x'), ('identificador', 'z'), ('=', '='), ('int', '4'), ('+', '+'), ('int', '5'), ('$', '$')]


for i in range(0,len(entrada)):
    if entrada[i][0] in ["logico","aritmetico"]:
        entrada[i] = entrada[i][1], entrada[i][0]

proximo = 0
pilha = ["P"]
M = {"P":{"tipo":"D","identificador":"A","$":"$"}, "D":{"tipo":"T I"},
	"T":{"tipo":"tipo"}, "I":{"identificador":"identificador"}, "A":{"id":"I L I"}, "L":{"=":"="}}
terminais = ["tipo","identificador","="]
nao_terminais = [x for x in m]
terminais = ["+=","-=","*=","/=","%=","**=","=","tipo","int","identificador",
            "<",">","<=",">=","!", "!=","==","+","-","*","/","//","&&","||","e","$"]

x = pilha[-1]

def parser(nt_atual):
    global proximo
    inicio = proximo
    for producao in nt_atual:
        print nt_atual
        print "producao", producao
        proximo = inicio
        for elemento in nt_atual[producao].split(" "):
            print "elemento", elemento
            print "entrada", entrada[proximo]
            if elemento in nao_terminais:
                if not parser(m[elemento]):
                    break
                else:
                    if len(nt_atual[producao].split(" ")) == (proximo - inicio):
                        print "ENTROU <-----"
                        return True
            elif elemento in terminais and elemento == entrada[proximo][0]:
                print "proximo",proximo,inicio,nt_atual
                proximo += 1
                if len(nt_atual[producao].split(" ")) == (proximo - inicio):
                    print "ENTROU <-----"
                    return True 
            else:
                break
        if entrada[proximo][0] == "$":
            print "ACHOU FIM DE CADEIA", nt_atual
            return True
    else:
        for elemento in nt_atual:
            if "e" == elemento[0]:
                return True
    
        if nt_atual == m["P"]:
            return parser(m["P"])
        else:
            return False

    
print parser(m["P"])
