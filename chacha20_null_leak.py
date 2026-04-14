"""
=========================================================
🎯 Objective: ChaCha20 Keystream Leak
💀 Vulnerability: Known Plaintext Attack (KPA) via Null-byte Injection
🛠️ Method: 
   1. Leverage the XOR property: Plaintext ⊕ Keystream = Ciphertext.
   2. By sending a null-byte payload (b"00"*16), the output becomes the raw Keystream.
   3. Use the leaked keystream to XOR and decrypt the hidden flag.
=========================================================
"""
from pwn import *
def xor_bytes(a, b):
    return bytes([a[i%len(a)]^b[i%len(b)]for i in range(max(len(a), len(b)))])
#molto intuitivo a dire il vero
r=remote('danceable.challs.cyberchallenge.it', 9036)
r.recvuntil(b"0. Exit")
r.sendline(b"1")
r.recvuntil(b"?")
r.sendline(b"00" * 16)
outp=r.recvline().strip().decode() 
outp=bytes.fromhex(outp)
flag=xor_bytes(outp[:16], outp[16:])
print(flag.decode())
