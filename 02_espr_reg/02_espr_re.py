import random
import re

elenco_studenti = [
    {"nome": "Marco", "cognome": "Arlotti"},
    {"nome": "Angelo", "cognome": "Berlini"},
    {"nome": "Luca", "cognome": "Bernardini"},
    {"nome": "Alberto", "cognome": "Bruscolini"},
    {"nome": "Francesco", "cognome": "Cervesi"},
    {"nome": "Marco", "cognome": "Clementi"},
    {"nome": "Romeo", "cognome": "D'Angelosante"},
    {"nome": "Alessandro", "cognome": "Del Baldo"},
    {"nome": "Ibragimov", "cognome": "Kamil"},
    {"nome": "Amin", "cognome": "Kriouech"},
    {"nome": "Simon", "cognome": "Kola"},
    {"nome": "Matteo", "cognome": "Massa"},
    {"nome": "Cristian", "cognome": "Monticelli"},
    {"nome": "Eldar", "cognome": "Nedria"},
    {"nome": "Lorenzo", "cognome": "Pezzolesi"},
    {"nome": "Luca", "cognome": "Pontellini"},
    {"nome": "Nicolo", "cognome": "Romagna"},
    {"nome": "Alessandro", "cognome": "Sanchi"},
    {"nome": "Luca", "cognome": "Santini"},
    {"nome": "Diego", "cognome": "Torsani"},
]


def estrai_3_studenti(elenco, pattern=".*"):
    regex = re.compile(pattern, re.IGNORECASE)
    
    studenti_filtrati = []
    for studente in elenco:
        nome_cognome = f"{studente['nome']} {studente['cognome']}"
        if regex.search(nome_cognome):
            studenti_filtrati.append(studente)
    
    if len(studenti_filtrati) <= 3:
        studenti_selezionati = studenti_filtrati
    else:
        studenti_selezionati = random.sample(studenti_filtrati, 3)
    
    return studenti_selezionati


if __name__ == "__main__":
    pattern = "el"
    
    studenti = estrai_3_studenti(elenco_studenti, pattern)
    print(f"Studenti selezionati per l'interrogazione ({len(studenti)}):")
    for idx, studente in enumerate(studenti, 1):
        print(f"  {idx}. {studente['nome']} {studente['cognome']}")
