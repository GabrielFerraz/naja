from estado import Estado, Automato

automatos = {}
#-------------------------- IDENTIFICADOR
estados = []
estados.append(Estado("q0", False))
estados.append(Estado("q1", False))
estados.append(Estado("q2", True))

estados[0].set_transicoes({"minusculo": estados[1],"maiusculo": estados[1],"_": estados[1]})
estados[1].set_transicoes({"minusculo": estados[1],"maiusculo": estados[1],"digito":estados[1],"_": estados[1],"outro":estados[2]})

automatos["identificador"] = Automato("identificador", estados, estados[0])


#-------------------------- COMENTARIO
estados = []
estados.append(Estado("q0", False))
estados.append(Estado("q1", False))
estados.append(Estado("q2", True))

estados[0].set_transicoes({"#": estados[1]})
estados[1].set_transicoes({"\n": estados[2],"outro":estados[1]})

automatos["comentario"] = Automato("comentario", estados, estados[0])


#-------------------------- STRING
estados = []
estados.append(Estado("q0", False))
estados.append(Estado("q1", False))
estados.append(Estado("q2", False))
estados.append(Estado("q3", True))
estados.append(Estado("erro", False))

estados[0].set_transicoes({"'": estados[1],'"':estados[2]})
estados[1].set_transicoes({"'": estados[3],"outro":estados[1],"\n": estados[4]})
estados[2].set_transicoes({'"': estados[3],"outro":estados[2],"\n": estados[4]})

automatos["string"] = Automato("string", estados, estados[0])


#--------------------------- OP LOGICO
estados = []
estados.append(Estado("q0", False))
estados.append(Estado("q1", False))
estados.append(Estado("q4", False))
estados.append(Estado("q7", False))
estados.append(Estado("q10", False))
estados.append(Estado("q13", False))
estados.append(Estado("q15", False))
estados.append(Estado("q2", True))
estados.append(Estado("q3", True))
estados.append(Estado("q5", True))
estados.append(Estado("q6", True))
estados.append(Estado("q8", True))
estados.append(Estado("q9", True))
estados.append(Estado("q11", True))
estados.append(Estado("q12", True))
estados.append(Estado("q14", True))
estados.append(Estado("q16", True))

estados[0].set_transicoes({"=": estados[1], "<": estados[4], ">": estados[7], "!": estados[10], "&": estados[13], "|": estados[15]})
estados[1].set_transicoes({"=": estados[2], "outro": estados[3]})
estados[4].set_transicoes({"=": estados[5], "outro": estados[6]})
estados[7].set_transicoes({"=": estados[8], "outro": estados[9]})
estados[10].set_transicoes({"=": estados[11], "outro": estados[12]})
estados[13].set_transicoes({"&": estados[14]})
estados[15].set_transicoes({"|": estados[16]})

automatos["logico"] = Automato("logico", estados, estados[0])


#--------------------------- OP MATEMATICO
estados = []
estados.append(Estado("q1", False))
estados.append(Estado("q4", False))
estados.append(Estado("q7", False))
estados.append(Estado("q8", False))
estados.append(Estado("q13", False))
estados.append(Estado("q15", False))
estados.append(Estado("q2", True))
estados.append(Estado("q3", True))
estados.append(Estado("q5", True))
estados.append(Estado("q6", True))
estados.append(Estado("q9", True))
estados.append(Estado("q10", True))
estados.append(Estado("q11", True))
estados.append(Estado("q12", True))
estados.append(Estado("q14", True))
estados.append(Estado("q16", True))
estados.append(Estado("q17", True))
estados.append(Estado("q18", True))

estados[0].set_transicoes({"+": estados[1], "-": estados[4], "*": estados[7], "/": estados[13]})
estados[1].set_transicoes({"=": estados[2], "outro": estados[3]})
estados[4].set_transicoes({"=": estados[5], "outro": estados[6]})
estados[7].set_transicoes({"*": estados[8], "=": estados[11], "outro": estados[12]})
estados[8].set_transicoes({"=": estados[9], "outro": estados[10]})
estados[13].set_transicoes({"|": estados[15], "=": estados[16], "outro": estados[14]})
estados[15].set_transicoes({"=": estados[17], "outro": estados[18]})

automatos["matematico"] = Automato("matematico", estados, estados[0])
