# PROJET_FIL_ROUGE_W3_G4

[![Test backend](https://github.com/Hetic-web3-g1/PROJET_FIL_ROUGE_W3_G4/actions/workflows/test-backend.yml/badge.svg)](https://github.com/Hetic-web3-g1/PROJET_FIL_ROUGE_W3_G4/actions/workflows/test-backend.yml)

## Sommaire

- [PROJET\_FIL\_ROUGE\_W3\_G4](#projet_fil_rouge_w3_g4)
  - [Sommaire](#sommaire)
  - [Présentation de l’équipe](#présentation-de-léquipe)
  - [Présentation du projet](#présentation-du-projet)
  - [Lancement du Projet](#lancement-du-projet)
    - [**En développement :**](#en-développement-)
    - [**En production :**](#en-production-)
  - [Test de l'API](#test-de-lapi)
  - [Conditions Légales](#conditions-légales)
  - [Documentation Backend](#documentation-backend)

## Présentation de l’équipe

FERRIER Sammy → Front / Repository / Design

JANKOWSKI Jonas → Front / Design

JOURDA Jérémie → CTO / Backend / Cloud

THIBORD Alexandre → Front / Design

SION Martin → CEO / Back / Devops / Design

---

## Présentation du projet

La mission de la Saline Royale Academy est d'aider les musiciens à se former et à progresser dans leur carrière en leur donnant accès aux enseignements des meilleurs professeurs, où qu'ils soient.

Actuellement, la [Saline Royale academy](https://www.salineacademy.com/) dispose d'un site web conçu comme une plateforme médiatique. Cependant, pour mieux répondre aux besoins des utilisateurs, il est prévu de le transformer en une plateforme pédagogique efficace pour la formation musicale.

Dans le cadre de cette évolution, nous allons développer une solution numérique permettant une gestion optimale des contenus du projet. Cette solution facilitera le suivi du processus de production, notamment le montage des vidéos, la préparation des masterclass et l'enregistrement des cours. Elle permettra également de gérer les différents contenus et versions associées de manière simple et efficace.

L'interface de cette solution sera accessible à travers une API, ce qui facilitera son intégration avec le site existant et d'autres écosystèmes.

Dans le cadre de cette évolution, nous avons développé une solution numérique permettant une gestion optimale des contenus du projet. Cette solution facilite le suivi du processus de production et la préparation des masterclass. Elle permet également de gérer les différents contenus et leur versionning associé de manière simple et efficace.

La solution comporte une API publique permettant d'accéder aux différents contenus et la création de certains types de données, facilitant ainsi son intégration avec le site existant et d'autres écosystèmes.

---

## Lancement du Projet

### **En développement :**

**Compléter fichier env :**
`backend/.env.development` & `frontend/.env.development`

**Lancer le projet (a la racine) :**
`ENVIRONMENT=development docker compose -f docker-compose.yml -p projet_fil_rouge_dev up -d --build`

### **En production :**

**Compléter fichier env :** `backend/.env.production` & `frontend/.env.production`	

**Lancer le projet (a la racine) :** `ENVIRONMENT=production docker compose -f docker-compose.override.yml -p projet_fil_rouge_prod up -d --build`

---

## Test de l'API

`pytest /tests`

---

## Conditions Légales

Les présentes conditions légales régissent l'utilisation du projet étudiant PROJET_FIL_ROUGE_W3_G4. Veuillez lire attentivement ces conditions avant d'utiliser le projet. En accédant ou en utilisant le projet, vous acceptez d'être lié par ces conditions.

Lien vers les [Conditions Légales](.readme/conditions_legales.md).

## [Documentation Backend](.readme/backend.md)