import random
from tkinter import *
from tkinter import messagebox              #Če posebaj ne uvozim messageboxa funkcija kombinirajFunkcije sproži izjemo, ko poskuša ena od funkcij poklicati messagebox
           

####### Računalnikova "logika" #######

def racunalnik(kocke=[0, 0]):                       # Računalnik izbere naključno možno potezo
    if kocke == [0, 0]:
        kocka1 = random.randrange(1, 7)
        kocka2 = random.randrange(1, 7)
        if kocka1 == kocka2: kocke = [kocka1, kocka1, kocka1, kocka1]
        else: kocke = [kocka1, kocka2]
    poteze = moznePoteze(kocke)
    while poteze:
        izbira = random.choice(poteze)
        spremeni(izbira[0], izbira[1], 1)
        kocke.pop(kocke.index(izbira[0]))
        poteze = moznePoteze(kocke)
                     
def moznePoteze(kocke):                             # Računalnik pridobi seznam možnih potez
    a = []
    for i in kocke:
        for j in range(25):
            if veljavnaPoteza(i, j, 1):
                a.append([i, j])
    return a

####### Pravila igre #######

def poteza(tocka1):                                 # Funkcija za eno potezo igralca
    global kocke
    global kocka
    global crni
    global beli
    global nacin
    global igralec

    if kocke == [0, 0]:
        messagebox.showinfo("Nova igra", "Za nadaljevanje prosim začnite novo igro.")
        return
    if len(kocke) == 1:
        kocka = 0
    elif kocke[0] == kocke[1]:
        kocka = 0
    if kocka == -1:
        messagebox.showinfo("Kocka", "Izberite kocko!")
    elif veljavnaPoteza(kocke[kocka], tocka1, igralec):
        spremeni(kocke[kocka], tocka1, igralec)
        kocke.pop(kocka)
        kocka = -1
        if beli == 0:
            messagebox.showinfo("Zmaga", "Beli je zmagal!")
            kocke = [0, 0]
            return
        if crni == 0:
            messagebox.showinfo("Zmaga", "Črni je zmagal!")
            kocke = [0, 0]
    else: messagebox.showinfo("Neveljavna", "Izbrana poteza je neveljavna!")
    if kocke == []:
        if nacin == "pve":
            racunalnik()
            if crni == 0:
                messagebox.showinfo("Zmaga", "Črni je zmagal!")
                kocke = [0, 0]
                return
            vrziKocke()
        else:
            igralec = (igralec + 1) % 2
            vrziKocke()

def vrziKocke():                                    # Funkcija, ki določi nov nabor premikov
    global kocke
    kocka1 = random.randrange(1, 7)
    kocka2 = random.randrange(1, 7)
    if kocka1 == kocka2: kocke = [kocka1]*4
    else: kocke = [kocka1, kocka2]
        
def dodaj(tocka, igralec, k):                       # Funkcija, ko na mesto tocka doda k figur izbranega igralca
        polje[tocka][igralec] += k

def premakni(tocka1, tocka2, igralec):
    dodaj(tocka1, igralec, -1)
    dodaj(tocka2, igralec, 1)


def vsiDoma(igralec):                               # Funkcija, ki preveri ali so vse figure izbranega igralca na zadnjih 6 mestih poti
    global beli
    global crni
    if igralec == 0 and beliLevo(25) == beli:
        return True
    elif igralec == 1 and crniLevo(0) == crni:
        return True
    else:
        return False
        

def crniLevo(tocka):                                # Funkcija, ki prešteje tiste crne figure na zadnjih 6 mestih, ki so levo od izbranega mesta
    k = 0
    for i in range(tocka + 1, 7):
        k += polje[i][1]
    return k

def beliLevo(tocka):                                # Funkcija, ki prešteje tiste bele figure na zadnjih 6 mestih, ki so levo od izbranega mesta
    k = 0
    for i in range(tocka - 1, 18, -1):
        k += polje[i][0]
    return k

def veljavnaPoteza(kocka, tocka1, igralec):         # Funkcija, ki preveri ali je igralčeva poteza veljavna
    igralec2 = (igralec + 1) % 2
    if igralec == 0: tocka2 = tocka1 + kocka
    elif tocka1 == 0: tocka2 = 25 - kocka
    else: tocka2 = tocka1 - kocka        
    if polje[tocka1][igralec] == 0: return False
    elif tocka2 > 24:
        if vsiDoma(0) and beliLevo(tocka1) == 0: return True
        else: return False
    elif tocka2 < 1:
        if vsiDoma(1) and crniLevo(tocka1) == 0: return True
        else: return False
    elif polje[tocka2][igralec2] > 1: return False
    else: return True

