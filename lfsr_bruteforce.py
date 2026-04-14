"""
=========================================================
🎯 Objective: LFSR (Linear Feedback Shift Register) State & Tap Recovery
💀 Vulnerability: Small state space (6-bit)
🛠️ Method: 
   1. Offline brute-force of all possible 6-bit initial states (seeds) and tap configurations.
   2. Simulates the LFSR bit-shifting and output generation for both MSB and LSB endianness.
   3. XORs the generated keystream with the ciphertext.
   4. Prunes invalid paths instantly if the resulting character is not printable ASCII (32-126).
=========================================================
"""
cipher = [0x9a, 0x1a, 0x7c, 0x38, 0xa7, 0x98, 0x77, 0x90, 0xe0, 0xad, 0x7a, 0xef, 0x69, 0xc1, 0x2f, 0x5a]

def solve():
    print("[*] Ricerca automatica della Flag in corso...")
    
    # Prova tutti i possibili Tap (1-63)
    for taps_mask in range(1, 64):
        # Prova tutti i possibili Seed iniziali (1-63)
        for seed_val in range(1, 64):
            # Prova i due versi di costruzione del byte
            for endianness in ['MSB', 'LSB']:
                
                # Converte il seed intero in una lista di 6 bit
                stato_init = [(seed_val >> (5-i)) & 1 for i in range(6)]
                stato = list(stato_init)
                risultato = ""
                
                for numero_cifrato in cipher:
                    keystream_byte = 0
                    for i in range(8):
                        uscita = stato[5] # Il bit che esce a destra
                        
                        # Calcola il nuovo bit basato sulla maschera dei Tap
                        nuovo = 0
                        for j in range(6):
                            if (taps_mask >> (5-j)) & 1:
                                nuovo ^= stato[j]
                        
                        # Shift a destra
                        stato = [nuovo] + stato[:-1]
                        
                        if endianness == 'MSB':
                            keystream_byte = (keystream_byte << 1) | uscita
                        else:
                            keystream_byte = keystream_byte | (uscita << i)
                    
                    carattere = numero_cifrato ^ keystream_byte
                    # Se il carattere non è ASCII stampabile, interrompi questo tentativo
                    if not (32 <= carattere <= 126):
                        break
                    risultato += chr(carattere)
                
                # Se abbiamo decriptato tutti i 16 byte con successo
                if len(risultato) == len(cipher):
                    print(f"\n[+] TROVATA!")
                    print(f"    Seed: {bin(seed_val)} | Tap Mask: {bin(taps_mask)} | Ordine: {endianness}")
                    print(f"    Flag: {risultato}\n")
                    return

    print("[!] Nessuna flag trovata. Forse il formato è diverso?")

solve(
