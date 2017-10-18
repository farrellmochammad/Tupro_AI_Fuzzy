from __future__ import division
from xlrd import open_workbook


wb = open_workbook('DataSet.xlsx')

value1 = []
value2 = []
value3 = []
value4 = []
for s in wb.sheets():
    for i in range(s.nrows):
         value1.append(s.cell(i,1).value)
         value2.append(s.cell(i,2).value)
         value3.append(s.cell(i,3).value)
         value4.append(s.cell(i,4).value)

Data = [value1 , value2 , value3 , value4]

#Kecil dan besar menandakan bahwa kemungkinan hoax kecil atau besar
#ya atau tidak berdasarkan label data kolom ke 2

totalEmosiya,countKecil = 0,0
totalEmositidak,countBesar = 0,0

totalProvokasiya,totalProvokasitidak = 0,0

for i in range(1,21):
    if (Data[2][i]=='Y'):
        totalProvokasiya += Data[1][i]
        totalEmosiya += Data[0][i]
        countBesar += 1
    else:
        totalProvokasitidak += Data[1][i]
        totalEmositidak += Data[0][i]
        countKecil += 1


nilaiPotensiprovokasikecil = totalProvokasitidak / countKecil
nilaiPotensiprovokasibesar = totalProvokasiya / countBesar
nilaiPotensiemosikecil = totalEmositidak / countKecil
nilaiPotensiemosibesar = totalEmosiya / countBesar

print nilaiPotensiprovokasikecil,nilaiPotensiprovokasibesar
print nilaiPotensiemosikecil,nilaiPotensiemosibesar

def fungsitrapesiumemosikecil(x):
    if(x<37):
        return 1
    elif(x>63.5):
        return 0
    else:
        return -(x-63.5)/(63.5-37)

"""def fungsitrapesiumemosikecil(x):
    if(x<30):
        return 1
    elif(x>63.5):
        return 0
    else:
        return -(x-63.5)/(63.5-30)"""

def fungsitrapeiumemosisedang(x):
    if(x<=50):
        return 0
    elif(x>50 and x<=63.5):
        return (x-50)/(63.5-50)
    elif(x>63.5 and x<=64.7):
        return 1
    elif(x>64.7 and x<=nilaiPotensiemosibesar):
        return -(x-nilaiPotensiemosibesar)/(nilaiPotensiemosibesar-65.8)
    else:
        return 0

"""def fungsitrapeiumemosisedang(x):
    if(x<=37):
        return 0
    elif(x>37 and x<=63.5):
        return (x-37)/(63.5-37)
    elif(x>63.5 and x<=64.7):
        return 1
    elif(x>64.7 and x<=nilaiPotensiemosibesar):
        return -(x-nilaiPotensiemosibesar)/(nilaiPotensiemosibesar-65.8)
    else:
        return 0"""

def fungsitrapesiumemosibesar(x):
    if(x<64.7):
        return 0
    elif(x>64.7 and x<nilaiPotensiemosibesar):
        return -(x-64.7)/(nilaiPotensiemosibesar-64.7)
    else:
        return 1

def fungsianggotaemosi(x):
    kategori = []
    peluang = []
    if(fungsitrapesiumemosikecil(x)!=0):
        peluang.append(fungsitrapesiumemosikecil(x))
        kategori.append("kecil")
    if(fungsitrapeiumemosisedang(x)!=0):
        peluang.append(fungsitrapeiumemosisedang(x))
        kategori.append("sedang")
    if(fungsitrapesiumemosibesar(x)!=0):
        peluang.append(fungsitrapesiumemosibesar(x))
        kategori.append("besar")
    return kategori,peluang

def fungsitrapeiumprovokasikecil(x):
    if(x<30):
        return 1
    elif (x>=30 and x<=nilaiPotensiprovokasikecil):
        return -(x-53)/(53-30)
    else:
        return 0

def fungsitrapesiumprovokasisedang(x):
    if(x>40 and x<=55):
        return (x-40)/(55-40)
    elif(x>55 and x<=70):
        return 1
    elif (x>70 and x<=nilaiPotensiprovokasibesar):
        return -(x-nilaiPotensiprovokasibesar)/(nilaiPotensiprovokasibesar-70)
    else:
        return 0

def fungsitrapesiumprovokasibesar(x):
    if(x>65 and x<=nilaiPotensiprovokasibesar):
        return (x-65)/(nilaiPotensiprovokasibesar-65)
    elif(x>nilaiPotensiprovokasibesar):
        return 1
    else:
        return 0

def fungsianggotaprovokasi(x):
    peluang = []
    kategori = []
    if(fungsitrapeiumprovokasikecil(x)!=0):
        peluang.append(fungsitrapeiumprovokasikecil(x))
        kategori.append("kecil")
    if(fungsitrapesiumprovokasisedang(x)!=0):
        peluang.append(fungsitrapesiumprovokasisedang(x))
        kategori.append("sedang")
    if(fungsitrapesiumprovokasibesar(x)!=0):
        peluang.append(fungsitrapesiumprovokasibesar(x))
        kategori.append("besar")
    return kategori,peluang

def inferensi(emosi,provokasi):
    if(emosi=="besar" and provokasi=="sedang"):
        return "Hoax"
    elif(emosi=="besar" and provokasi=="besar"):
        return "Hoax"
    elif(emosi=="kecil" and provokasi=="besar"):
        return "Hoax"
    else:
        return "tidak"

def fuzzyfikasi(angkaemosi,angkaprovokasi):
    min = 100
    out1,out3 = [],[]
    mat1,mat2 = fungsianggotaemosi(angkaemosi)
    mat3,mat4 = fungsianggotaprovokasi(angkaprovokasi)
    for i in range(0,len(mat1)):
        for j in range(0,len(mat3)):
            out1.append(inferensi(mat1[i],mat3[j]))
            if (mat2[i]>mat4[j]):
                out3.append(mat4[j])
            else:
                out3.append(mat2[i])
    return defuzzyfikasisugeno(out1,out3)
    #return out1,out3

def defuzzyfikasisugeno(matrixinferensi,matrixprob):
    makshoax = 0
    makstidak = 0
    for i in range(0,len(matrixinferensi)):
        if (matrixinferensi[i]=="Hoax"):
            if(makshoax<matrixprob[i]):
                makshoax = matrixprob[i]
        if (matrixinferensi[i]=="tidak"):
            if(makstidak<matrixprob[i]):
                makstidak = matrixprob[i]
    value = ((makshoax*50) + (makstidak*30))/(makshoax+makstidak)
    #return value
    """print "Nilai maks hoax = ",makshoax
    print "Nilai maks tidak = ",makstidak
    print value """
    if (value>=50):
        return "Hoax"
    else:
        return "tidak"



for i in range(1,31):
    print "Data ke- ",i,":",fuzzyfikasi(Data[0][i],Data[1][i])

totalbenar = 0
for i in range(1,21):
    if (fuzzyfikasi(Data[0][i],Data[1][i])==Data[3][i]):
        totalbenar += 1

print "Nilai akurasi = ",totalbenar/20

"""
print fungsianggotaemosi(Data[0][15])
print fungsianggotaprovokasi(Data[1][15])"""