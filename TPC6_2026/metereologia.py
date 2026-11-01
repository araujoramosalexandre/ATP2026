import matplotlib.pyplot as plt

def menu(lista):
    for op in lista:
        print(op)

menuOpcoes = [
    "(1) - Carregar tabela de ficheiro",
    "(2) - Guardar tabela em ficheiro",
    "(3) - Adicionar registo à tabela",
    "(4) - Listar tabela",
    "(5) - Temperatura média",
    "(6) - Temperatura mínima mais baixa",
    "(7) - Dia de maior precipitação",
    "(8) - Dias chuvosos",
    "(9) - Maior período consecutivo de dias secos",
    "(10) - Amplitude térmica",
    "(11) - Gerar gráficos meteorológicos",
    "(0) - Sair"
]

def carregaTabMeteo(fnome):
    f = open(fnome)
    res = []
    for linha in f:
        campos = linha.split(",")
        data = campos[0].split("|")
        res.append(((int(data[0]), int(data[1]), int(data[2])), float(campos[1]), float(campos[2]), float(campos[3])))  
    f.close()
    return res

def guardaTabMeteo(t, fnome):
    f = open(fnome, "w")
    for registo in t:
        f.write(f"{registo[0][0]}|{registo[0][1]}|{registo[0][2]},{registo[1]},{registo[2]},{registo[3]}\n")
    f.close()

def medias(tabMeteo):
    res = []
    for elem in tabMeteo:
        res.append((elem[0], (elem[1] + elem[2]) / 2))
    return res

def minMin(tabMeteo):
    min_val = tabMeteo[0][1]
    for registo in tabMeteo[1:]:
        if registo[1] < min_val:
            min_val = registo[1]
    return min_val

def maxChuva(tabMeteo):
    max_data = tabMeteo[0][0]
    max_prec = tabMeteo[0][3]
    for registo in tabMeteo[1:]:
        if registo[3] > max_prec:
            max_data = registo[0]
            max_prec = registo[3]
    return (max_data, max_prec)

def diasChuvosos(tabMeteo, p):
    res = []
    for registo in tabMeteo:
        if registo[3] > p:
            res.append((registo[0], registo[3]))
    return res

def maxPeriodoCalor(tabMeteo, p):
    max_dias = 0
    atual = 0
    for registo in tabMeteo:
        if registo[3] < p:
            atual = atual + 1
            if atual > max_dias:
                max_dias = atual
        else:
            atual = 0
    return max_dias

def amplTerm(tabMeteo):
    res = []
    for registo in tabMeteo:
        res.append((registo[0], registo[2] - registo[1]))
    return res 

def grafTabMeteo(t):
    datas = [f"{r[0][0]}/{r[0][1]}/{r[0][2]}" for r in t]
    tmin = [r[1] for r in t]
    tmax = [r[2] for r in t]
    prec = [r[3] for r in t]
    
    plt.figure(figsize=(10, 4))
    plt.plot(datas, tmax, label="Temp Máxima (ºC)", color="red", marker="o")
    plt.plot(datas, tmin, label="Temp Mínima (ºC)", color="blue", marker="o")
    plt.xlabel("Datas")
    plt.ylabel("Temperatura (ºC)")
    plt.title("Temperaturas Mínima e Máxima")
    plt.legend()
    plt.grid(True)
    plt.show()
    
    plt.figure(figsize=(10, 4))
    plt.bar(datas, prec, color="cyan", edgecolor="black")
    plt.xlabel("Datas")
    plt.ylabel("Precipitação (mm)")
    plt.title("Precipitação por Dia")
    plt.grid(True)
    plt.show()
    return

tabMeteo = [((2022,1,20), 2, 16, 0), ((2022,1,21), 1, 13, 0.2), ((2022,1,22), 7, 17, 0.01)]

if __name__ == "__main__":
    op = ""
    while op != '0':
        print("\n--- MENU METEOROLOGIA ---")
        menu(menuOpcoes)
        op = input("\nQual a opção pretendida? ")
        
        if op == '1':
            ficheiro = input("Introduza o nome do ficheiro a carregar: ")
            tabMeteo = carregaTabMeteo(ficheiro)
            print("Tabela carregada com sucesso!")
            print(tabMeteo)
                
        elif op == '2':
            ficheiro = input("Introduza o nome do ficheiro para guardar: ")
            guardaTabMeteo(tabMeteo, ficheiro)
            print("Tabela guardada com sucesso!")
            print(tabMeteo)
            
        elif op == '3':
            ano = int(input("Ano: "))
            mes = int(input("Mês: "))
            dia = int(input("Dia: "))
            tmin = float(input("Temperatura Mínima: "))
            tmax = float(input("Temperatura Máxima: "))
            prec = float(input("Precipitação: "))
            registo = ((ano, mes, dia), tmin, tmax, prec)
            tabMeteo.append(registo)
            print("Registo adicionado com sucesso!")
            print(tabMeteo)
            
        elif op == '4':
            print(tabMeteo)
                
        elif op == '5':
            m = medias(tabMeteo)
            print("\nTemperaturas Médias por dia:")
            for r in m:
                print(f"Data {r[0]}: {r[1]}ºC")
                
        elif op == '6':
            minima = minMin(tabMeteo)
            print(f"\nA temperatura mínima mais baixa registada foi: {minima}ºC")
            
        elif op == '7':
            dia_max, prec_max = maxChuva(tabMeteo)
            print(f"\nDia de maior precipitação: {dia_max} com {prec_max}mm")
            
        elif op == '8':
            p = float(input("Introduza o limite de precipitação (mm): "))
            dias = diasChuvosos(tabMeteo, p)
            print(f"\nDias com precipitação superior a {p}mm:")
            for d in dias:
                print(f"Data {d[0]}: {d[1]}mm")
                
        elif op == '9':
            p = float(input("Introduza o limite de precipitação (mm) para considerar dia seco: "))
            periodo = maxPeriodoCalor(tabMeteo, p)
            print(f"\nMaior período consecutivo de dias secos (< {p}mm): {periodo} dias")

        elif op == '10':
            at = amplTerm(tabMeteo)
            print("\nAmplitude térmica por dia:")
            for r in at:
                print(f"Data {r[0]}: {r[1]}ºC")

        elif op == '11':
            grafTabMeteo(tabMeteo)
            print("\nGráficos gerados com sucesso!")
            
        elif op == '0':
            print("Saiu da aplicação. Até breve!")
        else:
            print("Opção inválida. Tente novamente.")