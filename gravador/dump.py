import serial
import random

def dump():
    file = open('../BIOS/backup.bin', 'wb')

    i = 0x000000
    ser.write(b'\x01')

    while(i <= 0x0FFFFF):
        j = 0
        print(f"{hex(i)} : ", end="")
        while(j < 16):
            byte = ser.read()
            file.write(byte)
            print("{}".format(byte.hex()), end=" ")
            j += 1
        print()
        i += 16
    file.close()

def flash_page(file_name, start):
    start = [start >> (8 * (2 - i)) & 0xFF for i in range(3)]

    file_name = '../BIOS/' + file_name
    with open(file_name, 'rb') as file:
        arr = list(file.read(256))

    ser.write(b'\x02')

    for i in range(0, 3):
        ser.write(start[i].to_bytes(1, 'big'))
    for i in range(0, 256):
        ser.write(arr[i].to_bytes(1, 'big'))
    print("Página gravada")

def flash_bios(file_name):
    file_name = '../BIOS/' + file_name

    file =  open(file_name, 'rb')

    start = 0

    for j in range(0, 2 ** 12):
        page = [start >> (8 * (2 - i)) & 0xFF for i in range(3)]
        arr = list(file.read(256))

        ser.write(b'\x02')
        if(ser.read() == b'\x20'):
            for i in range(0, 3):
                ser.write(page[i].to_bytes(1, 'big'))
            for i in range(0, 256):
                ser.write(arr[i].to_bytes(1, 'big'))

        if(ser.read() == b'\x21'):
            print(j)
        else:
            print('Erro')
            return

        start += 256
    file.close()
    print("Gravado")

def create_page():
    arr = [
        b'\x65', b'\x52', b'\x45', b'\x45', b'\x20', b'\x46', b'\x49', b'\x52', b'\x45', b'\x20', b'\x4d', b'\x45', b'\x4c', b'\x48', b'\x4f', b'\x52',
        b'\x20', b'\x4a', b'\x4f', b'\x47', b'\x4f', b'\x20', b'\x44', b'\x4f', b'\x20', b'\x4d', b'\x55', b'\x4e', b'\x44', b'\x4f', b'\x31', b'\x9c',
        b'\xb1', b'\x48', b'\x33', b'\x21', b'\x35', b'\x92', b'\x20', b'\xf8', b'\x7f', b'\x1d', b'\xea', b'\x07', b'\xe8', b'\xa0', b'\x35', b'\x18',
        b'\xe7', b'\x2d', b'\x72', b'\x4f', b'\xac', b'\xd7', b'\x8c', b'\xb8', b'\xb7', b'\x33', b'\x09', b'\x27', b'\xf8', b'\x73', b'\x82', b'\xd4',
        b'\x06', b'\x31', b'\x21', b'\x86', b'\xcb', b'\x25', b'\x35', b'\xe1', b'\x9c', b'\xdd', b'\xd1', b'\x81', b'\x01', b'\xf7', b'\xa9', b'\xaf',
        b'\xfa', b'\xbd', b'\x0c', b'\x13', b'\xff', b'\x86', b'\x91', b'\x3e', b'\xe7', b'\xe0', b'\xf5', b'\x44', b'\x97', b'\x25', b'\x31', b'\x5d',
        b'\x00', b'\x17', b'\xa3', b'\x23', b'\x39', b'\x08', b'\x1b', b'\x66', b'\x47', b'\x6d', b'\x08', b'\x5b', b'\x1b', b'\x49', b'\x89', b'\xaa',
        b'\x69', b'\x87', b'\x98', b'\x7c', b'\xe4', b'\xca', b'\xe1', b'\x6e', b'\xc4', b'\x6f', b'\x5e', b'\xdf', b'\x9d', b'\x32', b'\x91', b'\x7d',
        b'\x8c', b'\xc1', b'\x54', b'\x2d', b'\xd9', b'\xeb', b'\x57', b'\x4d', b'\x4d', b'\x59', b'\x92', b'\x9c', b'\x0c', b'\x8b', b'\xe1', b'\x84',
        b'\x61', b'\x56', b'\x4f', b'\x66', b'\x54', b'\xa9', b'\x8c', b'\xfb', b'\xa6', b'\x0c', b'\xdf', b'\x71', b'\x5f', b'\xe4', b'\x68', b'\x8b',
        b'\xa0', b'\xc9', b'\xc2', b'\x63', b'\x54', b'\xd2', b'\x7e', b'\x82', b'\xe0', b'\xc3', b'\xa9', b'\x59', b'\x72', b'\xf5', b'\xcf', b'\xed',
        b'\x43', b'\xc8', b'\xf3', b'\x4e', b'\x2e', b'\x40', b'\xad', b'\xe2', b'\x10', b'\xd9', b'\xcc', b'\x6e', b'\x18', b'\x28', b'\x16', b'\xc5',
        b'\x79', b'\x8d', b'\x88', b'\x52', b'\x7d', b'\x40', b'\x16', b'\x30', b'\xc8', b'\x66', b'\x07', b'\x80', b'\x19', b'\x62', b'\x03', b'\x01',
        b'\xc3', b'\xcd', b'\x75', b'\x01', b'\x96', b'\x92', b'\x4b', b'\x6b', b'\x23', b'\x38', b'\x7c', b'\x95', b'\x55', b'\x7c', b'\x98', b'\x33',
        b'\x0d', b'\x22', b'\x98', b'\x37', b'\x0a', b'\x39', b'\x00', b'\x39', b'\x34', b'\x14', b'\xa0', b'\x4e', b'\xc4', b'\xed', b'\x99', b'\x91',
        b'\xf5', b'\x0a', b'\x91', b'\xfe', b'\x01', b'\x4d', b'\xdb', b'\x03', b'\xf5', b'\x0d', b'\xb5', b'\x2c', b'\xe6', b'\x02', b'\xff', b'\x4c'
    ]
    file = open('../BIOS/page.bin', 'wb')
    for i in range(0, 256):
        file.write(arr[i])
    file.close()
    print(f"page.bin criado")

