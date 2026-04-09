from pwn import *
from randcrack import RandCrack

# 1. Inizializziamo il nostro "clonatore" di Mersenne Twister
rc = RandCrack()

# Connettiti al server (cambia IP e Porta)
r = remote('srng.challs.cyberchallenge.it', 9064) 

print("[*] Inizio la fase di raccolta (624 round)...")

# 2. Ci arrendiamo 624 volte per rubare la sequenza
for i in range(624):
    # Aspettiamo il prompt
    r.recvuntil(b"> ")
    
    # Scegliamo 2 (Give up)
    r.sendline(b"2")
    
    # Leggiamo la risposta: "You lost! My number was XXXXX"
    r.recvuntil(b"was ")
    numero_rubato = int(r.recvline().strip())
    
    # Diamo il numero in pasto al clonatore
    rc.submit(numero_rubato)
    
    if i % 100 == 0:
        print(f"[*] Raccolti {i} numeri...")

print("[!] RACCOLTA COMPLETATA! Stato di Python clonato con successo.")

# 3. ROUND 625: L'Esecuzione
print("[*] Entro nel Round 625. Prevedo il futuro...")

# Chiediamo al nostro clone quale sarà il prossimo numero del server
numero_previsto = rc.predict_getrandbits(32)
print(f"[!] Il server genererà esattamente: {numero_previsto}")

# Aspettiamo il prompt del round 625
r.recvuntil(b"> ")

# Scegliamo 1 (Guess my number)
r.sendline(b"1")

# Aspettiamo che ci chieda il numero
r.recvuntil(b"> ")

# Spariamo il nostro numero previsto!
r.sendline(str(numero_previsto).encode())

# 4. Godiamoci lo spettacolo
print("\n[!] Risultato:")
print(r.recvall(timeout=2).decode())