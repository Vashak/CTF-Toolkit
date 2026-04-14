"""
=========================================================
🎯 Objective: Local Binary Error-Based Oracle Extraction
💀 Vulnerability: Character-by-character validation with verbose error output
🛠️ Method: 
   1. Wraps a local compiled ELF binary using Python's subprocess.
   2. Brute-forces the flag one character at a time.
   3. Uses the standard output/error (stdout/stderr) as an oracle: the absence of the specific error "Learn to move properly" indicates a correct character guess.
   4. Appends the correct character and repeats until the closing brace '}' is found.
=========================================================
"""
import subprocess
import string

# --- 1. CONFIGURAZIONE ---
# nome file 
target = "./cha-cha" 

# La base della flag che conosciamo già
flag = "CCIT{" 

# Carichiamo tutte le lettere (maiuscole/minuscole), numeri e simboli comuni
# string.printable contiene quasi tutto, ma noi usiamo una lista mirata
alfabeto = string.ascii_letters + string.digits + "{}_!"

print(f"[*] Operazione avviata. Bersaglio: {target}")
print(f"[*] Partenza da: {flag}")

# --- 2. IL MOTORE DI RICERCA ---
while True:
    trovato_in_questo_giro = False
    
    for carattere in alfabeto:
        tentativo = flag + carattere
        
        # Eseguiamo il programma. 
        # Usiamo stdout=PIPE e stderr=STDOUT per fondere i canali ed evitare conflitti
        processo = subprocess.run(
            [target, tentativo],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # --- 3. LA LOGICA CHIRURGICA ---
        # Se il messaggio di errore NON è presente, abbiamo fatto centro!
        if "Learn to move properly" not in processo.stdout:
            flag = tentativo
            print(f"[+] Carattere trovato! Flag attuale: {flag}")
            trovato_in_questo_giro = True
            break # Esci dal ciclo 'for' (abbiamo trovato la lettera per questa posizione)

    # --- 4. CONDIZIONI DI USCITA ---
    # Se abbiamo trovato la parentesi di chiusura, la missione è finita
    if flag.endswith("}"):
        print("\n" + "="*30)
        print(f"🎯 FLAG ESTRATTA: {flag}")
        print("="*30)
        break
        
    # Se abbiamo provato tutto l'alfabeto e non abbiamo trovato nulla...
    if not trovato_in_questo_giro:
        print("\n[-] Errore: Nessun nuovo carattere trovato. Forse la flag usa simboli rari?")
        break
