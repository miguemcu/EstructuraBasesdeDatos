import hashlib

def calcular_hash(dato):
    return hashlib.sha256(dato.encode('utf-8')).hexdigest()

# 7 transacciones
txs = ["t1","t2","t3","t4","t5","t6","t7"]

# -------- NIVEL 0 (hojas) --------
h1 = calcular_hash(txs[0])
h2 = calcular_hash(txs[1])
h3 = calcular_hash(txs[2])
h4 = calcular_hash(txs[3])
h5 = calcular_hash(txs[4])
h6 = calcular_hash(txs[5])
h7 = calcular_hash(txs[6])

# -------- NIVEL 1 --------
h12 = calcular_hash(h1 + h2)
h34 = calcular_hash(h3 + h4)
h56 = calcular_hash(h5 + h6)
# h7 sube directo (no se duplica)

# -------- NIVEL 2 --------
h1234 = calcular_hash(h12 + h34)
h567 = calcular_hash(h56 + h7)

# -------- NIVEL 3 (raíz) --------
root = calcular_hash(h1234 + h567)

print("Raíz del Merkle Tree:")
print(root)
