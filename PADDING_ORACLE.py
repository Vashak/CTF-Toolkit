from pwn import *

# Configurazione
context.log_level = 'error' 

print("[*] Connessione al server...")
r = remote("padding.challs.cyberchallenge.it", 9033)
r.recvuntil(b"Hello! Here's an encrypted flag\n")

hex_data = r.recvline().strip().decode()
dati_grezzi = bytes.fromhex(hex_data)

iv_server = dati_grezzi[:16]
tutto_il_ciphertext = dati_grezzi[16:]
blocchi = [tutto_il_ciphertext[i:i+16] for i in range(0, len(tutto_il_ciphertext), 16)]
blocchi_completi = [iv_server] + blocchi

# --- CHECKPOINT ---
# Abbiamo già: Blocco 1 (CCIT{7h3_m057_f4) e Blocco 2 (m0u5_4774ck_0n_A)
# Partiamo dal Blocco 3 (indice 3 nella lista blocchi_completi)
flag_gia_nota = "CCIT{7h3_m057_f4m0u5_4774ck_0n_A" 
flag_completa = flag_gia_nota 

print(f"[*] Checkpoint attivo: salto i primi 2 blocchi.")
print(f"[*] Testo noto: {flag_gia_nota}")

for b in range(3, len(blocchi_completi)): # Inizia dal terzo blocco
    print(f"\n[>>>] ATTACCO AL BLOCCO {b} / {len(blocchi)} [<<<]")
    
    iv_originale_corrente = blocchi_completi[b-1]
    blocco_cifrato_corrente = blocchi_completi[b]
    
    intermedi = [0] * 16
    flag_blocco = [0] * 16
    
    for padding in range(1, 17):
        target = 16 - padding
        iv_falso = bytearray(16)
        
        for k in range(15, target, -1):
            iv_falso[k] = intermedi[k] ^ padding
            
        # Priorità Leetspeak e caratteri comuni
        caratteri_probabili = b"\t9abcdefghijklmnopqrstuvwxyz0123456789_{}ABCDEFGHIJKLMNOPQRSTUVWXYZ "
        tentativi_j = []
        for char in caratteri_probabili:
            j_ottimizzato = char ^ iv_originale_corrente[target] ^ padding
            if j_ottimizzato not in tentativi_j: tentativi_j.append(j_ottimizzato)
        for j in range(256):
            if j not in tentativi_j: tentativi_j.append(j)

        byte_trovato = False
        for j in tentativi_j:
            iv_falso[target] = j
            
            try:
                r.recvuntil(b"What do you want to decrypt (in hex)? ")
                payload = (iv_falso + blocco_cifrato_corrente).hex().encode()
                r.sendline(payload)
                risposta = r.recvline()
                
                if b"Wow you are so strong" in risposta:
                    intermedi[target] = j ^ padding
                    flag_blocco[target] = intermedi[target] ^ iv_originale_corrente[target]
                    print(f" [+] Byte {target:02d} -> {repr(chr(flag_blocco[target]))}")
                    byte_trovato = True
                    break
            except EOFError:
                print(f" [!] Timeout! Riconnessione...")
                # Nota: Se il server cambia chiave al riavvio, il checkpoint fallirà
                # perché il ciphertext corrente non sarà più valido.
                exit("Il server ha chiuso la connessione. Riavvia per un nuovo ciphertext.")

    testo_blocco = "".join(chr(byte) for byte in flag_blocco)
    flag_completa += testo_blocco
    print(f"[=] Blocco {b} completato: {testo_blocco}")

print("\n" + "="*60)
print(f"[🏆] FLAG FINALE COMPLETA: {flag_completa}")
print("="*60)