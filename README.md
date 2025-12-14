#!/bin/bash

# 1. Vidange des règles existantes
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X

# 2. Politique par défaut : On interdit tout
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# 3. On accepte le localhost et le trafic déjà établi
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

# 4. Accès SSH et HTTP vers le routeur lui-même (Optionnel mais utile pour admin)
iptables -A INPUT -i enp0s3 -p tcp --dport 22 -j ACCEPT

# 5. RÈGLES DMZ (Vers VM2 - 192.168.10.10)
# On autorise Internet (enp0s3) à aller vers DMZ (enp0s8) sur port 80 (Web) et 21 (FTP)
iptables -A FORWARD -i enp0s3 -o enp0s8 -p tcp --dport 80 -d 192.168.10.10 -j ACCEPT
iptables -A FORWARD -i enp0s3 -o enp0s8 -p tcp --dport 21 -d 192.168.10.10 -j ACCEPT

# 6. RÈGLES LAN (Vers Internet uniquement)
# Le LAN (enp0s9) a le droit d'aller vers Internet (enp0s3)
iptables -A FORWARD -i enp0s9 -o enp0s3 -j ACCEPT

# 7. NAT (Masquerade)
# Permet à DMZ et LAN d'avoir internet en utilisant l'IP de VM1
iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE

# Autoriser le ping pour les tests (Optionnel mais recommandé)
iptables -A INPUT -p icmp -j ACCEPT
iptables -A FORWARD -p icmp -j ACCEPT

echo "Pare-feu appliqué."
