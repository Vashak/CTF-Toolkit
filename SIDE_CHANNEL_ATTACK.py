import socket
import re

HOST = 'benchmark.challs.cyberchallenge.it'
PORT = 9031
ALFABETO = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}"
# TORNA INDIETRO: l'ultimo punto sicuro era s1d3_ch4
FLAG = "CCIT{s1d3_ch4" 

def get_cycles(attempt):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((HOST, PORT))
            s.recv(1024)
            s.sendall((attempt + "\n").encode())
            resp = s.recv(1024).decode()
            m = re.search(r'(\d+)', resp)
            return int(m.group(1)) if m else 0
    except: return 0

print(f"[*] Caccia alla flag ripartendo da: {FLAG}")

while not FLAG.endswith("}"):
    risultati = []
    
    for char in ALFABETO:
        # Usiamo '}' come sentinella: se la lettera è giusta, 
        # il server proverà a cercare la graffa e il tempo salirà.
        clock = get_cycles(FLAG + char + "}")
        risultati.append((char, clock))
    
    # Ordiniamo i risultati per tempo di clock (dal più lento al più veloce)
    risultati.sort(key=lambda x: x[1], reverse=True)
    
    # Il vincitore è il primo della lista
    best_char, best_clock = risultati[0]
    second_best_char, second_best_clock = risultati[1]
    
    # VERIFICA CRUCIALE: In un esame, controlla lo scarto!
    # Se il migliore è molto più lento del secondo, è quasi certamente lui.
    if best_clock > second_best_clock + 15: # 15 è un margine di sicurezza
        FLAG += best_char
        print(f"[+] Confermata: {best_char} | Flag: {FLAG} | Clock: {best_clock}")
    else:
        # Se i tempi sono troppo simili, siamo in un vicolo cieco
        print(f"[-] Errore: tempi troppo simili ({best_clock} vs {second_best_clock}).")
        print("La lettera precedente era probabilmente sbagliata!")
        break