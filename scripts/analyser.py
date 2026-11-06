#!/usr/bin/env python3
"""Analyse du corpus arménien HYE_train.tsv"""

import pandas as pd
from collections import Counter
import os

# Chemins des fichiers
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
TRAIN_FILE = os.path.join(DATA_DIR, 'HYE_train.tsv')
TAGSET_FILE = os.path.join(DATA_DIR, 'HYE_tagset copie.txt')
TEST_IN = os.path.join(DATA_DIR, 'HYE_test_in-domain.tsv')
TEST_OUT = os.path.join(DATA_DIR, 'HYE_test_out-of-domain.tsv')

# Lire les données
df_train = pd.read_csv(TRAIN_FILE, sep='\t')
df_test_in = pd.read_csv(TEST_IN, sep='\t')
df_test_out = pd.read_csv(TEST_OUT, sep='\t')

# Lire le tagset
with open(TAGSET_FILE, 'r', encoding='utf-8') as f:
    tagset_lines = f.readlines()

# Extraire les étiquettes du tagset (en normalisant: on enlève les espaces finales)
tagset_tags = set()
tagset_tags_with_space = set()
for line in tagset_lines:
    if '\t' in line:
        tag = line.split('\t')[0]
        # Garder à la fois la version avec espace et sans espace pour la comparaison
        tagset_tags.add(tag.rstrip())  # Version normalisée (sans espace finale)
        tagset_tags_with_space.add(tag)  # Version originale

print("=" * 60)
print("ANALYSE DU CORPUS ARMÉNIEN")
print("=" * 60)

# Q1: Top 5 des catégories (pos) les plus fréquentes
print("\nQ1: Top 5 des catégories (pos) les plus fréquentes dans le train")
pos_counts = df_train['pos'].value_counts()
top5_pos = pos_counts.head(5)
for pos, count in top5_pos.items():
    print(f"  {pos}: {count}")

# Q2: Proportion des mots avec formes composées (@ dans pos)
print("\nQ2: Proportion des mots du train avec formes composées (@ dans pos)")
composed_count = df_train[df_train['pos'].str.contains('@', na=False)].shape[0]
total_count = len(df_train)
proportion = composed_count / total_count * 100
print(f"  Mots avec @ dans pos: {composed_count}/{total_count} ({proportion:.2f}%)")

# Q3: Top 5 des combinaisons les plus fréquentes
print("\nQ3: Top 5 des combinaisons les plus fréquentes")
composed_pos = df_train[df_train['pos'].str.contains('@', na=False)]['pos']
composed_counts = composed_pos.value_counts()
top5_composed = composed_counts.head(5)
for pos, count in top5_composed.items():
    print(f"  {pos}: {count}")

# Q4: Mots avec article suffixé et lemmes commençant par ز
print("\nQ4: Mots avec article suffixé (pos finit par @PRO+Dem) et lemmes commençant par զ@")
# Mots avec article suffixé (pos finit par @PRO+Dem)
article_suffixe_count = df_train[df_train['pos'].str.endswith('@PRO+Dem', na=False)].shape[0]
print(f"  Mots avec pos finissant par @PRO+Dem: {article_suffixe_count}")

# Lemmes commençant par զ@ (note: զ est le caractère arménien 'ze')
lemma_ze_count = df_train[df_train['lemma'].str.startswith('զ@', na=False)].shape[0]
print(f"  Lemmes commençant par զ@: {lemma_ze_count}")

# Q5: Étiquettes du train non présentes dans le tagset
print("\nQ5: Étiquettes du train non présentes dans HYE_tagset.txt")

# Fonction pour vérifier si une étiquette (ou ses parties) est dans le tagset
def is_tag_valid(tag, tagset):
    """Vérifie si une étiquette est valide selon les règles :
    - Si simple: doit être dans le tagset (en normalisant les espaces)
    - Si composée (@): chaque partie doit être dans le tagset (normalisée)
    """
    if '@' not in tag:
        # Étiquette simple: vérifier si elle existe dans le tagset (avec ou sans espace finale)
        return tag in tagset or tag + ' ' in tagset_tags_with_space
    else:
        # Étiquette composée: vérifier chaque partie
        parts = tag.split('@')
        for part in parts:
            # Chaque partie doit exister dans le tagset
            if part not in tagset and part + ' ' not in tagset_tags_with_space:
                return False
        return True

# Trouver les étiquettes uniques dans le train
train_tags = df_train['pos'].unique()

# Trouver celles qui ne sont pas valides selon le tagset
invalid_tags = {}
for tag in train_tags:
    if not is_tag_valid(tag, tagset_tags):
        count = (df_train['pos'] == tag).sum()
        invalid_tags[tag] = count

# Afficher par ordre décroissant
if invalid_tags:
    for tag, count in sorted(invalid_tags.items(), key=lambda x: x[1], reverse=True):
        print(f"  {tag}: {count}")
else:
    print("  Aucune étiquette invalide trouvée")

# Dictionnaire de la partie 12
print("\n" + "=" * 60)
print("DICTIONNAIRE (Partie 12 du notebook)")
print("=" * 60)

# Créer le dictionnaire: pour chaque form, on prend le pos le plus fréquent
form_pos_counter = Counter()
for _, row in df_train.iterrows():
    form_pos_counter[(row['form'], row['pos'])] += 1

dictionary = {}
for (form, pos), count in form_pos_counter.most_common():
    if form not in dictionary:
        dictionary[form] = pos
    # Si on a déjà une entrée, on garde la plus fréquente
    # (déjà trié par most_common, donc la première est la plus fréquente)

print(f"Taille du dictionnaire: {len(dictionary)} entrées")

# Évaluer sur le test in-domain
def evaluate(dictionary, df_test):
    correct = 0
    total = len(df_test)
    for _, row in df_test.iterrows():
        form = row['form']
        true_pos = row['pos']
        if form in dictionary:
            predicted_pos = dictionary[form]
            if predicted_pos == true_pos:
                correct += 1
    return correct / total if total > 0 else 0

score_in = evaluate(dictionary, df_test_in)
score_out = evaluate(dictionary, df_test_out)

print(f"\nScore sur test in-domain: {score_in:.4f}")
print(f"Score sur test out-of-domain: {score_out:.4f}")
print(f"Baisse: {score_in - score_out:.4f}")
print(f"Comparaison avec grec (0.73 → 0.51, baisse de 0.22): ")
print(f"  Baisse arménienne: {score_in - score_out:.4f}")
print(f"  Baisse grecque: 0.22")
if (score_in - score_out) <= 0.22:
    print(f"  La baisse est MOINS importante qu'en grec")
else:
    print(f"  La baisse est PLUS importante qu'en grec")
