import json

from ml.AmbiguityDetector import AmbiguityDetector
from ml.Hyperparameters import Hyperparameters
from ml.LayerParameter import LayerParameter

if __name__ == "__main__":
    model = AmbiguityDetector()
    model.setupWithDefaultValues("./data/sarcasm.json")

    layerParameters = [
        LayerParameter(24, "relu")
    ]

    model.createModel(layerParameters)
    model.load()

    words = "former versace store clerk sues over secret 'black code' for minority shoppers"
    print(model.detect([words]))

