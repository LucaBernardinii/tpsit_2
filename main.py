from espr_reg import EsprReg

espressione = EsprReg()
espressione.set_pattern(r'(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(19[0-9][0-9]|20[0-1][0-9]|20[2][0-5])') # pattern per date italiane dal 1900 al 2025
risultato = espressione.validate("31/12/2020")
print(risultato)