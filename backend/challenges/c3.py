"""Chapter 3: Recursive definitions - Challenges from 'Piensa en Haskell'."""

from typing import Dict

from .data import Challenge, TestCase


CHAPTER_3_CHALLENGES: Dict[str, Challenge] = {
    # -------------------------------------------------------------------------
    # 3.1.1  Potencia de exponente natural
    # -------------------------------------------------------------------------
    "c3-potencia": Challenge(
        id="c3-potencia",
        title="Power with a Natural Exponent",
        description="""## Power with a Natural Exponent

Define, by recursion, a function `potencia` such that `potencia x n` is `x` raised to the natural number `n`. Assume `n >= 0`; the base case should handle exponent `0`.

### Examples:
```haskell
potencia 2 3  -- returns 8
potencia 5 0  -- returns 1
```

### Signature:
```haskell
potencia :: Integer -> Integer -> Integer
```
""",
        solution="potencia :: Integer -> Integer -> Integer\npotencia _ 0 = 1\npotencia x n = x * potencia x (n - 1)",
        starter_code="-- Define the potencia function recursively\npotencia :: Integer -> Integer -> Integer",
        tests=[
            TestCase(code="potencia 2 3", expected="8"),
            TestCase(code="potencia 5 0", expected="1"),
            TestCase(code="potencia 3 4", expected="81"),
        ],
        title_es="Potencia de exponente natural",
        description_es="""## Potencia de exponente natural

Definir, por recursion, la funcion `potencia` tal que `potencia x n` es `x` elevado al numero natural `n`. Suponer que `n >= 0`; el caso base debe cubrir el exponente `0`.

### Ejemplos:
```haskell
potencia 2 3  -- devuelve 8
potencia 5 0  -- devuelve 1
```

### Perfil:
```haskell
potencia :: Integer -> Integer -> Integer
```
""",
        starter_code_es="-- Definir recursivamente la funcion potencia\npotencia :: Integer -> Integer -> Integer",
    ),

    # -------------------------------------------------------------------------
    # 3.2.1  Replicacion de un elemento
    # -------------------------------------------------------------------------
    "c3-replicate-prima": Challenge(
        id="c3-replicate-prima",
        title="Replicate an Element Recursively",
        description="""## Replicate an Element Recursively

Define, by recursion, a function `replicate'` such that `replicate' n x` is the list formed by `n` copies of `x`. Assume `n` is non-negative; when `n = 0`, return `[]`.

### Examples:
```haskell
replicate' 3 2     -- returns [2,2,2]
replicate' 2 True  -- returns [True,True]
```

### Signature:
```haskell
replicate' :: Int -> a -> [a]
```
""",
        solution="replicate' :: Int -> a -> [a]\nreplicate' 0 _ = []\nreplicate' n x = x : replicate' (n - 1) x",
        starter_code="-- Define the replicate' function recursively\nreplicate' :: Int -> a -> [a]",
        tests=[
            TestCase(code="replicate' 3 2", expected="[2,2,2]"),
            TestCase(code="replicate' 2 True", expected="[True,True]"),
            TestCase(code="replicate' 0 'a'", expected="\"\""),
        ],
        title_es="Replicacion de un elemento",
        description_es="""## Replicacion de un elemento

Definir, por recursion, la funcion `replicate'` tal que `replicate' n x` es la lista formada por `n` copias del elemento `x`. Suponer que `n` es no negativo; cuando `n = 0`, devolver `[]`.

### Ejemplos:
```haskell
replicate' 3 2     -- devuelve [2,2,2]
replicate' 2 True  -- devuelve [True,True]
```

### Perfil:
```haskell
replicate' :: Int -> a -> [a]
```
""",
        starter_code_es="-- Definir recursivamente la funcion replicate'\nreplicate' :: Int -> a -> [a]",
    ),

    # -------------------------------------------------------------------------
    # 3.3.1  Doble factorial
    # -------------------------------------------------------------------------
    "c3-doble-factorial": Challenge(
        id="c3-doble-factorial",
        title="Double Factorial",
        description="""## Double Factorial

The double factorial of `n` multiplies every second number down to `1` or `2`.

Define, by recursion, a function `dobleFactorial` such that `dobleFactorial n` is the double factorial of `n`. Assume `n >= 0`; use `0` and `1` as base cases.

### Examples:
```haskell
dobleFactorial 8  -- returns 384
dobleFactorial 9  -- returns 945
```

### Signature:
```haskell
dobleFactorial :: Integer -> Integer
```
""",
        solution="dobleFactorial :: Integer -> Integer\ndobleFactorial 0 = 1\ndobleFactorial 1 = 1\ndobleFactorial n = n * dobleFactorial (n - 2)",
        starter_code="-- Define the dobleFactorial function recursively\ndobleFactorial :: Integer -> Integer",
        tests=[
            TestCase(code="dobleFactorial 0", expected="1"),
            TestCase(code="dobleFactorial 8", expected="384"),
            TestCase(code="dobleFactorial 9", expected="945"),
        ],
        title_es="Doble factorial",
        description_es="""## Doble factorial

El doble factorial de `n` multiplica numeros alternos hasta llegar a `1` o `2`.

Definir, por recursion, la funcion `dobleFactorial` tal que `dobleFactorial n` es el doble factorial de `n`. Suponer que `n >= 0`; usa `0` y `1` como casos base.

### Ejemplos:
```haskell
dobleFactorial 8  -- devuelve 384
dobleFactorial 9  -- devuelve 945
```

### Perfil:
```haskell
dobleFactorial :: Integer -> Integer
```
""",
        starter_code_es="-- Definir recursivamente la funcion dobleFactorial\ndobleFactorial :: Integer -> Integer",
    ),

    # -------------------------------------------------------------------------
    # 3.4.1  Algoritmo de Euclides del maximo comun divisor
    # -------------------------------------------------------------------------
    "c3-mcd": Challenge(
        id="c3-mcd",
        title="Euclidean Greatest Common Divisor",
        description="""## Euclidean Greatest Common Divisor

Define a function `mcd` such that `mcd a b` is the greatest common divisor of `a` and `b`, computed with Euclid's algorithm. When the second argument is `0`, return the first argument.

### Examples:
```haskell
mcd 30 45  -- returns 15
mcd 18 24  -- returns 6
```

### Signature:
```haskell
mcd :: Integer -> Integer -> Integer
```
""",
        solution="mcd :: Integer -> Integer -> Integer\nmcd a 0 = a\nmcd a b = mcd b (a `mod` b)",
        starter_code="-- Define the mcd function recursively\nmcd :: Integer -> Integer -> Integer",
        tests=[
            TestCase(code="mcd 30 45", expected="15"),
            TestCase(code="mcd 18 24", expected="6"),
            TestCase(code="mcd 7 3", expected="1"),
        ],
        title_es="Algoritmo de Euclides del maximo comun divisor",
        description_es="""## Algoritmo de Euclides del maximo comun divisor

Definir la funcion `mcd` tal que `mcd a b` es el maximo comun divisor de `a` y `b`, calculado mediante el algoritmo de Euclides. Cuando el segundo argumento es `0`, devolver el primero.

### Ejemplos:
```haskell
mcd 30 45  -- devuelve 15
mcd 18 24  -- devuelve 6
```

### Perfil:
```haskell
mcd :: Integer -> Integer -> Integer
```
""",
        starter_code_es="-- Definir recursivamente la funcion mcd\nmcd :: Integer -> Integer -> Integer",
    ),

    # -------------------------------------------------------------------------
    # 3.5.1  Menor numero divisible por una sucesion de numeros
    # -------------------------------------------------------------------------
    "c3-menor-divisible": Challenge(
        id="c3-menor-divisible",
        title="Smallest Number Divisible by a Range",
        description="""## Smallest Number Divisible by a Range

Define, by recursion, a function `menorDivisible` such that `menorDivisible a b` is the smallest number divisible by every integer from `a` to `b`, including both endpoints. Assume `a <= b`.

**Hint:** Use `lcm`, the least common multiple.

### Examples:
```haskell
menorDivisible 2 5   -- returns 60
menorDivisible 1 10  -- returns 2520
```

### Signature:
```haskell
menorDivisible :: Integer -> Integer -> Integer
```
""",
        solution="menorDivisible :: Integer -> Integer -> Integer\nmenorDivisible a b\n  | a == b    = a\n  | otherwise = lcm a (menorDivisible (a + 1) b)",
        starter_code="-- Define the menorDivisible function recursively\nmenorDivisible :: Integer -> Integer -> Integer",
        tests=[
            TestCase(code="menorDivisible 2 5", expected="60"),
            TestCase(code="menorDivisible 1 10", expected="2520"),
            TestCase(code="menorDivisible 6 6", expected="6"),
        ],
        title_es="Menor numero divisible por una sucesion",
        description_es="""## Menor numero divisible por una sucesion

Definir, por recursion, la funcion `menorDivisible` tal que `menorDivisible a b` es el menor numero divisible por todos los enteros desde `a` hasta `b`, incluyendo ambos extremos. Suponer que `a <= b`.

**Indicacion:** Usar `lcm`, el minimo comun multiplo.

### Ejemplos:
```haskell
menorDivisible 2 5   -- devuelve 60
menorDivisible 1 10  -- devuelve 2520
```

### Perfil:
```haskell
menorDivisible :: Integer -> Integer -> Integer
```
""",
        starter_code_es="-- Definir recursivamente la funcion menorDivisible\nmenorDivisible :: Integer -> Integer -> Integer",
    ),

    # -------------------------------------------------------------------------
    # 3.5.2  Problema 5 de Project Euler
    # -------------------------------------------------------------------------
    "c3-euler5": Challenge(
        id="c3-euler5",
        title="Project Euler Problem 5",
        description="""## Project Euler Problem 5

Define the constant `euler5` as the smallest number divisible by all integers from `1` to `20`. This is a constant, not a function.

Include any helper definitions you use.

### Example:
```haskell
euler5  -- returns 232792560
```

### Signature:
```haskell
euler5 :: Integer
```
""",
        solution="menorDivisible :: Integer -> Integer -> Integer\nmenorDivisible a b\n  | a == b    = a\n  | otherwise = lcm a (menorDivisible (a + 1) b)\n\neuler5 :: Integer\neuler5 = menorDivisible 1 20",
        starter_code="-- Define the euler5 constant\neuler5 :: Integer",
        tests=[
            TestCase(code="euler5", expected="232792560"),
            TestCase(code="euler5 `mod` 20", expected="0"),
        ],
        title_es="Problema 5 de Project Euler",
        description_es="""## Problema 5 de Project Euler

Definir la constante `euler5` como el menor numero divisible por todos los enteros desde `1` hasta `20`. Es una constante, no una funcion.

Incluir las funciones auxiliares que uses.

### Ejemplo:
```haskell
euler5  -- devuelve 232792560
```

### Perfil:
```haskell
euler5 :: Integer
```
""",
        starter_code_es="-- Definir la constante euler5\neuler5 :: Integer",
    ),

    # -------------------------------------------------------------------------
    # 3.6.1  Numero de pasos para resolver las torres de Hanoi
    # -------------------------------------------------------------------------
    "c3-num-pasos-hanoi": Challenge(
        id="c3-num-pasos-hanoi",
        title="Number of Steps for Towers of Hanoi",
        description="""## Number of Steps for Towers of Hanoi

Define a function `numPasosHanoi` such that `numPasosHanoi n` is the number of steps needed to move `n` rings in the Towers of Hanoi problem. Assume `n >= 1`.

### Examples:
```haskell
numPasosHanoi 2   -- returns 3
numPasosHanoi 7   -- returns 127
numPasosHanoi 64  -- returns 18446744073709551615
```

### Signature:
```haskell
numPasosHanoi :: Integer -> Integer
```
""",
        solution="numPasosHanoi :: Integer -> Integer\nnumPasosHanoi 1 = 1\nnumPasosHanoi n = 1 + 2 * numPasosHanoi (n - 1)",
        starter_code="-- Define the numPasosHanoi function recursively\nnumPasosHanoi :: Integer -> Integer",
        tests=[
            TestCase(code="numPasosHanoi 2", expected="3"),
            TestCase(code="numPasosHanoi 7", expected="127"),
            TestCase(code="numPasosHanoi 64", expected="18446744073709551615"),
        ],
        title_es="Numero de pasos para resolver las torres de Hanoi",
        description_es="""## Numero de pasos para resolver las torres de Hanoi

Definir la funcion `numPasosHanoi` tal que `numPasosHanoi n` es el numero de pasos necesarios para trasladar `n` anillos en el problema de las torres de Hanoi. Suponer que `n >= 1`.

### Ejemplos:
```haskell
numPasosHanoi 2   -- devuelve 3
numPasosHanoi 7   -- devuelve 127
numPasosHanoi 64  -- devuelve 18446744073709551615
```

### Perfil:
```haskell
numPasosHanoi :: Integer -> Integer
```
""",
        starter_code_es="-- Definir recursivamente la funcion numPasosHanoi\nnumPasosHanoi :: Integer -> Integer",
    ),

    # -------------------------------------------------------------------------
    # 3.7.1  Conjuncion de una lista
    # -------------------------------------------------------------------------
    "c3-and-prima": Challenge(
        id="c3-and-prima",
        title="Conjunction of a List",
        description="""## Conjunction of a List

Define, by recursion, a function `and'` such that `and' xs` returns `True` when every element of `xs` is `True`. The empty list should return `True`.

### Examples:
```haskell
and' [1+2 < 4, 2:[3] == [2,3]]  -- returns True
and' [1+2 < 3, 2:[3] == [2,3]]  -- returns False
```

### Signature:
```haskell
and' :: [Bool] -> Bool
```
""",
        solution="and' :: [Bool] -> Bool\nand' [] = True\nand' (b:bs) = b && and' bs",
        starter_code="-- Define the and' function recursively\nand' :: [Bool] -> Bool",
        tests=[
            TestCase(code="and' [1+2 < 4, 2:[3] == [2,3]]", expected="True"),
            TestCase(code="and' [1+2 < 3, 2:[3] == [2,3]]", expected="False"),
            TestCase(code="and' []", expected="True"),
        ],
        title_es="Conjuncion de una lista",
        description_es="""## Conjuncion de una lista

Definir, por recursion, la funcion `and'` tal que `and' xs` se verifica si todos los elementos de `xs` son verdaderos. La lista vacia debe devolver `True`.

### Ejemplos:
```haskell
and' [1+2 < 4, 2:[3] == [2,3]]  -- devuelve True
and' [1+2 < 3, 2:[3] == [2,3]]  -- devuelve False
```

### Perfil:
```haskell
and' :: [Bool] -> Bool
```
""",
        starter_code_es="-- Definir recursivamente la funcion and'\nand' :: [Bool] -> Bool",
    ),

    # -------------------------------------------------------------------------
    # 3.8.1  Pertenencia a una lista
    # -------------------------------------------------------------------------
    "c3-elem-prima": Challenge(
        id="c3-elem-prima",
        title="Membership in a List",
        description="""## Membership in a List

Define, by recursion, a function `elem'` such that `elem' x xs` returns whether `x` belongs to `xs`.

### Examples:
```haskell
elem' 3 [2,3,5]  -- returns True
elem' 4 [2,3,5]  -- returns False
```

### Signature:
```haskell
elem' :: Eq a => a -> [a] -> Bool
```
""",
        solution="elem' :: Eq a => a -> [a] -> Bool\nelem' _ [] = False\nelem' x (y:ys)\n  | x == y    = True\n  | otherwise = elem' x ys",
        starter_code="-- Define the elem' function recursively\nelem' :: Eq a => a -> [a] -> Bool",
        tests=[
            TestCase(code="elem' 3 [2,3,5]", expected="True"),
            TestCase(code="elem' 4 [2,3,5]", expected="False"),
            TestCase(code="elem' 'a' \"banana\"", expected="True"),
        ],
        title_es="Pertenencia a una lista",
        description_es="""## Pertenencia a una lista

Definir, por recursion, la funcion `elem'` tal que `elem' x xs` se verifica si `x` pertenece a la lista `xs`.

### Ejemplos:
```haskell
elem' 3 [2,3,5]  -- devuelve True
elem' 4 [2,3,5]  -- devuelve False
```

### Perfil:
```haskell
elem' :: Eq a => a -> [a] -> Bool
```
""",
        starter_code_es="-- Definir recursivamente la funcion elem'\nelem' :: Eq a => a -> [a] -> Bool",
    ),

    # -------------------------------------------------------------------------
    # 3.9.1  Ultimo elemento de una lista
    # -------------------------------------------------------------------------
    "c3-last-prima": Challenge(
        id="c3-last-prima",
        title="Last Element of a List",
        description="""## Last Element of a List

Define, by recursion, a function `last'` such that `last' xs` is the last element of `xs`. Assume the list is non-empty; the base case is a list with exactly one element.

### Examples:
```haskell
last' [2,3,5]  -- returns 5
last' "abc"    -- returns 'c'
```

### Signature:
```haskell
last' :: [a] -> a
```
""",
        solution="last' :: [a] -> a\nlast' [x] = x\nlast' (_:xs) = last' xs",
        starter_code="-- Define the last' function recursively\nlast' :: [a] -> a",
        tests=[
            TestCase(code="last' [2,3,5]", expected="5"),
            TestCase(code="last' \"abc\"", expected="'c'"),
            TestCase(code="last' [True]", expected="True"),
        ],
        title_es="Ultimo elemento de una lista",
        description_es="""## Ultimo elemento de una lista

Definir, por recursion, la funcion `last'` tal que `last' xs` es el ultimo elemento de `xs`. Se supone que la lista no es vacia; el caso base es una lista con exactamente un elemento.

### Ejemplos:
```haskell
last' [2,3,5]  -- devuelve 5
last' "abc"    -- devuelve 'c'
```

### Perfil:
```haskell
last' :: [a] -> a
```
""",
        starter_code_es="-- Definir recursivamente la funcion last'\nlast' :: [a] -> a",
    ),

    # -------------------------------------------------------------------------
    # 3.10.1  Concatenacion de una lista
    # -------------------------------------------------------------------------
    "c3-concat-prima": Challenge(
        id="c3-concat-prima",
        title="Concatenate a List of Lists",
        description="""## Concatenate a List of Lists

Define, by recursion, a function `concat'` such that `concat' xss` is the list obtained by concatenating the lists in `xss` from left to right.

### Examples:
```haskell
concat' [[1..3],[5..7],[8..10]]  -- returns [1,2,3,5,6,7,8,9,10]
concat' ["ha","sk","ell"]        -- returns "haskell"
```

### Signature:
```haskell
concat' :: [[a]] -> [a]
```
""",
        solution="concat' :: [[a]] -> [a]\nconcat' [] = []\nconcat' (xs:xss) = xs ++ concat' xss",
        starter_code="-- Define the concat' function recursively\nconcat' :: [[a]] -> [a]",
        tests=[
            TestCase(code="concat' [[1..3],[5..7],[8..10]]", expected="[1,2,3,5,6,7,8,9,10]"),
            TestCase(code="concat' [\"ha\",\"sk\",\"ell\"]", expected="\"haskell\""),
            TestCase(code="concat' ([] :: [[Int]])", expected="[]"),
        ],
        title_es="Concatenacion de una lista",
        description_es="""## Concatenacion de una lista

Definir, por recursion, la funcion `concat'` tal que `concat' xss` es la lista obtenida concatenando las listas de `xss` de izquierda a derecha.

### Ejemplos:
```haskell
concat' [[1..3],[5..7],[8..10]]  -- devuelve [1,2,3,5,6,7,8,9,10]
concat' ["ha","sk","ell"]        -- devuelve "haskell"
```

### Perfil:
```haskell
concat' :: [[a]] -> [a]
```
""",
        starter_code_es="-- Definir recursivamente la funcion concat'\nconcat' :: [[a]] -> [a]",
    ),

    # -------------------------------------------------------------------------
    # 3.11.1  Seleccion de un elemento
    # -------------------------------------------------------------------------
    "c3-selecciona": Challenge(
        id="c3-selecciona",
        title="Select an Element",
        description="""## Select an Element

Define, by recursion, a function `selecciona` such that `selecciona xs n` is the element of `xs` at zero-based position `n`. The tests only use valid positions.

### Examples:
```haskell
selecciona [2,3,5,7] 2  -- returns 5
selecciona "haskell" 0  -- returns 'h'
```

### Signature:
```haskell
selecciona :: [a] -> Int -> a
```
""",
        solution="selecciona :: [a] -> Int -> a\nselecciona (x:_) 0 = x\nselecciona (_:xs) n = selecciona xs (n - 1)",
        starter_code="-- Define the selecciona function recursively\nselecciona :: [a] -> Int -> a",
        tests=[
            TestCase(code="selecciona [2,3,5,7] 2", expected="5"),
            TestCase(code="selecciona \"haskell\" 0", expected="'h'"),
            TestCase(code="selecciona [10,20,30] 1", expected="20"),
        ],
        title_es="Seleccion de un elemento",
        description_es="""## Seleccion de un elemento

Definir, por recursion, la funcion `selecciona` tal que `selecciona xs n` es el elemento de `xs` en la posicion `n`, empezando desde cero. Las pruebas solo usan posiciones validas.

### Ejemplos:
```haskell
selecciona [2,3,5,7] 2  -- devuelve 5
selecciona "haskell" 0  -- devuelve 'h'
```

### Perfil:
```haskell
selecciona :: [a] -> Int -> a
```
""",
        starter_code_es="-- Definir recursivamente la funcion selecciona\nselecciona :: [a] -> Int -> a",
    ),

    # -------------------------------------------------------------------------
    # 3.12.1  Seleccion de los primeros elementos
    # -------------------------------------------------------------------------
    "c3-take-prima": Challenge(
        id="c3-take-prima",
        title="Select the First Elements",
        description="""## Select the First Elements

Define, by recursion, a function `take'` such that `take' n xs` is the list of the first `n` elements of `xs`. Assume `n` is non-negative; if `xs` has fewer than `n` elements, return the whole list.

### Examples:
```haskell
take' 3 [4..12]  -- returns [4,5,6]
take' 2 "abcd"   -- returns "ab"
```

### Signature:
```haskell
take' :: Int -> [a] -> [a]
```
""",
        solution="take' :: Int -> [a] -> [a]\ntake' 0 _ = []\ntake' _ [] = []\ntake' n (x:xs) = x : take' (n - 1) xs",
        starter_code="-- Define the take' function recursively\ntake' :: Int -> [a] -> [a]",
        tests=[
            TestCase(code="take' 3 [4..12]", expected="[4,5,6]"),
            TestCase(code="take' 2 \"abcd\"", expected="\"ab\""),
            TestCase(code="take' 5 [1,2]", expected="[1,2]"),
        ],
        title_es="Seleccion de los primeros elementos",
        description_es="""## Seleccion de los primeros elementos

Definir, por recursion, la funcion `take'` tal que `take' n xs` es la lista de los `n` primeros elementos de `xs`. Suponer que `n` es no negativo; si `xs` tiene menos de `n` elementos, devolver la lista completa.

### Ejemplos:
```haskell
take' 3 [4..12]  -- devuelve [4,5,6]
take' 2 "abcd"   -- devuelve "ab"
```

### Perfil:
```haskell
take' :: Int -> [a] -> [a]
```
""",
        starter_code_es="-- Definir recursivamente la funcion take'\ntake' :: Int -> [a] -> [a]",
    ),

    # -------------------------------------------------------------------------
    # 3.13.1  Intercalacion de la media aritmetica
    # -------------------------------------------------------------------------
    "c3-refinada": Challenge(
        id="c3-refinada",
        title="Interleave Arithmetic Means",
        description="""## Interleave Arithmetic Means

Define a function `refinada` such that `refinada xs` inserts the arithmetic mean between each pair of consecutive elements in `xs`. Keep the original elements; lists of length `0` or `1` are unchanged.

### Examples:
```haskell
refinada [2,7,1,8]  -- returns [2.0,4.5,7.0,4.0,1.0,4.5,8.0]
refinada [2]        -- returns [2.0]
refinada []         -- returns []
```

### Signature:
```haskell
refinada :: [Float] -> [Float]
```
""",
        solution="refinada :: [Float] -> [Float]\nrefinada (x:y:zs) = x : (x + y) / 2 : refinada (y:zs)\nrefinada xs = xs",
        starter_code="-- Define the refinada function\nrefinada :: [Float] -> [Float]",
        tests=[
            TestCase(code="refinada [2,7,1,8]", expected="[2.0,4.5,7.0,4.0,1.0,4.5,8.0]"),
            TestCase(code="refinada [2]", expected="[2.0]"),
            TestCase(code="refinada []", expected="[]"),
        ],
        title_es="Intercalacion de la media aritmetica",
        description_es="""## Intercalacion de la media aritmetica

Definir la funcion `refinada` tal que `refinada xs` es la lista obtenida intercalando entre cada dos elementos consecutivos de `xs` su media aritmetica. Conserva los elementos originales; las listas de longitud `0` o `1` no cambian.

### Ejemplos:
```haskell
refinada [2,7,1,8]  -- devuelve [2.0,4.5,7.0,4.0,1.0,4.5,8.0]
refinada [2]        -- devuelve [2.0]
refinada []         -- devuelve []
```

### Perfil:
```haskell
refinada :: [Float] -> [Float]
```
""",
        starter_code_es="-- Definir la funcion refinada\nrefinada :: [Float] -> [Float]",
    ),

    # -------------------------------------------------------------------------
    # 3.14.1  Mezcla de listas ordenadas
    # -------------------------------------------------------------------------
    "c3-mezcla": Challenge(
        id="c3-mezcla",
        title="Merge Ordered Lists",
        description="""## Merge Ordered Lists

Define, by recursion, a function `mezcla` such that `mezcla xs ys` is the ordered list obtained by merging the ordered lists `xs` and `ys`. Assume both input lists are already sorted in nondecreasing order.

### Examples:
```haskell
mezcla [2,5,6] [1,3,4]  -- returns [1,2,3,4,5,6]
```

### Signature:
```haskell
mezcla :: Ord a => [a] -> [a] -> [a]
```
""",
        solution="mezcla :: Ord a => [a] -> [a] -> [a]\nmezcla [] ys = ys\nmezcla xs [] = xs\nmezcla (x:xs) (y:ys)\n  | x <= y    = x : mezcla xs (y:ys)\n  | otherwise = y : mezcla (x:xs) ys",
        starter_code="-- Define the mezcla function recursively\nmezcla :: Ord a => [a] -> [a] -> [a]",
        tests=[
            TestCase(code="mezcla [2,5,6] [1,3,4]", expected="[1,2,3,4,5,6]"),
            TestCase(code="mezcla [1,4,7] [2,2,8]", expected="[1,2,2,4,7,8]"),
            TestCase(code="mezcla ([] :: [Int]) [1,2]", expected="[1,2]"),
        ],
        title_es="Mezcla de listas ordenadas",
        description_es="""## Mezcla de listas ordenadas

Definir, por recursion, la funcion `mezcla` tal que `mezcla xs ys` es la lista ordenada obtenida mezclando las listas ordenadas `xs` e `ys`. Suponer que ambas listas de entrada ya estan ordenadas de menor a mayor.

### Ejemplos:
```haskell
mezcla [2,5,6] [1,3,4]  -- devuelve [1,2,3,4,5,6]
```

### Perfil:
```haskell
mezcla :: Ord a => [a] -> [a] -> [a]
```
""",
        starter_code_es="-- Definir recursivamente la funcion mezcla\nmezcla :: Ord a => [a] -> [a] -> [a]",
    ),

    # -------------------------------------------------------------------------
    # 3.14.2  Mitades de una lista
    # -------------------------------------------------------------------------
    "c3-mitades": Challenge(
        id="c3-mitades",
        title="Halves of a List",
        description="""## Halves of a List

Define a function `mitades` such that `mitades xs` is the pair formed by splitting `xs` into two halves whose lengths differ by at most one. Put `length xs div 2` elements in the first half.

### Examples:
```haskell
mitades [2,3,5,7,9]  -- returns ([2,3],[5,7,9])
mitades [1,2,3,4]    -- returns ([1,2],[3,4])
```

### Signature:
```haskell
mitades :: [a] -> ([a], [a])
```
""",
        solution="mitades :: [a] -> ([a], [a])\nmitades xs = splitAt (length xs `div` 2) xs",
        starter_code="-- Define the mitades function\nmitades :: [a] -> ([a], [a])",
        tests=[
            TestCase(code="mitades [2,3,5,7,9]", expected="([2,3],[5,7,9])"),
            TestCase(code="mitades [1,2,3,4]", expected="([1,2],[3,4])"),
            TestCase(code="mitades \"abc\"", expected="(\"a\",\"bc\")"),
        ],
        title_es="Mitades de una lista",
        description_es="""## Mitades de una lista

Definir la funcion `mitades` tal que `mitades xs` es el par formado por las dos mitades en que se divide `xs`, con longitudes que difieren como maximo en uno. Pon `length xs div 2` elementos en la primera mitad.

### Ejemplos:
```haskell
mitades [2,3,5,7,9]  -- devuelve ([2,3],[5,7,9])
mitades [1,2,3,4]    -- devuelve ([1,2],[3,4])
```

### Perfil:
```haskell
mitades :: [a] -> ([a], [a])
```
""",
        starter_code_es="-- Definir la funcion mitades\nmitades :: [a] -> ([a], [a])",
    ),

    # -------------------------------------------------------------------------
    # 3.14.3  Ordenacion por mezcla
    # -------------------------------------------------------------------------
    "c3-ord-mezcla": Challenge(
        id="c3-ord-mezcla",
        title="Merge Sort",
        description="""## Merge Sort

Define, by recursion, a function `ordMezcla` such that `ordMezcla xs` sorts `xs` by merge sort. The empty list and singleton lists are already sorted.

Include any helper definitions you use.

### Examples:
```haskell
ordMezcla [5,2,3,1,7,2,5]  -- returns [1,2,2,3,5,5,7]
```

### Signature:
```haskell
ordMezcla :: Ord a => [a] -> [a]
```
""",
        solution="mezcla :: Ord a => [a] -> [a] -> [a]\nmezcla [] ys = ys\nmezcla xs [] = xs\nmezcla (x:xs) (y:ys)\n  | x <= y    = x : mezcla xs (y:ys)\n  | otherwise = y : mezcla (x:xs) ys\n\nmitades :: [a] -> ([a], [a])\nmitades xs = splitAt (length xs `div` 2) xs\n\nordMezcla :: Ord a => [a] -> [a]\nordMezcla [] = []\nordMezcla [x] = [x]\nordMezcla xs = mezcla (ordMezcla ys) (ordMezcla zs)\n  where (ys, zs) = mitades xs",
        starter_code="-- Define the ordMezcla function recursively\nordMezcla :: Ord a => [a] -> [a]",
        tests=[
            TestCase(code="ordMezcla [5,2,3,1,7,2,5]", expected="[1,2,2,3,5,5,7]"),
            TestCase(code="ordMezcla \"haskell\"", expected="\"aehklls\""),
            TestCase(code="ordMezcla ([] :: [Int])", expected="[]"),
        ],
        title_es="Ordenacion por mezcla",
        description_es="""## Ordenacion por mezcla

Definir, por recursion, la funcion `ordMezcla` tal que `ordMezcla xs` ordena `xs` mediante ordenacion por mezcla. La lista vacia y las listas unitarias ya estan ordenadas.

Incluir las funciones auxiliares que uses.

### Ejemplos:
```haskell
ordMezcla [5,2,3,1,7,2,5]  -- devuelve [1,2,2,3,5,5,7]
```

### Perfil:
```haskell
ordMezcla :: Ord a => [a] -> [a]
```
""",
        starter_code_es="-- Definir recursivamente la funcion ordMezcla\nordMezcla :: Ord a => [a] -> [a]",
    ),

    # -------------------------------------------------------------------------
    # 3.14.4  La ordenacion por mezcla da listas ordenadas
    # -------------------------------------------------------------------------
    "c3-ordenada": Challenge(
        id="c3-ordenada",
        title="Ordered List Predicate",
        description="""## Ordered List Predicate

Define, by recursion, a function `ordenada` such that `ordenada xs` returns whether `xs` is ordered in nondecreasing order. Repeated adjacent elements are allowed; empty and singleton lists are ordered.

### Examples:
```haskell
ordenada [2,3,5]  -- returns True
ordenada [2,5,3]  -- returns False
```

### Signature:
```haskell
ordenada :: Ord a => [a] -> Bool
```
""",
        solution="ordenada :: Ord a => [a] -> Bool\nordenada [] = True\nordenada [_] = True\nordenada (x:y:xs) = x <= y && ordenada (y:xs)",
        starter_code="-- Define the ordenada function recursively\nordenada :: Ord a => [a] -> Bool",
        tests=[
            TestCase(code="ordenada [2,3,5]", expected="True"),
            TestCase(code="ordenada [2,5,3]", expected="False"),
            TestCase(code="ordenada \"aehklls\"", expected="True"),
        ],
        title_es="Reconocimiento de listas ordenadas",
        description_es="""## Reconocimiento de listas ordenadas

Definir, por recursion, la funcion `ordenada` tal que `ordenada xs` se verifica si `xs` es una lista ordenada de menor a mayor. Se permiten elementos repetidos consecutivos; las listas vacias y unitarias estan ordenadas.

### Ejemplos:
```haskell
ordenada [2,3,5]  -- devuelve True
ordenada [2,5,3]  -- devuelve False
```

### Perfil:
```haskell
ordenada :: Ord a => [a] -> Bool
```
""",
        starter_code_es="-- Definir recursivamente la funcion ordenada\nordenada :: Ord a => [a] -> Bool",
    ),

    # -------------------------------------------------------------------------
    # 3.14.5  QuickCheck: la ordenacion por mezcla da listas ordenadas
    # -------------------------------------------------------------------------
    "c3-prop-ord-mezcla-ordenada": Challenge(
        id="c3-prop-ord-mezcla-ordenada",
        title="Merge Sort Produces Ordered Lists",
        description="""## Merge Sort Produces Ordered Lists

Define the property function `prop_ordMezcla_ordenada` such that `prop_ordMezcla_ordenada xs` checks that `ordMezcla xs` is ordered. The platform tests this function with sample inputs, so do not call `quickCheck` yourself.

Include any helper definitions you use.

### Examples:
```haskell
prop_ordMezcla_ordenada [5,2,3,1,7,2,5]  -- returns True
prop_ordMezcla_ordenada "haskell"        -- returns True
```

### Signature:
```haskell
prop_ordMezcla_ordenada :: Ord a => [a] -> Bool
```
""",
        solution="mezcla :: Ord a => [a] -> [a] -> [a]\nmezcla [] ys = ys\nmezcla xs [] = xs\nmezcla (x:xs) (y:ys)\n  | x <= y    = x : mezcla xs (y:ys)\n  | otherwise = y : mezcla (x:xs) ys\n\nmitades :: [a] -> ([a], [a])\nmitades xs = splitAt (length xs `div` 2) xs\n\nordMezcla :: Ord a => [a] -> [a]\nordMezcla [] = []\nordMezcla [x] = [x]\nordMezcla xs = mezcla (ordMezcla ys) (ordMezcla zs)\n  where (ys, zs) = mitades xs\n\nordenada :: Ord a => [a] -> Bool\nordenada [] = True\nordenada [_] = True\nordenada (x:y:xs) = x <= y && ordenada (y:xs)\n\nprop_ordMezcla_ordenada :: Ord a => [a] -> Bool\nprop_ordMezcla_ordenada xs = ordenada (ordMezcla xs)",
        starter_code="-- Define the prop_ordMezcla_ordenada property\nprop_ordMezcla_ordenada :: Ord a => [a] -> Bool",
        tests=[
            TestCase(code="prop_ordMezcla_ordenada [5,2,3,1,7,2,5]", expected="True"),
            TestCase(code="prop_ordMezcla_ordenada \"haskell\"", expected="True"),
            TestCase(code="prop_ordMezcla_ordenada ([] :: [Int])", expected="True"),
        ],
        title_es="La ordenacion por mezcla da listas ordenadas",
        description_es="""## La ordenacion por mezcla da listas ordenadas

Definir la propiedad `prop_ordMezcla_ordenada` tal que `prop_ordMezcla_ordenada xs` comprueba que `ordMezcla xs` esta ordenada. La plataforma prueba esta funcion con entradas de ejemplo, asi que no llames a `quickCheck`.

Incluir las funciones auxiliares que uses.

### Ejemplos:
```haskell
prop_ordMezcla_ordenada [5,2,3,1,7,2,5]  -- devuelve True
prop_ordMezcla_ordenada "haskell"        -- devuelve True
```

### Perfil:
```haskell
prop_ordMezcla_ordenada :: Ord a => [a] -> Bool
```
""",
        starter_code_es="-- Definir la propiedad prop_ordMezcla_ordenada\nprop_ordMezcla_ordenada :: Ord a => [a] -> Bool",
    ),

    # -------------------------------------------------------------------------
    # 3.14.6  Borrar una ocurrencia
    # -------------------------------------------------------------------------
    "c3-borra": Challenge(
        id="c3-borra",
        title="Delete One Occurrence",
        description="""## Delete One Occurrence

Define, by recursion, a function `borra` such that `borra x xs` is the list obtained by deleting the first occurrence of `x` from `xs`. If `x` does not appear, return the original list.

### Examples:
```haskell
borra 1 [1,2,1]  -- returns [2,1]
borra 3 [1,2,1]  -- returns [1,2,1]
```

### Signature:
```haskell
borra :: Eq a => a -> [a] -> [a]
```
""",
        solution="borra :: Eq a => a -> [a] -> [a]\nborra _ [] = []\nborra x (y:ys)\n  | x == y    = ys\n  | otherwise = y : borra x ys",
        starter_code="-- Define the borra function recursively\nborra :: Eq a => a -> [a] -> [a]",
        tests=[
            TestCase(code="borra 1 [1,2,1]", expected="[2,1]"),
            TestCase(code="borra 3 [1,2,1]", expected="[1,2,1]"),
            TestCase(code="borra 'a' \"banana\"", expected="\"bnana\""),
        ],
        title_es="Borrar una ocurrencia",
        description_es="""## Borrar una ocurrencia

Definir, por recursion, la funcion `borra` tal que `borra x xs` es la lista obtenida borrando la primera ocurrencia de `x` en `xs`. Si `x` no aparece, devuelve la lista original.

### Ejemplos:
```haskell
borra 1 [1,2,1]  -- devuelve [2,1]
borra 3 [1,2,1]  -- devuelve [1,2,1]
```

### Perfil:
```haskell
borra :: Eq a => a -> [a] -> [a]
```
""",
        starter_code_es="-- Definir recursivamente la funcion borra\nborra :: Eq a => a -> [a] -> [a]",
    ),

    # -------------------------------------------------------------------------
    # 3.14.7  Determinacion de permutaciones
    # -------------------------------------------------------------------------
    "c3-es-permutacion": Challenge(
        id="c3-es-permutacion",
        title="Permutation Predicate",
        description="""## Permutation Predicate

Define, by recursion, a function `esPermutacion` such that `esPermutacion xs ys` returns whether `xs` is a permutation of `ys`. Duplicates matter: each value must appear the same number of times in both lists.

Include any helper definitions you use.

### Examples:
```haskell
esPermutacion [1,2,1] [2,1,1]  -- returns True
esPermutacion [1,2,1] [1,2,2]  -- returns False
```

### Signature:
```haskell
esPermutacion :: Eq a => [a] -> [a] -> Bool
```
""",
        solution="borra :: Eq a => a -> [a] -> [a]\nborra _ [] = []\nborra x (y:ys)\n  | x == y    = ys\n  | otherwise = y : borra x ys\n\nesPermutacion :: Eq a => [a] -> [a] -> Bool\nesPermutacion [] [] = True\nesPermutacion [] (_:_) = False\nesPermutacion (x:xs) ys = elem x ys && esPermutacion xs (borra x ys)",
        starter_code="-- Define the esPermutacion function recursively\nesPermutacion :: Eq a => [a] -> [a] -> Bool",
        tests=[
            TestCase(code="esPermutacion [1,2,1] [2,1,1]", expected="True"),
            TestCase(code="esPermutacion [1,2,1] [1,2,2]", expected="False"),
            TestCase(code="esPermutacion \"haskell\" \"llhakse\"", expected="True"),
        ],
        title_es="Determinacion de permutaciones",
        description_es="""## Determinacion de permutaciones

Definir, por recursion, la funcion `esPermutacion` tal que `esPermutacion xs ys` se verifica si `xs` es una permutacion de `ys`. Los duplicados importan: cada valor debe aparecer la misma cantidad de veces en ambas listas.

Incluir las funciones auxiliares que uses.

### Ejemplos:
```haskell
esPermutacion [1,2,1] [2,1,1]  -- devuelve True
esPermutacion [1,2,1] [1,2,2]  -- devuelve False
```

### Perfil:
```haskell
esPermutacion :: Eq a => [a] -> [a] -> Bool
```
""",
        starter_code_es="-- Definir recursivamente la funcion esPermutacion\nesPermutacion :: Eq a => [a] -> [a] -> Bool",
    ),

    # -------------------------------------------------------------------------
    # 3.14.8  QuickCheck: la ordenacion por mezcla da una permutacion
    # -------------------------------------------------------------------------
    "c3-prop-ord-mezcla-permutacion": Challenge(
        id="c3-prop-ord-mezcla-permutacion",
        title="Merge Sort Produces a Permutation",
        description="""## Merge Sort Produces a Permutation

Define the property function `prop_ordMezcla_permutacion` such that `prop_ordMezcla_permutacion xs` checks that `ordMezcla xs` is a permutation of `xs`. The platform tests this function with sample inputs, so do not call `quickCheck` yourself.

Include any helper definitions you use.

### Examples:
```haskell
prop_ordMezcla_permutacion [5,2,3,1,7,2,5]  -- returns True
prop_ordMezcla_permutacion "haskell"        -- returns True
```

### Signature:
```haskell
prop_ordMezcla_permutacion :: Ord a => [a] -> Bool
```
""",
        solution="mezcla :: Ord a => [a] -> [a] -> [a]\nmezcla [] ys = ys\nmezcla xs [] = xs\nmezcla (x:xs) (y:ys)\n  | x <= y    = x : mezcla xs (y:ys)\n  | otherwise = y : mezcla (x:xs) ys\n\nmitades :: [a] -> ([a], [a])\nmitades xs = splitAt (length xs `div` 2) xs\n\nordMezcla :: Ord a => [a] -> [a]\nordMezcla [] = []\nordMezcla [x] = [x]\nordMezcla xs = mezcla (ordMezcla ys) (ordMezcla zs)\n  where (ys, zs) = mitades xs\n\nborra :: Eq a => a -> [a] -> [a]\nborra _ [] = []\nborra x (y:ys)\n  | x == y    = ys\n  | otherwise = y : borra x ys\n\nesPermutacion :: Eq a => [a] -> [a] -> Bool\nesPermutacion [] [] = True\nesPermutacion [] (_:_) = False\nesPermutacion (x:xs) ys = elem x ys && esPermutacion xs (borra x ys)\n\nprop_ordMezcla_permutacion :: Ord a => [a] -> Bool\nprop_ordMezcla_permutacion xs = esPermutacion (ordMezcla xs) xs",
        starter_code="-- Define the prop_ordMezcla_permutacion property\nprop_ordMezcla_permutacion :: Ord a => [a] -> Bool",
        tests=[
            TestCase(code="prop_ordMezcla_permutacion [5,2,3,1,7,2,5]", expected="True"),
            TestCase(code="prop_ordMezcla_permutacion \"haskell\"", expected="True"),
            TestCase(code="prop_ordMezcla_permutacion ([] :: [Int])", expected="True"),
        ],
        title_es="La ordenacion por mezcla da una permutacion",
        description_es="""## La ordenacion por mezcla da una permutacion

Definir la propiedad `prop_ordMezcla_permutacion` tal que `prop_ordMezcla_permutacion xs` comprueba que `ordMezcla xs` es una permutacion de `xs`. La plataforma prueba esta funcion con entradas de ejemplo, asi que no llames a `quickCheck`.

Incluir las funciones auxiliares que uses.

### Ejemplos:
```haskell
prop_ordMezcla_permutacion [5,2,3,1,7,2,5]  -- devuelve True
prop_ordMezcla_permutacion "haskell"        -- devuelve True
```

### Perfil:
```haskell
prop_ordMezcla_permutacion :: Ord a => [a] -> Bool
```
""",
        starter_code_es="-- Definir la propiedad prop_ordMezcla_permutacion\nprop_ordMezcla_permutacion :: Ord a => [a] -> Bool",
    ),
}
