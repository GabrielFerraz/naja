entrada = [('tipo', 'int'), ('identificador', 'x'), ('$','$')]
proximo = entrada.pop(0)
pilha = ["P"]
m = {"P":{"tipo":"D", "$":"$"}, "D":{"tipo":"I T"}, "T":{"tipo":"tipo"}, "I":{"identificador":"identificador"}}
terminais = ["tipo","identificador"]
nao_terminais = ["P","D","T","I"]
x = pilha[-1]
while x != "$":
	if x in terminais:
		if x == proximo[0]:
			pilha.pop(-1)
			x = pilha[-1]
			proximo = entrada.pop(0)
		else:
			print "Erro de Sintaxe"
	elif x in nao_terminais:
		if pilha[-1] != "P":
			pilha.pop(-1)
		for i in m[x][proximo[0]].split(" "):
			pilha.append(i)
		x = pilha[-1]
	else:
		print "Erro de Sintaxe"
if proximo[0] != "$":
	print "Erro de Sintaxe"
print "funfou"


