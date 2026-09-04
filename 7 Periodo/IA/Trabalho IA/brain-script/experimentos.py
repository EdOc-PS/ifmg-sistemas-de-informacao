
from dataset import carregar_dados, verificar_estrutura
from modelos import criar_mlp, criar_transformer
from metricas import avaliar_e_salvar

# Quantas épocas treinar cada modelo
EPOCAS = 20

EXPERIMENTOS = [
    ("Exp1", "MLP", "base (neuronios=128, dropout=0.3)",
     lambda: criar_mlp(neuronios=128, dropout=0.3)),
    ("Exp2", "MLP", "mais neuronios=256",
     lambda: criar_mlp(neuronios=256, dropout=0.3)),
    ("Exp3", "MLP", "dropout alto=0.5 (anti-overfit)",
     lambda: criar_mlp(neuronios=128, dropout=0.5)),
    ("Exp4", "MLP", "regularizacao L2=0.001 (anti-overfit)",
     lambda: criar_mlp(neuronios=128, dropout=0.3, l2=0.001)),
    ("Exp5", "Transformer", "base (dim=64, heads=4, blocos=4, dropout=0.1)",
     lambda: criar_transformer(dim=64, num_heads=4, num_blocos=4, dropout=0.1)),
    ("Exp6", "Transformer", "maior dim=128",
     lambda: criar_transformer(dim=128, num_heads=4, num_blocos=4, dropout=0.1)),
    ("Exp7", "Transformer", "mais heads=8",
     lambda: criar_transformer(dim=64, num_heads=8, num_blocos=4, dropout=0.1)),
    ("Exp8", "Transformer", "dropout alto=0.3 (anti-overfit)",
     lambda: criar_transformer(dim=64, num_heads=4, num_blocos=4, dropout=0.3)),
]

def rodar_experimentos():
    verificar_estrutura()
    train_data, test_data = carregar_dados()

    for nome, tecnica, descricao, criar_modelo in EXPERIMENTOS:
        print(f"\n{'='*60}")
        print(f"  {nome} | {tecnica} | {descricao}")
        print(f"{'='*60}")

        modelo = criar_modelo()
        modelo.fit(train_data, epochs=EPOCAS, verbose=1)
        avaliar_e_salvar(nome, tecnica, descricao, modelo, test_data)

    print("\nTodos os experimentos concluídos! Veja 'resultados.csv'.")


if __name__ == "__main__":
    rodar_experimentos()
