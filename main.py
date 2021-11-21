import os
import matplotlib.pyplot as plt
import numpy

tekst1 = """Witaj w programie wspomagającym pracę z VASPem!
Wybierz jeden z następujących trybów:
1 - podziel DOSCAR na konktrtne pierwiastki,
2 - wyplotuj DOS jednego z pierwiastków
3 - scałkuj DOS na potrzeby wyliczenia stopnia domieszkowania
4 - przypisanie pierwiastków
"""

def cutDoscar(folder):
    numbers={}
    for i in os.listdir(folder):
        if i == "DOSCAR":
            doscar_dir=os.path.join(folder,i)
        if i == "POSCAR":
            poscar_dir = os.path.join(folder,i)
    r1=open(poscar_dir, "r")
    r=open(doscar_dir, "r")
    poscar = r1.readlines()
    elements = poscar[5].split()
    howMany = len(elements)
    for i in range(0, howMany):
        numbers[poscar[5].split()[i]] = int(poscar[6].split()[i])
    print(numbers)
    doscar = r.readlines()
    nedos = int(doscar[5].split()[2])

    def TotalDosDat(doscar, nedos):
        total_path = os.path.join(folder, "total_density.dat")
        total = open(total_path, "w")
        for i in range(5, nedos+6):
            total.write("{}\t{}\t{}\n".format(doscar[i].split()[0], doscar[i].split()[1], doscar[i].split()[2]))
        total.close()

    TotalDosDat(doscar, nedos)

    def wypiszPierwiastek(poscar, doscar, nedos, numbers):
        chosenElement = False
        listaPier = poscar[5].split()
        while chosenElement == False:
            pier = input("Jaki pierwiastek chciałbyś wypisać?\n")
            if pier in listaPier:
                indeks = listaPier.index(pier)
                suma = 0
                for j in range(0, indeks):
                    suma = suma + int(poscar[6].split()[j])
                break
            else:
                print("Opisanego przez Ciebie pierwiastka nie ma w tej cząsteczce!")
        startElement = 6 + 3001 * (suma + 1)
        print(
            "Przed tym pierwiastem jest {} innych. Dane na temat tego pierwiastka zaczynają się od {} linijki. Doscar ma {} linijek.".format(
                suma, startElement, len(doscar)))
        atomsNumber = int(numbers[pier])
        print(atomsNumber)
        for i in range(0, atomsNumber):
            datName = pier + "_number_" + str(i + 1) + ".dat"
            datPath = os.path.join(folder, datName)
            w = open(datPath, "w")
            for j in range(startElement - 1, startElement + nedos):
                w.write(doscar[j])
            startElement = startElement + nedos + 1

    wypiszPierwiastek(poscar, doscar, nedos, numbers)