def spremeni(kocka, tocka1, igralec):               # Funkcija, ki premakne dano figuro za izbran korak in morebitne ostale figure kot je potrebno
    global beli
    global crni
    igralec2 = (igralec + 1) % 2
    if igralec == 0: tocka2 = tocka1 + kocka
    elif tocka1 == 0: tocka2 = 25 - kocka
    else: tocka2 = tocka1 - kocka
    if veljavnaPoteza(kocka, tocka1, igralec):
        if tocka2 > 24:
            dodaj(tocka1, igralec, -1)
            beli -= 1
        elif tocka2 < 1:
            dodaj(tocka1, igralec, -1)
            crni -= 1
        elif polje[tocka2][igralec2] == 1:
            premakni(tocka1, tocka2, igralec)
            premakni(tocka2, 0, igralec2)
        else: premakni(tocka1, tocka2, igralec)

def pravila1():                                     # Začetna postavitev polje
    global beli
    global crni
    global polje
    beli = 15
    crni = 15
    polje = [[0, 0] for i in range(25)]
    dodaj(1, 0, 2)
    dodaj(6, 1, 5)
    dodaj(8, 1, 3)
    dodaj(12, 0, 5)
    dodaj(13, 1, 5)
    dodaj(17, 0, 3)
    dodaj(19, 0, 5)
    dodaj(24, 1, 2)

####### Grafični vmesnik #######

class Plosca:                                       # Glavno okno z vsemi parametri
    global kocka
    global crni
    global beli
    global polje
    global kocke
    global igralec
    global nacin

    nacin = "pvp"
    igralec = 0

    polje = [[0, 0] for i in range(25)]
    crni = 0
    beli = 0
    kocke = [0, 0]
    kocka = -1    


    
    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        exec(gumbi())

        tocka0 = Button(frame, text = "Izgnani", height = 2, width = 8, command=kombinirajFunkcije(lambda: poteza(0), self.posodobi))
        tocka0.grid(row = 3, column = 9)
        
        self.navrsti = Label(frame, text = "")
        self.navrsti.grid(row = 1, column = 1, columnspan = 2)

        self.izgnani = Canvas(frame, height = 110, width = 66)
        self.izgnani.grid(row = 2, column = 9)

        self.izgnani.create_oval(8, 5, 58, 55, fill = "white" )
        self.izgnani.create_oval(8, 60, 58, 110, fill = "#3C3C3C" )

        self.izgnaniB = self.izgnani.create_text(33, 30, text = "0")
        self.izgnaniC = self.izgnani.create_text(33, 85, text = "0", fill = "white")

        self.kocka1 = Button(frame, text = "", height = 2, width = 8, command=kombinirajFunkcije(lambda: self.kockaj(0), self.posodobi))
        self.kocka1.grid(row = 2, column = 1)

        self.kocka2 = Button(frame, text = "", height = 2, width = 8, command=kombinirajFunkcije(lambda: self.kockaj(1), self.posodobi))
        self.kocka2.grid(row = 2, column = 2)

        self.koncaj = Button(frame, text = "Končaj potezo", height = 2, width = 16, command=kombinirajFunkcije(lambda: self.kockaj(-1), self.posodobi))
        self.koncaj.grid(row = 3, column = 1, columnspan = 2)

        self.levo = Canvas(frame, height = 400, width = 392, background = "white")
        self.levo.grid(row = 2, rowspan = 2, column = 3, columnspan = 6)
        exec(porisi("self.levo"))

        self.desno = Canvas(frame, height = 400, width = 392, background = "white")
        self.desno.grid(row = 2, rowspan = 2, column = 10, columnspan = 6)
        exec(porisi("self.desno"))

        exec(popisi())

        exec(figure())

        menu = Menu(master)
        master.config(menu=menu)

        file_menu = Menu(menu)
        menu.add_cascade(label="Možnosti", menu=file_menu)

        file_menu.add_command(label="Nova igra", command=kombinirajFunkcije(self.novaIgra, self.posodobi))
        file_menu.add_command(label="Proti računalniku", command=kombinirajFunkcije(lambda: self.nastavi("pve"),self.novaIgra, self.posodobi))
        file_menu.add_command(label="Proti igralcu", command=kombinirajFunkcije(lambda: self.nastavi("pvp"), self.novaIgra, self.posodobi))                         
        file_menu.add_separator()
        file_menu.add_command(label="Izhod", command=master.destroy)


    def nastavi(self, nastavitev):
        global nacin
        nacin = nastavitev

    def kockaj(self, a):                            # Funkcija, ki nastavi vrednost kocke na izbrano
        global kocka
        global igralec
        global kocke
        if kocke == [0, 0]:
            messagebox.showinfo("Nova igra", "Za nadaljevanje prosim začnite novo igro.")
            return
        if a == -1:
            if nacin == "pve":
                racunalnik()
                if crni == 0:
                    messagebox.showinfo("Zmaga", "Črni je zmagal!")
                    kocke = [0, 0]
                    return
                vrziKocke()
            else:
                igralec = (igralec + 1) % 2
                vrziKocke()
        elif len(kocke) > a:
            kocka = a

    def posodobi(self):                             # Funkcija, ki posodobi prikazano stanje
