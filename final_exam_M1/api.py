from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tensorflow.keras.models import load_model
import numpy as np
from typing import List
import uvicorn


def load_and_predict(state):
    model = load_model("ia_morpion.h5")
    state_np = np.array(state).reshape(1, 9)
    prediction = model.predict(state_np)[0]  # Probabilités pour les 9 coups

    # 🔒 Filtrer les coups invalides
    available_moves = [i for i, val in enumerate(state) if val == 0]
    # Mettre les probabilités des coups invalides à -1
    filtered_probs = [prediction[i] if i in available_moves else -1 for i in range(9)]

    move = int(np.argmax(filtered_probs))
    return move


# Schéma de requête
class BoardRequest(BaseModel):
    board: List[int]

# Initialisation FastAPI
app = FastAPI()

# Permettre les requêtes depuis le frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["http://localhost:3000"] en dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/predict")
def predict(data: BoardRequest):
    move = load_and_predict(data.board)  # 👈 ici tu dois passer data.board
    return {"proposed_move": int(move)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
