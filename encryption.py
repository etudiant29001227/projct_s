from typing import Tuple
import random


class VigenereTable:
    #création de la table de vigenere sur la table ascii codé sur 256 
    def __init__(self):
        self.l = [chr(i) for i in range(256)]
        self.matrix = [self.l[i:]+self.l[:i] for i in range(len(self.l))]
 
    def __str__(self):
        return "\n".join('|'.join(row) for row in self.matrix)

    def encode(self, row, column):
        return self.matrix[ord(row)][ord(column)]
    
    def decode(self,row,column):
        decode_letter = self.matrix[ord(row)].index(column)
        return self.matrix[0][decode_letter]
    
    def VigenereCode(self,message,key,mode):
        message = list(message)
        key = list(key)
        matrix = VigenereTable()
        encrypted_message = []

        for i in range(len(message)):
            j = i%len(key)
            if(mode == 'c'):
                encrypted_message.append(matrix.encode(key[j],message[i]))
            elif(mode=='d'):
                encrypted_message.append(matrix.decode(key[j],message[i]))
            else:
                print('Bad argument for mode attribute.')
                break

        return ''.join(encrypted_message)
        


class Hill():
    
    def __init__(self,a,b,c,d):
        #La table de correspondance contenant les 256 caractères de la table ASCII
        self.table = [chr(i) for i in range(256)]
        self.matrix = [a,b,c,d]
        #Déterminant de la Matrix inverse
        self.det_inv = (self.xgcd((a*d)-(b*c),256)[1])+256
        self.matrix_inv = [d,-b,-c,a]
        if((self.pgcd((a*b-c*d),256)) == 1):
            self.valid_matrix = True
        else:
            self.valid_matrix = False
            
    def matrixIsValid(self):
        return self.valid_matrix
        
    def pgcd(self,a,b):
        if b==0:
            return a
        else:
            return self.pgcd(b,a%b)

    #Euclide étendu
    def xgcd(self,a: int, b: int) -> Tuple[int, int, int]:
        x0, x1, y0, y1 = 0, 1, 1, 0
        while a != 0:
            (q, a), b = divmod(b, a), a
            y0, y1 = y1, y0 - q * y1
            x0, x1 = x1, x0 - q * x1
        return b, x0, y0

    #chiffre le tuple
    def code_pair(self,l1,l2) -> Tuple[int, int]:
        a,b,c,d = self.matrix[0], self.matrix[1], self.matrix[2], self.matrix[3]
        cl1 = (l1*a+l2*b)%256
        cl2 = (l1*c+l2*d)%256
        return cl1, cl2
    #déchiffre le tuple
    def decode_pair(self,l1,l2) -> Tuple[int, int]:
        a,b,c,d = self.matrix_inv[0], self.matrix_inv[1], self.matrix_inv[2], self.matrix_inv[3]
        cl1 = (self.det_inv*(l1*a+l2*b))%256
        cl2 = (self.det_inv*(l1*c+l2*d))%256
        return cl1, cl2
    
    def code(self,message):
        
        message = list(message)
        while(len(message)%2 !=0):
            message.append('X')
        #Parcours le mot de 2 en 2
        for i in range(0,len(message),2):
            l1,l2 = message[i], message[i+1]
            code_tuple = self.code_pair(ord(l1),ord(l2))
            message[i] = chr(code_tuple[0])
            message[i+1] = chr(code_tuple[1])
            
        message = ''.join(message)
        return message
    
    def decode(self,message):
        message = list(message)
        
        for i in range(0,len(message),2):
            l1,l2 = message[i], message[i+1]
            code_tuple = self.decode_pair(ord(l1),ord(l2))
            message[i] = chr(code_tuple[0])
            message[i+1] = chr(code_tuple[1])
            
        message = ''.join(message)
        return message


