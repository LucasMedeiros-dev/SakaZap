import openpyxl


def corrigir_numero(numero):
    for caractere in numero:
        if not caractere.isdigit():
            numero = numero.replace(caractere, "")
        if len(numero) == 12:
            ddd = numero[1:3]
            numero = numero[3:]

        if len(numero) == 9:
            return f"+55{ddd}{numero}"

        if len(numero) == 8:
            f"+55{ddd}9{numero}"


def buscar_nome_telefone(arquivo):
    wb = openpyxl.load_workbook(arquivo)
    ws = wb.active
    tupla_nomes_telefones = []
    for row in ws.iter_rows(values_only=True):
        dia = row[0]
        nome = row[1]
        telefone = row[2]
        celular = row[3]

        try:
            int(row[0])
        except:
            continue

        if celular:
            telefone = celular

        if telefone:
            pass

        if not telefone:
            continue

        telefone = corrigir_numero(telefone)
        primeiro_nome = nome.split(" ")[0].capitalize()

        tupla_nomes_telefones.append((dia, nome, primeiro_nome, telefone))
    return tupla_nomes_telefones
