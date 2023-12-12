class convertion:

    def __init__(self):
        self.somme_a = 0        #   C'est la somme des aij
        

    # Récupération du fichier instance
    def loadFromFile(self, filename):
        file = open(filename, "r")
        lines = file.readlines()
        file.close()

    # division de la premiere ligne pour récupérer le nombre de convives et le nombre de relations
        self.nbConvives, self.nbRelations=int(lines[0].split()[0]), int(lines[0].split()[1])
        self.listeRelation = [[] for i in range(self.nbConvives)]  # ici je vois une erreur il en argument le nombre de relation et non le nbre de convives

        #print(f"N: {self.nbConvives}")
        #print(f"M: {self.nbRelations}")
        self.listeConvives = [0 for i in range(self.nbConvives)]
        
    # Récupère les valeurs i et affectation de son ci
        for i in range(self.nbConvives):
            numConvive = int(lines[i+1].split()[0])
            self.listeConvives[numConvive] = int(lines[i+1].split()[1])
            #print(f"i: {d} - Ci: {self.listeConvives[d]}")
    
    #   Creation matrice  a[i][j] et initilisation à 0
        self.a = [[0 for i in range(self.nbConvives)] for j in range(self.nbConvives)] 

    # Récupère les relations i et j des lignes restante sur M (si un convive en connait un autre)
        for j in range(self.nbConvives+1, self.nbConvives+self.nbRelations+1):
            convive1, convive2 = int(lines[j].split()[0]), int(lines[j].split()[1])
            self.listeRelation[convive1].append(convive2)
            self.a[convive1][convive2] = 1                      # Ajout de 1 dans la matrice a[i][j] pour chaque relation existante 


        #for i in range(self.nbConvives):
            #print(f"i : {i} ,Vi: {len(self.listeRelation[i])}, Ci: {self.listeConvives[i]}")

        
        self.tabRelation = [[0 for i in range(self.nbConvives)] for j in range(self.nbConvives)]
        for i in range(self.nbConvives):
            for j in range(i, self.nbConvives):
                if i == j:
                    self.tabRelation[i][j] = 0
                else:
                    if j in self.listeRelation[i]:
                        self.tabRelation[i][j] = 1
                    else:
                        self.tabRelation[i][j] = 0
        #for i in range(self.nbConvives):
            #print(f"{len(self.tabRelation[i])}")
    
    # Création du vecteur des coef xi de la contrainte (self.ligne = [coef_x1,coef_x2,coef_x3,...,coef_xN])
        self.ligne=[0 for i in range(self.nbConvives)]    

    # Réalisation de la contrainte
        for i in range(self.nbConvives):  # 1ere composante de l'équation 
            self.ligne[i] += self.nbConvives - 2

        for j in range(self.nbConvives):  #  2 e composante de l'équation (Elle est ajoutée à la 1ere)
            self.ligne[j] += self.nbConvives

        self.elt3 = -(self.nbConvives - 1)*self.nbConvives # 3e composante avant l'inégalité

        for i in range(self.nbConvives):  # sommation des a[i][j]
            for j in range(self.nbConvives):
                self.somme_a += self.a[i][j]
        self.somme_a = self.somme_a - self.elt3         # je soustrait la somme de a par le 3e élt
        
        

    def conversion(self, filename):
        
        with open(filename, "w") as filout: 
            # Ouverture du fichier
            filout.write("Maximize\n")  
            # Ecriture de la fonction Objectif
            for i in range(self.nbConvives):
                if i == 0:
                    filout.write(f" z: {self.listeConvives[i]} x{i+1} ")
                else:
                    filout.write(f"+ {self.listeConvives[i]} x{i+1} ")
            filout.write("\nSubject To\n")
            for i in range(self.nbConvives):
                if i == 0:
                    filout.write(f" poids: {self.ligne[i]} x{i+1} ")
                else:
                    filout.write(f"+ {self.ligne[i]} x{i+1} ")
                 
            filout.write(f"<= {self.somme_a}")              #Ecriture de somme_a

            filout.write("\nBinaries\n")
            # Ecriture des variables
            for i in range(self.nbConvives):
                filout.write(f" x{i+1}\n")
            filout.write("End") 
            # Fin du fichier lp
