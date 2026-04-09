# 1. Definiamo prima il nostro "mattone" matematico
def calcola_blocco_pubblico(i):
    blocco = 0
    for r in range(1337):
        for j in range(64):
            blocco = blocco ^ ((r + i + j + 1) % 256)
    return blocco
# 2. Leggiamo il file cifrato
cipher = bytes.fromhex("2e6e247916415d5ab29e0b4bdddf5a728bc1591bb2cb5d5fb2993241ddda321e8bcb5d5fdaf20e1c9dc55e5f90")

# 3. Calcoliamo la chiave segreta usando la prima lettera ('C')
K_secret = cipher[0] ^ ord('C') ^ calcola_blocco_pubblico(0)
print(f"[*] K_secret collassato trovato: {K_secret}")

# 4. Usiamo la chiave per decriptare TUTTO il messaggio
flag_decifrata = ""

for i in range(len(cipher)):
    # Applichiamo l'equazione inversa lettera per lettera
    byte_chiaro = cipher[i] ^ K_secret ^ calcola_blocco_pubblico(i)
    # Trasformiamo il numero in un carattere leggibile (chr) e lo uniamo alla flag
    flag_decifrata += chr(byte_chiaro)

print(f"[+] Vittoria! La flag è: {flag_decifrata}")