# eud-portugues

This repo gives access to the rules developed to annotate sentences in Portuguese with Enhanced Universal Dependencies (EUD) as well as Extended Enhanced Universal Dependencies (EEUD).

More info on EUD: [https://universaldependencies.org/u/overview/enhanced-syntax.html](https://universaldependencies.org/u/overview/enhanced-syntax.html)

More info on EEUD: [https://aclanthology.org/2025.udw-1.16.pdf](https://aclanthology.org/2025.udw-1.16.pdf)

# References

* [https://eud-portugues.souelvis.dev](https://eud-portugues.souelvis.dev) - Demonstration of the User Interface

* DE SOUZA, Elvis A.; DURAN, Magali S.; NUNES, Maria das Graças V.; SAMPAIO, Gustavo; BELASCO, Giovanna; PARDO, Thiago A. S.. Automatic Annotation of Enhanced Universal Dependencies for Brazilian Portuguese. In: SIMPÓSIO BRASILEIRO DE TECNOLOGIA DA INFORMAÇÃO E DA LINGUAGEM HUMANA (STIL), 15. , 2024, Belém/PA. Anais […]. Porto Alegre: Sociedade Brasileira de Computação, 2024. p. 217-226. DOI: https://doi.org/10.5753/stil.2024.245342. - Paper reporting the rules development

# Instructions

1) Install Grew, the graph rewriting tool:

https://grew.fr/usage/install/

2) Install the Python 3 requirements:

`pip3 install -r requirements.txt`

3.a) OPTIONAL: In order to run the User Interface:

`flask run`

3.b) OPTIONAL: In order to use the application in command-line:

`cd flask`

`python3 app.py {conllu_path} {rules_path} {strategy} [udpipe_model] > {out_path}`

Examples:

a) Annotate UD parsed sentences from `sentences.conllu` using the `eud_portuguese` strategy for Portuguese EUD:

`python3 app.py sentences.conllu conjunto_regras_porttinari.grs eud_portuguese > out.conllu`

b) Annotate raw sentences from `sentences.txt` using Porttinari 2.15 for UD Portuguese parsing and the `eud_portuguese` strategy for Portuguese EUD:

`python3 app.py sentences.txt conjunto_regras_porttinari.grs eud_portuguese portuguese-porttinari-ud-2.15-241121 > out.conllu`

c) Annotate raw sentences from `sentences.txt` using Porttinari 2.15 for UD Portuguese parsing and `eud_portuguese_extended` for Portuguese EEUD:

`python3 app.py sentences.txt conjunto_regras_porttinari.grs eud_portuguese_extended portuguese-porttinari-ud-2.15-241121 > out.conllu`