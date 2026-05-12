"""Chapter 2: List comprehensions - Challenges from 'Piensa en Haskell'."""

from typing import Dict

from .data import Challenge, TestCase


CHAPTER_2_CHALLENGES: Dict[str, Challenge] = {
    # -------------------------------------------------------------------------
    # 2.1.1  Suma de los cuadrados de los n primeros numeros
    # -------------------------------------------------------------------------
    "c2-suma-de-cuadrados": Challenge(
        id="c2-suma-de-cuadrados",
        title="Sum of Squares",
        description="""## Sum of Squares

Define, using a list comprehension, a function `sumaDeCuadrados` such that `sumaDeCuadrados n` is the sum of the squares of the integers from `1` through `n`. For `n = 0`, the result is `0`.

### Examples:
```haskell
sumaDeCuadrados 3    -- returns 14
sumaDeCuadrados 100  -- returns 338350
```

### Signature:
```haskell
sumaDeCuadrados :: Integer -> Integer
```
""",
        solution="sumaDeCuadrados :: Integer -> Integer\nsumaDeCuadrados n = sum [x^2 | x <- [1..n]]",
        starter_code="-- Define the sumaDeCuadrados function\nsumaDeCuadrados :: Integer -> Integer",
        tests=[
            TestCase(code="sumaDeCuadrados 3", expected="14"),
            TestCase(code="sumaDeCuadrados 100", expected="338350"),
            TestCase(code="sumaDeCuadrados 0", expected="0"),
        ],
        title_es="Suma de cuadrados",
        description_es="""## Suma de cuadrados

Definir, por comprension, la funcion `sumaDeCuadrados` tal que `sumaDeCuadrados n` es la suma de los cuadrados de los enteros desde `1` hasta `n`. Para `n = 0`, el resultado es `0`.

### Ejemplos:
```haskell
sumaDeCuadrados 3    -- devuelve 14
sumaDeCuadrados 100  -- devuelve 338350
```

### Perfil:
```haskell
sumaDeCuadrados :: Integer -> Integer
```
""",
        starter_code_es="-- Definir la funcion sumaDeCuadrados\nsumaDeCuadrados :: Integer -> Integer",
    ),

    # -------------------------------------------------------------------------
    # 2.2.1  Listas con un elemento replicado
    # -------------------------------------------------------------------------
    "c2-replica": Challenge(
        id="c2-replica",
        title="Replicate an Element",
        description="""## Replicate an Element

Define, using a list comprehension, a function `replica` such that `replica n x` is the list formed by `n` copies of `x`. Assume `n` is non-negative; when `n = 0`, the result is the empty list.

### Examples:
```haskell
replica 3 True  -- returns [True,True,True]
replica 2 7     -- returns [7,7]
```

### Signature:
```haskell
replica :: Int -> a -> [a]
```
""",
        solution="replica :: Int -> a -> [a]\nreplica n x = [x | _ <- [1..n]]",
        starter_code="-- Define the replica function\nreplica :: Int -> a -> [a]",
        tests=[
            TestCase(code="replica 3 True", expected="[True,True,True]"),
            TestCase(code="replica 2 7", expected="[7,7]"),
            TestCase(code="replica 0 True", expected="[]"),
        ],
        title_es="Replicar un elemento",
        description_es="""## Replicar un elemento

Definir, por comprension, la funcion `replica` tal que `replica n x` es la lista formada por `n` copias de `x`. Suponer que `n` es no negativo; cuando `n = 0`, el resultado es la lista vacia.

### Ejemplos:
```haskell
replica 3 True  -- devuelve [True,True,True]
replica 2 7     -- devuelve [7,7]
```

### Perfil:
```haskell
replica :: Int -> a -> [a]
```
""",
        starter_code_es="-- Definir la funcion replica\nreplica :: Int -> a -> [a]",
    ),

    # -------------------------------------------------------------------------
    # 2.3.1  Suma de los n primeros numeros
    # -------------------------------------------------------------------------
    "c2-suma": Challenge(
        id="c2-suma",
        title="Sum of the First N Numbers",
        description="""## Sum of the First N Numbers

Define a function `suma` such that `suma n` is the sum of the integers from `1` through `n`. For `n = 0`, the result is `0`.

### Examples:
```haskell
suma 3   -- returns 6
suma 10  -- returns 55
```

### Signature:
```haskell
suma :: Integer -> Integer
```
""",
        solution="suma :: Integer -> Integer\nsuma n = sum [1..n]",
        starter_code="-- Define the suma function\nsuma :: Integer -> Integer",
        tests=[
            TestCase(code="suma 3", expected="6"),
            TestCase(code="suma 10", expected="55"),
            TestCase(code="suma 0", expected="0"),
        ],
        title_es="Suma de los primeros numeros",
        description_es="""## Suma de los primeros numeros

Definir la funcion `suma` tal que `suma n` es la suma de los enteros desde `1` hasta `n`. Para `n = 0`, el resultado es `0`.

### Ejemplos:
```haskell
suma 3   -- devuelve 6
suma 10  -- devuelve 55
```

### Perfil:
```haskell
suma :: Integer -> Integer
```
""",
        starter_code_es="-- Definir la funcion suma\nsuma :: Integer -> Integer",
    ),

    # -------------------------------------------------------------------------
    # 2.3.2  Linea de un triangulo aritmetico
    # -------------------------------------------------------------------------
    "c2-linea": Challenge(
        id="c2-linea",
        title="Arithmetic Triangle Line",
        description="""## Arithmetic Triangle Line

Arithmetic triangles are formed as:
```haskell
[1]
[2,3]
[4,5,6]
[7,8,9,10]
```

Define `linea` such that `linea n` is the `n`th line of the arithmetic triangle, with rows numbered from `1`. Include any helper definitions you use.

### Examples:
```haskell
linea 4  -- returns [7,8,9,10]
linea 5  -- returns [11,12,13,14,15]
```

### Signature:
```haskell
linea :: Integer -> [Integer]
```
""",
        solution="suma :: Integer -> Integer\nsuma n = sum [1..n]\n\nlinea :: Integer -> [Integer]\nlinea n = [suma (n - 1) + 1..suma n]",
        starter_code="-- Define the linea function\nlinea :: Integer -> [Integer]",
        tests=[
            TestCase(code="linea 1", expected="[1]"),
            TestCase(code="linea 4", expected="[7,8,9,10]"),
            TestCase(code="linea 5", expected="[11,12,13,14,15]"),
        ],
        title_es="Linea de un triangulo aritmetico",
        description_es="""## Linea de un triangulo aritmetico

Los triangulos aritmeticos se forman asi:
```haskell
[1]
[2,3]
[4,5,6]
[7,8,9,10]
```

Definir `linea` tal que `linea n` es la linea `n`-esima del triangulo aritmetico, con filas numeradas desde `1`. Incluir las funciones auxiliares que uses.

### Ejemplos:
```haskell
linea 4  -- devuelve [7,8,9,10]
linea 5  -- devuelve [11,12,13,14,15]
```

### Perfil:
```haskell
linea :: Integer -> [Integer]
```
""",
        starter_code_es="-- Definir la funcion linea\nlinea :: Integer -> [Integer]",
    ),

    # -------------------------------------------------------------------------
    # 2.3.3  Triangulo aritmetico
    # -------------------------------------------------------------------------
    "c2-triangulo": Challenge(
        id="c2-triangulo",
        title="Arithmetic Triangle",
        description="""## Arithmetic Triangle

Define `triangulo` such that `triangulo n` is the arithmetic triangle of height `n`. A triangle of height `0` is the empty list. Include any helper definitions you use.

### Examples:
```haskell
triangulo 3  -- returns [[1],[2,3],[4,5,6]]
triangulo 4  -- returns [[1],[2,3],[4,5,6],[7,8,9,10]]
```

### Signature:
```haskell
triangulo :: Integer -> [[Integer]]
```
""",
        solution="suma :: Integer -> Integer\nsuma n = sum [1..n]\n\nlinea :: Integer -> [Integer]\nlinea n = [suma (n - 1) + 1..suma n]\n\ntriangulo :: Integer -> [[Integer]]\ntriangulo n = [linea m | m <- [1..n]]",
        starter_code="-- Define the triangulo function\ntriangulo :: Integer -> [[Integer]]",
        tests=[
            TestCase(code="triangulo 0", expected="[]"),
            TestCase(code="triangulo 3", expected="[[1],[2,3],[4,5,6]]"),
            TestCase(code="triangulo 4", expected="[[1],[2,3],[4,5,6],[7,8,9,10]]"),
        ],
        title_es="Triangulo aritmetico",
        description_es="""## Triangulo aritmetico

Definir `triangulo` tal que `triangulo n` es el triangulo aritmetico de altura `n`. Un triangulo de altura `0` es la lista vacia. Incluir las funciones auxiliares que uses.

### Ejemplos:
```haskell
triangulo 3  -- devuelve [[1],[2,3],[4,5,6]]
triangulo 4  -- devuelve [[1],[2,3],[4,5,6],[7,8,9,10]]
```

### Perfil:
```haskell
triangulo :: Integer -> [[Integer]]
```
""",
        starter_code_es="-- Definir la funcion triangulo\ntriangulo :: Integer -> [[Integer]]",
    ),

    # -------------------------------------------------------------------------
    # 2.4.1  Numeros perfectos
    # -------------------------------------------------------------------------
    "c2-perfectos": Challenge(
        id="c2-perfectos",
        title="Perfect Numbers",
        description="""## Perfect Numbers

A positive integer is perfect when it is equal to the sum of its proper factors. Proper factors are the positive factors smaller than the number itself.

Define, using a list comprehension, `perfectos` such that `perfectos n` returns the perfect numbers less than or equal to `n`, in increasing order.

### Examples:
```haskell
perfectos 500  -- returns [6,28,496]
```

### Signature:
```haskell
perfectos :: Int -> [Int]
```
""",
        solution="factores :: Int -> [Int]\nfactores n = [x | x <- [1..n], n `mod` x == 0]\n\nperfectos :: Int -> [Int]\nperfectos n = [x | x <- [1..n], sum (init (factores x)) == x]",
        starter_code="-- Define the perfectos function\nperfectos :: Int -> [Int]",
        tests=[
            TestCase(code="perfectos 7", expected="[6]"),
            TestCase(code="perfectos 29", expected="[6,28]"),
            TestCase(code="perfectos 500", expected="[6,28,496]"),
        ],
        title_es="Numeros perfectos",
        description_es="""## Numeros perfectos

Un entero positivo es perfecto si es igual a la suma de sus factores propios. Los factores propios son los factores positivos menores que el propio numero.

Definir, por comprension, `perfectos` tal que `perfectos n` devuelve los numeros perfectos menores o iguales que `n`, en orden creciente.

### Ejemplos:
```haskell
perfectos 500  -- devuelve [6,28,496]
```

### Perfil:
```haskell
perfectos :: Int -> [Int]
```
""",
        starter_code_es="-- Definir la funcion perfectos\nperfectos :: Int -> [Int]",
    ),

    # -------------------------------------------------------------------------
    # 2.5.1  Numero abundante
    # -------------------------------------------------------------------------
    "c2-numero-abundante": Challenge(
        id="c2-numero-abundante",
        title="Abundant Number",
        description="""## Abundant Number

A natural number is abundant when it is less than the sum of its proper divisors. Proper divisors are the positive divisors smaller than the number itself.

Define `numeroAbundante` such that `numeroAbundante n` returns whether `n` is abundant.

### Examples:
```haskell
numeroAbundante 5   -- returns False
numeroAbundante 12  -- returns True
numeroAbundante 28  -- returns False
numeroAbundante 30  -- returns True
```

### Signature:
```haskell
numeroAbundante :: Int -> Bool
```
""",
        solution="divisores :: Int -> [Int]\ndivisores n = [m | m <- [1..n - 1], n `mod` m == 0]\n\nnumeroAbundante :: Int -> Bool\nnumeroAbundante n = n < sum (divisores n)",
        starter_code="-- Define the numeroAbundante function\nnumeroAbundante :: Int -> Bool",
        tests=[
            TestCase(code="numeroAbundante 5", expected="False"),
            TestCase(code="numeroAbundante 12", expected="True"),
            TestCase(code="numeroAbundante 28", expected="False"),
            TestCase(code="numeroAbundante 30", expected="True"),
        ],
        title_es="Numero abundante",
        description_es="""## Numero abundante

Un numero natural es abundante si es menor que la suma de sus divisores propios. Los divisores propios son los divisores positivos menores que el propio numero.

Definir `numeroAbundante` tal que `numeroAbundante n` comprueba si `n` es abundante.

### Ejemplos:
```haskell
numeroAbundante 5   -- devuelve False
numeroAbundante 12  -- devuelve True
numeroAbundante 28  -- devuelve False
numeroAbundante 30  -- devuelve True
```

### Perfil:
```haskell
numeroAbundante :: Int -> Bool
```
""",
        starter_code_es="-- Definir la funcion numeroAbundante\nnumeroAbundante :: Int -> Bool",
    ),

    # -------------------------------------------------------------------------
    # 2.5.2  Numeros abundantes menores o iguales
    # -------------------------------------------------------------------------
    "c2-numeros-abundantes-menores": Challenge(
        id="c2-numeros-abundantes-menores",
        title="Abundant Numbers Up To N",
        description="""## Abundant Numbers Up To N

Define `numerosAbundantesMenores` such that `numerosAbundantesMenores n` is the list of abundant numbers less than or equal to `n`, in increasing order. Include any helper definitions you use.

### Examples:
```haskell
numerosAbundantesMenores 50  -- returns [12,18,20,24,30,36,40,42,48]
```

### Signature:
```haskell
numerosAbundantesMenores :: Int -> [Int]
```
""",
        solution="divisores :: Int -> [Int]\ndivisores n = [m | m <- [1..n - 1], n `mod` m == 0]\n\nnumeroAbundante :: Int -> Bool\nnumeroAbundante n = n < sum (divisores n)\n\nnumerosAbundantesMenores :: Int -> [Int]\nnumerosAbundantesMenores n = [x | x <- [1..n], numeroAbundante x]",
        starter_code="-- Define the numerosAbundantesMenores function\nnumerosAbundantesMenores :: Int -> [Int]",
        tests=[
            TestCase(code="numerosAbundantesMenores 11", expected="[]"),
            TestCase(code="numerosAbundantesMenores 12", expected="[12]"),
            TestCase(code="numerosAbundantesMenores 50", expected="[12,18,20,24,30,36,40,42,48]"),
        ],
        title_es="Numeros abundantes hasta n",
        description_es="""## Numeros abundantes hasta n

Definir `numerosAbundantesMenores` tal que `numerosAbundantesMenores n` es la lista de numeros abundantes menores o iguales que `n`, en orden creciente. Incluir las funciones auxiliares que uses.

### Ejemplos:
```haskell
numerosAbundantesMenores 50  -- devuelve [12,18,20,24,30,36,40,42,48]
```

### Perfil:
```haskell
numerosAbundantesMenores :: Int -> [Int]
```
""",
        starter_code_es="-- Definir la funcion numerosAbundantesMenores\nnumerosAbundantesMenores :: Int -> [Int]",
    ),

    # -------------------------------------------------------------------------
    # 2.5.3  Todos pares
    # -------------------------------------------------------------------------
    "c2-todos-pares": Challenge(
        id="c2-todos-pares",
        title="All Abundant Numbers Are Even",
        description="""## All Abundant Numbers Are Even

Define `todosPares` such that `todosPares n` returns whether all abundant numbers less than or equal to `n` are even. If there are no abundant numbers up to `n`, the result is `True`. Include any helper definitions you use.

### Examples:
```haskell
todosPares 10    -- returns True
todosPares 100   -- returns True
todosPares 1000  -- returns False
```

### Signature:
```haskell
todosPares :: Int -> Bool
```
""",
        solution="divisores :: Int -> [Int]\ndivisores n = [m | m <- [1..n - 1], n `mod` m == 0]\n\nnumeroAbundante :: Int -> Bool\nnumeroAbundante n = n < sum (divisores n)\n\nnumerosAbundantesMenores :: Int -> [Int]\nnumerosAbundantesMenores n = [x | x <- [1..n], numeroAbundante x]\n\ntodosPares :: Int -> Bool\ntodosPares n = and [even x | x <- numerosAbundantesMenores n]",
        starter_code="-- Define the todosPares function\ntodosPares :: Int -> Bool",
        tests=[
            TestCase(code="todosPares 10", expected="True"),
            TestCase(code="todosPares 100", expected="True"),
            TestCase(code="todosPares 1000", expected="False"),
        ],
        title_es="Todos los abundantes son pares",
        description_es="""## Todos los abundantes son pares

Definir `todosPares` tal que `todosPares n` comprueba si todos los numeros abundantes menores o iguales que `n` son pares. Si no hay numeros abundantes hasta `n`, el resultado es `True`. Incluir las funciones auxiliares que uses.

### Ejemplos:
```haskell
todosPares 10    -- devuelve True
todosPares 100   -- devuelve True
todosPares 1000  -- devuelve False
```

### Perfil:
```haskell
todosPares :: Int -> Bool
```
""",
        starter_code_es="-- Definir la funcion todosPares\ntodosPares :: Int -> Bool",
    ),

    # -------------------------------------------------------------------------
    # 2.5.4  Primer abundante impar
    # -------------------------------------------------------------------------
    "c2-primer-abundante-impar": Challenge(
        id="c2-primer-abundante-impar",
        title="First Odd Abundant Number",
        description="""## First Odd Abundant Number

Define the constant `primerAbundanteImpar` as the first natural number that is both abundant and odd. This is a constant, not a function, so it takes no arguments. Include any helper definitions you use.

### Example:
```haskell
primerAbundanteImpar  -- returns 945
```

### Signature:
```haskell
primerAbundanteImpar :: Int
```
""",
        solution="divisores :: Int -> [Int]\ndivisores n = [m | m <- [1..n - 1], n `mod` m == 0]\n\nnumeroAbundante :: Int -> Bool\nnumeroAbundante n = n < sum (divisores n)\n\nprimerAbundanteImpar :: Int\nprimerAbundanteImpar = head [x | x <- [1..], numeroAbundante x, odd x]",
        starter_code="-- Define the primerAbundanteImpar constant\nprimerAbundanteImpar :: Int",
        tests=[
            TestCase(code="primerAbundanteImpar", expected="945"),
        ],
        title_es="Primer abundante impar",
        description_es="""## Primer abundante impar

Definir la constante `primerAbundanteImpar` como el primer numero natural que es abundante e impar. Es una constante, no una funcion, por lo que no recibe argumentos. Incluir las funciones auxiliares que uses.

### Ejemplo:
```haskell
primerAbundanteImpar  -- devuelve 945
```

### Perfil:
```haskell
primerAbundanteImpar :: Int
```
""",
        starter_code_es="-- Definir la constante primerAbundanteImpar\nprimerAbundanteImpar :: Int",
    ),

    # -------------------------------------------------------------------------
    # 2.6.1  Problema 1 del proyecto Euler
    # -------------------------------------------------------------------------
    "c2-euler1": Challenge(
        id="c2-euler1",
        title="Project Euler Problem 1",
        description="""## Project Euler Problem 1

Define `euler1` such that `euler1 n` is the sum of all multiples of 3 or 5 below `n`. The bound `n` is not included, and each number must be counted only once.

### Examples:
```haskell
euler1 10    -- returns 23
euler1 1000  -- returns 233168
```

### Signature:
```haskell
euler1 :: Integer -> Integer
```
""",
        solution="euler1 :: Integer -> Integer\neuler1 n = sum [x | x <- [1..n - 1], multiplo x 3 || multiplo x 5]\n  where multiplo x y = mod x y == 0",
        starter_code="-- Define the euler1 function\neuler1 :: Integer -> Integer",
        tests=[
            TestCase(code="euler1 10", expected="23"),
            TestCase(code="euler1 16", expected="60"),
            TestCase(code="euler1 1000", expected="233168"),
        ],
        title_es="Problema 1 de Project Euler",
        description_es="""## Problema 1 de Project Euler

Definir `euler1` tal que `euler1 n` es la suma de todos los multiplos de 3 o 5 menores que `n`. El limite `n` no se incluye, y cada numero debe contarse una sola vez.

### Ejemplos:
```haskell
euler1 10    -- devuelve 23
euler1 1000  -- devuelve 233168
```

### Perfil:
```haskell
euler1 :: Integer -> Integer
```
""",
        starter_code_es="-- Definir la funcion euler1\neuler1 :: Integer -> Integer",
    ),

    # -------------------------------------------------------------------------
    # 2.7.1  Numero de pares de naturales en un circulo
    # -------------------------------------------------------------------------
    "c2-circulo": Challenge(
        id="c2-circulo",
        title="Natural Pairs Inside a Circle",
        description="""## Natural Pairs Inside a Circle

Define `circulo` such that `circulo n` is the number of natural pairs `(x,y)` inside the circle of radius `n`, using the strict inequality `x^2 + y^2 < n^2`. Natural coordinates include `0`.

### Examples:
```haskell
circulo 3  -- returns 9
circulo 4  -- returns 15
circulo 5  -- returns 22
```

### Signature:
```haskell
circulo :: Int -> Int
```
""",
        solution="circulo :: Int -> Int\ncirculo n = length [(x, y) | x <- [0..n], y <- [0..n], x^2 + y^2 < n^2]",
        starter_code="-- Define the circulo function\ncirculo :: Int -> Int",
        tests=[
            TestCase(code="circulo 1", expected="1"),
            TestCase(code="circulo 3", expected="9"),
            TestCase(code="circulo 4", expected="15"),
            TestCase(code="circulo 5", expected="22"),
        ],
        title_es="Pares naturales dentro de un circulo",
        description_es="""## Pares naturales dentro de un circulo

Definir `circulo` tal que `circulo n` es la cantidad de pares naturales `(x,y)` que estan dentro del circulo de radio `n`, usando la desigualdad estricta `x^2 + y^2 < n^2`. Las coordenadas naturales incluyen el `0`.

### Ejemplos:
```haskell
circulo 3  -- devuelve 9
circulo 4  -- devuelve 15
circulo 5  -- devuelve 22
```

### Perfil:
```haskell
circulo :: Int -> Int
```
""",
        starter_code_es="-- Definir la funcion circulo\ncirculo :: Int -> Int",
    ),

    # -------------------------------------------------------------------------
    # 2.8.1  Aproximacion del numero e
    # -------------------------------------------------------------------------
    "c2-aprox-e": Challenge(
        id="c2-aprox-e",
        title="Approximation of e",
        description="""## Approximation of e

Define `aproxE` such that `aproxE n` returns the first `n` terms of the sequence `(1 + 1/m)^m`, for `m = 1, 2, ..., n`. Treat `n` as an integer-valued `Double`.

### Examples:
```haskell
aproxE 1  -- returns [2.0]
aproxE 4  -- returns [2.0,2.25,2.37037037037037,2.44140625]
```

### Signature:
```haskell
aproxE :: Double -> [Double]
```
""",
        solution="aproxE :: Double -> [Double]\naproxE n = [(1 + 1 / m) ** m | m <- [1..n]]",
        starter_code="-- Define the aproxE function\naproxE :: Double -> [Double]",
        tests=[
            TestCase(code="aproxE 1", expected="[2.0]"),
            TestCase(code="aproxE 4", expected="[2.0,2.25,2.37037037037037,2.44140625]"),
        ],
        title_es="Aproximacion de e",
        description_es="""## Aproximacion de e

Definir `aproxE` tal que `aproxE n` devuelve los primeros `n` terminos de la sucesion `(1 + 1/m)^m`, para `m = 1, 2, ..., n`. Trata `n` como un `Double` con valor entero.

### Ejemplos:
```haskell
aproxE 1  -- devuelve [2.0]
aproxE 4  -- devuelve [2.0,2.25,2.37037037037037,2.44140625]
```

### Perfil:
```haskell
aproxE :: Double -> [Double]
```
""",
        starter_code_es="-- Definir la funcion aproxE\naproxE :: Double -> [Double]",
    ),

    # -------------------------------------------------------------------------
    # 2.8.3  Error en la aproximacion de e
    # -------------------------------------------------------------------------
    "c2-error-aprox-e": Challenge(
        id="c2-error-aprox-e",
        title="Error in the Approximation of e",
        description="""## Error in the Approximation of e

Define `errorAproxE` such that `errorAproxE x` is the smallest `m` for which `(1 + 1/m)^m` approximates `e` with absolute error strictly less than `x`.

### Examples:
```haskell
errorAproxE 0.1    -- returns 13.0
errorAproxE 0.01   -- returns 135.0
errorAproxE 0.001  -- returns 1359.0
```

### Signature:
```haskell
errorAproxE :: Double -> Double
```
""",
        solution="errorAproxE :: Double -> Double\nerrorAproxE x = head [m | m <- [1..], abs ((exp 1) - (1 + 1 / m) ** m) < x]",
        starter_code="-- Define the errorAproxE function\nerrorAproxE :: Double -> Double",
        tests=[
            TestCase(code="errorAproxE 0.1", expected="13.0"),
            TestCase(code="errorAproxE 0.01", expected="135.0"),
            TestCase(code="errorAproxE 0.001", expected="1359.0"),
        ],
        title_es="Error en la aproximacion de e",
        description_es="""## Error en la aproximacion de e

Definir `errorAproxE` tal que `errorAproxE x` es el menor `m` para el que `(1 + 1/m)^m` aproxima `e` con error absoluto estrictamente menor que `x`.

### Ejemplos:
```haskell
errorAproxE 0.1    -- devuelve 13.0
errorAproxE 0.01   -- devuelve 135.0
errorAproxE 0.001  -- devuelve 1359.0
```

### Perfil:
```haskell
errorAproxE :: Double -> Double
```
""",
        starter_code_es="-- Definir la funcion errorAproxE\nerrorAproxE :: Double -> Double",
    ),

    # -------------------------------------------------------------------------
    # 2.8.4  Aproximacion de e mediante serie
    # -------------------------------------------------------------------------
    "c2-aprox-e-prima": Challenge(
        id="c2-aprox-e-prima",
        title="Approximation of e by Series",
        description="""## Approximation of e by Series

The number `e` can also be approximated by the series `1/0! + 1/1! + 1/2! + ...`.

Define `aproxE'` such that `aproxE' n` sums the series from `1/0!` through `1/n!`.

### Examples:
```haskell
aproxE' 10   -- returns 2.718281801146385
aproxE' 100  -- returns 2.7182818284590455
```

### Signature:
```haskell
aproxE' :: Double -> Double
```
""",
        solution="aproxE' :: Double -> Double\naproxE' n = 1 + sum [1 / factorial k | k <- [1..n]]\n\nfactorial :: Double -> Double\nfactorial n = product [1..n]",
        starter_code="-- Define the aproxE' function\naproxE' :: Double -> Double",
        tests=[
            TestCase(code="aproxE' 10", expected="2.718281801146385"),
            TestCase(code="aproxE' 100", expected="2.7182818284590455"),
        ],
        title_es="Aproximacion de e por serie",
        description_es="""## Aproximacion de e por serie

El numero `e` tambien puede aproximarse mediante la serie `1/0! + 1/1! + 1/2! + ...`.

Definir `aproxE'` tal que `aproxE' n` suma la serie desde `1/0!` hasta `1/n!`.

### Ejemplos:
```haskell
aproxE' 10   -- devuelve 2.718281801146385
aproxE' 100  -- devuelve 2.7182818284590455
```

### Perfil:
```haskell
aproxE' :: Double -> Double
```
""",
        starter_code_es="-- Definir la funcion aproxE'\naproxE' :: Double -> Double",
    ),

    # -------------------------------------------------------------------------
    # 2.8.5  Constante e
    # -------------------------------------------------------------------------
    "c2-e": Challenge(
        id="c2-e",
        title="Constant e",
        description="""## Constant e

Define the constant `e` as `2.71828459`.

### Example:
```haskell
e  -- returns 2.71828459
```

### Signature:
```haskell
e :: Double
```
""",
        solution="e :: Double\ne = 2.71828459",
        starter_code="-- Define the e constant\ne :: Double",
        tests=[
            TestCase(code="e", expected="2.71828459"),
            TestCase(code="e == 2.71828459", expected="True"),
        ],
        title_es="Constante e",
        description_es="""## Constante e

Definir la constante `e` como `2.71828459`.

### Ejemplo:
```haskell
e  -- devuelve 2.71828459
```

### Perfil:
```haskell
e :: Double
```
""",
        starter_code_es="-- Definir la constante e\ne :: Double",
    ),

    # -------------------------------------------------------------------------
    # 2.8.6  Error en la aproximacion de e mediante serie
    # -------------------------------------------------------------------------
    "c2-error-e-prima": Challenge(
        id="c2-error-e-prima",
        title="Error in the Series Approximation of e",
        description="""## Error in the Series Approximation of e

Define `errorE'` such that `errorE' x` is the smallest `n` for which the factorial series approximation has absolute error strictly less than `x`. Use the constant `e = 2.71828459` from this chapter. Include any helper definitions you use.

### Examples:
```haskell
errorE' 0.1     -- returns 3.0
errorE' 0.01    -- returns 4.0
errorE' 0.001   -- returns 6.0
errorE' 0.0001  -- returns 7.0
```

### Signature:
```haskell
errorE' :: Double -> Double
```
""",
        solution="aproxE' :: Double -> Double\naproxE' n = 1 + sum [1 / factorial k | k <- [1..n]]\n\nfactorial :: Double -> Double\nfactorial n = product [1..n]\n\ne :: Double\ne = 2.71828459\n\nerrorE' :: Double -> Double\nerrorE' x = head [n | n <- [0..], abs (aproxE' n - e) < x]",
        starter_code="-- Define the errorE' function\nerrorE' :: Double -> Double",
        tests=[
            TestCase(code="errorE' 0.1", expected="3.0"),
            TestCase(code="errorE' 0.01", expected="4.0"),
            TestCase(code="errorE' 0.001", expected="6.0"),
            TestCase(code="errorE' 0.0001", expected="7.0"),
        ],
        title_es="Error en la aproximacion de e por serie",
        description_es="""## Error en la aproximacion de e por serie

Definir `errorE'` tal que `errorE' x` es el menor `n` para el que la aproximacion por la serie factorial tiene error absoluto estrictamente menor que `x`. Usa la constante `e = 2.71828459` de este capitulo. Incluir las funciones auxiliares que uses.

### Ejemplos:
```haskell
errorE' 0.1     -- devuelve 3.0
errorE' 0.01    -- devuelve 4.0
errorE' 0.001   -- devuelve 6.0
errorE' 0.0001  -- devuelve 7.0
```

### Perfil:
```haskell
errorE' :: Double -> Double
```
""",
        starter_code_es="-- Definir la funcion errorE'\nerrorE' :: Double -> Double",
    ),

    # -------------------------------------------------------------------------
    # 2.9.1  Aproximacion del limite del seno
    # -------------------------------------------------------------------------
    "c2-aprox-lim-seno": Challenge(
        id="c2-aprox-lim-seno",
        title="Sine Limit Approximation",
        description="""## Sine Limit Approximation

Define `aproxLimSeno` such that `aproxLimSeno n` returns the first `n` terms of the sequence `sin (1/m) / (1/m)`, for `m = 1, 2, ..., n`. Treat `n` as an integer-valued `Double`.

### Examples:
```haskell
aproxLimSeno 1  -- returns [0.8414709848078965]
aproxLimSeno 2  -- returns [0.8414709848078965,0.958851077208406]
```

### Signature:
```haskell
aproxLimSeno :: Double -> [Double]
```
""",
        solution="aproxLimSeno :: Double -> [Double]\naproxLimSeno n = [sin (1 / m) / (1 / m) | m <- [1..n]]",
        starter_code="-- Define the aproxLimSeno function\naproxLimSeno :: Double -> [Double]",
        tests=[
            TestCase(code="aproxLimSeno 1", expected="[0.8414709848078965]"),
            TestCase(code="aproxLimSeno 2", expected="[0.8414709848078965,0.958851077208406]"),
        ],
        title_es="Aproximacion del limite del seno",
        description_es="""## Aproximacion del limite del seno

Definir `aproxLimSeno` tal que `aproxLimSeno n` devuelve los primeros `n` terminos de la sucesion `sin (1/m) / (1/m)`, para `m = 1, 2, ..., n`. Trata `n` como un `Double` con valor entero.

### Ejemplos:
```haskell
aproxLimSeno 1  -- devuelve [0.8414709848078965]
aproxLimSeno 2  -- devuelve [0.8414709848078965,0.958851077208406]
```

### Perfil:
```haskell
aproxLimSeno :: Double -> [Double]
```
""",
        starter_code_es="-- Definir la funcion aproxLimSeno\naproxLimSeno :: Double -> [Double]",
    ),

    # -------------------------------------------------------------------------
    # 2.9.3  Error en la aproximacion del limite del seno
    # -------------------------------------------------------------------------
    "c2-error-lim-seno": Challenge(
        id="c2-error-lim-seno",
        title="Error in the Sine Limit Approximation",
        description="""## Error in the Sine Limit Approximation

Define `errorLimSeno` such that `errorLimSeno x` is the smallest `m` for which `sin (1/m) / (1/m)` approximates its limit `1` with absolute error strictly less than `x`.

### Examples:
```haskell
errorLimSeno 0.1     -- returns 2.0
errorLimSeno 0.01    -- returns 5.0
errorLimSeno 0.001   -- returns 13.0
errorLimSeno 0.0001  -- returns 41.0
```

### Signature:
```haskell
errorLimSeno :: Double -> Double
```
""",
        solution="errorLimSeno :: Double -> Double\nerrorLimSeno x = head [m | m <- [1..], abs (1 - sin (1 / m) / (1 / m)) < x]",
        starter_code="-- Define the errorLimSeno function\nerrorLimSeno :: Double -> Double",
        tests=[
            TestCase(code="errorLimSeno 0.1", expected="2.0"),
            TestCase(code="errorLimSeno 0.01", expected="5.0"),
            TestCase(code="errorLimSeno 0.001", expected="13.0"),
            TestCase(code="errorLimSeno 0.0001", expected="41.0"),
        ],
        title_es="Error en la aproximacion del limite del seno",
        description_es="""## Error en la aproximacion del limite del seno

Definir `errorLimSeno` tal que `errorLimSeno x` es el menor `m` para el que `sin (1/m) / (1/m)` aproxima su limite `1` con error absoluto estrictamente menor que `x`.

### Ejemplos:
```haskell
errorLimSeno 0.1     -- devuelve 2.0
errorLimSeno 0.01    -- devuelve 5.0
errorLimSeno 0.001   -- devuelve 13.0
errorLimSeno 0.0001  -- devuelve 41.0
```

### Perfil:
```haskell
errorLimSeno :: Double -> Double
```
""",
        starter_code_es="-- Definir la funcion errorLimSeno\nerrorLimSeno :: Double -> Double",
    ),

    # -------------------------------------------------------------------------
    # 2.10.1  Calculo de pi
    # -------------------------------------------------------------------------
    "c2-calcula-pi": Challenge(
        id="c2-calcula-pi",
        title="Approximation of pi",
        description="""## Approximation of pi

Define `calculaPi` such that `calculaPi n` approximates `pi` by summing terms from index `0` through index `n` in:
```haskell
4 * (1 - 1/3 + 1/5 - 1/7 + ... + (-1)^n/(2*n+1))
```

### Examples:
```haskell
calculaPi 3    -- returns 2.8952380952380956
calculaPi 300  -- returns 3.1449149035588526
```

### Signature:
```haskell
calculaPi :: Double -> Double
```
""",
        solution="calculaPi :: Double -> Double\ncalculaPi n = 4 * sum [(-1) ** x / (2 * x + 1) | x <- [0..n]]",
        starter_code="-- Define the calculaPi function\ncalculaPi :: Double -> Double",
        tests=[
            TestCase(code="calculaPi 3", expected="2.8952380952380956"),
            TestCase(code="calculaPi 300", expected="3.1449149035588526"),
        ],
        title_es="Aproximacion de pi",
        description_es="""## Aproximacion de pi

Definir `calculaPi` tal que `calculaPi n` aproxima `pi` sumando terminos desde el indice `0` hasta el indice `n` en:
```haskell
4 * (1 - 1/3 + 1/5 - 1/7 + ... + (-1)^n/(2*n+1))
```

### Ejemplos:
```haskell
calculaPi 3    -- devuelve 2.8952380952380956
calculaPi 300  -- devuelve 3.1449149035588526
```

### Perfil:
```haskell
calculaPi :: Double -> Double
```
""",
        starter_code_es="-- Definir la funcion calculaPi\ncalculaPi :: Double -> Double",
    ),

    # -------------------------------------------------------------------------
    # 2.10.2  Error en el calculo de pi
    # -------------------------------------------------------------------------
    "c2-error-pi": Challenge(
        id="c2-error-pi",
        title="Error in the Approximation of pi",
        description="""## Error in the Approximation of pi

Define `errorPi` such that `errorPi x` is the smallest index `n` for which `calculaPi n` approximates `pi` with absolute error strictly less than `x`. Include any helper definitions you use.

### Examples:
```haskell
errorPi 0.1    -- returns 9.0
errorPi 0.01   -- returns 99.0
errorPi 0.001  -- returns 999.0
```

### Signature:
```haskell
errorPi :: Double -> Double
```
""",
        solution="calculaPi :: Double -> Double\ncalculaPi n = 4 * sum [(-1) ** x / (2 * x + 1) | x <- [0..n]]\n\nerrorPi :: Double -> Double\nerrorPi x = head [n | n <- [1..], abs (pi - calculaPi n) < x]",
        starter_code="-- Define the errorPi function\nerrorPi :: Double -> Double",
        tests=[
            TestCase(code="errorPi 0.1", expected="9.0"),
            TestCase(code="errorPi 0.01", expected="99.0"),
            TestCase(code="errorPi 0.001", expected="999.0"),
        ],
        title_es="Error en la aproximacion de pi",
        description_es="""## Error en la aproximacion de pi

Definir `errorPi` tal que `errorPi x` es el menor indice `n` para el que `calculaPi n` aproxima `pi` con error absoluto estrictamente menor que `x`. Incluir las funciones auxiliares que uses.

### Ejemplos:
```haskell
errorPi 0.1    -- devuelve 9.0
errorPi 0.01   -- devuelve 99.0
errorPi 0.001  -- devuelve 999.0
```

### Perfil:
```haskell
errorPi :: Double -> Double
```
""",
        starter_code_es="-- Definir la funcion errorPi\nerrorPi :: Double -> Double",
    ),

    # -------------------------------------------------------------------------
    # 2.11.1  Ternas pitagoricas
    # -------------------------------------------------------------------------
    "c2-pitagoricas": Challenge(
        id="c2-pitagoricas",
        title="Pythagorean Triples",
        description="""## Pythagorean Triples

A triple `(x,y,z)` of positive integers is Pythagorean when `x^2 + y^2 = z^2`.

Define `pitagoricas` such that `pitagoricas n` returns all ordered Pythagorean triples whose components are between `1` and `n`. Ordered means `(3,4,5)` and `(4,3,5)` are different results.

### Examples:
```haskell
pitagoricas 10  -- returns [(3,4,5),(4,3,5),(6,8,10),(8,6,10)]
```

### Signature:
```haskell
pitagoricas :: Int -> [(Int,Int,Int)]
```
""",
        solution="pitagoricas :: Int -> [(Int, Int, Int)]\npitagoricas n = [(x, y, z) | x <- [1..n], y <- [1..n], z <- [1..n], x^2 + y^2 == z^2]",
        starter_code="-- Define the pitagoricas function\npitagoricas :: Int -> [(Int,Int,Int)]",
        tests=[
            TestCase(code="pitagoricas 4", expected="[]"),
            TestCase(code="pitagoricas 5", expected="[(3,4,5),(4,3,5)]"),
            TestCase(code="pitagoricas 10", expected="[(3,4,5),(4,3,5),(6,8,10),(8,6,10)]"),
        ],
        title_es="Ternas pitagoricas",
        description_es="""## Ternas pitagoricas

Una terna `(x,y,z)` de enteros positivos es pitagorica si `x^2 + y^2 = z^2`.

Definir `pitagoricas` tal que `pitagoricas n` devuelve todas las ternas pitagoricas ordenadas cuyas componentes estan entre `1` y `n`. Ordenadas significa que `(3,4,5)` y `(4,3,5)` son resultados distintos.

### Ejemplos:
```haskell
pitagoricas 10  -- devuelve [(3,4,5),(4,3,5),(6,8,10),(8,6,10)]
```

### Perfil:
```haskell
pitagoricas :: Int -> [(Int,Int,Int)]
```
""",
        starter_code_es="-- Definir la funcion pitagoricas\npitagoricas :: Int -> [(Int,Int,Int)]",
    ),

    # -------------------------------------------------------------------------
    # 2.11.2  Numero de pares de una terna
    # -------------------------------------------------------------------------
    "c2-numero-de-pares": Challenge(
        id="c2-numero-de-pares",
        title="Number of Even Elements",
        description="""## Number of Even Elements

Define `numeroDePares` such that `numeroDePares t` is the number of even elements in the triple `t`.

### Examples:
```haskell
numeroDePares (3,5,7)  -- returns 0
numeroDePares (3,6,7)  -- returns 1
numeroDePares (3,6,4)  -- returns 2
numeroDePares (4,6,4)  -- returns 3
```

### Signature:
```haskell
numeroDePares :: (Int,Int,Int) -> Int
```
""",
        solution="numeroDePares :: (Int, Int, Int) -> Int\nnumeroDePares (x, y, z) = sum [1 | n <- [x, y, z], even n]",
        starter_code="-- Define the numeroDePares function\nnumeroDePares :: (Int,Int,Int) -> Int",
        tests=[
            TestCase(code="numeroDePares (3,5,7)", expected="0"),
            TestCase(code="numeroDePares (3,6,7)", expected="1"),
            TestCase(code="numeroDePares (3,6,4)", expected="2"),
            TestCase(code="numeroDePares (4,6,4)", expected="3"),
        ],
        title_es="Numero de elementos pares",
        description_es="""## Numero de elementos pares

Definir `numeroDePares` tal que `numeroDePares t` es el numero de elementos pares de la terna `t`.

### Ejemplos:
```haskell
numeroDePares (3,5,7)  -- devuelve 0
numeroDePares (3,6,7)  -- devuelve 1
numeroDePares (3,6,4)  -- devuelve 2
numeroDePares (4,6,4)  -- devuelve 3
```

### Perfil:
```haskell
numeroDePares :: (Int,Int,Int) -> Int
```
""",
        starter_code_es="-- Definir la funcion numeroDePares\nnumeroDePares :: (Int,Int,Int) -> Int",
    ),

    # -------------------------------------------------------------------------
    # 2.11.3  Conjetura de paridad en ternas pitagoricas
    # -------------------------------------------------------------------------
    "c2-conjetura": Challenge(
        id="c2-conjetura",
        title="Parity Conjecture for Pythagorean Triples",
        description="""## Parity Conjecture for Pythagorean Triples

Define `conjetura` such that `conjetura n` returns whether every Pythagorean triple with components between `1` and `n` has an odd number of even elements. If there are no such triples, the result is `True`. Include any helper definitions you use.

### Examples:
```haskell
conjetura 10  -- returns True
```

### Signature:
```haskell
conjetura :: Int -> Bool
```
""",
        solution="pitagoricas :: Int -> [(Int, Int, Int)]\npitagoricas n = [(x, y, z) | x <- [1..n], y <- [1..n], z <- [1..n], x^2 + y^2 == z^2]\n\nnumeroDePares :: (Int, Int, Int) -> Int\nnumeroDePares (x, y, z) = sum [1 | n <- [x, y, z], even n]\n\nconjetura :: Int -> Bool\nconjetura n = and [odd (numeroDePares t) | t <- pitagoricas n]",
        starter_code="-- Define the conjetura function\nconjetura :: Int -> Bool",
        tests=[
            TestCase(code="conjetura 10", expected="True"),
            TestCase(code="conjetura 30", expected="True"),
        ],
        title_es="Conjetura de paridad en ternas pitagoricas",
        description_es="""## Conjetura de paridad en ternas pitagoricas

Definir `conjetura` tal que `conjetura n` comprueba si todas las ternas pitagoricas cuyas componentes estan entre `1` y `n` tienen un numero impar de elementos pares. Si no hay ternas, el resultado es `True`. Incluir las funciones auxiliares que uses.

### Ejemplos:
```haskell
conjetura 10  -- devuelve True
```

### Perfil:
```haskell
conjetura :: Int -> Bool
```
""",
        starter_code_es="-- Definir la funcion conjetura\nconjetura :: Int -> Bool",
    ),

    # -------------------------------------------------------------------------
    # 2.12.1  Ternas pitagoricas con una suma dada
    # -------------------------------------------------------------------------
    "c2-ternas-pitagoricas": Challenge(
        id="c2-ternas-pitagoricas",
        title="Pythagorean Triples with a Given Sum",
        description="""## Pythagorean Triples with a Given Sum

Define `ternasPitagoricas` such that `ternasPitagoricas x` returns the Pythagorean triples `(a,b,c)` where `a < b < c` and `a + b + c = x`. Do not include reordered versions of the same triple.

### Examples:
```haskell
ternasPitagoricas 12  -- returns [(3,4,5)]
ternasPitagoricas 60  -- returns [(10,24,26),(15,20,25)]
```

### Signature:
```haskell
ternasPitagoricas :: Integer -> [(Integer,Integer,Integer)]
```
""",
        solution="ternasPitagoricas :: Integer -> [(Integer, Integer, Integer)]\nternasPitagoricas x = [(a, b, c) | a <- [1..x], b <- [a + 1..x], c <- [x - a - b], a^2 + b^2 == c^2]",
        starter_code="-- Define the ternasPitagoricas function\nternasPitagoricas :: Integer -> [(Integer,Integer,Integer)]",
        tests=[
            TestCase(code="ternasPitagoricas 11", expected="[]"),
            TestCase(code="ternasPitagoricas 12", expected="[(3,4,5)]"),
            TestCase(code="ternasPitagoricas 60", expected="[(10,24,26),(15,20,25)]"),
        ],
        title_es="Ternas pitagoricas con suma dada",
        description_es="""## Ternas pitagoricas con suma dada

Definir `ternasPitagoricas` tal que `ternasPitagoricas x` devuelve las ternas pitagoricas `(a,b,c)` donde `a < b < c` y `a + b + c = x`. No incluyas reordenamientos de la misma terna.

### Ejemplos:
```haskell
ternasPitagoricas 12  -- devuelve [(3,4,5)]
ternasPitagoricas 60  -- devuelve [(10,24,26),(15,20,25)]
```

### Perfil:
```haskell
ternasPitagoricas :: Integer -> [(Integer,Integer,Integer)]
```
""",
        starter_code_es="-- Definir la funcion ternasPitagoricas\nternasPitagoricas :: Integer -> [(Integer,Integer,Integer)]",
    ),

    # -------------------------------------------------------------------------
    # 2.12.2  Problema 9 del proyecto Euler
    # -------------------------------------------------------------------------
    "c2-euler9": Challenge(
        id="c2-euler9",
        title="Project Euler Problem 9",
        description="""## Project Euler Problem 9

Define the constant `euler9` as the product `a*b*c`, where `(a,b,c)` is the unique Pythagorean triple with `a + b + c = 1000`. This is a constant, not a function. Include any helper definitions you use.

### Example:
```haskell
euler9  -- returns 31875000
```

### Signature:
```haskell
euler9 :: Integer
```
""",
        solution="ternasPitagoricas :: Integer -> [(Integer, Integer, Integer)]\nternasPitagoricas x = [(a, b, c) | a <- [1..x], b <- [a + 1..x], c <- [x - a - b], a^2 + b^2 == c^2]\n\neuler9 :: Integer\neuler9 = a * b * c\n  where (a, b, c) = head (ternasPitagoricas 1000)",
        starter_code="-- Define the euler9 constant\neuler9 :: Integer",
        tests=[
            TestCase(code="euler9", expected="31875000"),
        ],
        title_es="Problema 9 de Project Euler",
        description_es="""## Problema 9 de Project Euler

Definir la constante `euler9` como el producto `a*b*c`, donde `(a,b,c)` es la unica terna pitagorica con `a + b + c = 1000`. Es una constante, no una funcion. Incluir las funciones auxiliares que uses.

### Ejemplo:
```haskell
euler9  -- devuelve 31875000
```

### Perfil:
```haskell
euler9 :: Integer
```
""",
        starter_code_es="-- Definir la constante euler9\neuler9 :: Integer",
    ),

    # -------------------------------------------------------------------------
    # 2.13.1  Producto escalar
    # -------------------------------------------------------------------------
    "c2-producto-escalar": Challenge(
        id="c2-producto-escalar",
        title="Dot Product",
        description="""## Dot Product

The dot product of two integer lists of the same length is the sum of the products of corresponding elements. Assume both input lists have the same length.

Define `productoEscalar` using a list comprehension.

### Examples:
```haskell
productoEscalar [1,2,3] [4,5,6]  -- returns 32
```

### Signature:
```haskell
productoEscalar :: [Int] -> [Int] -> Int
```
""",
        solution="productoEscalar :: [Int] -> [Int] -> Int\nproductoEscalar xs ys = sum [x * y | (x, y) <- zip xs ys]",
        starter_code="-- Define the productoEscalar function\nproductoEscalar :: [Int] -> [Int] -> Int",
        tests=[
            TestCase(code="productoEscalar [1,2,3] [4,5,6]", expected="32"),
            TestCase(code="productoEscalar [1,-2,3] [4,5,-6]", expected="-24"),
            TestCase(code="productoEscalar [] []", expected="0"),
        ],
        title_es="Producto escalar",
        description_es="""## Producto escalar

El producto escalar de dos listas de enteros de la misma longitud es la suma de los productos de los elementos correspondientes. Suponer que ambas listas tienen la misma longitud.

Definir `productoEscalar` usando una lista por comprension.

### Ejemplos:
```haskell
productoEscalar [1,2,3] [4,5,6]  -- devuelve 32
```

### Perfil:
```haskell
productoEscalar :: [Int] -> [Int] -> Int
```
""",
        starter_code_es="-- Definir la funcion productoEscalar\nproductoEscalar :: [Int] -> [Int] -> Int",
    ),

    # -------------------------------------------------------------------------
    # 2.14.1  Suma de pares de elementos consecutivos
    # -------------------------------------------------------------------------
    "c2-suma-consecutivos": Challenge(
        id="c2-suma-consecutivos",
        title="Sums of Consecutive Elements",
        description="""## Sums of Consecutive Elements

Define, using a list comprehension, `sumaConsecutivos` such that `sumaConsecutivos xs` is the list of sums of consecutive pairs in `xs`. Lists with fewer than two elements return `[]`.

### Examples:
```haskell
sumaConsecutivos [3,1,5,2]  -- returns [4,6,7]
sumaConsecutivos [3]        -- returns []
```

### Signature:
```haskell
sumaConsecutivos :: [Int] -> [Int]
```
""",
        solution="sumaConsecutivos :: [Int] -> [Int]\nsumaConsecutivos xs = [x + y | (x, y) <- zip xs (tail xs)]",
        starter_code="-- Define the sumaConsecutivos function\nsumaConsecutivos :: [Int] -> [Int]",
        tests=[
            TestCase(code="sumaConsecutivos [3,1,5,2]", expected="[4,6,7]"),
            TestCase(code="sumaConsecutivos [3]", expected="[]"),
            TestCase(code="sumaConsecutivos []", expected="[]"),
        ],
        title_es="Suma de consecutivos",
        description_es="""## Suma de consecutivos

Definir, por comprension, `sumaConsecutivos` tal que `sumaConsecutivos xs` es la lista de las sumas de pares consecutivos de `xs`. Las listas con menos de dos elementos devuelven `[]`.

### Ejemplos:
```haskell
sumaConsecutivos [3,1,5,2]  -- devuelve [4,6,7]
sumaConsecutivos [3]        -- devuelve []
```

### Perfil:
```haskell
sumaConsecutivos :: [Int] -> [Int]
```
""",
        starter_code_es="-- Definir la funcion sumaConsecutivos\nsumaConsecutivos :: [Int] -> [Int]",
    ),

    # -------------------------------------------------------------------------
    # 2.15.1  Posiciones de un elemento en una lista
    # -------------------------------------------------------------------------
    "c2-posiciones-prima": Challenge(
        id="c2-posiciones-prima",
        title="Positions of an Element",
        description="""## Positions of an Element

Define `posiciones'` such that `posiciones' x xs` is the list of zero-based positions occupied by `x` in `xs`, from left to right. The chapter asks for a definition using a helper function `busca`; include any helper definitions you use.

### Examples:
```haskell
posiciones' 5 [1,5,3,5,5,7]  -- returns [1,3,4]
posiciones' 'a' "banana"     -- returns [1,3,5]
```

### Signature:
```haskell
posiciones' :: Eq a => a -> [a] -> [Int]
```
""",
        solution="busca :: Eq a => a -> [(a, b)] -> [b]\nbusca c t = [v | (c', v) <- t, c' == c]\n\nposiciones' :: Eq a => a -> [a] -> [Int]\nposiciones' x xs = busca x (zip xs [0..])",
        starter_code="-- Define the posiciones' function\nposiciones' :: Eq a => a -> [a] -> [Int]",
        tests=[
            TestCase(code="posiciones' 5 [1,5,3,5,5,7]", expected="[1,3,4]"),
            TestCase(code="posiciones' 'a' \"banana\"", expected="[1,3,5]"),
            TestCase(code="posiciones' True [False,False]", expected="[]"),
        ],
        title_es="Posiciones de un elemento",
        description_es="""## Posiciones de un elemento

Definir `posiciones'` tal que `posiciones' x xs` es la lista de posiciones, empezando en cero, ocupadas por `x` en `xs`, de izquierda a derecha. El capitulo pide una definicion usando la funcion auxiliar `busca`; incluir las funciones auxiliares que uses.

### Ejemplos:
```haskell
posiciones' 5 [1,5,3,5,5,7]  -- devuelve [1,3,4]
posiciones' 'a' "banana"     -- devuelve [1,3,5]
```

### Perfil:
```haskell
posiciones' :: Eq a => a -> [a] -> [Int]
```
""",
        starter_code_es="-- Definir la funcion posiciones'\nposiciones' :: Eq a => a -> [a] -> [Int]",
    ),

    # -------------------------------------------------------------------------
    # 2.16.1  Representacion densa de un polinomio
    # -------------------------------------------------------------------------
    "c2-densa": Challenge(
        id="c2-densa",
        title="Dense Polynomial Representation",
        description="""## Dense Polynomial Representation

A polynomial can be represented densely by listing its coefficients from highest degree to constant term. Define `densa` such that it converts that dense representation into `(degree, coefficient)` pairs, omitting zero coefficients.

### Examples:
```haskell
densa [6,0,-5,4,-7]  -- returns [(4,6),(2,-5),(1,4),(0,-7)]
densa [6,0,0,3,0,4]  -- returns [(5,6),(2,3),(0,4)]
```

### Signature:
```haskell
densa :: [Int] -> [(Int,Int)]
```
""",
        solution="densa :: [Int] -> [(Int, Int)]\ndensa xs = [(x, y) | (x, y) <- zip [n - 1, n - 2..0] xs, y /= 0]\n  where n = length xs",
        starter_code="-- Define the densa function\ndensa :: [Int] -> [(Int,Int)]",
        tests=[
            TestCase(code="densa [6,0,-5,4,-7]", expected="[(4,6),(2,-5),(1,4),(0,-7)]"),
            TestCase(code="densa [6,0,0,3,0,4]", expected="[(5,6),(2,3),(0,4)]"),
            TestCase(code="densa [0,0,0]", expected="[]"),
        ],
        title_es="Representacion densa de polinomios",
        description_es="""## Representacion densa de polinomios

Un polinomio puede representarse de forma densa listando sus coeficientes desde el grado mayor hasta el termino constante. Definir `densa` tal que convierta esa representacion densa en pares `(grado, coeficiente)`, omitiendo coeficientes cero.

### Ejemplos:
```haskell
densa [6,0,-5,4,-7]  -- devuelve [(4,6),(2,-5),(1,4),(0,-7)]
densa [6,0,0,3,0,4]  -- devuelve [(5,6),(2,3),(0,4)]
```

### Perfil:
```haskell
densa :: [Int] -> [(Int,Int)]
```
""",
        starter_code_es="-- Definir la funcion densa\ndensa :: [Int] -> [(Int,Int)]",
    ),

    # -------------------------------------------------------------------------
    # 2.17.1  Producto cartesiano
    # -------------------------------------------------------------------------
    "c2-pares-prima": Challenge(
        id="c2-pares-prima",
        title="Cartesian Product",
        description="""## Cartesian Product

Define `pares'` equivalent to:
```haskell
pares xs ys = [(x,y) | x <- xs, y <- ys]
```

Use two list comprehensions with one generator each. Preserve the same order as the standard nested comprehension: pair each `x` with every element of `ys` before moving to the next `x`.

### Examples:
```haskell
pares' [1..3] [4..6]  -- returns [(1,4),(1,5),(1,6),(2,4),(2,5),(2,6),(3,4),(3,5),(3,6)]
```

### Signature:
```haskell
pares' :: [a] -> [b] -> [(a,b)]
```
""",
        solution="pares' :: [a] -> [b] -> [(a, b)]\npares' xs ys = concat [[(x, y) | y <- ys] | x <- xs]",
        starter_code="-- Define the pares' function\npares' :: [a] -> [b] -> [(a,b)]",
        tests=[
            TestCase(code="pares' [1..3] [4..6]", expected="[(1,4),(1,5),(1,6),(2,4),(2,5),(2,6),(3,4),(3,5),(3,6)]"),
            TestCase(code="pares' \"ab\" [1,2]", expected="[(\'a\',1),(\'a\',2),(\'b\',1),(\'b\',2)]"),
            TestCase(code="pares' ([] :: [Int]) [1,2]", expected="[]"),
        ],
        title_es="Producto cartesiano",
        description_es="""## Producto cartesiano

Definir `pares'` equivalente a:
```haskell
pares xs ys = [(x,y) | x <- xs, y <- ys]
```

Usar dos listas por comprension con un generador cada una. Conserva el mismo orden que la comprension anidada: combina cada `x` con todos los elementos de `ys` antes de pasar al siguiente `x`.

### Ejemplos:
```haskell
pares' [1..3] [4..6]  -- devuelve [(1,4),(1,5),(1,6),(2,4),(2,5),(2,6),(3,4),(3,5),(3,6)]
```

### Perfil:
```haskell
pares' :: [a] -> [b] -> [(a,b)]
```
""",
        starter_code_es="-- Definir la funcion pares'\npares' :: [a] -> [b] -> [(a,b)]",
    ),

    # -------------------------------------------------------------------------
    # 2.18.1  Nombres en una base de datos
    # -------------------------------------------------------------------------
    "c2-nombres": Challenge(
        id="c2-nombres",
        title="Names in a Database",
        description="""## Names in a Database

A person database is represented as a list of `(name, activity, birthYear, deathYear)` tuples. Preserve the order of the database rows.

Define `nombres` such that `nombres bd` is the list of names in `bd`.

### Example:
```haskell
nombres [("Ana","Ciencia",1900,1980),("Luis","Musica",1910,1990)]
-- returns ["Ana","Luis"]
```

### Signature:
```haskell
nombres :: [(String,String,Int,Int)] -> [String]
```
""",
        solution="nombres :: [(String, String, Int, Int)] -> [String]\nnombres bd = [x | (x, _, _, _) <- bd]",
        starter_code="-- Define the nombres function\nnombres :: [(String,String,Int,Int)] -> [String]",
        tests=[
            TestCase(code="nombres [(\"Ana\",\"Ciencia\",1900,1980),(\"Luis\",\"Musica\",1910,1990)]", expected="[\"Ana\",\"Luis\"]"),
            TestCase(code="nombres []", expected="[]"),
        ],
        title_es="Nombres en una base de datos",
        description_es="""## Nombres en una base de datos

Una base de datos de personas se representa como una lista de tuplas `(nombre, actividad, nacimiento, fallecimiento)`. Conserva el orden de las filas de la base de datos.

Definir `nombres` tal que `nombres bd` es la lista de nombres de `bd`.

### Ejemplo:
```haskell
nombres [("Ana","Ciencia",1900,1980),("Luis","Musica",1910,1990)]
-- devuelve ["Ana","Luis"]
```

### Perfil:
```haskell
nombres :: [(String,String,Int,Int)] -> [String]
```
""",
        starter_code_es="-- Definir la funcion nombres\nnombres :: [(String,String,Int,Int)] -> [String]",
    ),

    # -------------------------------------------------------------------------
    # 2.18.2  Musicos en una base de datos
    # -------------------------------------------------------------------------
    "c2-musicos": Challenge(
        id="c2-musicos",
        title="Musicians in a Database",
        description="""## Musicians in a Database

Define `musicos` such that `musicos bd` is the list of names whose activity is exactly `"Musica"`.

### Example:
```haskell
musicos [("Ana","Ciencia",1900,1980),("Luis","Musica",1910,1990)]
-- returns ["Luis"]
```

### Signature:
```haskell
musicos :: [(String,String,Int,Int)] -> [String]
```
""",
        solution="musicos :: [(String, String, Int, Int)] -> [String]\nmusicos bd = [x | (x, m, _, _) <- bd, m == \"Musica\"]",
        starter_code="-- Define the musicos function\nmusicos :: [(String,String,Int,Int)] -> [String]",
        tests=[
            TestCase(code="musicos [(\"Ana\",\"Ciencia\",1900,1980),(\"Luis\",\"Musica\",1910,1990),(\"Marta\",\"Musica\",1920,2000)]", expected="[\"Luis\",\"Marta\"]"),
            TestCase(code="musicos [(\"Ana\",\"Ciencia\",1900,1980)]", expected="[]"),
        ],
        title_es="Musicos en una base de datos",
        description_es="""## Musicos en una base de datos

Definir `musicos` tal que `musicos bd` es la lista de nombres cuya actividad es exactamente `"Musica"`.

### Ejemplo:
```haskell
musicos [("Ana","Ciencia",1900,1980),("Luis","Musica",1910,1990)]
-- devuelve ["Luis"]
```

### Perfil:
```haskell
musicos :: [(String,String,Int,Int)] -> [String]
```
""",
        starter_code_es="-- Definir la funcion musicos\nmusicos :: [(String,String,Int,Int)] -> [String]",
    ),

    # -------------------------------------------------------------------------
    # 2.18.3  Seleccion por actividad
    # -------------------------------------------------------------------------
    "c2-seleccion": Challenge(
        id="c2-seleccion",
        title="Select by Activity",
        description="""## Select by Activity

Define `seleccion` such that `seleccion bd m` is the list of names whose activity is `m`.

### Example:
```haskell
seleccion [("Velazquez","Pintura",1599,1660),("Bach","Musica",1685,1750)] "Pintura"
-- returns ["Velazquez"]
```

### Signature:
```haskell
seleccion :: [(String,String,Int,Int)] -> String -> [String]
```
""",
        solution="seleccion :: [(String, String, Int, Int)] -> String -> [String]\nseleccion bd m = [x | (x, m', _, _) <- bd, m == m']",
        starter_code="-- Define the seleccion function\nseleccion :: [(String,String,Int,Int)] -> String -> [String]",
        tests=[
            TestCase(code="seleccion [(\"Velazquez\",\"Pintura\",1599,1660),(\"Picasso\",\"Pintura\",1881,1973),(\"Bach\",\"Musica\",1685,1750)] \"Pintura\"", expected="[\"Velazquez\",\"Picasso\"]"),
            TestCase(code="seleccion [(\"Bach\",\"Musica\",1685,1750)] \"Ciencia\"", expected="[]"),
        ],
        title_es="Seleccion por actividad",
        description_es="""## Seleccion por actividad

Definir `seleccion` tal que `seleccion bd m` es la lista de nombres cuya actividad es `m`.

### Ejemplo:
```haskell
seleccion [("Velazquez","Pintura",1599,1660),("Bach","Musica",1685,1750)] "Pintura"
-- devuelve ["Velazquez"]
```

### Perfil:
```haskell
seleccion :: [(String,String,Int,Int)] -> String -> [String]
```
""",
        starter_code_es="-- Definir la funcion seleccion\nseleccion :: [(String,String,Int,Int)] -> String -> [String]",
    ),

    # -------------------------------------------------------------------------
    # 2.18.4  Musicos usando seleccion
    # -------------------------------------------------------------------------
    "c2-musicos-prima": Challenge(
        id="c2-musicos-prima",
        title="Musicians Using Selection",
        description="""## Musicians Using Selection

Define `musicos'` using `seleccion`, such that `musicos' bd` is the list of names whose activity is `"Musica"`. Include any helper definitions you use.

### Example:
```haskell
musicos' [("Ana","Ciencia",1900,1980),("Luis","Musica",1910,1990)]
-- returns ["Luis"]
```

### Signature:
```haskell
musicos' :: [(String,String,Int,Int)] -> [String]
```
""",
        solution="seleccion :: [(String, String, Int, Int)] -> String -> [String]\nseleccion bd m = [x | (x, m', _, _) <- bd, m == m']\n\nmusicos' :: [(String, String, Int, Int)] -> [String]\nmusicos' bd = seleccion bd \"Musica\"",
        starter_code="-- Define the musicos' function\nmusicos' :: [(String,String,Int,Int)] -> [String]",
        tests=[
            TestCase(code="musicos' [(\"Ana\",\"Ciencia\",1900,1980),(\"Luis\",\"Musica\",1910,1990),(\"Marta\",\"Musica\",1920,2000)]", expected="[\"Luis\",\"Marta\"]"),
            TestCase(code="musicos' [(\"Ana\",\"Ciencia\",1900,1980)]", expected="[]"),
        ],
        title_es="Musicos usando seleccion",
        description_es="""## Musicos usando seleccion

Definir `musicos'` usando `seleccion`, tal que `musicos' bd` es la lista de nombres cuya actividad es `"Musica"`. Incluir las funciones auxiliares que uses.

### Ejemplo:
```haskell
musicos' [("Ana","Ciencia",1900,1980),("Luis","Musica",1910,1990)]
-- devuelve ["Luis"]
```

### Perfil:
```haskell
musicos' :: [(String,String,Int,Int)] -> [String]
```
""",
        starter_code_es="-- Definir la funcion musicos'\nmusicos' :: [(String,String,Int,Int)] -> [String]",
    ),

    # -------------------------------------------------------------------------
    # 2.18.5  Personas vivas en un anio
    # -------------------------------------------------------------------------
    "c2-vivas": Challenge(
        id="c2-vivas",
        title="People Alive in a Year",
        description="""## People Alive in a Year

Define `vivas` such that `vivas bd a` is the list of names of people who were alive in year `a`. A person is alive in year `a` when `birthYear <= a <= deathYear`.

### Example:
```haskell
vivas [("Cervantes","Literatura",1547,1616),("Bach","Musica",1685,1750)] 1600
-- returns ["Cervantes"]
```

### Signature:
```haskell
vivas :: [(String,String,Int,Int)] -> Int -> [String]
```
""",
        solution="vivas :: [(String, String, Int, Int)] -> Int -> [String]\nvivas ps a = [x | (x, _, a1, a2) <- ps, a1 <= a, a <= a2]",
        starter_code="-- Define the vivas function\nvivas :: [(String,String,Int,Int)] -> Int -> [String]",
        tests=[
            TestCase(code="vivas [(\"Cervantes\",\"Literatura\",1547,1616),(\"Velazquez\",\"Pintura\",1599,1660),(\"Quevedo\",\"Literatura\",1580,1654),(\"Borromini\",\"Arquitectura\",1599,1667)] 1600", expected="[\"Cervantes\",\"Velazquez\",\"Quevedo\",\"Borromini\"]"),
            TestCase(code="vivas [(\"Bach\",\"Musica\",1685,1750),(\"Einstein\",\"Ciencia\",1879,1955)] 1800", expected="[]"),
        ],
        title_es="Personas vivas en un anio",
        description_es="""## Personas vivas en un anio

Definir `vivas` tal que `vivas bd a` es la lista de nombres de las personas que estaban vivas en el anio `a`. Una persona esta viva en el anio `a` cuando `nacimiento <= a <= fallecimiento`.

### Ejemplo:
```haskell
vivas [("Cervantes","Literatura",1547,1616),("Bach","Musica",1685,1750)] 1600
-- devuelve ["Cervantes"]
```

### Perfil:
```haskell
vivas :: [(String,String,Int,Int)] -> Int -> [String]
```
""",
        starter_code_es="-- Definir la funcion vivas\nvivas :: [(String,String,Int,Int)] -> Int -> [String]",
    ),
}
