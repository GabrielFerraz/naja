from estado import Estado, Automato

automatos = {}
#-------------------------- IDENTIFICADOR
estados = []
estados.append(Estado("q0", False))
estados.append(Estado("q1", False))
estados.append(Estado("identificador", True))

estados[0].set_transicoes({"minusculo": estados[1],"maiusculo": estados[1],"_": estados[1]})
estados[1].set_transicoes({"minusculo": estados[1],"maiusculo": estados[1],"digito":estados[1],"_": estados[1],"outro":estados[2]})

automatos["identificador"] = Automato("identificador", estados, estados[0])


#-------------------------- COMENTARIO
estados = []
estados.append(Estado("q0", False))
estados.append(Estado("q1", False))
estados.append(Estado("comentario", True))

estados[0].set_transicoes({"#": estados[1]})
estados[1].set_transicoes({"\n": estados[2],"outro":estados[1]})

automatos["comentario"] = Automato("comentario", estados, estados[0])


#-------------------------- STRING
estados = []
estados.append(Estado("q0", False))
estados.append(Estado("q1", False))
estados.append(Estado("q2", False))
estados.append(Estado("q3", False))
estados.append(Estado("string", True))
estados.append(Estado("blibli", False))

estados[0].set_transicoes({"'": estados[1],'"':estados[2]})
estados[1].set_transicoes({"'": estados[3],"outro":estados[1],"\n": estados[5]})
estados[2].set_transicoes({'"': estados[3],"outro":estados[2],"\n": estados[5]})
estados[3].set_transicoes({"outro":estados[4]})

automatos["string"] = Automato("string", estados, estados[0])


#--------------------------- OP LOGICO
estados = []
estados.append(Estado("q0", False))
estados.append(Estado("q1", False))
estados.append(Estado("logico", False))
estados.append(Estado("logico", True))
estados.append(Estado("q4", False))
estados.append(Estado("logico", False))
estados.append(Estado("logico", True))
estados.append(Estado("q7", False))
estados.append(Estado("logico", False))
estados.append(Estado("logico", True))
estados.append(Estado("q10", False))
estados.append(Estado("logico", False))
estados.append(Estado("logico", True))
estados.append(Estado("q13", False))
estados.append(Estado("logico", False))
estados.append(Estado("q15", False))
estados.append(Estado("logico", False))

estados[0].set_transicoes({"=": estados[1], "<": estados[4], ">": estados[7], "!": estados[10], "&": estados[13], "|": estados[15]})
estados[1].set_transicoes({"=": estados[2], "outro": estados[3]})
estados[2].set_transicoes({"outro": estados[3]})
estados[4].set_transicoes({"=": estados[5], "outro": estados[6]})
estados[5].set_transicoes({"outro": estados[3]})
estados[7].set_transicoes({"=": estados[8], "outro": estados[9]})
estados[8].set_transicoes({"outro": estados[3]})
estados[10].set_transicoes({"=": estados[11], "outro": estados[12]})
estados[11].set_transicoes({"outro": estados[3]})
estados[13].set_transicoes({"&": estados[14]})
estados[14].set_transicoes({"outro": estados[3]})
estados[15].set_transicoes({"|": estados[16]})
estados[16].set_transicoes({"outro": estados[3]})

automatos["logico"] = Automato("logico", estados, estados[0])


#--------------------------- OP MATEMATICO
estados = []
estados.append(Estado("q0", False))
estados.append(Estado("q1", False))
estados.append(Estado("q2", False))
estados.append(Estado("aritmetico", True))
estados.append(Estado("q4", False))
estados.append(Estado("q5", False))
estados.append(Estado("aritmetico", True))
estados.append(Estado("q7", False))
estados.append(Estado("q8", False))
estados.append(Estado("q9", False))
estados.append(Estado("aritmetico", True))
estados.append(Estado("q11", False))
estados.append(Estado("aritmetico", True))
estados.append(Estado("q13", False))
estados.append(Estado("aritmetico", True))
estados.append(Estado("q15", False))
estados.append(Estado("q16", False))
estados.append(Estado("q17", False))
estados.append(Estado("aritmetico", True))

estados[0].set_transicoes({"+": estados[1], "-": estados[4], "*": estados[7], "/": estados[13]})
estados[1].set_transicoes({"=": estados[2], "outro": estados[3]})
estados[2].set_transicoes({"outro": estados[3]})
estados[4].set_transicoes({"=": estados[5], "outro": estados[6]})
estados[5].set_transicoes({"outro": estados[3]})
estados[7].set_transicoes({"*": estados[8], "=": estados[11], "outro": estados[12]})
estados[8].set_transicoes({"=": estados[9], "outro": estados[10]})
estados[9].set_transicoes({"outro": estados[3]})
estados[11].set_transicoes({"outro": estados[3]})
estados[13].set_transicoes({"/": estados[15], "=": estados[16], "outro": estados[14]})
estados[15].set_transicoes({"=": estados[17], "outro": estados[18]})
estados[16].set_transicoes({"outro": estados[3]})
estados[17].set_transicoes({"outro": estados[3]})

automatos["aritmetico"] = Automato("aritmetico", estados, estados[0])


#--------------------------- NUMEROS
estados = []
estados.append(Estado("q0", False))
estados.append(Estado("q1", False))
estados.append(Estado("int", True))
estados.append(Estado("q3", False))
estados.append(Estado("q4", False))
estados.append(Estado("hexa", True))
estados.append(Estado("q6", False))
estados.append(Estado("int", True))
estados.append(Estado("q8", False))
estados.append(Estado("q9", False))
estados.append(Estado("real", True))
estados.append(Estado("real", True))
estados.append(Estado("q12", False))

estados[0].set_transicoes({"0": estados[1], "naozero": estados[6],".": estados[12]})
estados[1].set_transicoes({"outro": estados[2], "x": estados[3],"X": estados[3],".": estados[8],"0": estados[1]})
estados[3].set_transicoes({"hexamin": estados[4], "hexamai": estados[4],"digito": estados[4]})
estados[4].set_transicoes({"hexamin": estados[4], "hexamai": estados[4],"digito": estados[4],"outro": estados[5]})
estados[6].set_transicoes({"digito": estados[6],"outro": estados[7],".": estados[8]})
estados[8].set_transicoes({"digito": estados[9],"outro": estados[11]})
estados[9].set_transicoes({"digito": estados[9],"outro": estados[10]})
estados[12].set_transicoes({"digito": estados[9]})

automatos["numero"] = Automato("numero", estados, estados[0])
