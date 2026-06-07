import json

def top3():

    banco = open("log.dat", "r")
    dados = banco.read()
    banco.close()

    if dados == "":
        return []

    dadosDict = json.loads(dados)

    ranking = []

    for nome, info in dadosDict.items():

        pontos = info[0]
        data = info[1]
        hora = info[2]

        ranking.append(
            (
                nome,
                pontos,
                data,
                hora
            )
        )

    ranking.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return ranking[:3]