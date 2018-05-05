from head import *


phenotype_to_genes = read_lines('annotation/ALL_SOURCES_ALL_FREQUENCIES_phenotype_to_genes.txt')
del phenotype_to_genes[0]

hps = read_lines("hp.obo")

parents = {}
parents['HP:0000001'] = HP('HP:0000001', parents)

# Matching phenotypes to genes
phenotypes = {}

manual_phenotype_to_gene = ['HP_0000001', 'HP_0000005', 'HP_0000118', 'HP_0012823']
for hp in manual_phenotype_to_gene:
    with open('annotation/genes_for_' + hp + '.csv') as hp_file:
        hp_file_lines = csv.reader(hp_file, quotechar='"')
        genes = []
        for row in hp_file_lines:
            genes.append(row[0].split(' ')[0])
        del genes[0:2]
        phenotypes[hp.replace('_', ':')] = genes

for line in phenotype_to_genes:
    line = line.split('\t')
    hp_id = line[0]
    gene = line[-1].strip()
    if hp_id in phenotypes:
        phenotypes[hp_id].append(gene)
    else:
        phenotypes[hp_id] = [gene]


# Building tree

for line in hps:
    line = line.strip()
    row = line.split(' ')
    if row[0] == 'id:':
        hp_id = row[1]
        last_id = hp_id
        if hp_id not in parents:
            parents[hp_id] = HP(hp_id, parents)
        last_child = parents[hp_id]
    elif row[0] == 'is_a:':
        hp_id = row[1]
        if hp_id not in parents:
            parents[hp_id] = HP(hp_id, parents)
        parents[hp_id].add_child(last_child)
        last_child.add_parent(hp_id)
    elif row[0] == 'name:':
        hp_id = row[1]
        parents[last_id].name = ' '.join(row[1:])

# Adding genes to leaves

for key in parents:
    if key in phenotypes:
        parents[key].genes = phenotypes[key]

write_object(parents, 'hp_db')


# TODO check whether parents' genes include all children's ones. NO! hp_p = 'HP:0000005', hp_c = 'HP:0010985' {'GPR101', 'AMMECR1'}
# TODO sprawdzić czy zwracanie przez referencje nie powoduje gdzieś problemów
