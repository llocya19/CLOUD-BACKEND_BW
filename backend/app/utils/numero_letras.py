UNIDADES = (
    '', 'UNO', 'DOS', 'TRES', 'CUATRO', 'CINCO', 'SEIS',
    'SIETE', 'OCHO', 'NUEVE', 'DIEZ', 'ONCE', 'DOCE',
    'TRECE', 'CATORCE', 'QUINCE', 'DIECISÉIS', 'DIECISIETE',
    'DIECIOCHO', 'DIECINUEVE', 'VEINTE'
)

DECENAS = (
    'VEINTI', 'TREINTA', 'CUARENTA', 'CINCUENTA',
    'SESENTA', 'SETENTA', 'OCHENTA', 'NOVENTA'
)

CENTENAS = (
    'CIENTO', 'DOSCIENTOS', 'TRESCIENTOS', 'CUATROCIENTOS',
    'QUINIENTOS', 'SEISCIENTOS', 'SETECIENTOS', 'OCHOCIENTOS',
    'NOVECIENTOS'
)

def convertir_grupo(n):
    output = ''

    cientos = n // 100
    decenas = (n % 100) // 10
    unidades = n % 10

    if n == 100:
        return 'CIEN'
    elif cientos != 0:
        output += CENTENAS[cientos - 1] + ' '

    k = n % 100
    if k <= 20:
        output += UNIDADES[k]
    else:
        if k <= 29:
            output += DECENAS[0] + UNIDADES[unidades].lower()
        else:
            output += DECENAS[decenas - 2]
            if unidades != 0:
                output += ' Y ' + UNIDADES[unidades]

    return output.strip()


def numero_a_letras(numero):
    partes = f"{numero:.2f}".split(".")
    entero = int(partes[0])
    decimal = int(partes[1])
    
    if entero == 0:
        resultado = "CERO"
    else:
        resultado = ''
        millones = entero // 1_000_000
        miles = (entero % 1_000_000) // 1_000
        resto = entero % 1_000

        if millones > 0:
            if millones == 1:
                resultado += 'UN MILLÓN '
            else:
                resultado += f'{convertir_grupo(millones)} MILLONES '

        if miles > 0:
            if miles == 1:
                resultado += 'MIL '
            else:
                resultado += f'{convertir_grupo(miles)} MIL '

        if resto > 0:
            resultado += convertir_grupo(resto)

    return f"{resultado.strip()} CON {decimal:02d}/100 SOLES"
