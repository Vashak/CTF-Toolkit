"""
=========================================================
🎯 Objective: RSA Signature Forgery via Duplicate Key Selection
💀 Vulnerability: Insecure Parameter Input (User-provided p, q)
🛠️ Method: 
   1. Requests a target hash (H) and a signature (sig) from the server.
   2. Generates two custom 512-bit "Smooth Primes" (p, q).
   3. Solves the Discrete Logarithm Problem (DLP) modulo p and q 
      independently using the Pohlig-Hellman algorithm.
   4. Uses the Chinese Remainder Theorem (CRT) to unify the 
      exponents into a single public exponent (e).
   5. Forges a valid modulus n = p*q where sig^e ≡ H (mod n).
=========================================================
"""
from pwn import *
import random
from sympy import isprime, discrete_log
from sympy.ntheory.modular import crt

# 1. DIVIDIAMO I MATTONCINI IN DUE SQUADRE (Per evitare conflitti CRT)
tutti_i_primi = [i for i in range(3, 500) if isprime(i)]
random.shuffle(tutti_i_primi)
meta = len(tutti_i_primi) // 2
squadra_p = tutti_i_primi[:meta]
squadra_q = tutti_i_primi[meta:]

def genera_primo(squadra):
    while True:
        n = 2 # Solo il 2 è in comune
        while n.bit_length() < 512:
            n *= random.choice(squadra)
        p = n + 1
        if isprime(p): return p

def main():
    r = remote('multirsa.challs.cyberchallenge.it', 9068)
    r.recvuntil(b"Hash of the flag: ")
    H = int(r.recvline().strip())
    r.recvuntil(b"Signature: ")
    sig = int(r.recvline().strip())
    print("[+] Dati ricevuti. Inizio trivellazione...")

    while True:
        try:
            # Cerchiamo un p compatibile
            p = genera_primo(squadra_p)
            if pow(H, (p-1)//2, p) != pow(sig, (p-1)//2, p): continue
            e_p = discrete_log(p, H % p, sig % p)
            
            # Cerchiamo un q compatibile (ora è molto più facile!)
            for _ in range(50): 
                q = genera_primo(squadra_q)
                if pow(H, (q-1)//2, q) != pow(sig, (q-1)//2, q): continue
                e_q = discrete_log(q, H % q, sig % q)
                
                # Controllo parità (unica condizione rimasta grazie alle due squadre)
                if (e_p % 2) == (e_q % 2):
                    res = crt([p - 1, q - 1], [e_p, e_q])
                    if res:
                        e_user = res[0]
                        print(f"[!] BINGO! Esponente trovato: {e_user}")
                        
                        r.sendlineafter(b"First prime factor: ", str(p).encode())
                        r.sendlineafter(b"Second prime factor: ", str(q).encode())
                        r.sendlineafter(b"Public exponent: ", str(e_user).encode())
                        print("\n--- FLAG ---")
                        print(r.recvall().decode())
                        return # CHIUDIAMO TUTTO
        except Exception:
            continue

if __name__ == "__main__":
    main()
