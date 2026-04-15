# 🗡️ CTF Crypto Toolkit

This repository contains my personal collection of Python exploits and scripts developed to solve Cryptography and Hardware Reverse Engineering challenges during Capture The Flag (CTF) competitions.

The toolkit covers a variety of attack vectors, from breaking classic algorithms (RSA, AES) to exploiting hardware vulnerabilities (LFSR) and side-channel data.

> **🌟 Highlight:** Looking for something more advanced? Check out my standalone project where I bypassed ChaCha20 padding using linear cryptanalysis on GF(2): [https://github.com/Vashak/ChaCha20-Linear-Exploit]

## 🧰 The Arsenal

Below is an index of the exploits available in this toolkit. Files are organized into specific directories based on their cryptographic domain.

| Script | Category | Vulnerability | Description |
| :--- | :--- | :--- | :--- |
| **`rng_time_seed_exploit.py`** | PRNG | State Recovery & Time Seed | Extracts a custom RNG internal state via modular inverse and brute-forces the server's timestamp seed. |
| **`mt19937_state_clone.py`** | PRNG | MT19937 State Recovery | Collects 624 consecutive outputs to reconstruct the internal state of Python's Mersenne Twister. |
| **`aes_ctr_recycle.py`** | Block Ciphers | Counter Sync & Keystream | Exploits nonce length manipulation to sync the AES-CTR counter and extract the exact keystream. |
| **`des_ecb_oracle_bypass.py`**| Block Ciphers | ECB Determinism | Exploits DES-ECB mode by forcing a known padding block to leak a hidden OTP layer. |
| **`cbc_padding_oracle.py`** | Block Ciphers | CBC Padding Oracle | Exploits verbose PKCS#7 padding errors to perform a byte-by-byte decryption. |
| **`cbc_bit_flipping.py`** | Block Ciphers | CBC Bit-Flipping | Alters the IV of a CBC token via XOR to manipulate the decrypted plaintext, bypassing authentication. |
| **`chacha20_null_leak.py`** | Stream Ciphers| Null-Byte Injection | Leaks the raw ChaCha20 keystream by injecting null bytes, enabling full decryption. |
| **`stream_kpa_sliding.py`** | Stream Ciphers| Known Plaintext (KPA) | Extracts a keystream segment using a known plaintext-ciphertext pair and slides it across the target. |
| **`xor_stream_collapse.py`** | Stream Ciphers| Known Plaintext (1 Byte) | Uses a single known plaintext byte to collapse an XOR equation and recover the static secret key. |
| **`dsa_linear_nonce.py`** | Asymmetric | Linear Nonce (*k*) | Recovers the DSA private key *x* by solving a modular linear system built from related nonces. |
| **`rsa_common_factor_gcd.py`**| Asymmetric | Prime Reuse (GCD) | Exploits poor prime generation by calculating the GCD of multiple RSA moduli to extract shared factors. |
| **`timing_side_channel.py`** | Side-Channel | Timing Leak | Exploits an insecure string comparison by measuring server response latency to leak the flag. |
| **`elf_error_oracle.py`** | Side-Channel | Error-Based Oracle | Brute-forces a local ELF binary by monitoring stdout/stderr for specific error strings. |
| **`lfsr_bruteforce.py`** | Hardware/LFSR | State Space Exhaustion | Performs an offline brute-force of a 6-bit LFSR's seed, tap mask, and endianness. |
| `rsa_key_selection.py` | Asymmetric | Signature Forgery (Smooth Primes) | Exploits insecure RSA factor input by generating smooth primes to solve the Discrete Logarithm Problem (DLP) using Pohlig-Hellman and CRT. |

---

## ⚠️ Disclaimer

*All scripts were developed for educational purposes and authorized CTF competitions. Do not use them against real systems without explicit permission.*
