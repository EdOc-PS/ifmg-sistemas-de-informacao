import os

DATASET_PATH = "../brain-tumor-mri-dataset"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 42

CLASSES = ["glioma", "meningioma", "notumor", "pituitary"]
NUM_CLASSES = len(CLASSES)

TRAIN_DIR = os.path.join(DATASET_PATH, "Training")
TEST_DIR  = os.path.join(DATASET_PATH, "Testing")

CSV_RESULTADOS = "resultados.csv"
