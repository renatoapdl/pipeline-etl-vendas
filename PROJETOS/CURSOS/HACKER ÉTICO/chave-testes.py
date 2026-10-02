def AND (a, b): return a & b # & = AND bit a bit em PY 
def OR (a, b): return a | b # OR bit a bit
def NOT (a): return 1 - a # com 0/1 subtrair de 1 inverte [1-0=1, 1-1=0]
def XOR (a, b): return a ^ b # ^ = XOR bit a bit
def NAND (a, b): return NOT(AND(a, b)) # NAND = AND com saida invertida

def tabela_verdade(nome, porta):
    #imprime as 4 combinações possíveis de duas entradas (00, 01, 10, 11)
    print(f"=== {nome} ===")
    print("a b | saída")
    for a in (0, 1):
        for b in (0, 1):
            print(f"{a} {b} | {porta(a, b)}")
    print()

# Imprime as tabelas
tabela_verdade("AND", AND)
tabela_verdade("OR", OR)
tabela_verdade("XOR", XOR)
tabela_verdade("NAND", NAND)

# A cifra XOR em um byte: cifra e decifra (encode e decode) com a mesma operação
texto = 0b01001000 # a letra "H" em binário (72 na tabela ASCII)
chave = 0b10110101 # uma chave aleatória de 8 bits
cifrado = texto ^ chave # ^ Aplica XOR nos 8 bits de uma vez
volta = cifrado ^ chave # ^ de novo com a mesma cheve desfaz a cifra

print(f"texto   = {texto:08b} ({chr(texto)!r})") # :08b = binário com 8 dígitos
print(f"chave   = {chave:08b}")
print(f"cifrado = {cifrado:08b}  (texto or chave)")
print(f"volta   = {volta:08b} ({chr(volta)!r}) <- cifrado XOR chave")
