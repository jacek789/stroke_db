from head import *

hp_db = read_object('hp_db')

""""
hp_db to słownik, gdzie kluczem jest np 'HP:0000005', a wartością obiekt HP

Przydatną metodą jest funkcja tree(), która rysuje drzewo od rodzica na którym została wywołana w dół.
Wyświetla ona id (klucz w słowniku), liczbę genów i nazwę

Inne metody:
    def get_children_ids(self)
    Zwraca ids dzieci
    
    def get_children(self):
    Zwraca dzieci danego węzła jako listę obiektów HP
    
    def get_parents_ids(self):
    Zwraca ids rodziców
    
    def get_parents(self):
    Zwraca rodziców danego węzła jako listę obiektów HP
    
    def get_genes(self, sort=False):
    Zwraca listę genów związanych z danym węzłem
    
    def get_children_genes(self, unique=False, sort=False):
    Zwraca listę genów związanych ze wszystkimi dzieciami danego węzła (bez genów węzła)
    
    def get_all_genes(self, unique=False, sort=False):
    Zwraca listę wszystkich genów (węzła i dzieci)
    
    def up(self, parent=''):
    Pozwala przejść do rodzica
    
    def down(self, child=''):
    Pozwala przejść do dziecka
    
    def tree(self, depth=-1, drop_empty=False):
    Rysuje drzewko.

    def dump(self, all_genes=False):
    Zapisuje geny do pliku
Np:
"""

print(hp_db['HP:0000005'].tree(depth=1, drop_empty=True))

print(hp_db['HP:0000005'].down(0).down('HP:0001452').get_genes())