#        global igralec
        self.izgnani.itemconfig(self.izgnaniB, text = str(polje[0][0]))
        self.izgnani.itemconfig(self.izgnaniC, text = str(polje[0][1]))                     
        for i in range(1, len(polje)):              # Ta for zanka nastavi vidnost figur in besedila nad njimi
            if i in range(7, 19):
                k = [1 for i in range(polje[i][0])]
                l = [1 for i in range(polje[i][1])]
                k += [0, 0, 0, 0, 0]
                l += [0, 0, 0, 0, 0]   
                for j in range(1, 4):
                    exec('self.levo.itemconfig(self.krogB_{0}_{1}, state = {2})'.format(i, j, ["HIDDEN", "NORMAL"][k[j-1]]))
                if k[3]: exec('self.levo.itemconfig(self.t{0}, text = "+{1}")'.format(i, polje[i][0]-3))
                for j in range(1, 4): exec('self.levo.itemconfig(self.krogC_{0}_{1}, state = {2})'.format(i, j, ["HIDDEN", "NORMAL"][l[j-1]]))
                if l[3]: exec('self.levo.itemconfig(self.t{0}, text = "+{1}")'.format(i, polje[i][1]-3))
                if l[3] == k[3]: exec('self.levo.itemconfig(self.t{0}, text = "")'.format(i))
            else:
                k = [1 for i in range(polje[i][0])]
                l = [1 for i in range(polje[i][1])]
                k += [0, 0, 0, 0, 0]
                l += [0, 0, 0, 0, 0]
                for j in range(1, 4):
                    exec('self.desno.itemconfig(self.krogB_{0}_{1}, state = {2})'.format(i, j, ["HIDDEN", "NORMAL"][k[j-1]]))
                if k[4]: exec('self.desno.itemconfig(self.t{0}, text = "+{1}")'.format(i, polje[i][0]-3))
                for j in range(1, 4):
                    exec('self.desno.itemconfig(self.krogC_{0}_{1}, state = {2})'.format(i, j, ["HIDDEN", "NORMAL"][l[j-1]]))
                if l[4]: exec('self.desno.itemconfig(self.t{0}, text = "+{1}")'.format(i, polje[i][1]-3))
                if l[4] == k[4]: exec('self.desno.itemconfig(self.t{0}, text = "")'.format(i))

        if kocke != [0, 0]:                         # Nastavi prikazane vrednosti kock 
            if len(kocke) > 1:
                self.kocka1["text"] = str(kocke[0])
                self.kocka2["text"] = str(kocke[1])
            else:
                self.kocka1["text"] = str(kocke[0])
                self.kocka2["text"] = ""
            self.navrsti["text"] = "Na potezi je {0}.".format(["beli", "črni"][igralec])
        else:
                self.kocka1["text"] = ""
                self.kocka2["text"] = ""

    def novaIgra(self):                             # Funkcija, ki ponastavi stanje mize in določi začetnega igralca
        global nacin
        global igralec
        
        pravila1()
        vrziKocke()
        while kocke[0] == kocke[1]:
            vrziKocke()
        if kocke[1] > kocke[0]:
            if nacin == "pve":
                racunalnik(kocke)
                vrziKocke()
            else: igralec = 1
        else: igralec = 0

        
    
####### Pomožne funkcije - za generiranje vmesnika #######

def column(i):                                      # Določi vrsico gumba i
    if i < 13:
        if 13 - i > 6: return 16 - i
        else: return 15 - i
    else:
        if i - 12 > 6: return i - 9
        else: return i - 10

def row(i, j):                                      # Določi stolpec gumba i
    if i < 13:
        return 5 - j
    else:
        return j

