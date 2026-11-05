Ajout de skills pandas absents du notebook et ajout de fonctions qui répondent à des questions spécifiques
Voici la liste : 

| Je veux… | pandas |
|---|---|
| tester la fin d'un texte | `df["pos"].str.endswith("@PRO+Dem")` |
| tester le début d'un texte | `df["lemma"].str.startswith("զ@")` |
| enlever les espaces autour d'un texte | `df["tag"].str.strip()` |
| découper un texte sur un séparateur | `df["pos"].str.split("@")` |
| une ligne par élément d'une liste | `.explode()` |
| inverser un test | `~condition` |
| lire des lignes par leur index | `df.loc[index, "col"]`, `.index.unique()` |

`endswith` et `startswith` sont préférés à `contains` avec un `$` ou un `^` : `+` est un
symbole spécial dans une expression régulière, donc `@PRO+Dem` serait mal compris.

**Q4, étiquettes invalides.** Une étiquette composée est valide si chacune de ses parties l'est.
1. Lire le tagset, nettoyer les noms avec `.str.strip()`.
2. `parties = train["pos"].str.split("@").explode()` (l'index d'origine est conservé).
3. `invalides = parties[~parties.isin(valides)]`.
4. `train.loc[invalides.index.unique(), "pos"].value_counts()`.

**Q5, dictionnaire (partie 12).**
1. `dico = train[["form", "pos"]].drop_duplicates("form").rename(columns={"pos": "pos_dico"})`
2. `resultat = test.merge(dico, on="form", how="left")`
3. `round((resultat["pos"] == resultat["pos_dico"]).mean(), 2)`
Un mot absent du train donne `NaN`, donc une erreur : c'est voulu.

**Résultats de l'agent 
Les 5 réponses de l'agent : 

Q1: Top 5 des catégories (pos) les plus fréquentes dans le train
  V: 1008
  N+Com: 786
  I+Conj: 745
  I+Prep: 310
  A: 295

Q2: Proportion des mots du train avec formes composées (@ dans pos)
  Mots avec @ dans pos: 669/4712 (14.20%)

Q3: Top 5 des combinaisons les plus fréquentes
  N+Com@PRO+Dem: 166
  I+Prep@N+Com: 164
  I+Prep@N+Com@PRO+Dem: 76
  A@PRO+Dem: 41
  I+Prep@PRO+Dem: 37

Q4: Mots avec article suffixé (pos finit par @PRO+Dem) et lemmes commençant par զ@
  Mots avec pos finissant par @PRO+Dem: 383
  Lemmes commençant par զ@: 339

Q5: Étiquettes du train non présentes dans HYE_tagset.txt
  PRO+Pos3: 10

============================================================
DICTIONNAIRE (Partie 12 du notebook)
============================================================
Taille du dictionnaire: 2014 entrées

Score sur test in-domain: 0.5667
Score sur test out-of-domain: 0.5191
Baisse: 0.0476
Comparaison avec grec (0.73 → 0.51, baisse de 0.22):
  Baisse arménienne: 0.0476
  Baisse grecque: 0.22
  La baisse est MOINS importante qu'en grec
  
La consigne : 
Utilise le sous-agent analyste pour écrire scripts/analyser.py puis le lancer. Il doit afficher, sous un titre Q1 à Q5 : les 5 questions. 

Une erreur de l'agent : J'ai l'impression qu'il a assez bien exécuté les choses, je n'ai pas vu de mauvais filtre ni de fonction hors skills. 

En 3 lignes : qu'est-ce que l'agent apporte ici par rapport au notebook ? Qu'est-ce qu'il coûte ?