def plociara(folder):
    while True:
        el = input("Podaj symbol pierwiastka, który chcesz wyplotować.\n")
        number = input("Podaj numer pierwiastka, którego chcesz wyplotować.\n")
        elPart = el + "_"
        fileToPlot = ""
        numPart = "_" + number + ".dat"
        for i in os.listdir(folder):
            if elPart in i and numPart in i:
                fileToPlot = os.path.join(folder, i)
                print(fileToPlot)
                break
        if fileToPlot == "":
            print("Nie odnaleziono takiego pliku. Spróbuj jeszcze raz!\n")
        else:
            break
    r = open(fileToPlot, "r")
    toPlot = r.readlines()
    energies = []
    fermi = float(toPlot[0].split()[3])
    print(fermi)
    spin = False
    print(toPlot[1].split())
    if len(toPlot[1].split())<12:
        tekst= """Wypisz to, co chcesz wyplotować, oddzielając numery spacjami.
    Aby wyplotować S wypisz 1.
    Aby wyplotować P y wypisz 2.
    Aby wyplotować P z wypisz 3.
    Aby wyplotować P x wypisz 4.
    Aby wyplotować D xy wypisz 5.
    Aby wyplotować D yz wypisz 6.
    Aby wyplotować D z2 wypisz 7.
    Aby wyplotować D xz wypisz 8.
    Aby wyplotować D x2-y2 wypisz 9\n"""
    else:
        spin=True
        tekst = """Wypisz to, co chcesz wyplotować, oddzielając numery spacjami.
    Aby wyplotować S up wypisz 1.
    Aby wyplotować S down wypisz 2. 
    Aby wyplotować P y up wypisz 3.
    Aby wyplotować P y down wypisz 4.
    Aby wyplotować P z up wypisz 5.
    Aby wyplotować P z down wypisz 6.
    Aby wyplotować P x up wypisz 7.
    Aby wyplotować P x down wypisz 8.
    Aby wyplotować D xy up wypisz 9.
    Aby wyplotować D xy down wypisz 10.
    Aby wyplotować D yz up wypisz 11.
    Aby wyplotować D yz down wypisz 12.
    Aby wyplotować D z2 up wypisz 13.
    Aby wyplotować D z2 down wypisz 14.
    Aby wyplotować D xz up wypisz 15.
    Aby wyplotować D xz down wypisz 16.
    Aby wyplotować D x2-y2 up wypisz 17
    Aby wyplotować D x2-y2 down wypisz 18\n"""
    print(spin)
    whatToPlot = input(tekst)
    skipped = []
    plottingList = []
    for i in whatToPlot.split():
        if int(i) < 19 and int(i) > 0 and i not in plottingList:
            plottingList.append(i)
        else:
            skipped.append(i)
    print("Uruchamiam tryby {}. Pomijam {}, ponieważ nie są one zgodne ze składnią.".format(plottingList, skipped))


    def extractor(toPlot, number):
        values = []
        for i in range(1, len(toPlot)):
            doWpisania = float(toPlot[i].split()[int(number)])
            values.append(doWpisania)
        return values

    for i in range(1, len(toPlot)):
        energies.append(float(toPlot[i].split()[0]) - fermi)
    if spin == True:
        for i in plottingList:
            if i == "1":
                Sup = extractor(toPlot, i)
                plt.plot(energies, Sup, label='S up')
            elif i == "2":
                Sdown = extractor(toPlot, i)
                plt.plot(energies, Sdown, label='S down')
            elif i == "3":
                Pyup = extractor(toPlot, i)
                plt.plot(energies, Pyup, label='P y up')
            elif i == "4":
                Pydown = extractor(toPlot, i)
                plt.plot(energies, Pydown, label='P y down')
            elif i == "5":
                Pzup = extractor(toPlot, i)
                plt.plot(energies, Pzup, label='P z up')
            elif i == "6":
                Pzdown = extractor(toPlot, i)
                plt.plot(energies, Pzdown, label='P z down')
            elif i == "7":
                Pxup = extractor(toPlot, i)
                plt.plot(energies, Pxup, label='P x up')
            elif i == "8":
                Pxdown = extractor(toPlot, i)
                plt.plot(energies, Pxdown, label='P x down')
            elif i == "9":
                Dxyup = extractor(toPlot, i)
                plt.plot(energies, Dxyup, label='D xy up')
            elif i == "10":
                Dxydown = extractor(toPlot, i)
                plt.plot(energies, Dxydown, label='D xy down')
            elif i == "11":
                Dyzup = extractor(toPlot, i)
                plt.plot(energies, Dyzup, label='D yz up')
            elif i == "12":
                Dyzdown = extractor(toPlot, i)
                plt.plot(energies, Dyzdown, label='D yz down')
            elif i == "13":
                Dz2up = extractor(toPlot, i)
                plt.plot(energies, Dz2up, label='D z2 up')
            elif i == "14":
                Dz2down = extractor(toPlot, i)
                plt.plot(energies, Dz2down, label='D z2 down')
            elif i == "15":
                Dxzup = extractor(toPlot, i)
                plt.plot(energies, Dxzup, label='D xz up')
            elif i == "16":
                Dxzdown = extractor(toPlot, i)
                plt.plot(energies, Dxzdown, label="D xz down")
            elif i == "17":
                Dx2y2up = extractor(toPlot, i)
                plt.plot(energies, Dx2y2up, label="D x2−y2 up")
            elif i == "18":
                Dx2y2down = extractor(toPlot, i)
                plt.plot(energies, Dx2y2down, label='D x2−y2 down')
    else:
        for i in plottingList:
            if i == "1":
                Sdens=extractor(toPlot,i)
                plt.plot(energies,Sdens,label='Gęstość stanów S')
            elif i == "2":
                Pydens=extractor(toPlot,i)
                plt.plot(energies,Pydens, label='Gęstość stanów P y')
            elif i == "3":
                Pzdens=extractor(toPlot,i)
                plt.plot(energies, Pzdens, label='Gęstość stanów P z')
            elif i == "4":
                Pxdens =extractor(toPlot,i)
                plt.plot(energies,Pxdens,label="Gęstość stanów P x")
            elif i == "5":
                Dxydens=extractor(toPlot,i)
                plt.plot(energies,Dxydens, label="Gęstość stanów D xy")
            elif i == "6":
                Dyzdens = extractor(toPlot,i)
                plt.plot(energies,Dyzdens, label="Gęstość stanów D yz")
            elif i == "7":
                Dz2dens=extractor(toPlot,i)
                plt.plot(energies,Dz2dens, label = "Gęstość stanów D z2")
            elif i == "8":
                Dxzdens = extractor(toPlot,i)
                plt.plot(energies,Dxzdens, label = "Gęstość stanów D xz")
            elif i == "9":
                Dx2y2=extractor(toPlot,i)
                plt.plot(energies,Dx2y2, label = "Gęstość stanów D x2-y2")

    plt.legend(loc=2, prop={'size': 16})
    plt.axvline(color="red")
    plt.xlabel("Energia [eV]", fontsize=16)
    plt.xticks(size=12)
    plt.yticks(size=12)
    plt.ylabel("Gęstość stanów elektronowych [DOS/eV]", fontsize=16)
    structureName = folder.split(os.sep)[-2]
    plt.title("DOS dla układu {}.".format(structureName), fontsize=20)
    plt.show()

