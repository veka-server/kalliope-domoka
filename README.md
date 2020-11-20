# Domoka API

## Synopsis 

Interface for my DIY domotique

## Brain example

```yaml
---
  - name: "domoka-test-1"
    signals:
      - order:
          text: "{{ action }} le chauffage {{ room }}"
          matching-type: 'ordered-strict'
          stt-correction:
            - input: "la température"
              output: "le chauffage"
            - input: "radiateur"
              output: "chauffage"
    neurons:
      - domoka:
          url: "domoka.local"
          room: "{{ room }}"
          action: "{{ action }}"
          answers:
            - "C'est fait"
            - "Pas de souci"
            - "Je m'en occupe"
            - "Terminé"
          action_augmentation:
            - "monte"
            - "augmente"
            - "boost"
          action_diminution:
            - "baisse"
            - "diminue"
            - "ralenti"
          action_information:
            - "quelle est"
            - "quel est"
            - "donne moi"
          answer_information: "La température {{ room }} et de ## temperature ## degré"
          action_unknown:
            - "Je n'ai pas compris votre commande"
```

## Installation
```bash
kalliope install --git-url https://github.com/veka-server/kalliope-domoka.git
```

## Desinstallation
```bash
kalliope uninstall --neuron-name domoka
```

Pour plus d'info : https://kalliope-project.github.io/kalliope/brain/community_modules/
