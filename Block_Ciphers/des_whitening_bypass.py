"""
=========================================================
🎯 Objective: Custom Whitening Bypass & OTP Extraction
💀 Vulnerability: ECB Determinism / Predictable Padding Alignment
🛠️ Method: 
   1. Interrogates the encryption oracle with a 1-byte input to force a fully predictable, isolated second block containing exactly 8 bytes of PKCS#7 padding (0x08).
   2. Exploits the stateless nature of ECB mode by locally encrypting the known padding block using the user-chosen 3DES key.
   3. Extracts the 8-byte OTP by performing a XOR between the server's second ciphertext block and the locally calculated ciphertext.
   4. Recovers the final flag by retrieving the encrypted flag token and peeling back the cryptographic layers in reverse order: XOR(Unpad(Decrypt(Ciphertext ⊕ OTP)), OTP).
=========================================================
"""
from pwn import *
from Crypto.Cipher import DES3
from Crypto.Util.Padding import unpad

# Disabilita i log di pwntools per un output a terminale più pulito
context.log_level = 'error'

print("[*] Inizializzazione exploit...")

# --- SETUP AMBIENTE ---
host = 'trouble.challs.cyberchallenge.it'
port = 12000
r = remote(host, port)

# Scegliamo una chiave valida per 3DES (24 byte / 48 caratteri hex)
chiave_hex = "112233445566778888776655443322110099887766554433"
chiave_bytes = bytes.fromhex(chiave_hex)

# Inizializziamo il cifrario per le operazioni matematiche in locale
cipher = DES3.new(chiave_bytes, DES3.MODE_ECB)

# --- FASE 1: L'ORACOLO E L'ESTRAZIONE DELL'OTP ---
print("[*] Fase 1: Interrogazione dell'oracolo...")
r.recvuntil(b"0. Exit\n")
r.sendline(b"1")

r.recvuntil(b"? ")
# Inviamo un singolo byte (hex "00") per forzare il padding su un blocco intero noto
r.sendline(b"00") 

r.recvuntil(b"? ")
r.sendline(chiave_hex.encode())

# Riceviamo il ciphertext dall'oracolo e lo convertiamo in raw bytes
ct_hex = r.recvline().strip()
ct_bytes = bytes.fromhex(ct_hex.decode())

# Calcoliamo in locale la cifratura del blocco di padding puro
blocco_padding = b"\x08" * 8
L = cipher.encrypt(blocco_padding)

# Isoliamo il secondo blocco del ciphertext del server (dal byte 8 al 16)
C2 = ct_bytes[8:16]

# Estraggiamo l'OTP annullando il 3DES tramite XOR
otp = xor(C2, L)
print(f"[+] OTP Estratto con successo: {otp.hex()}")

# --- FASE 2: RECUPERO FLAG CIFRATA ---
print("[*] Fase 2: Richiesta della Flag cifrata...")
r.recvuntil(b"0. Exit\n") 
r.sendline(b"2")

r.recvuntil(b"? ")
r.sendline(chiave_hex.encode())

# Riceviamo la flag cifrata dal server
flag_hex = r.recvline().strip()
flag_bytes = bytes.fromhex(flag_hex.decode())

# --- FASE 3: DECRITTAZIONE FINALE ---
print("[*] Fase 3: Esecuzione dell'inversione crittografica strato per strato...")

# Strato 4: Rimuoviamo l'OTP esterno dal ciphertext
ct_senza_otp = xor(flag_bytes, otp)

# Strato 3: Decrittazione 3DES (ora abbiamo il testo "XORato" con in fondo il PADDING intatto)
testo_con_padding = cipher.decrypt(ct_senza_otp)

# Strato 2: Rimuoviamo il padding PKCS#7 ORA, mentre è ancora integro!
testo_senza_padding = unpad(testo_con_padding, 8)

# Strato 1: Rimuoviamo l'OTP iniziale dalla flag pulita
flag_pulita = xor(testo_senza_padding, otp)

print(f"\n[🔥] TARGET COMPROMESSO. FLAG: {flag_pulita.decode()}\n")

# Chiudiamo la connessione
r.close()
