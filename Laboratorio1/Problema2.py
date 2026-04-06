from merkle_tree import MerkleTree
import itertools

def reordenar(transacciones):
    ordenes = list(itertools.permutations(transacciones))
    return ordenes

def fuerza_bruta(ordenes, root_obj):
    i = 0
    root = ""
    while root != root_obj and i < len(ordenes):
        tree = MerkleTree(list(ordenes[i]))
        root = tree.construir()
        i += 1
    if root == root_obj:
        orden_correcto = list(ordenes[i - 1])
        return orden_correcto
    return None
        
def pedir_transacciones():
    while True:
        try:
            cantidad = int(input("Ingrese la cantidad de transacciones: "))
            if cantidad <= 0:
                print("La cantidad debe ser mayor que 0.")
                continue
            break
        except ValueError:
            print("Ingrese un numero entero valido.")

    transacciones = []
    for i in range(cantidad):
        while True:
            transaccion = input(f"Transaccion {i + 1}: ").strip()
            if not transaccion:
                print("La transaccion no puede estar vacia.")
                continue
            transacciones.append(transaccion)
            break
    return transacciones


def main():
    transacciones = pedir_transacciones()
    
    while True:
        root_objetivo = input("Ingrese el root objetivo: ").strip()
        if not root_objetivo:
            print("El root objetivo no puede estar vacio.")
            continue
        break
        
    ordenes = reordenar(transacciones)
    orden_correcto = fuerza_bruta(ordenes, root_objetivo)

    if orden_correcto is None:
        print("No se encontro un orden de transacciones que genere ese root.")
    else:
        print("Orden de transacciones encontrado:")
        print(orden_correcto)


if __name__ == "__main__":
    main()