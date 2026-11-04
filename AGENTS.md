# Mini-analyste pandas : arménien classique (HYE)

Répondre à des questions chiffrées sur le corpus HYE en écrivant et lançant un script pandas.

## Règles
- Python : `uv run python scripts/analyser.py`. Jamais `pip`, `python` seul ni `python -c`.
- Tout chiffre vient de pandas, via la sortie de `analyser.py`. Jamais de chiffre inventé.
- Ne pas lire `data/*.tsv` ni `.env` directement : passer par le script.
- Pandas sur colonnes entières, pas de boucle `for` ; seulement les fonctions de la skill `pandas-tuto`.
- Ne pas modifier la skill `tagset`.

## Rôles
- Répondre aux questions du RAPPORT.md et lancer le scriot pandas, agent `analyste`

## Repères
- Données : `data/HYE_train.tsv`, `data/HYE_test_in-domain.tsv`, `data/HYE_test_out-of-domain.tsv`, colonnes `text_form form lemma pos`.
- Tagset : `data/HYE_tagset.txt` (étiquette, tabulation, définition).