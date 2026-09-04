import os

from tensorflow.keras.preprocessing.image import ImageDataGenerator

from config import CLASSES, TRAIN_DIR, TEST_DIR, IMG_SIZE, BATCH_SIZE, SEED


def verificar_estrutura():
    print("Verificando estrutura do dataset...\n")

    for split, path in [("Training", TRAIN_DIR), ("Testing", TEST_DIR)]:
        if not os.path.exists(path):
            print(f"Pasta nao encontrada: {path}")
            continue

        print(f"{split}/")
        total = 0
        for classe in CLASSES:
            class_path = os.path.join(path, classe)
            if os.path.exists(class_path):
                qtd = len(os.listdir(class_path))
                total += qtd
                print(f"   {classe}: {qtd} imagens")
            else:
                print(f"   {classe}: nao encontrada")
        print(f"   Total: {total} imagens\n")


def carregar_dados():
    print("Carregando dados...\n")

    # deixa os pixels entre 0 e 1 em vez de 0 a 255
    datagen = ImageDataGenerator(rescale=1.0 / 255.0)

    # carrega as imagens de treino embaralhadas
    train_data = datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        classes=CLASSES,
        seed=SEED,
        shuffle=True,
    )

    # carrega as imagens de teste sem embaralhar
    test_data = datagen.flow_from_directory(
        TEST_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        classes=CLASSES,
        seed=SEED,
        shuffle=False,
    )

    print(f"Classes: {train_data.class_indices}")
    print(f"Batches de treino: {len(train_data)}")
    print(f"Batches de teste : {len(test_data)}")

    return train_data, test_data


if __name__ == "__main__":
    verificar_estrutura()
    train_data, test_data = carregar_dados()
    print("\nDataset carregado com sucesso!")
