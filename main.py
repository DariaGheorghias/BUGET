tranzactii=[
    {"id":1,"tip":"venit","categorie":"Salariu","suma":100},
    {"id":2,"tip":"cheltuiala","categorie":"Alimente","suma":20}
]
def calculeaza_sold(lista_tranzactii):
    sold=0
    for cnt in lista_tranzactii:
        if cnt["tip"]=="venit":
            sold += cnt["suma"]
        elif cnt["tip"]=="cheltuiala":
            sold -=cnt["suma"]
    return sold
sold_curent=calculeaza_sold(tranzactii)
print(f"Soldul curent este:{sold_curent}")