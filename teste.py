import csv

# Define the path to your CSV file
file_path = "relclientes_aniversariantes.csv"

# Open the CSV file
tupla_nomes_telefones = []
with open(file_path, newline="") as csvfile:
    # Create a CSV reader object
    csvreader = csv.reader(csvfile, delimiter=",")

    # Process each row in the CSV file
    for row in csvreader:
        dia = row[12]
        nome = row[13]
        telefone = row[14]
        celular = row[15]

        if not (telefone or celular):
            continue

        if celular:
            telefone = celular

        primeiro_nome = nome.split(" ")[0].capitalize()

        tupla_nomes_telefones.append((dia, nome, primeiro_nome, telefone))

    print(tupla_nomes_telefones)
