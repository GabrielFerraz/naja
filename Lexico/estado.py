def confere(tipo, entrada):
	if tipo == "minusculo":
		return "a" <= entrada <= "z"
	elif tipo == "maiusculo":
		return "A" <= entrada <= "Z"
	elif tipo == "digito":
		return "0" <= entrada <= "9"
	elif tipo == "naozero":
		return "1" <= entrada <= "9"
	elif tipo == "hexamin":
		return "a" <= entrada <= "f"
	elif tipo == "hexamai":
		return "F" <= entrada <= "F"
	else:
		return entrada == tipo

class Estado:
	
	def __init__(self, nome, final):
		self.nome = nome
		self.final = final
		self.transicoes = {}

	def __str__(self):
		return self.nome
		
	def set_transicoes(self, transicoes):
		self.transicoes = transicoes
	
	def	fim(self):
		return self.final
		
	def get_proximo(self, entrada):
		for tipo in self.transicoes.keys():
			if confere(tipo, entrada):
				#print tipo,"->",str(self.transicoes[tipo])
				return self.transicoes[tipo]
		
		if "outro" in self.transicoes.keys():
				#print "outro","->",str(self.transicoes["outro"])
				return self.transicoes["outro"]
			
		raise Exception("Proximo nao encontrado")

class Automato:
	
	def __init__(self, nome, estados, inicial):
		self.estados = estados
		self.inicial = inicial
		self.atual = inicial
		self.nome = nome

	def __str__(self):
		return str(self.atual)
		
	def get_nome(self):
		return self.nome
	
	def inicializa(self):
		self.atual = self.inicial

	def get_atual(self):
		return self.atual
		
	def proximo(self, entrada):
		self.atual = self.atual.get_proximo(entrada)
		
	def fim(self):
		return self.atual.fim()


if __name__ == "__main__":
	estados = []
	estados.append(Estado("q0", False))
	estados.append(Estado("q1", False))
	estados.append(Estado("q2", True))

	estados[0].set_transicoes({"#": estados[1]})
	estados[1].set_transicoes({"\n": estados[2],"outro":estados[1]})

	automato = Automato(estados, estados[0])
	#automatos["comentario"] = Automato(estados, estados[0])

