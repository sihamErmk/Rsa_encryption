import random

def is_prime_miller_rabin(n, k=40):
    """Test de primalité de Miller-Rabin."""
    if n == 2 or n == 3: return True
    if n % 2 == 0 or n < 2: return False

    # Ecrire n-1 sous la forme 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n) # Utilise l'exp rapide intégrée ou celle de utils
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime_candidate(length):
    """Génère un nombre impair aléatoire de 'length' bits."""
    p = random.getrandbits(length)
    # Appliquer le masque pour s'assurer que le bit de poids fort et faible sont à 1
    p |= (1 << length - 1) | 1
    return p

def get_prime(length=1024):
    """Génère un nombre premier de 'length' bits."""
    p = 4
    while not is_prime_miller_rabin(p):
        p = generate_prime_candidate(length)
    return p