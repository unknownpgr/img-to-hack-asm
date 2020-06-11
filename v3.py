import numpy as np
import cv2

IMG_PATH = 'input_2.png'
ASM_PATH = 'o4.asm'

LEVEL = 8
MAX_WIDTH = 512

# Read image
img = cv2.imread(IMG_PATH)
w = img.shape[1] if img.shape[1] <= MAX_WIDTH else MAX_WIDTH
h = w*img.shape[0]//img.shape[1]
img = cv2.resize(img, (w, h))
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img //= (255//LEVEL)

# Convrt to black-white image with tone
for y in range(h):
    for x in range(w):
        c = img[y][x]
        pos = (x+(3*y)) % LEVEL
        if c > pos:
            img[y][x] = 255
        else:
            img[y][x] = 0

# Show image
cv2.imshow('w', img)
cv2.waitKey(1)


# Convert 16 pixel array to short type integer
def pixel2bit(pixels):
    r = 0
    for i in range(16):
        if i < len(pixels):
            v = 0 if pixels[i] > 0 else 1
        else:
            v = 0
        r += v*2**i
    return r


BASE = 16384
line = 0
pixelSet = {}
for j in range(img.shape[0]):
    row = img[j]
    print('Processing line', j+1)
    for i in range(len(row)//16):
        pattern = pixel2bit(row[i*16:i*16+16])
        if pattern == 0:
            continue

        # Collect pixels with same pattern
        if pattern not in pixelSet:
            pixelSet[pattern] = []
        pixelSet[pattern].append(BASE+line*32+i)

    line += 1
    if line > 255:
        break

pc = 0
with open(ASM_PATH, 'w') as f:
    for pattern in sorted(list(pixelSet.keys())):
        if pattern > 2**15:
            f.write(f'@{65536-pattern}\n')
            f.write(f'D=-A\n')
        else:
            f.write(f'@{pattern}\n')
            f.write(f'D=A\n')
        pc += 2
        for addr in pixelSet[pattern]:
            f.write(f'@{addr}\n')
            f.write(f'M=D\n')
            pc += 2

        # 100=>D
        f.write('@1000\n')
        f.write('D=A\n')

        # D=>i
        f.write('@i\n')
        f.write('M=D\n')

        # i=>D
        f.write('@i\n')
        f.write('D=M\n')

        # i=i-1
        f.write('M=M-1\n')
        pc += 7

        f.write(f'@{pc-3}\n')
        f.write('D;JGT\n')
        pc += 2

    f.write(f'@{pc}\n')
    f.write(f'0;JMP\n')
