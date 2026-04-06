# Laboratorio 1

Esta carpeta contiene dos ejercicios de fuerza bruta y una clase de apoyo para arboles de Merkle

## Archivos

- `Problema1.py`: busca por fuerza bruta una secuencia numerica de 10 digitos cuyo hash SHA-256 coincida con el hash objetivo ingresado por el usuario
- `Problema2.py`: busca por fuerza bruta el orden de transacciones que genera un Merkle root objetivo ingresado por el usuario
- `merkle_tree.py`: implementacion de apoyo de la clase `MerkleTree` usada en el problema 2

## Entradas esperadas

### Problema 1

- Hash objetivo (texto no vacio)

### Problema 2

- Cantidad de transacciones (entero mayor que 0)
- Transacciones (una por una, texto no vacio)
- Root objetivo (texto no vacio)

## Nota

Ambos programas usan enfoque de fuerza bruta, por lo que el tiempo de ejecucion puede crecer bastaaaante segun el caso
