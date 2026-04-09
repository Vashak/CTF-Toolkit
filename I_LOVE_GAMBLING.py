import socket
import re
from math import gcd
import itertools

HOST = 'RSA-slot-machine.challs.cyberchallenge.it'
PORT = 38214
e = 65537

print("=== FASE 1: DOWNLOAD BRUTALE DEI DATI ===")
# Creiamo il pacchetto di 200 comandi esatti
comandi = (b"block_idx\n" * 152) + (b"respin\n" * 47) + b"jackpot\n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("[*] Connesso. Invio 200 comandi in un colpo solo...")
s.sendall(comandi)

print("[*] In attesa che il server processi e chiuda la connessione...")
testo_ricevuto = ""
while True:
    # recv() aspetta finché ci sono dati. Quando il server chiude, restituisce vuoto e si ferma.
    pezzo = s.recv(4096).decode(errors='ignore')
    if not pezzo: 
        break
    testo_ricevuto += pezzo

s.close()
print(f"[+] Download completato! ({len(testo_ricevuto)} caratteri ricevuti)")

# =====================================================================

print("\n=== FASE 2: ESTRAZIONE E CRITTANALISI ===")
# 1. Trovo N originale
match_n = re.search(r'n = (\d+)', testo_ricevuto)
if not match_n:
    print("[-] ERRORE: Non trovo l'N originale. Ecco cosa ha mandato il server:")
    print(testo_ricevuto[:500]) # Stampiamo un pezzo per capire il problema
    exit()
n_orig = int(match_n.group(1))

# 2. Trovo tutti i cloni (i respin)
n_clones = [int(x) for x in re.findall(r'new_n = (\d+)', testo_ricevuto)]
print(f"[+] Trovati {len(n_clones)} respin nel testo.")

# 3. Trovo il jackpot
match_jackpot = re.search(r'Encrypted jackpot:\s*(\d+)', testo_ricevuto)
if not match_jackpot:
    print("[-] ERRORE: Non trovo il jackpot. Ultime righe del server:")
    print(testo_ricevuto[-500:])
    exit()
jackpot_enc = int(match_jackpot.group(1))


print("\n[*] Calcolo incrociato (MCD) per trovare i fattori segreti...")
factors = set()
for i in range(len(n_clones)):
    for j in range(i+1, len(n_clones)):
        g = gcd(n_clones[i], n_clones[j])
        if g > 1 and g != n_clones[i] and g != n_clones[j]:
            factors.add(g)

factors_list = list(factors)
print(f"[+] Trovati {len(factors_list)} fattori primi.")

if len(factors_list) < 2:
    print("[-] Pochi fattori trovati. Il server ha pescato male. Rilancia lo script.")
    exit()

# Cerchiamo i due fattori che differiscono solo per massimo 3 cifre
valid_pair = None
for i in range(len(factors_list)):
    for j in range(i+1, len(factors_list)):
        s1, s2 = str(factors_list[i]), str(factors_list[j])
        if len(s1) == len(s2):
            diffs = [idx for idx in range(len(s1)) if s1[idx] != s2[idx]]
            if 0 < len(diffs) <= 3:
                valid_pair = (s1, diffs)
                break
    if valid_pair: break

if not valid_pair:
    print("[-] Nessuna coppia di fattori compatibile trovata. Rilancia lo script.")
    exit()

str_p1, diff_idxs = valid_pair
print(f"[*] Indici sbloccati trovati: {diff_idxs}")
print("[*] Inizio scasso delle combinazioni...")

p_original = None
base_p_chars = list(str_p1)

for combo in itertools.product("0123456789", repeat=len(diff_idxs)):
    for i, idx in enumerate(diff_idxs):
        base_p_chars[idx] = combo[i]
    
    test_p = int("".join(base_p_chars))
    if n_orig % test_p == 0:
        p_original = test_p
        break

if p_original:
    print(f"[+] FATTORE ORIGINALE TROVATO!")
    q_original = n_orig // p_original
    phi = (p_original - 1) * (q_original - 1)
    d = pow(e, -1, phi)
    flag_int = pow(jackpot_enc, d, n_orig)
    flag = flag_int.to_bytes((flag_int.bit_length() + 7) // 8, 'big').decode(errors='ignore')
    print(f"\n[!!!] FLAG: {flag} [!!!]")
else:
    print("[-] Brute force fallito.")