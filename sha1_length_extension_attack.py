from pwn import *
import base64
import hlextend

def main():
    context.log_level = 'error'
    print("[+] Accensione macchinari... ")
    r = remote('extendme.challs.cyberchallenge.it', 9069)

    # --- FASE 1: OTTENIAMO IL TESTIMONE ---
    # Creiamo una nota con i dati richiesti dai controlli logici
    r.sendlineafter(b"> ", b"1")
    r.sendlineafter(b"> ", b"flag")
    r.sendlineafter(b"> ", b"admin")
    r.sendlineafter(b"> ", b"c")

    r.recvuntil(b"identifier ")
    # Questo è il base64 (es. JmlkPTEmbmFtZT1mbGFnJmF1dGhvcj1hZG1pbg==)
    ident_b64 = r.recvuntil(b" ")[:-1]  
    
    r.recvuntil(b"checksum ")
    check_orig = r.recvuntil(b".")[:-1].decode()

    print(f"[-] Stringa Base64 (Dati noti per lo SHA1): {ident_b64.decode()}")
    print(f"[-] Testimone: {check_orig}")

    # --- FASE 2: LA MAGIA DELLA LENGTH EXTENSION ---
    # La coda ripulisce tutto e imposta id=0.
    coda_malvagia = b"&id=0&name=flag&author=admin"
    
    sha = hlextend.new('sha1')
    lunghezza_salt = 16 # Sappiamo che è 16 per l'assert del server!
    
    print("\n[+] Costruzione del Payload...")
    # ATTENZIONE QUI: Estendiamo ident_b64, NON il testo in chiaro!
    payload = sha.extend(coda_malvagia, ident_b64, lunghezza_salt, check_orig)
    hash_falsificato = sha.hexdigest()

    # --- FASE 3: CONSEGNA ALLA DOGANA ---
    print("[+] Invio del carico alla dogana...")
    r.sendlineafter(b"> ", b"2")
    
    # Il payload è già la stringa esatta che vogliamo far hashare alla Dogana.
    # Siccome la Dogana fa una b64decode, noi dobbiamo impacchettarlo in Base64!
    r.sendlineafter(b"> ", base64.b64encode(payload))
    r.sendlineafter(b"> ", hash_falsificato.encode())

    # Raccogliamo la Flag!
    print("\n--- RISULTATO DEL SERVER ---")
    risultato = r.recvall(timeout=2).decode()
    
    # Puliamo un po' l'output
    if "What do you want to do?" in risultato:
        print(risultato.split("What do you want to do?")[0].strip())
    else:
        print(risultato.strip())

if __name__ == "__main__":
    main()
