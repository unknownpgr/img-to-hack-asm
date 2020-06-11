# Img2hack.asm
A python script that convert iamage to nand2tetris HACK asm code.
## [Gen.py](./gen.py)
1. Resize image so that generated code would not be too large.
2. Convert it to grayscale.
3. Binarization it with Otsu's thresholding method.
4. Convert it to hack asm code.
## [Advanced.py](./advanced.py)
1. Resize image so that generated code would not be too large.
2. Convert it to grayscale.
3. Convert grayscale to grayscale-looks like black-white image.
4. Convert it to hack asm code.
## [v3.py](./v3.py)
Same as "Advanced", but reduces the code capacity by bundling the same bit patterns and moving them to RAM.
See the code for more details.

## Detail of Step 3 of Advanced.py
First, Divide grayscale image into some cluster. For example, by doing ``image//=(256//7)``, you can divide pixels into seven cluster. For low contrast image, histogram normalization required.

Second, generate a tone map. The tone map is a 2D numpy uint8 array that has same size as the original image. It is filled with given patter : [0,1,2,3,4...,N-1,0,1,2,3,4,...,N-1...,...,...,], N is the number of clusters.
Actually, If the width of the image is a multiple of N, the image will have vertical lines. So shift this pattern some pixels for each row. shifting N//2 or N//2-1 pixels works best. blow is an expample of tone map with N=4 and shift=2.

    0 1 2 3 0 1 2 3 ... ...
    2 3 0 1 2 3 0 1 ... ...
    0 1 2 3 0 1 2 3 ... ...
    2 3 0 1 2 3 0 1 ... ...
    ... ...

Then, the original image is compared with the tone map. so, if the value of a pixel in image is higher than the pixel of tone map, set the value of given pixel to 255, else, set it to 0.

This can be thought of as subtracting the tone map from the original image, and then performing binarization with threshold=0.
## Result
### Result of [Gen.py](./gen.py)
You can see the given image is shown in the program.
![](./demo_1.png)
After the given image is converted to a black and white image that looks like grayscale, it is displayed on the program screen.
### Result of Advanced.py
![](./demo_3.png)
