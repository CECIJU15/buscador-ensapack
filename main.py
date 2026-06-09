from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import sqlite3

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def inicio():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Buscador ENSAPACK</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 100px;
            }

            input {
                width: 350px;
                padding: 10px;
                font-size: 16px;
            }

            button {
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>

        <h1>Buscador ENSAPACK</h1>

        <form action="/buscar_web" method="get">
            <input
                type="text"
                name="codigo"
                placeholder="Ingrese código"
                required
            >
            <button type="submit">Buscar</button>
        </form>

    </body>
    </html>
    """

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


@app.get("/buscar_web", response_class=HTMLResponse)
def buscar_web(codigo: str):

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
        return f"""
        <html>
        <body style="font-family:Arial;text-align:center;margin-top:100px;">
            <h2>Código encontrado</h2>

            <p><b>Código:</b> {codigo}</p>
            <p><b>Archivo:</b> {data[0]}</p>
            <p><b>ID:</b> {data[1]}</p>

            <br>
            <a href="/">Nueva búsqueda</a>
        </body>
        </html>
        """

    return f"""
    <html>
    <body style="font-family:Arial;text-align:center;margin-top:100px;">
        <h2>Código no encontrado</h2>

        <p>{codigo}</p>

        <br>
        <a href="/">Volver</a>
    </body>
    </html>
    """