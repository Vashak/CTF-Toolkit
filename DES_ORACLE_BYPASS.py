"""
=========================================================
🎯 Objective: DES-ECB Oracle Bypass & OTP Extraction
💀 Vulnerability: ECB Mode Determinism & Known Padding
🛠️ Method: 
   1. Exploits the DES-ECB block cipher mode by sending an exact 8-byte payload, forcing the server to create a standalone block containing only standard PKCS#7 padding.
   2. Knowing the plaintext (the padding), locally calculates the expected DES encryption output.
   3. XORs the server's ciphertext with the locally calculated ECB block to leak the hidden OTP key.
   4. Requests the encrypted flag and decrypts it locally by stripping the OTP layer, the DES layer, the padding, and the inner OTP layer.
=========================================================
"""
from pwn import *
from Crypto.Cipher import DES
import sys

# Disattiviamo i log rumorosi di pwntools
context.log_level = 'info'

HOST = "desoracle.challs.cyberchallenge.it"
PORT = 9035

# Ricreiamo la funzione XOR esattamente come la fa il server (ciclica)
def xor_bytes(a, b):
    return bytes([a[i % len(a)] ^ b[i % len(b)] for i in range(max(len(a), len(b)))])

log.info(f"Connessione al bersaglio {HOST}:{PORT}...")
try:
    r = remote(HOST, PORT)
except Exception as e:
    log.error(f"Errore di connessione: {e}")
    sys.exit(1)

# --- FASE 1: L'ORRORE DELL'ECB E L'ESTRAZIONE DELL'OTP ---
log.info("Fase 1: Avvelenamento del padding per estrarre l'OTP...")
r.recvuntil(b"> ")
r.sendline(b"1")

# Manderemo esattamente 8 byte per forzare la creazione di un blocco di padding pulito
text_hex = "0808080808080808" # 8 byte di padding (\x08) in formato hex
key_hex = "0000000000000000"  # Chiave nulla per semplicità

r.sendlineafter(b"encrypt (in hex)? ", text_hex.encode())
r.sendlineafter(b"key (in hex)? ", key_hex.encode())

# Catturiamo la risposta e convertiamo in bytes
outp_hex = r.recvline().strip().decode()
outp_bytes = bytes.fromhex(outp_hex)

# Estraiamo il Blocco 2 (Saltiamo i primi 8 byte e prendiamo dal byte 8 al 16)
C2 = outp_bytes[8:16]

# Calcoliamo E_locale (Cosa fa il DES col blocco di padding)
key_bytes = bytes.fromhex(key_hex)
cipher = DES.new(key_bytes, DES.MODE_ECB)
E_locale = cipher.encrypt(b"\x08" * 8)

# BINGO! Estraiamo l'OTP
otp = xor_bytes(C2, E_locale)
log.success(f"OTP Segreto del Server estratto con successo: {otp.hex()}")

# --- FASE 2: IL FURTO DELLA FLAG CIFRATA ---
log.info("Fase 2: Richiesta della Flag cifrata...")
r.recvuntil(b"> ")
r.sendline(b"2")
r.sendlineafter(b"use (in hex)? ", key_hex.encode())

flag_outp_hex = r.recvline().strip().decode()
flag_outp_bytes = bytes.fromhex(flag_outp_hex)
log.info(f"Flag cifrata ricevuta ({len(flag_outp_bytes)} byte). Inizio decrittazione locale...")

# --- FASE 3: LA MATEMATICA NON MENTE (DECIFRATURA LOCALE) ---
log.info("Fase 3: Rimozione strati crittografici...")

# Mossa 1: Rimuoviamo l'OTP esterno
layer_1 = xor_bytes(flag_outp_bytes, otp)

# Mossa 2: Sblocchiamo il DES
# Mossa 2: Sblocchiamo il DES (dentro c'è Flag^OTP + Padding PURO)
layer_2 = cipher.decrypt(layer_1)

# Mossa 3: Leggiamo quanti byte di padding ci sono e li TAGLIAMO VIA subito!
pad_len = layer_2[-1]
layer_2_pulito = layer_2[:-pad_len]

# Mossa 4: Ora che abbiamo solo la (Flag ^ OTP) pura, togliamo l'OTP
flag_bytes = xor_bytes(layer_2_pulito, otp)

# E la stampiamo!
flag = flag_bytes.decode()

print("\n" + "="*50)
print(f"[+] -> BERSAGLIO DISTRUTTO. FLAG: {flag} <- [+]")
print("="*50 + "\n")