class Transpositions_rect:
    
    def __init__(self):
        self.table = None
        
        
    def create_table_for_code(self,message,key):
        dic = {}
        key = list(key)
        message = list(message)
        
        for i in range(len(message)):
            j = i%len(key)
            if key[j] in dic:
                dic[key[j]].append(message [i])
            else:
                dic.update({key[j]:[message[i]]})
                
        max_elem = len(dic[key[0]])
        
        for key in dic.keys():
            while(len(dic[key])<max_elem):
                char = random.randint(ord('A'), ord('Z'))
                dic[key].append(chr(char))
        return dic
    
    def create_table_for_decode(self,message,key):
        dic = {}
        key = list(key)
        key.sort()
        
        message = list(message)
        step = int(len(message)/len(key))
        j = 0

        for i in range(0,len(message),step):
            dic.update({key[j]:message[i:i+step]})
            j+=1
        return dic
    
    def code(self,message,key):
        
        message = message.upper()
        key = key.upper()
        key = ''.join([j for i,j in enumerate(key) if j not in key[:i]])
        
        self.table = self.create_table_for_code(message.replace(' ',''),key)
        key_list = list(self.table.keys())
        key_list.sort()
        m = ""
        
        for k in key_list:
            m+= ''.join(self.table[k])
        return m
    
    def decode(self,message,key):
        
        message = message.upper()
        key = key.upper()
        key = ''.join([j for i,j in enumerate(key) if j not in key[:i]])
        
        self.table = self.create_table_for_decode(message.replace(' ',''),key)
        key_list = list(key)
        m = ""
        
        for i in range(len(self.table[key_list[0]])):
            for key in key_list:
                m+= self.table[key][i]
        return m


