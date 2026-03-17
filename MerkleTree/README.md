# Merkle Tree

Aquí implementé el Merkle Tree con SHA-256 a partir de transacciones simples (t1 a t7).

- `merkle_tree.py`: este fue el Merkle Tree que hice. Lo construyo de forma iterativa con una clase y voy combinando hashes por niveles hasta obtener la raíz.
- `MekleTest.py`: este lo hice después junto con la IA, pero manual por niveles, solo para comprobar que el resultado del árbol principal estuviera bien.

En ambos casos, cuando hay un número impar de nodos en un nivel, el último sube directo sin duplicarse.
