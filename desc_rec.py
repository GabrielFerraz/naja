entrada = [('tipo', 'int'), ('identificador', 'x'), ('identificador', 'x'), ("=", "="), ('identificador', 'c'),('$','$')]
proximo = 0
pilha = ["P"]
m = {"P":{"tipo":"D","identificador":"A","$":"$"}, "D":{"tipo":"T I"},
	"T":{"tipo":"tipo"}, "I":{"identificador":"identificador"}, "A":{"id":"I = I"}}
terminais = ["tipo","identificador","="]
nao_terminais = ["P","D","T","I","A"]
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
            print "entrada", entrada[proximo][0]
            if elemento in nao_terminais:
                if not parser(m[elemento]):
                    break
            elif elemento in terminais and elemento == entrada[proximo][0]:
                print "proximo"
                proximo += 1
                if len(nt_atual) == (proximo - inicio):
                    return True
            else:
                break
        if entrada[proximo][0] == "$":
            print "ACHOU FIM DE CADEIA", nt_atual
            return True
    else:
        if nt_atual == m["P"]:
            return parser(m["P"])
        else:
            return False

    
print parser(m["P"])
