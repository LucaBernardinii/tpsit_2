import re

class EsprReg:
    def __init__(self):
        self.pattern = ""

    # definisce il pattern da utilizzare per la verifica di valudazione
    def set_pattern(self, pattern: str):
        self.pattern = pattern

    # il metodo validate prende una stringa in input e verifica se c'è un match con il pattern
    def validate(self, string:str):
        if re.match(self.pattern, string):
            return "Match"
        else:
            return "Mismatch"
