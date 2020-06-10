# A python script that convert iamage to nand2tetris HACK asm code
## Gen.py
1. Resize image so that generated code would not be too large.
2. Convert it to grayscale.
3. Binarization it with Otsu's thresholding method.
4. Convert it to sourcecode.
## Advanced.py
1. Resize image so that generated code would not be too large.
2. Convert it to grayscale.
3. Convert grayscale to grayscale-looks like black-white image.
4. Convert it to sourcecode.
## Detail of Step 3 of Advanced.py
First, Divide grayscale image into some cluster. For example, if you do ``image//=(256//7)``, you can divide image into seven cluster. For low contrast image, histogram normalization required.

Second, generate a tone map. The tone map is the same size as the original image. It is filled with given patter : [0,1,2,3,4...,N-1,0,1,2,3,4,...,N-1...,...,...,], N is the number of clusters. 

Then, the original image is compared with the tone map. so, if the value of a pixel in image is higher than the pixel of tone map, set the value of given pixel to 255, else, set it to 0.

This can be thought of as subtracting the tone map from the original image, and then performing binarization with threshold=zero.