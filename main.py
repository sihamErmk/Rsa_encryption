# Fichier: main.py
import time
from rsa import RSA

def main():
    print("=== TP RSA: Implémentation complète (2048 bits) ===")
    
    # CHANGEMENT ICI : Passer key_size à 2048
    rsa_system = RSA(key_size=2048)
    
    # Mesure temps de génération
    print("Génération des clés en cours (cela peut prendre quelques secondes)...")
    start = time.time()
    rsa_system.generate_keys()
    print(f"Temps génération clés: {time.time() - start:.4f} sec")
    
    # Le reste du fichier reste identique...
    message = "Ceci est un test TP RSA avec une clé de 2048 bits. " * 3 + "Fin."
    print(f"\nMessage original ({len(message)} chars):\n{message}")
    
    # Chiffrement
    start = time.time()
    cipher_b64 = rsa_system.encrypt(message)
    print(f"\nMessage chiffré (Base64) [premiers 100 chars]:\n{cipher_b64[:100]}...")
    print(f"Temps chiffrement: {time.time() - start:.4f} sec")
    
    # Déchiffrement
    start = time.time()
    decrypted_msg = rsa_system.decrypt(cipher_b64)
    print(f"\nMessage déchiffré:\n{decrypted_msg}")
    print(f"Temps déchiffrement: {time.time() - start:.4f} sec")
    
    if message == decrypted_msg:
        print("\nSUCCESS: Le message déchiffré correspond à l'original.")
    else:
        print("\nERROR: Le message ne correspond pas.")

if __name__ == "__main__":
    main()