class DES:
    
    def __init__(self):
        self.binary_message = None
        
    def decimalToBinary(self,decimal):
        binary = [int(i) for i in list('{0:0b}'.format(decimal))]
        while len(binary)<8:
            binary = [0]+binary
        return binary
    
    def binaryToDecimal(self,binary):
        decimal = 0
        power = 0
        binary.reverse()
        
        for bit in binary:
            decimal+= 2**power*bit
            power+= 1
        return decimal

    def stringToBinary(self,message):
        binary_table = []
        for l in message:
            binary_table+= self.decimalToBinary(ord(l))
        self.binary_message = binary_table
        return binary_table
        
    def binaryToString(self,binary_table):
        message = ""
        for i in range(0,len(binary_table),8):
            decimal = self.binaryToDecimal(binary_table[i:i+8])
            message+= chr(decimal)
        print(message)
        return message
    
    def key_scheduler(self,bit):

        pc1 = [57, 49, 41, 33, 25, 17,  9,
                1, 58, 50, 42, 34, 26, 18,
               10,  2, 59, 51, 43, 35, 27,
               19, 11,  3, 60, 52, 44, 36,
               63, 55, 47, 39, 31, 23, 15,
                7, 62, 54, 46, 38, 30, 22,
               14,  6, 61, 53, 45, 37, 29,
               21, 13,  5, 28, 20, 12,  4]


        pc2 = [14, 17, 11, 24,  1,  5,
               3,  28, 15,  6, 21, 10,
               23, 19, 12,  4, 26,  8,
               16,  7, 27, 20, 13,  2,
               41, 52, 31, 37, 47, 55,
               30, 40, 51, 45, 33, 48,
               44, 49, 39, 56, 34, 53,
               46, 42, 50, 36, 29, 32]
        
        lrt = [1, 2, 3, 4, 5, 6, 7, 8,
               9, 10, 11, 12, 13, 14, 15,
               16,17,18,19,20,21,22,23,24,
               25,26,27,0]
        
        k_prime = []
        for number in pc1:
            k_prime.append(bit[number-1])
            
        lkey = k_prime[:28]
        rkey = k_prime[28:]
        
        l_keys = []
        r_keys = []
        
        #décalage à gauche
        for i in range(16):

            lkey = lkey[1:]+lkey[:1]
            l_keys.append(lkey)

            rkey = rkey[1:]+rkey[:1]
            r_keys.append(rkey)
    
    
        keys = []
        
        for i in range(16):
            cat = l_keys[i] + r_keys[i]
            temp = []
            for number in pc2:
                temp.append(cat[number-1])
            keys.append(temp)

        return keys

    def expansion(self,bit):

        e = [32,  1,  2,  3,  4,  5,
              4,  5,  6,  7,  8,  9,
              8,  9, 10, 11, 12, 13,
             12, 13, 14, 15, 16, 17,
             16, 17, 18, 19, 20, 21,
             20, 21, 22, 23, 24, 25,
             24, 25, 26, 27, 28, 29,
             28, 29, 30, 31, 32,  1]

        out = []
        for number in e:
            out.append(bit[number-1])

        return out


    def Sbox(self,bit):

        s = [
             # s1
             [[14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
              [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8],
              [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
              [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]],
             # s2
             [[15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
              [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
              [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
              [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9]],
             # s3
             [[10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
              [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
              [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
              [ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]],
             # s4
             [[ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
              [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
              [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
              [ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14]],
             # s5
             [[ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
              [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
              [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
              [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3]],
             # s6
             [[12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
              [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
              [ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
              [ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13]],
             # s7
             [[ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
              [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
              [ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
              [ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12]],
             # s8
             [[13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
              [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2],
              [ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8],
              [ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11]]
            ]

        bit6_list = []
        for i in range(0, 48, 6):
            bit6_list.append(bit[i:i+6])

        out = []
        for i in range(8):
            chunk = bit6_list[i]
            row = self.binaryToDecimal(chunk[:1]+chunk[5:])
            col = self.binaryToDecimal(chunk[1:5])

            out += self.decimalToBinary((s[i][row][col]))

        return out


    def permute(self,bit):


        p = [16,  7, 20, 21,
             29, 12, 28, 17,
              1, 15, 23, 26,
              5, 18, 31, 10,
              2,  8, 24, 14,
             32, 27,  3,  9,
             19, 13, 30,  6,
             22, 11,  4, 25]

        out = []
        for number in p:
            out.append(bit[number-1])

        return out
    
    
    def XOR(self,t1,t2):
        
        t_final = []
        
        for i in range(len(t1)):
            t_final.append(t1[i]^t2[i])
            
        return t_final
    
    def feistel(self,block,subkey):
        
        block = self.expansion(block)
        block_xor = self.XOR(block,subkey)
        block = self.Sbox(block_xor)
        block = self.permute(block)
        
        return block
    
    def cipher(self,bit, keys):

        ip = [58, 50, 42, 34, 26, 18, 10, 2,
              60, 52, 44, 36, 28, 20, 12, 4,
              62, 54, 46, 38, 30, 22, 14, 6,
              64, 56, 48, 40, 32, 24, 16, 8,
              57, 49, 41, 33, 25, 17,  9, 1,
              59, 51, 43, 35, 27, 19, 11, 3,
              61, 53, 45, 37, 29, 21, 13, 5,
              63, 55, 47, 39, 31, 23, 15, 7]

        fp = [40,  8, 48, 16, 56, 24, 64, 32,
              39,  7, 47, 15, 55, 23, 63, 31,
              38,  6, 46, 14, 54, 22, 62, 30,
              37,  5, 45, 13, 53, 21, 61, 29,
              36,  4, 44, 12, 52, 20, 60, 28,
              35,  3, 43, 11, 51, 19, 59, 27,
              34,  2, 42, 10, 50, 18, 58, 26,
              33,  1, 41,  9, 49, 17, 57, 25]

        p = []
        for number in ip:
            p.append(bit[number-1])


        ln = p[:32]
        rn = p[32:]


        for i in range(16):
            temp = rn
            rn = self.XOR(self.feistel(rn,keys[i]),ln)
            ln = temp


        combined = ln + rn
        out = []
        for number in fp:
            out.append(combined[number-1])

        return out

    def decipher(self,bit, keys):

        ip = [58, 50, 42, 34, 26, 18, 10, 2,
              60, 52, 44, 36, 28, 20, 12, 4,
              62, 54, 46, 38, 30, 22, 14, 6,
              64, 56, 48, 40, 32, 24, 16, 8,
              57, 49, 41, 33, 25, 17,  9, 1,
              59, 51, 43, 35, 27, 19, 11, 3,
              61, 53, 45, 37, 29, 21, 13, 5,
              63, 55, 47, 39, 31, 23, 15, 7]

        fp = [40,  8, 48, 16, 56, 24, 64, 32,
              39,  7, 47, 15, 55, 23, 63, 31,
              38,  6, 46, 14, 54, 22, 62, 30,
              37,  5, 45, 13, 53, 21, 61, 29,
              36,  4, 44, 12, 52, 20, 60, 28,
              35,  3, 43, 11, 51, 19, 59, 27,
              34,  2, 42, 10, 50, 18, 58, 26,
              33,  1, 41,  9, 49, 17, 57, 25]

 
        p = []
        for number in ip:
            p.append(bit[number-1])


        ln = p[:32]
        rn = p[32:]


        for i in range(16):
            temp = ln
            ln = self.XOR(self.feistel(ln,keys[i]),rn)
            rn = temp



        combined = ln + rn
        out = []
        for number in fp:
            out.append(combined[number-1])

        return out
    
    def code(self,message, key):  

        message_size = len(message)
        while((message_size%8)!=0):
            message+= 'X'
            message_size = len(message)
        
        message = self.stringToBinary(message)
        k_prime = self.stringToBinary(key)
        keys = self.key_scheduler(k_prime)
        out = []
        
        for part in range(0,len(message),64):
            binary_message = message[part:part+64]
            out+= self.cipher(binary_message,keys)
    
        return out
    
    def decode(self,message,key):
        message = self.stringToBinary(message)
        k_prime = self.stringToBinary(key)
        keys = self.key_scheduler(k_prime)
        out = []
        
        for part in range(0,len(message),64):
            binary_message = message[part:part+64]
            out+= self.decipher(binary_message,keys)
    
        return out




print("Les chiffrement suivant sont disponible :",
    "\n - Vigenere",
    "\n - Hill",
    "\n - Transpositions rectangulaire",
    "\n - DES",
    "\n Pour utiliser les chiffrements taper Vigenere pour utiliser Vigenere, Hill pour utiliser Hill, ",
    "\n Transpositions pour utiliser Transpositions rectangulaire  et DES pour utiliser DES.",
    "Taper fin pour mettre fin au programme")
coding = input("\nEntre le type de chiffrement que vous voulez utiliser : ")
while(coding!="fin"):

    if(coding == "Vigenere"):
        print()
        v = VigenereTable()
        mode = input("Entre c pour chiffré et d pour déchiffré : ")

        if(mode == "c"):
            params1 = input("Entré le message : ")
            params2 = input("Entré la clé : ")
            message_encode = v.VigenereCode(params1,params2,'c')
            print("\n\n\nLe message chiffré est : ",message_encode)
        elif(mode == "d"):
            params1 = input("Entré le message : ")
            params2 = input("Entré la clé : ")
            message_encode = v.VigenereCode(params1,params2,'d')
            print("\n\n\nLe message déchiffré est : ",message_encode)

    elif(coding == "Hill"):
        print("")

        params = input("Entre la matrix a b c d dans cette ordre : ")
        params = params.split()
        h = Hill(int(params[0]),int(params[1]),int(params[2]),int(params[3]))
        matrix_is_valid = h.matrixIsValid()

        while(not matrix_is_valid):
            params = input("La matrix est invalide, entré une nouvel : ")
            params = params.split()
            h = Hill(int(params[0]),int(params[1]),int(params[2]),int(params[3]))
            matrix_is_valid = h.matrixIsValid()

        mode = input("Entre c pour chiffré et d pour déchiffré : ")

        if(mode == "c"):
            params = input("Entre le message : ")
            message_encode = h.code(params)
            print("\nLe message chiffré est : ")
            print(message_encode)
        elif(mode == "d"):
            params = input("Entre le message : ")
            message_encode = h.decode(params)
            print("\nLe message déchiffré est : ",message_encode)

    elif(coding == "Transpositions"):
        print()
        t = Transpositions_rect()
        mode = input("Entre c pour chiffré et d pour déchiffré : ")
        if(mode == "c"):
            params1 = input("Entré le message : ")
            params2 = input("Entré la clé : ")
            message_encode = t.code(params1,params2)
            print("\n\n\nLe message chiffré est : ",message_encode)
        elif(mode == "d"):
            params1 = input("Entré le message : ")
            params2 = input("Entré la clé : ")
            message_encode = t.code(params1,params2)
            print("\n\n\nLe message déchiffré est : ",message_encode)

    elif(coding == "DES"):

        print()
        d = DES()
        mode = input("Entre c pour chiffré et d pour déchiffré : ")

        if(mode == "c"):
            params1 = input("Entré le message : ")
            params2 = input("Entré la clé : ")
            message_encode = d.code(params1,params2)
            print("\n\n\nLe message chiffré est : ",message_encode)
        elif(mode == "d"):
            params1 = input("Entré le message : ")
            params2 = input("Entré la clé : ")
            message_encode = d.decode(params1,params2)
            print("\n\n\nLe message déchiffré est : ",message_encode)
    
    coding = input("Entre le type de chiffrement que vous voulez utiliser : ")