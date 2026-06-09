from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/")
def home():
    return {"estado": "activo"}

@app.get("/buscar")
def buscar(codigo: str):

    conn = sqlite3.connect("ensapack.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT archivo, id_original
        FROM codigos
        WHERE codigo = ?
    """, (codigo,))

    data = cur.fetchone()
    conn.close()

    if data:
        return {
            "codigo": codigo,
            "archivo": data[0],
            "id_original": data[1]
        }

    return {"error": "No encontrado"}