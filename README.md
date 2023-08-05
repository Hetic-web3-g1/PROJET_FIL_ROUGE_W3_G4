[![Test backend](https://github.com/Hetic-web3-g1/PROJET_FIL_ROUGE_W3_G4/actions/workflows/test-backend.yml/badge.svg)](https://github.com/Hetic-web3-g1/PROJET_FIL_ROUGE_W3_G4/actions/workflows/test-backend.yml)

# PROJET_FIL_ROUGE_W3_G4

## Présentation de l’équipe

FERRIER Sammy → Front / Repo / Design

JANKOWSKI Jonas → Front / Design

JOURDA Jérémie → CTO / Backend / Cloud

THIBORD Alexandre → Front / Design

SION Martin → CEO / Back / Devops

---

## Présentation du projet

La mission de la Saline Royale Academy est d'aider les musiciens à se former et à progresser dans leur carrière en leur donnant accès aux enseignements des meilleurs professeurs, où qu'ils soient.

Actuellement, la Saline Royale Academy dispose d'un site web conçu comme une plateforme médiatique. Cependant, pour mieux répondre aux besoins des utilisateurs, il est prévu de le transformer en une plateforme pédagogique efficace pour la formation musicale.

[https://www.salineacademy.com/](https://www.salineacademy.com/)

Dans le cadre de cette évolution, nous allons développer une solution numérique permettant une gestion optimale des contenus du projet. Cette solution facilitera le suivi du processus de production, notamment le montage des vidéos, la préparation des masterclass et l'enregistrement des cours. Elle permettra également de gérer les différents contenus et versions associées de manière simple et efficace.

L'interface de cette solution sera accessible à travers une API, ce qui facilitera son intégration avec le site existant et d'autres écosystèmes.

---

## Lancement du Projet

#### **En développement :**

`docker-compose -f docker-compose.yml up -d --build`

#### **En production :**

`docker compose -f docker-compose.override.yml up -d --build`

## Test de l'API

`pytest /tests`
