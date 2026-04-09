from pwn import *
import ast

# 0. Setup Connessione
host = "predictable.challs.cyberchallenge.it"
port = 9034
r = remote(host, port)

print("[+] Connessione stabilita. Inizio l'attacco...")

# 1. OPZIONE 4: Rubiamo l'IV dell'admin (Leggiamo il database)
r.recvuntil(b"> ")
r.sendline(b"4")
db_string = r.recvline().decode().strip()
# Trasformiamo la stringa del server in un vero dizionario Python
db = ast.literal_eval(db_string) 
iv_admin = db['admin']
print(f"[+] IV Admin recuperato: {iv_admin}")

# 2. OPZIONE 1: Registrazione dell'esca ("bdmin")
r.recvuntil(b"> ")
r.sendline(b"1")
r.recvuntil(b"Insert your username: ")
r.sendline(b"bdmin")
r.recvuntil(b"Your login token: ")
login_token = r.recvline().decode().strip()
print(f"[+] Token 'bdmin' ottenuto: {login_token}")

# 3. LA MAGIA: Bit-Flipping (XOR)
# Dividiamo IV e Ciphertext
iv_originale = bytearray.fromhex(login_token[:32])
ciphertext = login_token[32:]

# Malleabilità CBC: Cambiamo la 'b' in 'a' all'indice 12
iv_originale[12] = iv_originale[12] ^ ord('b') ^ ord('a')

# Ricreiamo il token falso
token_falso = iv_originale.hex() + ciphertext
print(f"[+] Token falsificato creato: {token_falso}")

# 4. OPZIONE 2: Usiamo il token falso per fargli credere che siamo admin
r.recvuntil(b"> ")
r.sendline(b"2")
r.recvuntil(b"Please give me your login token ")
r.sendline(token_falso.encode())

# Il server ci dà il benvenuto come admin!
print(r.recvline().decode().strip()) 

# Ora ci chiede il comando. Ricorda: lo vuole in esadecimale!
r.recvuntil(b"What command do you want to execute? ")
comando_hex = b"get_flag".hex().encode()
r.sendline(comando_hex)

r.recvuntil(b"Your command token: ")
command_token = r.recvline().decode().strip()
print(f"[+] Token del comando generato (con IV dell'admin!): {command_token}")

# 5. OPZIONE 3: Il colpo di grazia
r.recvuntil(b"> ")
r.sendline(b"3")
r.recvuntil(b"What do you want to do? ")
r.sendline(command_token.encode())

# 6. INCASSIAMO LA FLAG
risultato = r.recvline().decode().strip()
print("\n" + "="*50)
print(f"🎉 {risultato} 🎉")
print("="*50 + "\n")

r.close()