def dump_page(page):
    start = page
    final = start + 0xf0

    page = [page >> (8 * (2 - i)) & 0xFF for i in range(3)]

    ser.write(b'\x03')

    for i in range(0, 3):
        ser.write(page[i].to_bytes(1, 'big'))

    while(start <= final):
        j = 0
        print(f"{hex(start)} : ", end="")
        while(j < 16):
            byte = ser.read()
            print("{}".format(byte.hex()), end=" ")
            j += 1
        print()
        start += 16

def sector_erase(sector):
    prev = sector
    sector = [sector >> (8 * (2 - i)) & 0xFF for i in range(3)]

    ser.write(b'\x04')

    if(ser.read() == b'\x20'):
        for i in range(0, 3):
            ser.write(sector[i].to_bytes(1, 'big'))
    if(ser.read() == b'\x21'):
        print(f"Setor {prev} apagado")
    else:
        print("Erro")

def chip_erase():
    ser.write(b'\x05')

    if(ser.read() == b'\x20'):
        print("Chip sendo apagado...")
    if(ser.read() == b'\x21'):
        print("Chip apagado por completo")
    else:
        print("Erro")

def gen_random_bios():
    file = open('../BIOS/rand_bios.bin', 'wb')
    for i in range(0, 0x100000):
        num = random.randint(0, 255)
        num = num.to_bytes(1, 'big')
        file.write(num)
    file.close()
    print(f"Arquivo rand_bios.bin gerado com sucesso")

ser = serial.Serial('/dev/ttyUSB0', 115200)

print("Gravador de bios")
print("1 - Dump da bios")
print("2 - Gravar página")
print("3 - Create page")
print("4 - Dump page")
print("5 - Erase sector")
print("6 - Chip erase")
print("7 - Gerar bios aleatória")
print("8 - Gravar bios")
opc = int(input("Escolha sua opção: "))

if(opc == 1):
    print("Fazendo o dump da bios")
    dump()   

elif(opc == 2):
    start = input("Digite o endereço do começo do setor: ")
    start = int(start, 16)

    file_name = input("Digite o nome do arquivo a ser gravado: ")
    flash_page(file_name, start)

elif(opc == 3):
    create_page()

elif(opc == 4):
    start = input("Digite o endereço do começo do setor: ")
    start = int(start, 16)

    dump_page(start)
    
elif(opc == 5):
    start = input("Digite o endereço do começo do setor: ")
    start = int(start, 16)

    sector_erase(start)

elif(opc == 6):
    chip_erase()

elif(opc == 7):
    gen_random_bios()

elif(opc == 8):
    file_name = input("Digite o nome do arquivo a ser gravado: ")
    flash_bios(file_name)
else:
    print("Error")

ser.close()

