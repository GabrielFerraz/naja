from automatos import automatos

arquivo = open("entrada.txt", "a")
arquivo.write("\n   ")
arquivo.close
arquivo = open("entrada.txt", "r")
automato = ""
chave = ""
pares = []

for linha in arquivo.readlines():

	for entrada in linha:
		if automato == "":
			if entrada in [" ","\n"]:
				continue
			if entrada == "#":
				automato = automatos["comentario"]
			elif entrada in ["+","-","*","/"]:
				automato = automatos["matematico"]
			elif entrada in ["=","<",">","!","&","|"]:
				automato = automatos["logico"]
			elif "0" <= entrada <= "9":
				automato = automatos["numero"]
			elif "A" <= entrada <= "Z" or "a" <= entrada <= "z" or entrada == "_":
				automato = automatos["identificador"]
			elif entrada == '"' or entrada == "'":
				automato = automatos["string"]
			elif entrada == "(":
				pares.append("parentesis","(")
			elif entrada == ")":
				pares.append("parentesis",")")
			elif entrada == "[":
				pares.append("colchete","[")
			elif entrada == "]":
				pares.append("colchete","]")

		try:
			automato.proximo(entrada)
			if entrada not in [" ","\n"]:
				chave += entrada
				print chave
		except:
			print "Erro de sintaxe!"

		if automato.fim():
			automato.inicializa()
			pares.append((automato.get_nome(), chave))
			automato = ""
			chave = ""
			
print pares