def gumbi():                                        # Generator kode za postavljanje gumbov
    a = ""
    for i in range(1, 25):
        a += """self.tocka{0} = Button(frame, text = "{0}", height = 2, width = 8, command=kombinirajFunkcije(lambda: poteza({0}), self.posodobi))
self.tocka{0}.grid(row = {1}, column = {2})
""".format(i, row(i, 1) , column(i))
    return(a)

def porisi(l):                                      # Generator kode za trikotnike na igralni površini
    a = ""
    for i in range(6):
        a += """{0}.create_polygon({1}, 0, {2}, 0, {3}, 150, fill = "{4}", outline = "black")
{0}.create_polygon({1}, 400, {2}, 400, {3}, 250, fill = "{5}", outline = "black")
""".format(l, 66 * i, 66 * (i + 1), 66 * i + 33, ["#828282", "white"][i%2], ["#828282", "white"][(i+1)%2])
    return a

def popisi():                                       # Generator kode za napise nad trikotniki
    a = ""
    for i in range(1, 7):
        a += 'self.t{0} = self.desno.create_text({1}, 235, text = "")\n'.format(i, 431 - i * 66)
    for i in range(7, 13):
        a += 'self.t{0} = self.levo.create_text({1}, 235, text = "")\n'.format(i, 431 - (i - 6) * 66)
    for i in range(13, 19):
        a += 'self.t{0} = self.levo.create_text({1}, 165, text = "")\n'.format(i, 33 + (i - 13) * 66)
    for i in range(19, 25):
        a += 'self.t{0} = self.desno.create_text({1}, 165, text = "")\n'.format(i, 33 + (i - 19) * 66)
    return a

def figure():                                       # Generator kode za prikazovanje figur
    a = ""
    for j in range(1, 4):
        for i in range(1, 7):
            a += 'self.krogB_{0}_{1} = self.desno.create_oval({2}, {3}, {4}, {5}, outline = "black", fill = "white", state = HIDDEN)\n'.format(i, j, 392-((i-1)*66)-4, 400-j*50, 392-((i-1)*66+50)-4, 400-(j-1)*50)
            a += 'self.krogC_{0}_{1} = self.desno.create_oval({2}, {3}, {4}, {5}, outline = "black", fill = "#3C3C3C", state = HIDDEN)\n'.format(i, j, 392-((i-1)*66)-4, 400-j*50, 392-((i-1)*66+50)-4, 400-(j-1)*50)
        for i in range(7, 13):
            a += 'self.krogB_{0}_{1} = self.levo.create_oval({2}, {3}, {4}, {5}, outline = "black", fill = "white", state = HIDDEN)\n'.format(i, j, 392-((i-7)*66)-4, 400-j*50, 392-((i-7)*66+50)-4, 400-(j-1)*50)
            a += 'self.krogC_{0}_{1} = self.levo.create_oval({2}, {3}, {4}, {5}, outline = "black", fill = "#3C3C3C", state = HIDDEN)\n'.format(i, j, 392-((i-7)*66)-4, 400-j*50, 392-((i-7)*66+50)-4, 400-(j-1)*50)
        for i in range(13, 19):
            a += 'self.krogB_{0}_{1} = self.levo.create_oval({2}, {3}, {4}, {5}, outline = "black", fill = "white", state = HIDDEN)\n'.format(i, j, ((i-13)*66)+8, j*50-50, ((i-13)*66+50)+8, j*50)
            a += 'self.krogC_{0}_{1} = self.levo.create_oval({2}, {3}, {4}, {5}, outline = "black", fill = "#3C3C3C", state = HIDDEN)\n'.format(i, j, ((i-13)*66)+8, j*50-50, ((i-13)*66+50)+8, j*50)
        for i in range(19, 25):
            a += 'self.krogB_{0}_{1} = self.desno.create_oval({2}, {3}, {4}, {5}, outline = "black", fill = "white", state = HIDDEN)\n'.format(i, j, ((i-19)*66)+8, j*50-50, ((i-19)*66+50)+8, j*50)
            a += 'self.krogC_{0}_{1} = self.desno.create_oval({2}, {3}, {4}, {5}, outline = "black", fill = "#3C3C3C", state = HIDDEN)\n'.format(i, j, ((i-19)*66)+8, j*50-50, ((i-19)*66+50)+8, j*50)

    return a            

def kombinirajFunkcije(*funcs):                     # Funkcija, ki združi dane funkcije v novo funkcijo (izvedejo se zaporedno) - gumbi lahko tako izvajajo več ukazov hkrati
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func


        
root = Tk()

aplikacija = Plosca(root)

root.mainloop()
