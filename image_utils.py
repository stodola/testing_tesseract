import Levenshtein
import pytesseract
from PIL import Image
import io


def to_text(tekst):
    buf = io.StringIO(tekst)
    tekst=buf.readlines()

    poczatek=0 
    koniec=[]
    for i, item in enumerate(tekst):

        row = item.replace('\n','').split(' ') 
        for j in row:
            lev=Levenshtein.distance(j, 'FISKALNY')
            if lev  <= 2:
                poczatek = i

            lev2=Levenshtein.distance(j, 'Sprzed.')
            if lev2 <= 2:
                koniec.append(i)


    #tekst po opcieciu poczatku i konca
    tekst2 = tekst[poczatek+1:min(koniec)]

    #removing first element from list if it is new line or it is equal to 1
    while tekst2[0] == '\n' or len(tekst2[0])==1:
        tekst2=tekst2[1:]

    while tekst2[-1] == '\n' or len(tekst2[-1])==1:
        del tekst2[-1]

    tekst3=[]

    i=0
    while True:
        try :
            if tekst2[i+1] == '\n':
                tekst3.append(tekst2[i]+' ' +tekst2[i+2])
                i+=3
            else:
                tekst3.append(tekst2[i])
                i+=1
        except IndexError:
            tekst3.append(tekst2[i])
            break

    #tu moze byc kiedys problem jak nie bedzie co zastapic
    tekst4=[]
    for i in tekst3:
        tekst4.append(i.replace('\n',''))

    #funkcja sprawdzajaca czy w slowie jest wiecej liter czy liczb
    def letters_check(word):
        letters = 0
        numbers = 0
        for i in word:
            try :
                int(i)
                numbers +=1
            except ValueError:
                letters +=1

        if letters >numbers:
            return 'letter'
        else:
            return 'number'


    cena = []

    for i, item in enumerate(tekst4):
        for j, item1  in enumerate(item.split(' ')[::-1]):
            if len(item1) == 1:
                continue
            else:
                cena.append(item1)
                break


    #to ma na celu pozbycie sie liter z listy z cenami
    #to wynika z tego ze tesseract jest zle wytrenowany pozniej do usniecia
    new_cena_1=[]
    def bez_liter(lista):
        for i, item in enumerate(lista):
            if 'T' in item:
                new_item = item.replace('T', '1')
                new_cena_1.append(new_item)

            elif 'U' in item:
                new_item = item.replace('U', '0')
                new_cena_1.append(new_item)
            else:
                new_cena_1.append(item)
    bez_liter(cena)

    #kod testowy for paragon z biedronka
    #p=new_cena_1.pop(2)
    #p1=p+'D'
    #new_cena_1.insert(2, p1)


    # to teraz sie tyczy paragonow ze sklepow typy biedronka, ktore maja
    # na koncu litere razem z suma

    new_cena_2=[]
    def bez_liter_beidra(lista):
        for i, item in enumerate(lista):
            if letters_check(item[-1]) == 'letter':
                new_item = item[:-1]
                new_cena_2.append(new_item)
            else:
                new_cena_2.append(item)

    bez_liter_beidra(new_cena_1)

    def to_decimal_number(lista):
        new_cena_3=[]
        for i, item in enumerate(lista):
            if ',' in item:
                new_item = item.replace(',', '.')
                new_cena_3.append(new_item)
            else:
                new_cena_3.append(item)

        return new_cena_3

    new_cena_3 = to_decimal_number(new_cena_2)

    def to_floating_point(lista):
        new_cena_4=[]
        for i, item in enumerate(lista):
            try:
                a=float(item)
                new_cena_4.append(a)
            except ValueError:
                new_cena_4.append(None)

        return new_cena_4

    new_cena_4 = to_floating_point(new_cena_3)


    #teraz zajmiemy sie itemami z przodu

    #ta funkcja ma na celu pozbycie sie spacji na pierwszym mijescu w elementach paragonu
    #co mialo mijesce w jednym z paragonow
    def infront_spaces(lista):
        tekst5=[]
        for i, item in enumerate(lista):
            if item[0] ==' ':
                while item[0] ==' ':
                    item = item[1:]
                tekst5.append(item)
            else:
                tekst5.append(item)
        return tekst5

    tekst5 =infront_spaces(tekst4)

    nazwa_produktu = []
    for i, item in enumerate(tekst5):
        nazwa=''
        for j, item1 in enumerate(item.split(' ')[:4]):  #to wezmie tylko po uwage 4 pierwsze elemtny
            if j==0:
                nazwa=nazwa+item1+' '
            else:  # j >0:
                if letters_check(item1) == 'letter' and len(item1)>1:
                    nazwa=nazwa+item1+' '
                elif letters_check(item1) == 'letter' and len(item1) == 1 and item1 =='Z':
                    nazwa=nazwa+item1+' '
                else:
                    break

        nazwa_produktu.append(nazwa)

    return zip(nazwa_produktu,new_cena_3)

if __name__ =='__main__':
    tekst =pytesseract.image_to_string(Image.open('IMG_20170113_191448.jpg'), lang='pol')
    to_text(tekst)

