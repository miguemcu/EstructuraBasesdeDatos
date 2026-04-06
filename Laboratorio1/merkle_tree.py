# CLASE DE APOYO PARA EL PROBLEMA 2

import hashlib

class MerkleTree:
    
    def __init__(self, leaves1):
        self.root = ""
        self.leaves1 = leaves1
        self.leaves2 = []

    
    def hashear(self, dato):
        encode = dato.encode('utf-8')
        return hashlib.sha256(encode).hexdigest()
    
    def construir(self):
        for t in range(len(self.leaves1)):
            self.leaves1[t] = self.hashear(self.leaves1[t])
            
        i = 0
        while (len(self.leaves1) > 1):
            if (i > (len(self.leaves1)-1)):
                    self.leaves1 = self.leaves2
                    self.leaves2 = []
                    i = 0
                    
            if (i%2 == 0):
                hash_l = self.leaves1[i]
                if (len(self.leaves1) > i+1):
                    hash_r = self.leaves1[i+1]
                    self.leaves2.append(self.hashear(hash_l+hash_r))
                else:
                    self.leaves2.append(hash_l)
                    
            i = i+1
            
        self.root = self.leaves2[0]
        return self.root