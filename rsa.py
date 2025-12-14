import base64
from utils import pgcd, mod_inverse, exp_rapide, generate_large_e
from prime_generator import get_prime
import math

class RSA:
    def __init__(self, key_size=1024):
        self.key_size = key_size
        self.public_key = None
        self.private_key = None
        self.block_size = 0

    def generate_keys(self):
        print(f"--- Début de la génération des clés ({self.key_size} bits) ---")
        
        # 1. Génération de p et q
        p = get_prime(self.key_size // 2)
        q = get_prime(self.key_size // 2)
        
        while p == q:
            q = get_prime(self.key_size // 2)

        n = p * q
        phi = (p - 1) * (q - 1)

        # 2. Génération de e
        e = generate_large_e(phi, min_val=65537)
        
        # 3. Calcul de d
        d = mod_inverse(e, phi)

        self.public_key = (e, n)
        self.private_key = (d, n)
        
        self.block_size = (self.key_size // 8) - 1
        
        # --- NOUVEAUX AFFICHAGES DEMANDÉS ---
        print(f"Taille de p : {p.bit_length()} bits")
        print(f"Taille de q : {q.bit_length()} bits")
        print(f"Taille de n : {n.bit_length()} bits")
        print(f"Valeur de e choisie : {e}")
        print(f"Taille bloc max: {self.block_size} octets.")
        print("-------------------------------------------------------")

    def encrypt(self, message):
        e, n = self.public_key
        # 1. Conversion String -> Bytes
        message_bytes = message.encode('utf-8')
        
        encrypted_blocks = []
        
        # 2. Découpage en blocs
        for i in range(0, len(message_bytes), self.block_size):
            chunk = message_bytes[i:i + self.block_size]
            
            # Conversion Bytes -> Int (Big Endian)
            m_int = int.from_bytes(chunk, byteorder='big')
            
            # Chiffrement RSA: c = m^e mod n
            c_int = exp_rapide(m_int, e, n)
            
            encrypted_blocks.append(c_int)

        # 3. Encodage du résultat (On joint les nombres chiffrés)
        # Pour simplifier le transport, on peut convertir la liste d'ints en bytes puis base64
        # Ici on fait une méthode simple: Int -> Bytes -> Concat -> Base64
        # Note: chaque bloc chiffré a la taille du module (n)
        n_size_bytes = self.key_size // 8
        cipher_bytes = b"".join([c.to_bytes(n_size_bytes, 'big') for c in encrypted_blocks])
        
        return base64.b64encode(cipher_bytes).decode('utf-8')

    def decrypt(self, b64_cipher):
        d, n = self.private_key
        n_size_bytes = self.key_size // 8
        
        # 1. Base64 -> Bytes
        cipher_bytes = base64.b64decode(b64_cipher)
        
        decrypted_parts = []
        
        # 2. Lecture des blocs chiffrés
        for i in range(0, len(cipher_bytes), n_size_bytes):
            chunk = cipher_bytes[i:i + n_size_bytes]
            
            # Bytes -> Int
            c_int = int.from_bytes(chunk, byteorder='big')
            
            # Déchiffrement RSA: m = c^d mod n
            m_int = exp_rapide(c_int, d, n)
            
            # Int -> Bytes
            # On doit savoir combien d'octets cela représente. 
            # astuce python : (m_int.bit_length() + 7) // 8
            byte_len = (m_int.bit_length() + 7) // 8
            decrypted_part = m_int.to_bytes(byte_len, byteorder='big')
            decrypted_parts.append(decrypted_part)
            
        # 3. Reconstitution
        full_message = b"".join(decrypted_parts)
        return full_message.decode('utf-8')