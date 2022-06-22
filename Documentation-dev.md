# BibTex To Sparklis - Documentation dévelopement

## Installation

### Prérequis

Certain programmes sont nécessaires pour l'utilisation de BibTexToSparklis:

- [ ] [Git (Optionnel)](https://git-scm.com/downloads) : Pour cloner le projet
- [ ] [Docker](https://www.docker.com/community-edition) : Pour lancer les serveurs
- [ ] [Yarn](https://yarnpkg.com/) : Pour l'interface web
- [ ] [Node.js](https://nodejs.org/) : Pour l'interface web

### Téléchargement

```bash
# Récupération du projet (via ssh)
$ git clone git@github.com:pH0xe/septime.git 
```

```bash
# OU (via HTTPS)
$ git clone https://github.com/pH0xe/septime.git
```

### Mise en place des fichiers d'environnement

#### Dossier __racine__

1. Copier le fichier `.env.sample` dans le fichier `.env`
2. Dans le fichier `.env` :
   - Mettre un mot de passe fort pour `POSTGRES_ADMIN_PASSWORD`
   - Mettre un mot de passe fort pour `BIBTEX_USER_PASSWORD`

#### Dossier __bibtex-to-rdf__

1. Copier le fichier `.env.sample` dans le fichier `.env`
2. Dans le fichier `.env` :
    - Mettre `bibtex-user` dans `POSTGRESQL_USERNAME`
    - Mettre le mot de passe définit dans `BIBTEX_USER_PASSWORD` dans `POSTGRESQL_PASSWORD`
    - Mettre `postgres` dans `POSTGRESQL_HOST`
    - Mettre `5432` dans `POSTGRESQL_PORT`
    - Mettre `bibtex-project` dans `POSTGRESQL_DB`

#### Dossier __auth-service__

1. Copier le fichier `.env.sample` dans le fichier `.env`
2. Dans le fichier `.env` :
    - Mettre `bibtex-project` dans `DBNAME`
    - Mettre `bibtex-user` dans `DBUSER`
    - Mettre le mot de passe définit dans `BIBTEX_USER_PASSWORD` dans `DBPASSWORD`
    - Mettre `postgres` dans `DBHOST`
    - Mettre `5432` dans `DBPORT`
    - Mettre un mot de passe fort pour `AUTHSECRET` (Utiliser pour la génération de token JWT)
    - Mettre un mot de passe fort pour `ADMIN_PASSWORD` (Mot de passe par défaut de l'administrateur)

#### Dossier __gateway__

1. Copier le fichier `.env.sample` dans le fichier `.env`
2. Dans le fichier `.env` :
    - Mettre Le meme mot de passe dans `AUTHSECRET` que celui mis dans le dossier __auth-service__

### Lancement

Pour lancer le serveur il suffit de lancer le script `launch-dev.sh`
```bash	
./launch-dev.sh
```
Dans certain cas le script n'est pas executable après un clone. Il faut donc le rendre executable.
```bash	
chmod +x launch-dev.sh
```
