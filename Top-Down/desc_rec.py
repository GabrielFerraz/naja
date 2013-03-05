from gramatica import m

entrada = [('identificador', 'z'), ('=', '='), ('identificador', 'c'), ('+', '+'), ('int', '5'), ('$', '$')]


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

    if entrada[proximo][0] in nt_atual:
        for elemento in nt_atual[entrada[proximo][0]].split(" "):
            if elemento in nao_terminais:
                if parser(m[elemento]):
                    if (proximo - inicio) == len(nt_atual[entrada[inicio][0]].split(" ")):
                        return True
                else:
                    return False                    
            elif elemento == "e":
                continue
                
            elif elemento == entrada[proximo][0]:
                proximo += 1
                if (proximo - inicio) == len(nt_atual[entrada[proximo-1][0]].split(" ")):
                    return True
            else:
                return False
    else:
        return False

    if nt_atual == m["P"]:
       return parser(m["P"])
       
    return True   
print parser(m["P"])
