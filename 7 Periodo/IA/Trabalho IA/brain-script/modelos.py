import tensorflow as tf
from tensorflow.keras import layers, models, regularizers

from config import IMG_SIZE, NUM_CLASSES

INPUT_SHAPE = (IMG_SIZE[0], IMG_SIZE[1], 3)


def criar_mlp(neuronios=128, dropout=0.3, l2=0.0):
    reg = regularizers.l2(l2) if l2 > 0 else None

    modelo = models.Sequential([
        layers.Input(shape=INPUT_SHAPE),
        layers.Flatten(),                # transforma a imagem em uma lista de numeros
        layers.Dense(neuronios, activation="relu", kernel_regularizer=reg),
        layers.Dropout(dropout),  
        layers.Dense(neuronios // 2, activation="relu", kernel_regularizer=reg),
        layers.Dropout(dropout),
        layers.Dense(NUM_CLASSES, activation="softmax"),  # probabilidade pra cada classe
    ], name="MLP")

    modelo.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    return modelo


def _bloco_transformer(x, num_heads, dim, dropout):
    # o modelo aprende quais partes da imagem importam mais
    norm1 = layers.LayerNormalization(epsilon=1e-6)(x)
    attn = layers.MultiHeadAttention(num_heads=num_heads, key_dim=dim, dropout=dropout)(norm1, norm1)
    x = layers.Add()([attn, x])

    # camada feed-forward para processar o resultado da atencao
    norm2 = layers.LayerNormalization(epsilon=1e-6)(x)
    ff = layers.Dense(dim * 2, activation="relu")(norm2)
    ff = layers.Dropout(dropout)(ff)
    ff = layers.Dense(dim)(ff)
    x = layers.Add()([ff, x])
    return x


def criar_transformer(patch_size=16, dim=64, num_heads=4, num_blocos=4, dropout=0.1):
    num_patches = (IMG_SIZE[0] // patch_size) * (IMG_SIZE[1] // patch_size)

    entradas = layers.Input(shape=INPUT_SHAPE)

    # divide a imagem em patches
    x = layers.Conv2D(dim, kernel_size=patch_size, strides=patch_size)(entradas)
    x = layers.Reshape((num_patches, dim))(x)

    # informa a posicao de cada patche
    posicoes = tf.range(start=0, limit=num_patches, delta=1)
    pos_embed = layers.Embedding(input_dim=num_patches, output_dim=dim)(posicoes)
    x = x + pos_embed

    # passa pelos blocos transformer onde acontece a atencao
    for _ in range(num_blocos):
        x = _bloco_transformer(x, num_heads, dim, dropout)

    # classifica com base no que aprendeu
    x = layers.LayerNormalization(epsilon=1e-6)(x)
    x = layers.GlobalAveragePooling1D()(x)
    x = layers.Dropout(dropout)(x)
    saidas = layers.Dense(NUM_CLASSES, activation="softmax")(x)

    modelo = models.Model(entradas, saidas, name="Transformer")
    modelo.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    return modelo


if __name__ == "__main__":
    print("MLP:")
    criar_mlp().summary()
    print("\nTransformer:")
    criar_transformer().summary()
