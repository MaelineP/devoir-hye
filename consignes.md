# Devoir maison : un mini-analyste pandas pour l'arménien classique (HYE)

## L'idée

En cours, un agent `evaluateur` écrivait et lançait `scripts/evaluer.py`. Vous allez construire un système du même type, en plus petit : un agent `analyste` qui répond à des questions sur le corpus arménien (`HYE`) **uniquement** en écrivant et en lançant un script pandas.

Aucun appel d'API n'est nécessaire : créez le fichier `.env` dans ce dépôt pour l'éliminer dans le .gitignore mais on ne s'en servira pas.

## Le dépôt

```
devoir-hye/
├── consignes.md                      ← ce fichier
├── AGENTS.md                         ← squelette à compléter
├── .gitignore                        ← à écrire
├── pyproject.toml, uv.lock           ← créés par uv
├── data/                             ← à récupérer dans le dépôt du cours
│   ├── HYE_train.tsv
│   ├── HYE_test_in-domain.tsv
│   ├── HYE_test_out-of-domain.tsv
│   └── HYE_tagset.txt
├── scripts/analyser.py               ← écrit par l'agent, pas par vous
├── RAPPORT.md                        ← à écrire
└── .vibe/
    ├── agents/analyste.toml          ← squelette à compléter
    └── skills/
        ├── pandas-tuto/SKILL.md      ← squelette à compléter
        └── tagset/                   ← fourni, à ne pas modifier
            ├── SKILL.md
            └── references/HYE_tagset.txt
```

## 1. Mise en place

1. **L'environnement.** À la racine du dépôt, lancez seulement ces deux commandes :
   ```bash
   uv init --python 3.12
   uv add pandas
   ```
2. **Les données.** Copiez les fichiers du dépôt du cours dans `data/`,

   HYE_train.tsv
   HYE_test_in-domain.tsv
   HYE_test_out-of-domain.tsv
   HYE_tagset.txt

3. **Le `.gitignore`.** Il doit au moins empêcher de commiter l'environnement virtuel (`.venv/`), les caches Python et tout fichier `.env`. Vérifiez avec `git status` avant votre premier commit.

## 2. Ce que vous complétez

1. **`AGENTS.md`** (10 lignes au plus) : l'objectif du projet en une phrase, puis 3 ou 4 règles. Pensez à :
   - comment lancer Python ;
   - d'où doivent venir les chiffres ;
   - ce que l'agent n'a pas le droit de lire.
2. **`.vibe/agents/analyste.toml`** : un sous-agent qui écrit `scripts/analyser.py` puis le lance.
   - Sa liste de commandes autorisées (`allowlist`) ne contient que `uv run python scripts/analyser.py`.
   - Il fait 3 essais au plus et répond en 5 lignes.
3. **`.vibe/skills/pandas-tuto/SKILL.md`** : la liste des fonctions pandas que l'agent a le droit d'utiliser.
   - Partez du tableau récapitulatif du notebook.
   - Si une question demande une fonction absente du notebook, ajoutez-la au tableau et signalez-le dans votre rapport.
   - L'agent travaille sur des colonnes entières : pas de boucle `for` sur les lignes d'un tableau.

**Ne modifiez pas** la skill `tagset`.

## 3. Les questions

`scripts/analyser.py` doit afficher, sous un titre `Q1` à `Q5`, la réponse aux questions suivantes :

1. Quelles sont les 5 catégories (`pos`) les plus fréquentes dans le train ?
2. Quelle proportion des mots du train sont des formes composées (`@` dans `pos`) ? Quelles sont les 5 combinaisons les plus fréquentes ?
3. Combien de mots du train se terminent par l'article suffixé (`pos` qui finit par `@PRO+Dem`) ? Combien commencent par la préposition `զ` (`lemma` qui commence par `զ@`) ?
4. Quelles étiquettes du train **ne figurent pas** dans `HYE_tagset.txt`, et combien de fois chacune apparaît-elle ? Attention à deux pièges :
   - certains noms d'étiquettes du tagset se terminent par une espace ;
   - une étiquette composée est valide si chacune de ses parties l'est.
5. Refaites le **dictionnaire** de la partie 12 du notebook, avec le train arménien. Quel score obtient-il sur le test `in-domain`, puis sur le test `out-of-domain` ? Le score baisse-t-il autant qu'en grec (0,73 contre 0,51) ?

## 4. Le rapport : `RAPPORT.md`

- Les 5 réponses, copiées depuis la sortie du script.
- La consigne exacte que vous avez donnée à l'agent.
- **Une erreur de l'agent** : ce qu'il a fait de travers (mauvais filtre, boucle interdite, fonction hors skill, chiffre inventé…) et ce que vous avez changé dans `AGENTS.md`, le `.toml` ou la skill pour la corriger.
- Les fonctions que vous avez ajoutées à la skill `pandas-tuto`, s'il y en a.
- En 3 lignes : qu'est-ce que l'agent apporte ici par rapport au notebook ? Qu'est-ce qu'il coûte ?

## 5. Avant de rendre

- [ ] `uv run python scripts/analyser.py` fonctionne depuis un clone neuf du dépôt.
- [ ] Il n'y a ni `.venv/` ni `.env` dans le dépôt.
- [ ] `pyproject.toml` et `uv.lock` sont commités.
- [ ] Le script n'a pas été écrit à la main : il vient de l'agent, éventuellement corrigé après vos modifications de `AGENTS.md`, du `.toml` ou de la skill.