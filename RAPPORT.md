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

