fila0, fila1 = "",""

with open("matriz_escrita.txt", "w", encoding='utf-8') as f:
    for _ in range(100000):
        fila0 += "0"
        fila1 += "1"
    
    for _ in range(100000//2):
        f.write(fila0+"\n" + fila1+"\n")