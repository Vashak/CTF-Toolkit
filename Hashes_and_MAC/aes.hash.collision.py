from pwn import *
from Crypto.Cipher import AES

# 1. Connessione al cantiere
r = remote('haesh.challs.cyberchallenge.it', 9070)

# 2. Prepariamo il materiale (la chiave AES per il nostro attacco)
padding = b"\x10" * 16

# 3. Avvio delle ruspe per 10 round
for _ in range(10):
    # Ignoriamo il testo inutile fino all'inizio dell'Hash
    r.recvuntil(b", ")
    
    # Catturiamo l'Hash e lo ripuliamo dalla parentesi
    h_origin = r.recvuntil(b")")
    h_origin = h_origin[:-1].decode()
    
    # Mangiamo il prompt per allineare il tubo di comunicazione
    r.recvuntil(b"> ")
    
    # Frulliamo la crittografia all'incontrario
    cipher = AES.new(padding, AES.MODE_ECB)
    s2 = cipher.decrypt(bytes.fromhex(h_origin))
    
    # Riconvertiamo il risultato in esadecimale e lo inviamo
    s2_hex = s2.hex()
    r.sendline(s2_hex.encode())
    
    print(f"[*] Round superato inviando la collisione: {s2_hex}")

# Alla fine dei 10 round, raccogliamo la bandiera tra le macerie
print("\n--- RISULTATO DEL SERVER ---")
print(r.recvall(timeout=2).decode())
