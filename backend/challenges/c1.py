"""Chapter 1: Elementary function definitions — Challenges from 'Piensa en Haskell'."""

from typing import Dict

from .data import Challenge, TestCase

CHAPTER_1_CHALLENGES: Dict[str, Challenge] = {
    # -------------------------------------------------------------------------
    # 1.1  Media de 3 números
    # -------------------------------------------------------------------------
    "c1-media": Challenge(
        id="c1-media",
        title="Average of 3 Numbers",
        description="""## Average of 3 Numbers

Define a function `media` such that `media x y z` is the arithmetic mean of `x`, `y` and `z`.

### Examples:
```haskell
media 1 3 8   -- returns 4.0
media (-1) 0 7  -- returns 2.0
media 6 6 6   -- returns 6.0
```

### Signature:
```haskell
media :: Fractional a => a -> a -> a -> a
```
""",
        solution="media x y z = (x + y + z) / 3",
        starter_code="-- Define the media function\nmedia x y z = undefined",
        tests=[
            TestCase(code="media 1 3 8", expected="4.0"),
            TestCase(code="media (-1) 0 7", expected="2.0"),
            TestCase(code="media 6 6 6", expected="6.0"),
        ],
        title_es="Media de 3 números",
        description_es="""## Media de 3 números

Definir la función `media` tal que `media x y z` es la media aritmética de los números `x`, `y` y `z`.

### Ejemplos:
```haskell
media 1 3 8   -- devuelve 4.0
media (-1) 0 7  -- devuelve 2.0
media 6 6 6   -- devuelve 6.0
```

### Perfil:
```haskell
media :: Fractional a => a -> a -> a -> a
```
""",
        starter_code_es="-- Definir la función media\nmedia x y z = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.2  Suma de euros de una colección de monedas
    # -------------------------------------------------------------------------
    "c1-suma-euros": Challenge(
        id="c1-suma-euros",
        title="Sum of Euros from Coins",
        description="""## Sum of Euros from Coins

Define a function `sumaEuros` such that `sumaEuros a b c d e` is the total amount in euros given `a` coins of 1€, `b` of 2€, `c` of 5€, `d` of 10€ and `e` of 20€.

### Examples:
```haskell
sumaEuros 0 0 0 0 1   -- returns 20
sumaEuros 10 0 0 0 0  -- returns 10
sumaEuros 1 1 1 1 1   -- returns 38
```

### Signature:
```haskell
sumaEuros :: Num a => a -> a -> a -> a -> a -> a
```
""",
        solution="sumaEuros a b c d e = 1*a + 2*b + 5*c + 10*d + 20*e",
        starter_code="-- Define the sumaEuros function\nsumaEuros a b c d e = undefined",
        tests=[
            TestCase(code="sumaEuros 0 0 0 0 1", expected="20"),
            TestCase(code="sumaEuros 10 0 0 0 0", expected="10"),
            TestCase(code="sumaEuros 1 1 1 1 1", expected="38"),
            TestCase(code="sumaEuros 0 0 0 0 0", expected="0"),
        ],
        title_es="Suma de euros de una colección de monedas",
        description_es="""## Suma de euros de una colección de monedas

Definir la función `sumaEuros` tal que `sumaEuros a b c d e` es la suma de los euros correspondientes a `a` monedas de 1 euro, `b` de 2 euros, `c` de 5 euros, `d` de 10 euros y `e` de 20 euros.

### Ejemplos:
```haskell
sumaEuros 0 0 0 0 1   -- devuelve 20
sumaEuros 10 0 0 0 0  -- devuelve 10
sumaEuros 1 1 1 1 1   -- devuelve 38
```

### Perfil:
```haskell
sumaEuros :: Num a => a -> a -> a -> a -> a -> a
```
""",
        starter_code_es="-- Definir la función sumaEuros\nsumaEuros a b c d e = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.3  Volumen de la esfera
    # -------------------------------------------------------------------------
    "c1-volumen-esfera": Challenge(
        id="c1-volumen-esfera",
        title="Volume of a Sphere",
        description="""## Volume of a Sphere

Define a function `volumenEsfera` such that `volumenEsfera r` is the volume of a sphere with radius `r`.

**Hint:** Use the constant `pi`.

### Examples:
```haskell
volumenEsfera 10  -- returns 4188.790204786391
volumenEsfera 0   -- returns 0.0
```

### Signature:
```haskell
volumenEsfera :: Floating a => a -> a
```
""",
        solution="volumenEsfera r = (4/3) * pi * r^3",
        starter_code="-- Define the volumenEsfera function\nvolumenEsfera r = undefined",
        tests=[
            TestCase(code="volumenEsfera 0", expected="0.0"),
            TestCase(code="volumenEsfera 10", expected="4188.790204786391"),
        ],
        title_es="Volumen de la esfera",
        description_es="""## Volumen de la esfera

Definir la función `volumenEsfera` tal que `volumenEsfera r` es el volumen de la esfera de radio `r`.

**Indicación:** Usar la constante `pi`.

### Ejemplos:
```haskell
volumenEsfera 10  -- devuelve 4188.790204786391
volumenEsfera 0   -- devuelve 0.0
```

### Perfil:
```haskell
volumenEsfera :: Floating a => a -> a
```
""",
        starter_code_es="-- Definir la función volumenEsfera\nvolumenEsfera r = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.4  Área de una corona circular
    # -------------------------------------------------------------------------
    "c1-area-corona": Challenge(
        id="c1-area-corona",
        title="Area of an Annulus",
        description="""## Area of an Annulus (Circular Crown)

Define a function `areaCorona` such that `areaCorona r1 r2` is the area of an annulus with inner radius `r1` and outer radius `r2`.

### Examples:
```haskell
areaCorona 1 2  -- returns 9.42477796076938
areaCorona 2 5  -- returns 65.97344572538566
```

### Signature:
```haskell
areaCorona :: Floating a => a -> a -> a
```
""",
        solution="areaCorona r1 r2 = pi * (r2^2 - r1^2)",
        starter_code="-- Define the areaCorona function\nareaCorona r1 r2 = undefined",
        tests=[
            TestCase(code="areaCorona 1 2", expected="9.42477796076938"),
            TestCase(code="areaCorona 2 5", expected="65.97344572538566"),
        ],
        title_es="Área de una corona circular",
        description_es="""## Área de una corona circular

Definir la función `areaCorona` tal que `areaCorona r1 r2` es el área de una corona circular de radio interior `r1` y radio exterior `r2`.

### Ejemplos:
```haskell
areaCorona 1 2  -- devuelve 9.42477796076938
areaCorona 2 5  -- devuelve 65.97344572538566
```

### Perfil:
```haskell
areaCorona :: Floating a => a -> a -> a
```
""",
        starter_code_es="-- Definir la función areaCorona\nareaCorona r1 r2 = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.5  Última cifra de un número
    # -------------------------------------------------------------------------
    "c1-ultima-cifra": Challenge(
        id="c1-ultima-cifra",
        title="Last Digit of a Number",
        description="""## Last Digit of a Number

Define a function `ultimaCifra` such that `ultimaCifra x` is the last digit of the number `x`.

### Examples:
```haskell
ultimaCifra 325  -- returns 5
ultimaCifra 0    -- returns 0
ultimaCifra 100  -- returns 0
```

### Signature:
```haskell
ultimaCifra :: Integral a => a -> a
```
""",
        solution="ultimaCifra x = mod x 10",
        starter_code="-- Define the ultimaCifra function\nultimaCifra x = undefined",
        tests=[
            TestCase(code="ultimaCifra 325", expected="5"),
            TestCase(code="ultimaCifra 0", expected="0"),
            TestCase(code="ultimaCifra 100", expected="0"),
        ],
        title_es="Última cifra de un número",
        description_es="""## Última cifra de un número

Definir la función `ultimaCifra` tal que `ultimaCifra x` es la última cifra del número `x`.

### Ejemplos:
```haskell
ultimaCifra 325  -- devuelve 5
ultimaCifra 0    -- devuelve 0
ultimaCifra 100  -- devuelve 0
```

### Perfil:
```haskell
ultimaCifra :: Integral a => a -> a
```
""",
        starter_code_es="-- Definir la función ultimaCifra\nultimaCifra x = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.6  Máximo de 3 elementos
    # -------------------------------------------------------------------------
    "c1-max-tres": Challenge(
        id="c1-max-tres",
        title="Maximum of 3 Elements",
        description="""## Maximum of 3 Elements

Define a function `maxTres` such that `maxTres x y z` is the maximum of `x`, `y` and `z`.

### Examples:
```haskell
maxTres 6 2 4  -- returns 6
maxTres 6 7 4  -- returns 7
maxTres 6 7 9  -- returns 9
```

### Signature:
```haskell
maxTres :: Ord a => a -> a -> a -> a
```
""",
        solution="maxTres x y z = max x (max y z)",
        starter_code="-- Define the maxTres function\nmaxTres x y z = undefined",
        tests=[
            TestCase(code="maxTres 6 2 4", expected="6"),
            TestCase(code="maxTres 6 7 4", expected="7"),
            TestCase(code="maxTres 6 7 9", expected="9"),
        ],
        title_es="Máximo de 3 elementos",
        description_es="""## Máximo de 3 elementos

Definir la función `maxTres` tal que `maxTres x y z` es el máximo de `x`, `y` y `z`.

### Ejemplos:
```haskell
maxTres 6 2 4  -- devuelve 6
maxTres 6 7 4  -- devuelve 7
maxTres 6 7 9  -- devuelve 9
```

### Perfil:
```haskell
maxTres :: Ord a => a -> a -> a -> a
```
""",
        starter_code_es="-- Definir la función maxTres\nmaxTres x y z = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.7  Disyunción excluyente (XOR)
    # -------------------------------------------------------------------------
    "c1-xor": Challenge(
        id="c1-xor",
        title="Exclusive Disjunction (XOR)",
        description="""## Exclusive Disjunction (XOR)

The exclusive disjunction of two formulas is `True` when exactly one of them is `True` and the other is `False`.

Define a function `xor1` that computes the exclusive disjunction of two Boolean values.

### Examples:
```haskell
xor1 True True   -- returns False
xor1 True False  -- returns True
xor1 False True  -- returns True
xor1 False False -- returns False
```

### Signature:
```haskell
xor1 :: Bool -> Bool -> Bool
```
""",
        solution="xor1 x y = x /= y",
        starter_code="-- Define the xor1 function\nxor1 x y = undefined",
        tests=[
            TestCase(code="xor1 True True", expected="False"),
            TestCase(code="xor1 True False", expected="True"),
            TestCase(code="xor1 False True", expected="True"),
            TestCase(code="xor1 False False", expected="False"),
        ],
        title_es="Disyunción excluyente",
        description_es="""## Disyunción excluyente

La disyunción excluyente de dos fórmulas se verifica si una es verdadera y la otra es falsa.

Definir la función `xor1` que calcule la disyunción excluyente de dos valores booleanos.

### Ejemplos:
```haskell
xor1 True True   -- devuelve False
xor1 True False  -- devuelve True
xor1 False True  -- devuelve True
xor1 False False -- devuelve False
```

### Perfil:
```haskell
xor1 :: Bool -> Bool -> Bool
```
""",
        starter_code_es="-- Definir la función xor1\nxor1 x y = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.8.1  Rotación de listas (por 1)
    # -------------------------------------------------------------------------
    "c1-rota1": Challenge(
        id="c1-rota1",
        title="Rotate List by One",
        description="""## Rotate List by One

Define a function `rota1` such that `rota1 xs` is the list obtained by placing the first element of `xs` at the end of the list.

### Examples:
```haskell
rota1 [3,2,5,7]  -- returns [2,5,7,3]
rota1 [1]        -- returns [1]
```

### Signature:
```haskell
rota1 :: [a] -> [a]
```
""",
        solution="rota1 xs = tail xs ++ [head xs]",
        starter_code="-- Define the rota1 function\nrota1 xs = undefined",
        tests=[
            TestCase(code="rota1 [3,2,5,7]", expected="[2,5,7,3]"),
            TestCase(code="rota1 [1]", expected="[1]"),
            TestCase(code="rota1 [1,2]", expected="[2,1]"),
        ],
        title_es="Rotación de una lista por un elemento",
        description_es="""## Rotación de una lista por un elemento

Definir la función `rota1` tal que `rota1 xs` es la lista obtenida poniendo el primer elemento de `xs` al final de la lista.

### Ejemplos:
```haskell
rota1 [3,2,5,7]  -- devuelve [2,5,7,3]
rota1 [1]        -- devuelve [1]
```

### Perfil:
```haskell
rota1 :: [a] -> [a]
```
""",
        starter_code_es="-- Definir la función rota1\nrota1 xs = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.8.2  Rotación de listas (por n)
    # -------------------------------------------------------------------------
    "c1-rota": Challenge(
        id="c1-rota",
        title="Rotate List by N",
        description="""## Rotate List by N

Define a function `rota` such that `rota n xs` is the list obtained by placing the first `n` elements of `xs` at the end of the list.

### Examples:
```haskell
rota 1 [3,2,5,7]  -- returns [2,5,7,3]
rota 2 [3,2,5,7]  -- returns [5,7,3,2]
rota 3 [3,2,5,7]  -- returns [7,3,2,5]
```

### Signature:
```haskell
rota :: Int -> [a] -> [a]
```
""",
        solution="rota n xs = drop n xs ++ take n xs",
        starter_code="-- Define the rota function\nrota n xs = undefined",
        tests=[
            TestCase(code="rota 1 [3,2,5,7]", expected="[2,5,7,3]"),
            TestCase(code="rota 2 [3,2,5,7]", expected="[5,7,3,2]"),
            TestCase(code="rota 3 [3,2,5,7]", expected="[7,3,2,5]"),
        ],
        title_es="Rotación de una lista por n elementos",
        description_es="""## Rotación de una lista por n elementos

Definir la función `rota` tal que `rota n xs` es la lista obtenida poniendo los primeros `n` elementos de `xs` al final de la lista.

### Ejemplos:
```haskell
rota 1 [3,2,5,7]  -- devuelve [2,5,7,3]
rota 2 [3,2,5,7]  -- devuelve [5,7,3,2]
rota 3 [3,2,5,7]  -- devuelve [7,3,2,5]
```

### Perfil:
```haskell
rota :: Int -> [a] -> [a]
```
""",
        starter_code_es="-- Definir la función rota\nrota n xs = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.9  Rango de una lista
    # -------------------------------------------------------------------------
    "c1-rango": Challenge(
        id="c1-rango",
        title="Range of a List",
        description="""## Range of a List

Define a function `rango` such that `rango xs` is the list formed by the smallest and the largest element of `xs`.

**Hint:** You can use `minimum` and `maximum`.

### Examples:
```haskell
rango [3,2,7,5]  -- returns [2,7]
rango [1,1,1]    -- returns [1,1]
```

### Signature:
```haskell
rango :: Ord a => [a] -> [a]
```
""",
        solution="rango xs = [minimum xs, maximum xs]",
        starter_code="-- Define the rango function\nrango xs = undefined",
        tests=[
            TestCase(code="rango [3,2,7,5]", expected="[2,7]"),
            TestCase(code="rango [1,1,1]", expected="[1,1]"),
            TestCase(code="rango [10]", expected="[10,10]"),
        ],
        title_es="Rango de una lista",
        description_es="""## Rango de una lista

Definir la función `rango` tal que `rango xs` es la lista formada por el menor y el mayor elemento de `xs`.

**Indicación:** Se pueden usar `minimum` y `maximum`.

### Ejemplos:
```haskell
rango [3,2,7,5]  -- devuelve [2,7]
rango [1,1,1]    -- devuelve [1,1]
```

### Perfil:
```haskell
rango :: Ord a => [a] -> [a]
```
""",
        starter_code_es="-- Definir la función rango\nrango xs = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.10  Reconocimiento de palíndromos
    # -------------------------------------------------------------------------
    "c1-palindromo": Challenge(
        id="c1-palindromo",
        title="Palindrome Check",
        description="""## Palindrome Check

Define a function `palindromo` such that `palindromo xs` returns `True` if `xs` is a palindrome (reads the same forwards and backwards).

### Examples:
```haskell
palindromo [3,2,1,2,3]  -- returns True
palindromo [3,2,1]      -- returns False
```

### Signature:
```haskell
palindromo :: Eq a => [a] -> Bool
```
""",
        solution="palindromo xs = xs == reverse xs",
        starter_code="-- Define the palindromo function\npalindromo xs = undefined",
        tests=[
            TestCase(code="palindromo [3,2,1,2,3]", expected="True"),
            TestCase(code="palindromo [3,2,1]", expected="False"),
            TestCase(code="palindromo [1]", expected="True"),
            TestCase(code="palindromo ([] :: [Int])", expected="True"),
        ],
        title_es="Reconocimiento de palíndromos",
        description_es="""## Reconocimiento de palíndromos

Definir la función `palindromo` tal que `palindromo xs` se verifica si `xs` es un palíndromo; es decir, es lo mismo leer `xs` de izquierda a derecha que de derecha a izquierda.

### Ejemplos:
```haskell
palindromo [3,2,1,2,3]  -- devuelve True
palindromo [3,2,1]      -- devuelve False
```

### Perfil:
```haskell
palindromo :: Eq a => [a] -> Bool
```
""",
        starter_code_es="-- Definir la función palindromo\npalindromo xs = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.11  Elementos interiores de una lista
    # -------------------------------------------------------------------------
    "c1-interior": Challenge(
        id="c1-interior",
        title="Inner Elements of a List",
        description="""## Inner Elements of a List

Define a function `interior` such that `interior xs` is the list obtained by removing the first and last elements of `xs`.

### Examples:
```haskell
interior [2,5,3,7,3]  -- returns [5,3,7]
interior [2,3]         -- returns []
```

### Signature:
```haskell
interior :: [a] -> [a]
```
""",
        solution="interior xs = tail (init xs)",
        starter_code="-- Define the interior function\ninterior xs = undefined",
        tests=[
            TestCase(code="interior [2,5,3,7,3]", expected="[5,3,7]"),
            TestCase(code="interior [2,3]", expected="[]"),
            TestCase(code="interior [1,2,3]", expected="[2]"),
        ],
        title_es="Elementos interiores de una lista",
        description_es="""## Elementos interiores de una lista

Definir la función `interior` tal que `interior xs` es la lista obtenida eliminando los extremos de la lista `xs`.

### Ejemplos:
```haskell
interior [2,5,3,7,3]  -- devuelve [5,3,7]
interior [2,3]         -- devuelve []
```

### Perfil:
```haskell
interior :: [a] -> [a]
```
""",
        starter_code_es="-- Definir la función interior\ninterior xs = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.12  Finales de una lista
    # -------------------------------------------------------------------------
    "c1-finales": Challenge(
        id="c1-finales",
        title="Last N Elements of a List",
        description="""## Last N Elements of a List

Define a function `finales` such that `finales n xs` is the list formed by the last `n` elements of `xs`.

### Examples:
```haskell
finales 3 [2,5,4,7,9,6]  -- returns [7,9,6]
finales 1 [2,5,4,7,9,6]  -- returns [6]
```

### Signature:
```haskell
finales :: Int -> [a] -> [a]
```
""",
        solution="finales n xs = drop (length xs - n) xs",
        starter_code="-- Define the finales function\nfinales n xs = undefined",
        tests=[
            TestCase(code="finales 3 [2,5,4,7,9,6]", expected="[7,9,6]"),
            TestCase(code="finales 1 [2,5,4,7,9,6]", expected="[6]"),
            TestCase(code="finales 6 [2,5,4,7,9,6]", expected="[2,5,4,7,9,6]"),
        ],
        title_es="Finales de una lista",
        description_es="""## Finales de una lista

Definir la función `finales` tal que `finales n xs` es la lista formada por los `n` finales elementos de `xs`.

### Ejemplos:
```haskell
finales 3 [2,5,4,7,9,6]  -- devuelve [7,9,6]
finales 1 [2,5,4,7,9,6]  -- devuelve [6]
```

### Perfil:
```haskell
finales :: Int -> [a] -> [a]
```
""",
        starter_code_es="-- Definir la función finales\nfinales n xs = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.13  Segmentos de una lista
    # -------------------------------------------------------------------------
    "c1-segmento": Challenge(
        id="c1-segmento",
        title="Segment of a List",
        description="""## Segment of a List

Define a function `segmento` such that `segmento i j xs` is the list of elements of `xs` between positions `i` and `j` (1-indexed, inclusive).

### Examples:
```haskell
segmento 3 4 [3,4,1,2,7,9,0]  -- returns [1,2]
segmento 3 5 [3,4,1,2,7,9,0]  -- returns [1,2,7]
segmento 5 3 [3,4,1,2,7,9,0]  -- returns []
```

### Signature:
```haskell
segmento :: Int -> Int -> [a] -> [a]
```
""",
        solution="segmento i j xs = drop (i-1) (take j xs)",
        starter_code="-- Define the segmento function\nsegmento i j xs = undefined",
        tests=[
            TestCase(code="segmento 3 4 [3,4,1,2,7,9,0]", expected="[1,2]"),
            TestCase(code="segmento 3 5 [3,4,1,2,7,9,0]", expected="[1,2,7]"),
            TestCase(code="segmento 5 3 [3,4,1,2,7,9,0]", expected="[]"),
        ],
        title_es="Segmentos de una lista",
        description_es="""## Segmentos de una lista

Definir la función `segmento` tal que `segmento i j xs` es la lista de los elementos de `xs` comprendidos entre las posiciones `i` y `j` (indexadas desde 1, inclusivas).

### Ejemplos:
```haskell
segmento 3 4 [3,4,1,2,7,9,0]  -- devuelve [1,2]
segmento 3 5 [3,4,1,2,7,9,0]  -- devuelve [1,2,7]
segmento 5 3 [3,4,1,2,7,9,0]  -- devuelve []
```

### Perfil:
```haskell
segmento :: Int -> Int -> [a] -> [a]
```
""",
        starter_code_es="-- Definir la función segmento\nsegmento i j xs = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.14  Extremos de una lista
    # -------------------------------------------------------------------------
    "c1-extremos": Challenge(
        id="c1-extremos",
        title="Extremes of a List",
        description="""## Extremes of a List

Define a function `extremos` such that `extremos n xs` is the list formed by the first `n` and the last `n` elements of `xs`.

### Examples:
```haskell
extremos 3 [2,6,7,1,2,4,5,8,9,2,3]  -- returns [2,6,7,9,2,3]
```

### Signature:
```haskell
extremos :: Int -> [a] -> [a]
```
""",
        solution="extremos n xs = take n xs ++ drop (length xs - n) xs",
        starter_code="-- Define the extremos function\nextremos n xs = undefined",
        tests=[
            TestCase(code="extremos 3 [2,6,7,1,2,4,5,8,9,2,3]", expected="[2,6,7,9,2,3]"),
            TestCase(code="extremos 1 [1,2,3,4,5]", expected="[1,5]"),
        ],
        title_es="Extremos de una lista",
        description_es="""## Extremos de una lista

Definir la función `extremos` tal que `extremos n xs` es la lista formada por los `n` primeros elementos de `xs` y los `n` finales elementos de `xs`.

### Ejemplos:
```haskell
extremos 3 [2,6,7,1,2,4,5,8,9,2,3]  -- devuelve [2,6,7,9,2,3]
```

### Perfil:
```haskell
extremos :: Int -> [a] -> [a]
```
""",
        starter_code_es="-- Definir la función extremos\nextremos n xs = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.15  Mediano de 3 números
    # -------------------------------------------------------------------------
    "c1-mediano": Challenge(
        id="c1-mediano",
        title="Median of 3 Numbers",
        description="""## Median of 3 Numbers

Define a function `mediano` such that `mediano x y z` is the median of the three numbers `x`, `y` and `z`.

### Examples:
```haskell
mediano 3 2 5  -- returns 3
mediano 2 4 5  -- returns 4
mediano 2 6 6  -- returns 6
```

### Signature:
```haskell
mediano :: (Num a, Ord a) => a -> a -> a -> a
```
""",
        solution="mediano x y z = x + y + z - max x (max y z) - min x (min y z)",
        starter_code="-- Define the mediano function\nmediano x y z = undefined",
        tests=[
            TestCase(code="mediano 3 2 5", expected="3"),
            TestCase(code="mediano 2 4 5", expected="4"),
            TestCase(code="mediano 2 6 6", expected="6"),
        ],
        title_es="Mediano de 3 números",
        description_es="""## Mediano de 3 números

Definir la función `mediano` tal que `mediano x y z` es el número mediano de los tres números `x`, `y` y `z`.

### Ejemplos:
```haskell
mediano 3 2 5  -- devuelve 3
mediano 2 4 5  -- devuelve 4
mediano 2 6 6  -- devuelve 6
```

### Perfil:
```haskell
mediano :: (Num a, Ord a) => a -> a -> a -> a
```
""",
        starter_code_es="-- Definir la función mediano\nmediano x y z = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.16.1  Igualdad de 3 elementos
    # -------------------------------------------------------------------------
    "c1-tres-iguales": Challenge(
        id="c1-tres-iguales",
        title="Three Equal Elements",
        description="""## Three Equal Elements

Define a function `tresIguales` such that `tresIguales x y z` returns `True` if the three elements `x`, `y` and `z` are equal.

### Examples:
```haskell
tresIguales 4 4 4  -- returns True
tresIguales 4 3 4  -- returns False
```

### Signature:
```haskell
tresIguales :: Eq a => a -> a -> a -> Bool
```
""",
        solution="tresIguales x y z = x == y && y == z",
        starter_code="-- Define the tresIguales function\ntresIguales x y z = undefined",
        tests=[
            TestCase(code="tresIguales 4 4 4", expected="True"),
            TestCase(code="tresIguales 4 3 4", expected="False"),
            TestCase(code="tresIguales 0 0 0", expected="True"),
        ],
        title_es="Igualdad de 3 elementos",
        description_es="""## Igualdad de 3 elementos

Definir la función `tresIguales` tal que `tresIguales x y z` se verifica si los elementos `x`, `y` y `z` son iguales.

### Ejemplos:
```haskell
tresIguales 4 4 4  -- devuelve True
tresIguales 4 3 4  -- devuelve False
```

### Perfil:
```haskell
tresIguales :: Eq a => a -> a -> a -> Bool
```
""",
        starter_code_es="-- Definir la función tresIguales\ntresIguales x y z = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.16.2  Diferencia de 3 elementos
    # -------------------------------------------------------------------------
    "c1-tres-diferentes": Challenge(
        id="c1-tres-diferentes",
        title="Three Different Elements",
        description="""## Three Different Elements

Define a function `tresDiferentes` such that `tresDiferentes x y z` returns `True` if the three elements `x`, `y` and `z` are all different from each other.

### Examples:
```haskell
tresDiferentes 3 5 2  -- returns True
tresDiferentes 3 5 3  -- returns False
```

### Signature:
```haskell
tresDiferentes :: Eq a => a -> a -> a -> Bool
```
""",
        solution="tresDiferentes x y z = x /= y && x /= z && y /= z",
        starter_code="-- Define the tresDiferentes function\ntresDiferentes x y z = undefined",
        tests=[
            TestCase(code="tresDiferentes 3 5 2", expected="True"),
            TestCase(code="tresDiferentes 3 5 3", expected="False"),
            TestCase(code="tresDiferentes 1 1 1", expected="False"),
        ],
        title_es="Diferencia de 3 elementos",
        description_es="""## Diferencia de 3 elementos

Definir la función `tresDiferentes` tal que `tresDiferentes x y z` se verifica si los elementos `x`, `y` y `z` son distintos.

### Ejemplos:
```haskell
tresDiferentes 3 5 2  -- devuelve True
tresDiferentes 3 5 3  -- devuelve False
```

### Perfil:
```haskell
tresDiferentes :: Eq a => a -> a -> a -> Bool
```
""",
        starter_code_es="-- Definir la función tresDiferentes\ntresDiferentes x y z = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.17  Igualdad de 4 elementos
    # -------------------------------------------------------------------------
    "c1-cuatro-iguales": Challenge(
        id="c1-cuatro-iguales",
        title="Four Equal Elements",
        description="""## Four Equal Elements

Define a function `cuatroIguales` such that `cuatroIguales x y z w` returns `True` if all four elements are equal.

### Examples:
```haskell
cuatroIguales 5 5 5 5  -- returns True
cuatroIguales 5 5 4 5  -- returns False
```

### Signature:
```haskell
cuatroIguales :: Eq a => a -> a -> a -> a -> Bool
```
""",
        solution="cuatroIguales x y z w = x == y && y == z && z == w",
        starter_code="-- Define the cuatroIguales function\ncuatroIguales x y z w = undefined",
        tests=[
            TestCase(code="cuatroIguales 5 5 5 5", expected="True"),
            TestCase(code="cuatroIguales 5 5 4 5", expected="False"),
            TestCase(code="cuatroIguales 0 0 0 0", expected="True"),
        ],
        title_es="Igualdad de 4 elementos",
        description_es="""## Igualdad de 4 elementos

Definir la función `cuatroIguales` tal que `cuatroIguales x y z w` se verifica si los elementos `x`, `y`, `z` y `w` son iguales.

### Ejemplos:
```haskell
cuatroIguales 5 5 5 5  -- devuelve True
cuatroIguales 5 5 4 5  -- devuelve False
```

### Perfil:
```haskell
cuatroIguales :: Eq a => a -> a -> a -> a -> Bool
```
""",
        starter_code_es="-- Definir la función cuatroIguales\ncuatroIguales x y z w = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.18  Propiedad triangular
    # -------------------------------------------------------------------------
    "c1-triangular": Challenge(
        id="c1-triangular",
        title="Triangle Property",
        description="""## Triangle Property

The triangle inequality states that the length of each side of a triangle must be less than the sum of the other two sides.

Define a function `triangular` such that `triangular a b c` returns `True` if `a`, `b` and `c` satisfy the triangle inequality.

### Examples:
```haskell
triangular 3 4 5   -- returns True
triangular 30 4 5  -- returns False
triangular 3 4 4   -- returns True
```

### Signature:
```haskell
triangular :: (Num a, Ord a) => a -> a -> a -> Bool
```
""",
        solution="triangular a b c = a < b + c && b < a + c && c < a + b",
        starter_code="-- Define the triangular function\ntriangular a b c = undefined",
        tests=[
            TestCase(code="triangular 3 4 5", expected="True"),
            TestCase(code="triangular 30 4 5", expected="False"),
            TestCase(code="triangular 3 4 4", expected="True"),
        ],
        title_es="Propiedad triangular",
        description_es="""## Propiedad triangular

Las longitudes de los lados de un triángulo no pueden ser cualesquiera. Para que pueda construirse el triángulo, tiene que cumplirse la propiedad triangular; es decir, la longitud de cada lado tiene que ser menor que la suma de los otros dos lados.

Definir la función `triangular` tal que `triangular a b c` se verifica si `a`, `b` y `c` cumplen la propiedad triangular.

### Ejemplos:
```haskell
triangular 3 4 5   -- devuelve True
triangular 30 4 5  -- devuelve False
triangular 3 4 4   -- devuelve True
```

### Perfil:
```haskell
triangular :: (Num a, Ord a) => a -> a -> a -> Bool
```
""",
        starter_code_es="-- Definir la función triangular\ntriangular a b c = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.19  División segura
    # -------------------------------------------------------------------------
    "c1-division-segura": Challenge(
        id="c1-division-segura",
        title="Safe Division",
        description="""## Safe Division

Define a function `divisionSegura` such that `divisionSegura x y` returns `x / y` if `y` is not zero, and `9999` otherwise.

### Examples:
```haskell
divisionSegura 7 2  -- returns 3.5
divisionSegura 7 0  -- returns 9999.0
```

### Signature:
```haskell
divisionSegura :: (Eq a, Fractional a) => a -> a -> a
```
""",
        solution="divisionSegura x y\n  | y == 0    = 9999\n  | otherwise = x / y",
        starter_code="-- Define the divisionSegura function\ndivisionSegura x y = undefined",
        tests=[
            TestCase(code="divisionSegura 7 2", expected="3.5"),
            TestCase(code="divisionSegura 7 0", expected="9999.0"),
            TestCase(code="divisionSegura 0 5", expected="0.0"),
        ],
        title_es="División segura",
        description_es="""## División segura

Definir la función `divisionSegura` tal que `divisionSegura x y` es `x / y` si `y` no es cero y `9999` en caso contrario.

### Ejemplos:
```haskell
divisionSegura 7 2  -- devuelve 3.5
divisionSegura 7 0  -- devuelve 9999.0
```

### Perfil:
```haskell
divisionSegura :: (Eq a, Fractional a) => a -> a -> a
```
""",
        starter_code_es="-- Definir la función divisionSegura\ndivisionSegura x y = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.21  Módulo de un vector
    # -------------------------------------------------------------------------
    "c1-modulo": Challenge(
        id="c1-modulo",
        title="Module of a Vector",
        description="""## Module of a Vector

Define a function `modulo` such that `modulo x y` is the magnitude (Euclidean norm) of the vector `(x, y)`.

### Examples:
```haskell
modulo 3 4  -- returns 5.0
modulo 1 0  -- returns 1.0
```

### Signature:
```haskell
modulo :: Floating a => a -> a -> a
```
""",
        solution="modulo x y = sqrt (x^2 + y^2)",
        starter_code="-- Define the modulo function\nmodulo x y = undefined",
        tests=[
            TestCase(code="modulo 3 4", expected="5.0"),
            TestCase(code="modulo 1 0", expected="1.0"),
            TestCase(code="modulo 0 0", expected="0.0"),
        ],
        title_es="Módulo de un vector",
        description_es="""## Módulo de un vector

Definir la función `modulo` tal que `modulo x y` es el módulo del vector `(x, y)`.

### Ejemplos:
```haskell
modulo 3 4  -- devuelve 5.0
modulo 1 0  -- devuelve 1.0
```

### Perfil:
```haskell
modulo :: Floating a => a -> a -> a
```
""",
        starter_code_es="-- Definir la función modulo\nmodulo x y = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.22  Rectángulo de área máxima
    # -------------------------------------------------------------------------
    "c1-max-rect": Challenge(
        id="c1-max-rect",
        title="Rectangle with Maximum Area",
        description="""## Rectangle with Maximum Area

Rectangles can be represented as pairs `(base, height)`. Define a function `maxRect` such that `maxRect r1 r2` returns the rectangle with the larger area. If equal, return the first.

### Examples:
```haskell
maxRect (4,6) (3,7)  -- returns (4,6)
maxRect (2,3) (4,5)  -- returns (4,5)
```

### Signature:
```haskell
maxRect :: (Num a, Ord a) => (a, a) -> (a, a) -> (a, a)
```
""",
        solution="maxRect (a, b) (c, d)\n  | a * b >= c * d = (a, b)\n  | otherwise      = (c, d)",
        starter_code="-- Define the maxRect function\nmaxRect (a, b) (c, d) = undefined",
        tests=[
            TestCase(code="maxRect (4,6) (3,7)", expected="(4,6)"),
            TestCase(code="maxRect (2,3) (4,5)", expected="(4,5)"),
            TestCase(code="maxRect (4,6) (3,8)", expected="(4,6)"),
        ],
        title_es="Rectángulo de área máxima",
        description_es="""## Rectángulo de área máxima

Las dimensiones de los rectángulos pueden representarse por pares `(base, altura)`. Definir la función `maxRect` tal que `maxRect r1 r2` es el rectángulo de mayor área. Si son iguales, devolver el primero.

### Ejemplos:
```haskell
maxRect (4,6) (3,7)  -- devuelve (4,6)
maxRect (2,3) (4,5)  -- devuelve (4,5)
```

### Perfil:
```haskell
maxRect :: (Num a, Ord a) => (a, a) -> (a, a) -> (a, a)
```
""",
        starter_code_es="-- Definir la función maxRect\nmaxRect (a, b) (c, d) = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.23.1  Cuadrante de un punto
    # -------------------------------------------------------------------------
    "c1-cuadrante": Challenge(
        id="c1-cuadrante",
        title="Quadrant of a Point",
        description="""## Quadrant of a Point

Define a function `cuadrante` such that `cuadrante (x, y)` returns the quadrant of the point `(x, y)`. Assume the point is not on any axis.

### Examples:
```haskell
cuadrante (3, 5)    -- returns 1
cuadrante (-3, 5)   -- returns 2
cuadrante (-3, -5)  -- returns 3
cuadrante (3, -5)   -- returns 4
```

### Signature:
```haskell
cuadrante :: (Num a, Ord a) => (a, a) -> Int
```
""",
        solution="cuadrante (x, y)\n  | x > 0 && y > 0 = 1\n  | x < 0 && y > 0 = 2\n  | x < 0 && y < 0 = 3\n  | otherwise       = 4",
        starter_code="-- Define the cuadrante function\ncuadrante (x, y) = undefined",
        tests=[
            TestCase(code="cuadrante (3, 5)", expected="1"),
            TestCase(code="cuadrante (-3, 5)", expected="2"),
            TestCase(code="cuadrante (-3, -5)", expected="3"),
            TestCase(code="cuadrante (3, -5)", expected="4"),
        ],
        title_es="Cuadrante de un punto",
        description_es="""## Cuadrante de un punto

Definir la función `cuadrante` tal que `cuadrante (x, y)` es el cuadrante del punto `(x, y)` (se supone que no está sobre los ejes).

### Ejemplos:
```haskell
cuadrante (3, 5)    -- devuelve 1
cuadrante (-3, 5)   -- devuelve 2
cuadrante (-3, -5)  -- devuelve 3
cuadrante (3, -5)   -- devuelve 4
```

### Perfil:
```haskell
cuadrante :: (Num a, Ord a) => (a, a) -> Int
```
""",
        starter_code_es="-- Definir la función cuadrante\ncuadrante (x, y) = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.23.2  Intercambio de coordenadas
    # -------------------------------------------------------------------------
    "c1-intercambia": Challenge(
        id="c1-intercambia",
        title="Swap Coordinates",
        description="""## Swap Coordinates

Define a function `intercambia` such that `intercambia (x, y)` returns the point with swapped coordinates.

### Examples:
```haskell
intercambia (2, 5)  -- returns (5,2)
intercambia (5, 2)  -- returns (2,5)
```

### Signature:
```haskell
intercambia :: (a, b) -> (b, a)
```
""",
        solution="intercambia (x, y) = (y, x)",
        starter_code="-- Define the intercambia function\nintercambia (x, y) = undefined",
        tests=[
            TestCase(code="intercambia (2, 5)", expected="(5,2)"),
            TestCase(code="intercambia (5, 2)", expected="(2,5)"),
            TestCase(code="intercambia (1, 1)", expected="(1,1)"),
        ],
        title_es="Intercambio de coordenadas",
        description_es="""## Intercambio de coordenadas

Definir la función `intercambia` tal que `intercambia (x, y)` es el punto obtenido intercambiando las coordenadas del punto `(x, y)`.

### Ejemplos:
```haskell
intercambia (2, 5)  -- devuelve (5,2)
intercambia (5, 2)  -- devuelve (2,5)
```

### Perfil:
```haskell
intercambia :: (a, b) -> (b, a)
```
""",
        starter_code_es="-- Definir la función intercambia\nintercambia (x, y) = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.23.3  Punto simétrico
    # -------------------------------------------------------------------------
    "c1-simetrico-h": Challenge(
        id="c1-simetrico-h",
        title="Symmetric Point",
        description="""## Symmetric Point

Define a function `simetricoH` such that `simetricoH (x, y)` is the symmetric point of `(x, y)` with respect to the horizontal axis (x-axis).

### Examples:
```haskell
simetricoH (2, 5)    -- returns (2,-5)
simetricoH (3, -4)   -- returns (3,4)
```

### Signature:
```haskell
simetricoH :: Num a => (a, a) -> (a, a)
```
""",
        solution="simetricoH (x, y) = (x, -y)",
        starter_code="-- Define the simetricoH function\nsimetricoH (x, y) = undefined",
        tests=[
            TestCase(code="simetricoH (2, 5)", expected="(2,-5)"),
            TestCase(code="simetricoH (3, -4)", expected="(3,4)"),
            TestCase(code="simetricoH (0, 0)", expected="(0,0)"),
        ],
        title_es="Punto simétrico",
        description_es="""## Punto simétrico

Definir la función `simetricoH` tal que `simetricoH (x, y)` es el punto simétrico de `(x, y)` respecto del eje horizontal.

### Ejemplos:
```haskell
simetricoH (2, 5)    -- devuelve (2,-5)
simetricoH (3, -4)   -- devuelve (3,4)
```

### Perfil:
```haskell
simetricoH :: Num a => (a, a) -> (a, a)
```
""",
        starter_code_es="-- Definir la función simetricoH\nsimetricoH (x, y) = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.23.4  Distancia entre dos puntos
    # -------------------------------------------------------------------------
    "c1-distancia": Challenge(
        id="c1-distancia",
        title="Distance Between Two Points",
        description="""## Distance Between Two Points

Define a function `distancia` such that `distancia p1 p2` is the Euclidean distance between points `p1` and `p2`.

### Examples:
```haskell
distancia (1, 2) (4, 6)  -- returns 5.0
distancia (0, 0) (3, 4)  -- returns 5.0
```

### Signature:
```haskell
distancia :: Floating a => (a, a) -> (a, a) -> a
```
""",
        solution="distancia (x1, y1) (x2, y2) = sqrt ((x2-x1)^2 + (y2-y1)^2)",
        starter_code="-- Define the distancia function\ndistancia (x1, y1) (x2, y2) = undefined",
        tests=[
            TestCase(code="distancia (1, 2) (4, 6)", expected="5.0"),
            TestCase(code="distancia (0, 0) (3, 4)", expected="5.0"),
            TestCase(code="distancia (0, 0) (0, 0)", expected="0.0"),
        ],
        title_es="Distancia entre dos puntos",
        description_es="""## Distancia entre dos puntos

Definir la función `distancia` tal que `distancia p1 p2` es la distancia entre los puntos `p1` y `p2`.

### Ejemplos:
```haskell
distancia (1, 2) (4, 6)  -- devuelve 5.0
distancia (0, 0) (3, 4)  -- devuelve 5.0
```

### Perfil:
```haskell
distancia :: Floating a => (a, a) -> (a, a) -> a
```
""",
        starter_code_es="-- Definir la función distancia\ndistancia (x1, y1) (x2, y2) = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.23.5  Punto medio entre otros dos
    # -------------------------------------------------------------------------
    "c1-punto-medio": Challenge(
        id="c1-punto-medio",
        title="Midpoint",
        description="""## Midpoint Between Two Points

Define a function `puntoMedio` such that `puntoMedio p1 p2` is the midpoint between `p1` and `p2`.

### Examples:
```haskell
puntoMedio (0, 2) (0, 6)  -- returns (0.0,4.0)
puntoMedio (2, 4) (6, 8)  -- returns (4.0,6.0)
```

### Signature:
```haskell
puntoMedio :: Fractional a => (a, a) -> (a, a) -> (a, a)
```
""",
        solution="puntoMedio (x1, y1) (x2, y2) = ((x1+x2)/2, (y1+y2)/2)",
        starter_code="-- Define the puntoMedio function\npuntoMedio (x1, y1) (x2, y2) = undefined",
        tests=[
            TestCase(code="puntoMedio (0, 2) (0, 6)", expected="(0.0,4.0)"),
            TestCase(code="puntoMedio (2, 4) (6, 8)", expected="(4.0,6.0)"),
        ],
        title_es="Punto medio entre otros dos",
        description_es="""## Punto medio entre otros dos

Definir la función `puntoMedio` tal que `puntoMedio p1 p2` es el punto medio entre los puntos `p1` y `p2`.

### Ejemplos:
```haskell
puntoMedio (0, 2) (0, 6)  -- devuelve (0.0,4.0)
puntoMedio (2, 4) (6, 8)  -- devuelve (4.0,6.0)
```

### Perfil:
```haskell
puntoMedio :: Fractional a => (a, a) -> (a, a) -> (a, a)
```
""",
        starter_code_es="-- Definir la función puntoMedio\npuntoMedio (x1, y1) (x2, y2) = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.24.1  Suma de dos números complejos
    # -------------------------------------------------------------------------
    "c1-suma-complejos": Challenge(
        id="c1-suma-complejos",
        title="Sum of Complex Numbers",
        description="""## Sum of Two Complex Numbers

Complex numbers can be represented as pairs `(a, b)` meaning `a + bi`. Define a function `sumaComplejos` that computes the sum of two complex numbers.

### Examples:
```haskell
sumaComplejos (2, 3) (5, 6)  -- returns (7,9)
sumaComplejos (1, -2) (-1, 2)  -- returns (0,0)
```

### Signature:
```haskell
sumaComplejos :: Num a => (a, a) -> (a, a) -> (a, a)
```
""",
        solution="sumaComplejos (a, b) (c, d) = (a+c, b+d)",
        starter_code="-- Define the sumaComplejos function\nsumaComplejos (a, b) (c, d) = undefined",
        tests=[
            TestCase(code="sumaComplejos (2, 3) (5, 6)", expected="(7,9)"),
            TestCase(code="sumaComplejos (1, -2) (-1, 2)", expected="(0,0)"),
        ],
        title_es="Suma de dos números complejos",
        description_es="""## Suma de dos números complejos

Los números complejos pueden representarse mediante pares `(a, b)` que significan `a + bi`. Definir la función `sumaComplejos` tal que `sumaComplejos x y` es la suma de los números complejos `x` e `y`.

### Ejemplos:
```haskell
sumaComplejos (2, 3) (5, 6)    -- devuelve (7,9)
sumaComplejos (1, -2) (-1, 2)  -- devuelve (0,0)
```

### Perfil:
```haskell
sumaComplejos :: Num a => (a, a) -> (a, a) -> (a, a)
```
""",
        starter_code_es="-- Definir la función sumaComplejos\nsumaComplejos (a, b) (c, d) = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.24.2  Producto de dos números complejos
    # -------------------------------------------------------------------------
    "c1-producto-complejos": Challenge(
        id="c1-producto-complejos",
        title="Product of Complex Numbers",
        description="""## Product of Two Complex Numbers

Define a function `productoComplejos` that computes the product of two complex numbers represented as pairs. Recall: `(a+bi)(c+di) = (ac-bd) + (ad+bc)i`.

### Examples:
```haskell
productoComplejos (2, 3) (5, 6)  -- returns (-8,27)
productoComplejos (1, 0) (5, 3)  -- returns (5,3)
```

### Signature:
```haskell
productoComplejos :: Num a => (a, a) -> (a, a) -> (a, a)
```
""",
        solution="productoComplejos (a, b) (c, d) = (a*c - b*d, a*d + b*c)",
        starter_code="-- Define the productoComplejos function\nproductoComplejos (a, b) (c, d) = undefined",
        tests=[
            TestCase(code="productoComplejos (2, 3) (5, 6)", expected="(-8,27)"),
            TestCase(code="productoComplejos (1, 0) (5, 3)", expected="(5,3)"),
        ],
        title_es="Producto de dos números complejos",
        description_es="""## Producto de dos números complejos

Definir la función `productoComplejos` tal que `productoComplejos x y` es el producto de los números complejos `x` e `y`. Recordar: `(a+bi)(c+di) = (ac-bd) + (ad+bc)i`.

### Ejemplos:
```haskell
productoComplejos (2, 3) (5, 6)  -- devuelve (-8,27)
productoComplejos (1, 0) (5, 3)  -- devuelve (5,3)
```

### Perfil:
```haskell
productoComplejos :: Num a => (a, a) -> (a, a) -> (a, a)
```
""",
        starter_code_es="-- Definir la función productoComplejos\nproductoComplejos (a, b) (c, d) = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.24.3  Conjugado de un número complejo
    # -------------------------------------------------------------------------
    "c1-conjugado": Challenge(
        id="c1-conjugado",
        title="Conjugate of a Complex Number",
        description="""## Conjugate of a Complex Number

Define a function `conjugado` such that `conjugado (a, b)` is the conjugate of the complex number `a + bi`.

### Examples:
```haskell
conjugado (2, 3)  -- returns (2,-3)
conjugado (0, 0)  -- returns (0,0)
```

### Signature:
```haskell
conjugado :: Num a => (a, a) -> (a, a)
```
""",
        solution="conjugado (a, b) = (a, -b)",
        starter_code="-- Define the conjugado function\nconjugado (a, b) = undefined",
        tests=[
            TestCase(code="conjugado (2, 3)", expected="(2,-3)"),
            TestCase(code="conjugado (0, 0)", expected="(0,0)"),
            TestCase(code="conjugado (5, -7)", expected="(5,7)"),
        ],
        title_es="Conjugado de un número complejo",
        description_es="""## Conjugado de un número complejo

Definir la función `conjugado` tal que `conjugado (a, b)` es el conjugado del número complejo `a + bi`.

### Ejemplos:
```haskell
conjugado (2, 3)  -- devuelve (2,-3)
conjugado (0, 0)  -- devuelve (0,0)
```

### Perfil:
```haskell
conjugado :: Num a => (a, a) -> (a, a)
```
""",
        starter_code_es="-- Definir la función conjugado\nconjugado (a, b) = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.25  Intercalación de pares
    # -------------------------------------------------------------------------
    "c1-intercala": Challenge(
        id="c1-intercala",
        title="Interleave Two Pairs",
        description="""## Interleave Two Pairs

Define a function `intercala` that receives two lists of exactly two elements each and returns a four-element list constructed by interleaving the elements.

### Examples:
```haskell
intercala [1, 4] [3, 2]  -- returns [1,3,4,2]
```

### Signature:
```haskell
intercala :: [a] -> [a] -> [a]
```
""",
        solution="intercala [x1, x2] [y1, y2] = [x1, y1, x2, y2]",
        starter_code="-- Define the intercala function\nintercala xs ys = undefined",
        tests=[
            TestCase(code="intercala [1, 4] [3, 2]", expected="[1,3,4,2]"),
            TestCase(code="intercala [0, 0] [1, 1]", expected="[0,1,0,1]"),
        ],
        title_es="Intercalación de pares",
        description_es="""## Intercalación de pares

Definir la función `intercala` que reciba dos listas `xs` e `ys` de dos elementos cada una, y devuelva una lista de cuatro elementos, construida intercalando los elementos de `xs` e `ys`.

### Ejemplos:
```haskell
intercala [1, 4] [3, 2]  -- devuelve [1,3,4,2]
```

### Perfil:
```haskell
intercala :: [a] -> [a] -> [a]
```
""",
        starter_code_es="-- Definir la función intercala\nintercala xs ys = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.26  Permutación cíclica de una lista
    # -------------------------------------------------------------------------
    "c1-ciclo": Challenge(
        id="c1-ciclo",
        title="Cyclic Permutation",
        description="""## Cyclic Permutation of a List

Define a function `ciclo` that cyclically permutes the elements of a list, moving the last element to the beginning.

### Examples:
```haskell
ciclo [2, 5, 7, 9]  -- returns [9,2,5,7]
ciclo [1, 2, 3]     -- returns [3,1,2]
```

### Signature:
```haskell
ciclo :: [a] -> [a]
```
""",
        solution="ciclo xs = last xs : init xs",
        starter_code="-- Define the ciclo function\nciclo xs = undefined",
        tests=[
            TestCase(code="ciclo [2, 5, 7, 9]", expected="[9,2,5,7]"),
            TestCase(code="ciclo [1, 2, 3]", expected="[3,1,2]"),
            TestCase(code="ciclo [1]", expected="[1]"),
        ],
        title_es="Permutación cíclica de una lista",
        description_es="""## Permutación cíclica de una lista

Definir la función `ciclo` que permute cíclicamente los elementos de una lista, pasando el último elemento al principio de la lista.

### Ejemplos:
```haskell
ciclo [2, 5, 7, 9]  -- devuelve [9,2,5,7]
ciclo [1, 2, 3]     -- devuelve [3,1,2]
```

### Perfil:
```haskell
ciclo :: [a] -> [a]
```
""",
        starter_code_es="-- Definir la función ciclo\nciclo xs = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.27  Mayor número de 2 cifras con dos dígitos dados
    # -------------------------------------------------------------------------
    "c1-mayor-numero": Challenge(
        id="c1-mayor-numero",
        title="Largest 2-Digit Number",
        description="""## Largest 2-Digit Number from Two Digits

Define a function `mayorNumero` such that `mayorNumero x y` is the largest two-digit number that can be formed with digits `x` and `y`.

### Examples:
```haskell
mayorNumero 2 5  -- returns 52
mayorNumero 5 2  -- returns 52
```

### Signature:
```haskell
mayorNumero :: (Num a, Ord a) => a -> a -> a
```
""",
        solution="mayorNumero x y = 10 * max x y + min x y",
        starter_code="-- Define the mayorNumero function\nmayorNumero x y = undefined",
        tests=[
            TestCase(code="mayorNumero 2 5", expected="52"),
            TestCase(code="mayorNumero 5 2", expected="52"),
            TestCase(code="mayorNumero 9 3", expected="93"),
        ],
        title_es="Mayor número de 2 cifras con dos dígitos dados",
        description_es="""## Mayor número de 2 cifras con dos dígitos dados

Definir la función `mayorNumero` tal que `mayorNumero x y` es el mayor número de dos cifras que puede construirse con los dígitos `x` e `y`.

### Ejemplos:
```haskell
mayorNumero 2 5  -- devuelve 52
mayorNumero 5 2  -- devuelve 52
```

### Perfil:
```haskell
mayorNumero :: (Num a, Ord a) => a -> a -> a
```
""",
        starter_code_es="-- Definir la función mayorNumero\nmayorNumero x y = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.28  Número de raíces de una ecuación cuadrática
    # -------------------------------------------------------------------------
    "c1-num-raices": Challenge(
        id="c1-num-raices",
        title="Number of Roots of a Quadratic",
        description="""## Number of Roots of a Quadratic Equation

Define a function `numRaices` such that `numRaices a b c` is the number of real roots of the equation `ax² + bx + c = 0`.

### Examples:
```haskell
numRaices 2 0 3    -- returns 0
numRaices 4 4 1    -- returns 1
numRaices 5 23 12  -- returns 2
```

### Signature:
```haskell
numRaices :: (Num a, Ord a) => a -> a -> a -> Int
```
""",
        solution="numRaices a b c\n  | d > 0     = 2\n  | d == 0    = 1\n  | otherwise = 0\n  where d = b*b - 4*a*c",
        starter_code="-- Define the numRaices function\nnumRaices a b c = undefined",
        tests=[
            TestCase(code="numRaices 2 0 3", expected="0"),
            TestCase(code="numRaices 4 4 1", expected="1"),
            TestCase(code="numRaices 5 23 12", expected="2"),
        ],
        title_es="Número de raíces de una ecuación cuadrática",
        description_es="""## Número de raíces de una ecuación cuadrática

Definir la función `numRaices` tal que `numRaices a b c` es el número de raíces reales de la ecuación `ax² + bx + c = 0`.

### Ejemplos:
```haskell
numRaices 2 0 3    -- devuelve 0
numRaices 4 4 1    -- devuelve 1
numRaices 5 23 12  -- devuelve 2
```

### Perfil:
```haskell
numRaices :: (Num a, Ord a) => a -> a -> a -> Int
```
""",
        starter_code_es="-- Definir la función numRaices\nnumRaices a b c = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.29  Raíces de las ecuaciones cuadráticas
    # -------------------------------------------------------------------------
    "c1-raices": Challenge(
        id="c1-raices",
        title="Roots of a Quadratic Equation",
        description="""## Roots of a Quadratic Equation

Define a function `raices` such that `raices a b c` returns the list of real roots of the equation `ax² + bx + c = 0`. If the discriminant is negative, return an empty list.

### Examples:
```haskell
raices 1 3 2       -- returns [-1.0,-2.0]
raices 1 (-2) 1    -- returns [1.0,1.0]
raices 1 0 1       -- returns []
```

### Signature:
```haskell
raices :: Double -> Double -> Double -> [Double]
```
""",
        solution="raices a b c\n  | d >= 0    = [(-b + sqrt d) / (2*a), (-b - sqrt d) / (2*a)]\n  | otherwise = []\n  where d = b*b - 4*a*c",
        starter_code="-- Define the raices function\nraices a b c = undefined",
        tests=[
            TestCase(code="raices 1 3 2", expected="[-1.0,-2.0]"),
            TestCase(code="raices 1 (-2) 1", expected="[1.0,1.0]"),
            TestCase(code="raices 1 0 1", expected="[]"),
        ],
        title_es="Raíces de las ecuaciones cuadráticas",
        description_es="""## Raíces de las ecuaciones cuadráticas

Definir la función `raices` tal que `raices a b c` devuelve la lista de las raíces reales de la ecuación `ax² + bx + c = 0`. Si el discriminante es negativo, devolver una lista vacía.

### Ejemplos:
```haskell
raices 1 3 2       -- devuelve [-1.0,-2.0]
raices 1 (-2) 1    -- devuelve [1.0,1.0]
raices 1 0 1       -- devuelve []
```

### Perfil:
```haskell
raices :: Double -> Double -> Double -> [Double]
```
""",
        starter_code_es="-- Definir la función raices\nraices a b c = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.30  Área de un triángulo mediante la fórmula de Herón
    # -------------------------------------------------------------------------
    "c1-area-heron": Challenge(
        id="c1-area-heron",
        title="Triangle Area (Heron's Formula)",
        description="""## Triangle Area using Heron's Formula

Heron's formula states that the area of a triangle with sides `a`, `b`, `c` is `√(s(s-a)(s-b)(s-c))` where `s = (a+b+c)/2` is the semi-perimeter.

Define a function `areaHeron` that computes the area of a triangle using Heron's formula.

### Examples:
```haskell
areaHeron 3 4 5  -- returns 6.0
```

### Signature:
```haskell
areaHeron :: Floating a => a -> a -> a -> a
```
""",
        solution="areaHeron a b c = sqrt (s * (s-a) * (s-b) * (s-c))\n  where s = (a + b + c) / 2",
        starter_code="-- Define the areaHeron function\nareaHeron a b c = undefined",
        tests=[
            TestCase(code="areaHeron 3 4 5", expected="6.0"),
        ],
        title_es="Área de un triángulo mediante la fórmula de Herón",
        description_es="""## Área de un triángulo mediante la fórmula de Herón

La fórmula de Herón dice que el área de un triángulo cuyos lados miden `a`, `b` y `c` es `√(s(s−a)(s−b)(s−c))`, donde `s` es el semiperímetro `s = (a+b+c)/2`.

Definir la función `areaHeron` tal que `areaHeron a b c` es el área de un triángulo de lados `a`, `b` y `c`.

### Ejemplos:
```haskell
areaHeron 3 4 5  -- devuelve 6.0
```

### Perfil:
```haskell
areaHeron :: Floating a => a -> a -> a -> a
```
""",
        starter_code_es="-- Definir la función areaHeron\nareaHeron a b c = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.31.1  Forma reducida de un número racional
    # -------------------------------------------------------------------------
    "c1-forma-reducida": Challenge(
        id="c1-forma-reducida",
        title="Reduced Form of a Rational",
        description="""## Reduced Form of a Rational Number

Rational numbers can be represented as pairs of integers `(numerator, denominator)`. Define a function `formaReducida` that returns the reduced form of a rational number.

### Examples:
```haskell
formaReducida (4, 10)  -- returns (2,5)
formaReducida (0, 5)   -- returns (0,1)
```

### Signature:
```haskell
formaReducida :: Integral a => (a, a) -> (a, a)
```
""",
        solution="formaReducida (a, b) = (a `div` d, b `div` d)\n  where d = gcd a b",
        starter_code="-- Define the formaReducida function\nformaReducida (a, b) = undefined",
        tests=[
            TestCase(code="formaReducida (4, 10)", expected="(2,5)"),
            TestCase(code="formaReducida (0, 5)", expected="(0,1)"),
            TestCase(code="formaReducida (6, 3)", expected="(2,1)"),
        ],
        title_es="Forma reducida de un número racional",
        description_es="""## Forma reducida de un número racional

Los números racionales pueden representarse mediante pares de enteros `(numerador, denominador)`. Definir la función `formaReducida` tal que `formaReducida (a, b)` es la forma reducida del número racional `a/b`.

### Ejemplos:
```haskell
formaReducida (4, 10)  -- devuelve (2,5)
formaReducida (0, 5)   -- devuelve (0,1)
```

### Perfil:
```haskell
formaReducida :: Integral a => (a, a) -> (a, a)
```
""",
        starter_code_es="-- Definir la función formaReducida\nformaReducida (a, b) = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.31.2  Suma de dos números racionales
    # -------------------------------------------------------------------------
    "c1-suma-racional": Challenge(
        id="c1-suma-racional",
        title="Sum of Two Rationals",
        description="""## Sum of Two Rational Numbers

Define a function `sumaRacional` that computes the sum of two rational numbers (represented as pairs) and returns the result in reduced form.

### Examples:
```haskell
sumaRacional (2, 3) (5, 6)  -- returns (3,2)
```

### Signature:
```haskell
sumaRacional :: Integral a => (a, a) -> (a, a) -> (a, a)
```
""",
        solution="sumaRacional (a, b) (c, d) = (num `div` g, den `div` g)\n  where num = a*d + b*c\n        den = b*d\n        g = gcd num den",
        starter_code="-- Define the sumaRacional function\nsumaRacional (a, b) (c, d) = undefined",
        tests=[
            TestCase(code="sumaRacional (2, 3) (5, 6)", expected="(3,2)"),
            TestCase(code="sumaRacional (1, 2) (1, 2)", expected="(1,1)"),
        ],
        title_es="Suma de dos números racionales",
        description_es="""## Suma de dos números racionales

Definir la función `sumaRacional` tal que `sumaRacional x y` es la suma de los números racionales `x` e `y`, en forma reducida.

### Ejemplos:
```haskell
sumaRacional (2, 3) (5, 6)  -- devuelve (3,2)
```

### Perfil:
```haskell
sumaRacional :: Integral a => (a, a) -> (a, a) -> (a, a)
```
""",
        starter_code_es="-- Definir la función sumaRacional\nsumaRacional (a, b) (c, d) = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.31.3  Producto de dos números racionales
    # -------------------------------------------------------------------------
    "c1-producto-racional": Challenge(
        id="c1-producto-racional",
        title="Product of Two Rationals",
        description="""## Product of Two Rational Numbers

Define a function `productoRacional` that computes the product of two rational numbers (represented as pairs) and returns the result in reduced form.

### Examples:
```haskell
productoRacional (2, 3) (5, 6)  -- returns (5,9)
```

### Signature:
```haskell
productoRacional :: Integral a => (a, a) -> (a, a) -> (a, a)
```
""",
        solution="productoRacional (a, b) (c, d) = (num `div` g, den `div` g)\n  where num = a*c\n        den = b*d\n        g = gcd num den",
        starter_code="-- Define the productoRacional function\nproductoRacional (a, b) (c, d) = undefined",
        tests=[
            TestCase(code="productoRacional (2, 3) (5, 6)", expected="(5,9)"),
            TestCase(code="productoRacional (1, 2) (2, 1)", expected="(1,1)"),
        ],
        title_es="Producto de dos números racionales",
        description_es="""## Producto de dos números racionales

Definir la función `productoRacional` tal que `productoRacional x y` es el producto de los números racionales `x` e `y`, en forma reducida.

### Ejemplos:
```haskell
productoRacional (2, 3) (5, 6)  -- devuelve (5,9)
```

### Perfil:
```haskell
productoRacional :: Integral a => (a, a) -> (a, a) -> (a, a)
```
""",
        starter_code_es="-- Definir la función productoRacional\nproductoRacional (a, b) (c, d) = undefined",
    ),

    # -------------------------------------------------------------------------
    # 1.31.4  Igualdad de números racionales
    # -------------------------------------------------------------------------
    "c1-igualdad-racional": Challenge(
        id="c1-igualdad-racional",
        title="Equality of Two Rationals",
        description="""## Equality of Two Rational Numbers

Define a function `igualdadRacional` such that `igualdadRacional r1 r2` returns `True` if the rational numbers `r1` and `r2` are equal.

### Examples:
```haskell
igualdadRacional (1, 2) (2, 4)  -- returns True
igualdadRacional (1, 2) (3, 5)  -- returns False
```

### Signature:
```haskell
igualdadRacional :: (Eq a, Num a) => (a, a) -> (a, a) -> Bool
```
""",
        solution="igualdadRacional (a, b) (c, d) = a*d == b*c",
        starter_code="-- Define the igualdadRacional function\nigualdadRacional (a, b) (c, d) = undefined",
        tests=[
            TestCase(code="igualdadRacional (1, 2) (2, 4)", expected="True"),
            TestCase(code="igualdadRacional (1, 2) (3, 5)", expected="False"),
            TestCase(code="igualdadRacional (3, 9) (1, 3)", expected="True"),
        ],
        title_es="Igualdad de números racionales",
        description_es="""## Igualdad de números racionales

Definir la función `igualdadRacional` tal que `igualdadRacional r1 r2` se verifica si los números racionales `r1` e `r2` son iguales.

### Ejemplos:
```haskell
igualdadRacional (1, 2) (2, 4)  -- devuelve True
igualdadRacional (1, 2) (3, 5)  -- devuelve False
```

### Perfil:
```haskell
igualdadRacional :: (Eq a, Num a) => (a, a) -> (a, a) -> Bool
```
""",
        starter_code_es="-- Definir la función igualdadRacional\nigualdadRacional (a, b) (c, d) = undefined",
    ),
}
