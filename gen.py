import numpy as np
import cv2

# Read image
img = cv2.imread('./img.png')
# Resize
w = img.shape[1] if img.shape[1] <= 512 else 512
h = w*img.shape[0]//img.shape[1]
img = cv2.resize(img, (w, h))
# Grayscale
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Thresholding
thr, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# Write file
cv2.imwrite('o2.jpg', img)
# Show image
cv2.imshow('w', img)
cv2.waitKey(1)


# Convert 16pixel array to short type integer
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
counter = 0
pc = 0
with open('o2.asm', 'w') as f:
    for j in range(img.shape[0]):
        row = img[j]
        print('Processing line', j+1)
        for i in range(len(row)//16):
            r = pixel2bit(row[i*16:i*16+16])
            if r == 0:
                continue
            if r > 2**15:
                # Set pixel value to A.
                # Since CPUEmulator register can only use 15bit,
                f.write(f'@{65536-r}\n')
                # Copy it to D
                f.write(f'D=A\n')
                # Set address of image to A
                f.write(f'@{BASE+counter+i}\n')
                # Copy -D to M[A]
                f.write(f'M=-D\n')
                pc += 4
            else:
                # Set pixel value to A
                f.write(f'@{r}\n')
                # Copy it to D
                f.write(f'D=A\n')
                # Set address of image to A
                f.write(f'@{BASE+counter+i}\n')
                # Copy D to M[A]
                f.write(f'M=D\n')
                pc += 4
        # Newline of image
        counter += 32
    f.write(f'@{pc}\n')
    f.write(f'0;JMP\n')
