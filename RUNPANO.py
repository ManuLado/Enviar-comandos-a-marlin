import os

dire=str(input('folder'))


print("----------performimg random pano (pano2)")
os.system('python pano_libs/P2.py'+' '+dire)
print("----------end!")
print(".")
print(".")
print(".")
print("----------performimg nested pano(pano3)")
os.system('python pano_libs/P3.py'+' '+dire)
print("----------end!")
print(".")
print(".")
print(".")
print("----------performimg matrix pano(pano4)")
os.system('python pano_libs/P4.py'+' '+dire)
print("----------end!")
print(".")
print(".")
print(".")
print("----------performimg linear pano(pano1)")
#os.system('python pano_libs/P1.py'+' '+dire)
print("----------end!")
print(".")
print(".")
print(".")
print("----------performimg all-vs-all pano(pano0)")
lista=os.listdir(dire)



os.system("mkdir "+dire+"_P0")

k=0
for i in lista:
    for j in lista:
        if j!=i:
            os.system('python pano_libs/P0.py '+dire+" "+str(i)+' '+str(j)+' '+str(k))
            k+=1
