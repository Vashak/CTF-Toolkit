from pwn import *

r = remote('recycle.challs.cyberchallenge.it', 38213)

def xor(b1, b2):
    return bytes([a ^ b for a, b in zip(b1, b2)])

log.info("--- ATTACCO 'RECYCLE' (NO CRASH) ---")

# 1. NONCE 1 (15 byte: 14 di zeri + 01)
# In hex: 28 zeri e un "01" finale
r.sendlineafter(b"> ", b"3")
r.sendlineafter(b"> ", b"00" * 14 + b"01")

# 2. CATTURIAMO LA FLAG
r.sendlineafter(b"> ", b"2")
c_flag = bytes.fromhex(r.recvline().decode().strip())
log.success(f"Flag catturata! (Lunga {len(c_flag)} byte)")

# 3. CAMBIO NONCE (14 byte di zeri) -> IL TRUCCO SALVA-VITA
# Questo dà al contatore 2 byte di spazio (max 65535), evitando il crash a 256!
r.sendlineafter(b"> ", b"3")
r.sendlineafter(b"> ", b"00" * 14)
log.info("Nonce accorciato a 14 byte per prevenire il crash.")

# 4. SPAM (252 colpi per arrivare a 256)
spari = 252
log.info(f"Lancio {spari} spari per l'allineamento...")
r.send(b"1\n" * spari)

# Puliamo il buffer con precisione
for i in range(spari):
    r.recvuntil(b"> ") # Consuma il menu
    r.recvline()       # Consuma P e C
    if i % 50 == 0:
        print(f"Avanzamento... {i}/{spari}")

log.success("Counter a 256. Allineamento perfetto coi blocchi della flag!")

# 5. RECUPERO DEI KEYSTREAM PER TUTTA LA FLAG
# La flag è lunga 4 blocchi (52 byte), quindi ci servono i prossimi 4 keystream
all_keystreams = b""
log.info("Estrazione dei 4 veli crittografici...")

for i in range(4):
    r.sendlineafter(b"> ", b"1")
    line = r.recvline().decode().strip().split()
    p_rand = bytes.fromhex(line[0])
    c_rand = bytes.fromhex(line[1])
    all_keystreams += xor(p_rand, c_rand)

# 6. IL COLPO FINALE
final_flag = xor(c_flag, all_keystreams)

print("\n" + "🌟" * 25)
# Stampiamo rimuovendo i caratteri extra alla fine
print(f"FLAG: {final_flag.decode(errors='ignore')}")
print("🌟" * 25)

r.close()