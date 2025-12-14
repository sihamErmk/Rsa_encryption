import random

def pgcd(a, b):
    """Algorithme d'Euclide pour le PGCD (Déjà itératif)."""
    while b:
        a, b = b, a % b
    return a

def euclide_etendu(a, b):
    """
    Algorithme d'Euclide étendu en version ITERATIVE.
    (Indispensable pour les clés > 1024 bits pour éviter RecursionError)
    Retourne (g, x, y) tel que ax + by = g
    """
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0

def mod_inverse(a, m):
    """Calcule l'inverse modulaire de a modulo m."""
    g, x, y = euclide_etendu(a, m)
    if g != 1:
        
        raise Exception('L\'inverse modulaire n\'existe pas (e et phi ne sont pas premiers entre eux)')
    else:
        return x % m

def exp_rapide(base, exp, mod):
    """Exponentiation modulaire rapide."""
    res = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % mod
        exp = exp // 2
        base = (base * base) % mod
    return res

def generate_large_e(phi, min_val=65537):
    """Génère un e aléatoire grand et premier avec phi."""
    e = random.randint(min_val, phi - 1)
    if e % 2 == 0: e += 1
    
    while pgcd(e, phi) != 1:
        e += 2 
    return e