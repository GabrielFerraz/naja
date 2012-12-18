from automatos import automatos
from simbolos import simbolos
import sys

arquivo = open("entrada.txt", "a")
arquivo.write(" ")
arquivo.close
arquivo = open("entrada.txt", "r")
automato = ""
chave = ""
pares = []
erro = False
numero_linha = 0

for linha in arquivo.readlines():
	numero_linha += 1
	i = 0
	while i < len(linha):
		entrada = linha[i]
		
		if automato == "":
			if entrada in [" ","\n"]:
				i += 1
				continue
			if entrada == "#":
				automato = automatos["comentario"]
			elif entrada in ["+","-","*","/"]:
				automato = automatos["aritmetico"]
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
			elif entrada == ":":
				pares.append("doispontos", ":")

		try:
			automato.proximo(entrada)
			if entrada not in [" ","\n"]:
				if not automato.fim():
					chave += entrada
				else:
					i -= 1

		except:
			print "Erro de sintaxe! linha", numero_linha, ">>", chave
			erro = True
			break

		if automato.fim():
			if chave in simbolos:
				pares.append((simbolos[chave], chave))
			else:
				pares.append((str(automato), chave))
			automato.inicializa()
			automato = ""
			chave = ""
		
		i += 1

	if erro:
		break
	
arquivo.close()
arquivo = file("saida.txt", "w")
arquivo.write(str(pares))
print pares
