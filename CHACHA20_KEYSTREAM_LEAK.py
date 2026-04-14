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
