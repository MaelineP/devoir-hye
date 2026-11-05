---
name: pandas-tuto
description: À charger avant d'écrire scripts/analyser.py
---

Seules les fonctions pandas ci-dessous sont autorisées. On travaille sur des colonnes
entières : pas de boucle `for` sur les lignes d'un tableau.
Colonnes des TSV : `text_form`, `form`, `lemma`, `pos`.

| Je veux… | pandas |
|---|---|
| lire un TSV | `pd.read_csv(chemin, sep="\t")` |
| voir le début, la fin | `df.head()`, `df.tail()` |
| connaître la taille, les colonnes | `df.shape`, `df.columns`, `df.info()` |
| un résumé | `df.describe()` |
| une colonne, plusieurs colonnes | `df["col"]`, `df[["col1", "col2"]]` |
| compter les valeurs | `df["col"].value_counts()`, `.nunique()`, `.unique()` |
| filtrer des lignes | `df[df["col"] == valeur]`, `df[(condition1) & (condition2)]` |
| ajouter une colonne | `df["nouvelle"] = ...`, `.str.len()`, `.str.contains("@")` |
| trier | `df.sort_values("col", ascending=False)` |
| calculer par groupe | `df.groupby("col")["autre"].mean()` |
| réunir plusieurs tableaux | `pd.concat(liste_de_tableaux, ignore_index=True)` |
| tableau croisé | `pd.crosstab(df["col1"], df["col2"])` |
| tester l'appartenance | `df["col"].isin(autre_liste)` |
| associer deux tableaux | `df.merge(autre, on="col", how="left")` |
| renommer, dédoublonner | `df.rename(columns={"a": "b"})`, `df.drop_duplicates("col")` |
| enregistrer | `df.to_csv("fichier.csv", index=False)` |
| compter les True, proportion de True | `.sum()`, `.mean()` sur une colonne de booléens |
| comparer deux colonnes | `df["a"] == df["b"]`, `df["a"] != df["b"]` |

Python de base autorisé : `print`, `len`, `round`.

## Ajouts (absents du notebook)

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

## Recettes

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
