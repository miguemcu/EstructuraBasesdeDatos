import itertools

fila = b"01" * (100000//2)

with open("matriz.bin", "wb") as f:
    f.writelines(itertools.repeat(fila + b"\n", 100000))
