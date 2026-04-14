"""
=========================================================
🎯 Objective: Stream Cipher Known Plaintext Attack (KPA)
💀 Vulnerability: Keystream reuse / Deterministic keystream
🛠️ Method: 
   1. Uses a known plaintext (p_rand) and its corresponding ciphertext (c_rand).
   2. Recovers the raw keystream segment via XOR: Keystream = Plaintext ⊕ Ciphertext.
   3. Slides the recovered keystream across the encrypted flag byte-by-byte.
   4. Filters outputs searching for known flag formats (e.g., "CCIT{").
=========================================================
"""
def xor(b1, b2):
    return bytes([a ^ b for a, b in zip(b1, b2)])

# --- INCOLLA QUI I TUOI DATI ---
c_flag_hex = "fe4a40446cc36ba90f96c22fb586b33db765e240817ff164d047e186f2963a36a6a723808a55ea5fcf5f45a5567ef8e2963b3349"
p_rand_hex = "1666de8342937dbeec9da4f9c56b270b"
c_rand_hex = "0b27d785bd9a33da0680cca647614694"

c_flag = bytes.fromhex(c_flag_hex)
p_rand = bytes.fromhex(p_rand_hex)
c_rand = bytes.fromhex(c_rand_hex)

# Il keystream che hai ottenuto con l'opzione 1
keystream_ottenuto = xor(p_rand, c_rand)

print("🔍 Analisi dei blocchi della flag...")

# Proviamo a XORare il keystream con ogni possibile blocco della flag
for i in range(0, len(c_flag) - 15):
    fetta_flag = c_flag[i:i+16]
    tentativo = xor(fetta_flag, keystream_ottenuto)
    
    # Se troviamo "CCIT" o pezzi di flag, abbiamo vinto
    if b"CCIT" in tentativo or b"{" in tentativo or b"_" in tentativo:
        print(f"\n🎯 POSSIBILE MATCH AL BYTE {i}:")
        print(f"Contenuto: {tentativo}")
