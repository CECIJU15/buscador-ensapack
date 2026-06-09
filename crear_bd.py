import os
import csv
import sqlite3

conn = sqlite3.connect("ensapack.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS codigos(
    codigo TEXT PRIMARY KEY,
    archivo TEXT,
    id_original INTEGER
)
""")

total = 0

ruta = "ENSAPACK"

for archivo in os.listdir(ruta):

    if not archivo.endswith(".csv"):
        continue

    ruta_csv = os.path.join(ruta, archivo)

    print("Leyendo:", archivo)

    with open(ruta_csv, encoding="utf-8-sig", newline="") as f:

        reader = csv.DictReader(f)

        filas = []

        for row in reader:
            filas.append((
                row["CAMPO"].strip(),
                archivo,
                int(row["ID"])
            ))

        cur.executemany("""
        INSERT OR IGNORE INTO codigos
        (codigo, archivo, id_original)
        VALUES (?,?,?)
        """, filas)

        total += len(filas)

        conn.commit()

cur.execute("""
CREATE INDEX IF NOT EXISTS idx_codigo
ON codigos(codigo)
""")

conn.commit()
conn.close()

print("Total registros:", total)