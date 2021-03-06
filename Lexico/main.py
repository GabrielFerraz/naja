from automatos import automatos
from simbolos import simbolos
import sys

arquivo = open(sys.argv[1], "r")
automato = ""
chave = ""
pares = []
numero_linha = 0
erro = False

a = arquivo.readlines()

for linha in a:
	if erro:
		break
		
	numero_linha += 1
	i = 0
	while i < len(linha):
		entrada = linha[i]
		
		if automato == "":
			if entrada in [" ","\t","\n"]:
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
				pares.append(("parentesis","("))
				break
			elif entrada == ")":
				pares.append(("parentesis",")"))
				break
			elif entrada == "[":
				pares.append(("colchete","["))
				break
			elif entrada == "]":
				pares.append(("colchete","]"))
				break
			elif entrada == ":":
				pares.append(("doispontos", ":"))
				break

		try:
			automato.proximo(entrada)
			if entrada not in [" ","\n"]:
				if not automato.fim():
					chave += entrada
				else:
					i -= 1
			elif entrada in [" ","\t"] and automato.get_nome() == "string":
				chave += entrada
				
		except:
			print "Erro de sintaxe! linha", str(numero_linha)+":"
			print linha + " " * (i-1) + "^" 
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

	
arquivo.close()
arquivo = file("saida.txt", "w")
arquivo.write(str(pares))
print pares
