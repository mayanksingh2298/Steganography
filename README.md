# Steganography

Steganography (pronounced STEHG-uh-NAH-gruhf-ee, from Greek steganos, or "covered," and graphie, or "writing") is the hiding of a secret message within an ordinary message and the extraction of it at its destination. Steganography takes cryptography a step farther by hiding an encrypted message so that no one suspects it exists. Ideally, anyone scanning your data will fail to know it contains encrypted data.

We have implemented a software that can hide messages in images (bmp and png) and audio files. The new file is indistinguishable from the original file to a human, yet our decryptor can find out the hidden information from the file.

We have taken security one step further by using passwords during encryption. The effect is that, even though if someone knows that a certain file contains hidden information, they won't be able to get that information because they donot know the password which was used during encryption.

This is a sample image file

<img src="https://github.com/mayanksingh2298/Steganography/blob/master/sample_files/face.png" width="300"/>

And this is another file which contains a secret message

<img src="https://github.com/mayanksingh2298/Steganography/blob/master/sample_files/enface.png" width="300"/>

Can you distinguish between the two?


## In a hurry?
1. open executable folder
2. open ubuntu or windows accroding to your OS
3. run the executable file encrypt_f
4. type in the message which you want to hide
5. enter a password
6. browse the file
7. click on encrypt

This would generate a new file in the current folder.

Now you may want to decrypt its contents.
1. run the executable file decrypt_f 
2. select the file
3. enter the password which was used during encryption
4. click on decrypt

Voila! The secret message would be shown on the screen.

Alternatively you can run the python scripts encrypt_f.py and decrypt_f.py.

## What happens in the background?
We achieve encryption by manipulating the Least Significant Bit of some data points in file. The change that occurs is so minute that it is invisible to human eye.

We donot proceed in a Linear Fashion (i.e. manipulate LSB of adjacent datapoints), rather we follow something known as a [Hilbert Curve](https://en.wikipedia.org/wiki/Hilbert_curve)

## But where does the password come in?
We use the passwords to store information about the first datapoint which we are going to manipulate and then follow the hilbert curve.

Hence if someone doesn't know the password, while decrypting if they start the wrong place, all that they are gonna get is gibberish.


# Authors

* [**Mayank Singh Chauhan**](https://github.com/mayanksingh2298)
* [**Atishya Jain**](https://github.com/atishya-jain)