def integrator(folder):
    while True:
        element=input("Wpisz symnol pierwiastka, którego stopień domieszkowania chcesz określić. Pamiętaj, że wielkość liter robi różnicę!\n")
        numerek=input("Podaj numer pierwiastka:\n")
        nazwa = element+"_number_"+numerek+".dat"
        file_to_plot=""
        for i in os.listdir(folder):
            if i == nazwa:
                file_to_plot = os.path.join(folder,nazwa)
                break
        if file_to_plot=="":
            print("W tym katalogu nie ma takiego pierwiastka. Spróbuj jeszcze raz!")
        else:
            break
    r=open(file_to_plot,"r")
    doscar=r.readlines()
    fermi = float(doscar[0].split()[-2])
    energies=[]
    doses=[]
    for i in range(1,len(doscar)):
        energia= float(doscar[i].split()[0])-fermi
        energies.append(energia)
        doses.append(float(doscar[i].split()[9]))
    plt.plot(energies,doses, label='Gęstość stanów xy up')
    plt.axvline(color="red")
    print("Zapisz sobie odkąd dokąd chcesz całkować wbrany przez Ciebie sygnnał")
    plt.show()
    pikMin=float(input("Pik zaczyna się przy: "))
    pikMax=float(input("Pik kończy się przy: "))
    calypikE=[]
    calypikD=[]
    for i in range(0,len(energies)):
        if energies[i]>=pikMin and energies[i]<=pikMax:
            calypikE.append(energies[i])
            calypikD.append(doses[i])
    print("Po wycięciu ten wykres wygląda następująco: ")
    plt.axvline(color='red')
    plt.plot(calypikE,calypikD, label='Interesujący nas zakres')
    plt.show()
    doZeraE=[]
    doZeraD=[]
    for i in range(0,len(calypikE)):
        if calypikE[i]<= 0:
            doZeraE.append(float(calypikE[i]))
            doZeraD.append(float(calypikD[i]))
        else:
            x2=calypikE[i]
            y2=calypikD[i]
            x1=calypikE[i-1]
            y1=calypikD[i-1]
            a=(y2-y1)/(x2-x1)
            b=y1-a*x1
            break

    doZeraE.append(0)
    doZeraD.append(b)
    plt.plot(calypikE,calypikD)
    plt.plot(doZeraE,doZeraD)
    plt.fill_between(doZeraE,doZeraD, color="red")
    licznik=numpy.trapz(doZeraD,doZeraE)
    mianownik=numpy.trapz(calypikD,calypikE)
    plt.show()
    domieszkowanie=licznik/mianownik
    print("Stopień domieszkowania wynosi {}.".format(domieszkowanie))
while True:
    mode = input(tekst1)
    if mode == "1":
        print("Do użycia tego trybu będzie potrzebny folder zawierający POSCAR i DOSCAR.")
        folder_start = input("Wklej jego ścieżkę tutaj: ")
        cutDoscar(folder_start)
        break
    elif mode == "2":
        print("Do użycia tego trybu będzie potrzebny folder zawierający DOSY konkretnych pierwiastków.")
        folder_start = input("Wklej jego ścieżkę tutaj: ")
        plociara(folder_start)
        break
    elif mode == "3":
        print("Do użycia tego trybu będzie potrzebny folder zawierający DOSY poszczególnych pierwiastków.")
        folder_start = input("Wklej jego ścieżkę tutaj: ")
        integrator(folder_start)
        break
    elif mode == "4":
        print("Do użycia tego trybu konieczny będzie folder zawierający plik txt zawierający geometrie kolejnych pierwiastków oraz POSCAR.")
        folder_start = input("Wklej jego ścieżkę tutaj: ")
        break
    else:
        print("Nie wybrałeś odpowiedniego trybu! Spróbuj jeszcze raz")