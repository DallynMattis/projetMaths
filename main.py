from convertion import convertion  
import sys

if __name__ == "__main__":
    print("TO DO")
    modele = convertion()
    modele.loadFromFile(sys.argv[1])
    modele.conversion(sys.argv[2])
    


