import csv
import os
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from config import CSV_RESULTADOS

COLUNAS = ["experimento", "tecnica", "descricao", "acuracia", "precisao", "recall", "f_score"]


def avaliar(modelo, test_data):
    
    test_data.reset()
    y_pred = np.argmax(modelo.predict(test_data, verbose=0), axis=1)
    y_true = test_data.classes 

    return {
        # total de acertos
        "acuracia": accuracy_score(y_true, y_pred),
        # de tudo que o modelo disse ser tumor X, quantos realmente eram?
        "precisao": precision_score(y_true, y_pred, average="macro", zero_division=0),
        # de todos os tumores X que existiam, quantos o modelo encontrou?
        "recall":   recall_score(y_true, y_pred, average="macro", zero_division=0),
        # media entre precisao e recall
        "f_score":  f1_score(y_true, y_pred, average="macro", zero_division=0),
    }


def salvar_csv(experimento, tecnica, descricao, metricas):
    # cria o arquivo csv
    novo = not os.path.exists(CSV_RESULTADOS)

    with open(CSV_RESULTADOS, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUNAS)
        if novo:
            writer.writeheader()
        writer.writerow({
            "experimento": experimento,
            "tecnica":     tecnica,
            "descricao":   descricao,
            "acuracia":    round(metricas["acuracia"], 4),
            "precisao":    round(metricas["precisao"], 4),
            "recall":      round(metricas["recall"], 4),
            "f_score":     round(metricas["f_score"], 4),
        })

    print(f"Resultado de '{experimento}' salvo em '{CSV_RESULTADOS}'")


def avaliar_e_salvar(experimento, tecnica, descricao, modelo, test_data):
    print(f"\n{experimento} | {tecnica} | {descricao}")
    metricas = avaliar(modelo, test_data)
    for nome, valor in metricas.items():
        print(f"  {nome}: {valor:.4f}")
    salvar_csv(experimento, tecnica, descricao, metricas)
    return metricas
