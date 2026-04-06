from hashlib import sha256

def hashear(secuencia):
    encode = secuencia.encode("utf-8")
    return sha256(encode).hexdigest()

def construir_secuencia(cont):
    # Construye la secuencia de 10 digitos con ceros a la izquierda a partir de un contador
    contador = cont
    secuencia = ("0"*(10-len(str(contador)))+str(contador))
    return secuencia

def fuerza_bruta(hash_obj):
    hash = ""
    cont = 0
    secuencia = ""
    # Recorre todas las secuencias posibles hasta encontrar el hash objetivo
    while (hash != hash_obj and cont <= 9999999999):
        secuencia = construir_secuencia(cont)
        hash = hashear(secuencia)
        cont += 1
    if hash == hash_obj:
        return secuencia
    return None


def main():
    print("\n======================== DETECTANDO HASHES ANDO ========================\n")

    while True:
        hash_objetivo = input("Ingrese el hash objetivo: ").strip()
        if not hash_objetivo:
            print("El hash no puede estar vacio.")
            continue
        break

    secuencia = fuerza_bruta(hash_objetivo)

    if secuencia is None:
        print("No se encontro una secuencia para ese hash en el rango permitido.")
    else:
        print(f"\nSecuencia = {secuencia}\n")


if __name__ == "__main__":
    main()