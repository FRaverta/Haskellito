"""Challenge definitions and models."""

from typing import Dict, List, Optional

from pydantic import BaseModel


class TestCase(BaseModel):
    code: str
    expected: str


class Challenge(BaseModel):
    id: str
    title: str
    description: str
    solution: str  # Reference solution (hidden from user)
    tests: List[TestCase]
    starter_code: Optional[str] = ""


CHALLENGES: Dict[str, Challenge] = {
    "double": Challenge(
        id="double",
        title="Double Function",
        description="""## Double Function

Write a function called `double` that takes a number and returns twice its value.

### Examples:
```haskell
double 5  -- returns 10
double 0  -- returns 0
double (-3)  -- returns -6
```

### Signature:
```haskell
double :: Num a => a -> a
```
""",
        solution="double x = x * 2",
        starter_code="-- Write your double function here\ndouble x = undefined",
        tests=[
            TestCase(code="double 5", expected="10"),
            TestCase(code="double 0", expected="0"),
            TestCase(code="double (-3)", expected="-6"),
            TestCase(code="double 100", expected="200"),
        ]
    ),
    "factorial": Challenge(
        id="factorial",
        title="Factorial",
        description="""## Factorial

Write a function called `factorial` that computes the factorial of a non-negative integer.

The factorial of n (written as n!) is the product of all positive integers less than or equal to n.

### Examples:
```haskell
factorial 0  -- returns 1
factorial 1  -- returns 1
factorial 5  -- returns 120
```

### Signature:
```haskell
factorial :: Integer -> Integer
```
""",
        solution="factorial 0 = 1\nfactorial n = n * factorial (n - 1)",
        starter_code="-- Write your factorial function here\nfactorial n = undefined",
        tests=[
            TestCase(code="factorial 0", expected="1"),
            TestCase(code="factorial 1", expected="1"),
            TestCase(code="factorial 5", expected="120"),
            TestCase(code="factorial 10", expected="3628800"),
        ]
    ),
    "fibonacci": Challenge(
        id="fibonacci",
        title="Fibonacci",
        description="""## Fibonacci Sequence

Write a function called `fib` that returns the nth Fibonacci number.

The Fibonacci sequence starts with 0, 1, and each subsequent number is the sum of the two preceding ones: 0, 1, 1, 2, 3, 5, 8, 13, ...

### Examples:
```haskell
fib 0  -- returns 0
fib 1  -- returns 1
fib 10  -- returns 55
```

### Signature:
```haskell
fib :: Integer -> Integer
```
""",
        solution="fib 0 = 0\nfib 1 = 1\nfib n = fib (n-1) + fib (n-2)",
        starter_code="-- Write your fib function here\nfib n = undefined",
        tests=[
            TestCase(code="fib 0", expected="0"),
            TestCase(code="fib 1", expected="1"),
            TestCase(code="fib 5", expected="5"),
            TestCase(code="fib 10", expected="55"),
        ]
    ),
    "reverse-list": Challenge(
        id="reverse-list",
        title="Reverse a List",
        description="""## Reverse a List

Write a function called `myReverse` that reverses a list.

**Note:** Do not use the built-in `reverse` function!

### Examples:
```haskell
myReverse [1,2,3]  -- returns [3,2,1]
myReverse "hello"  -- returns "olleh"
myReverse []  -- returns []
```

### Signature:
```haskell
myReverse :: [a] -> [a]
```
""",
        solution="myReverse [] = []\nmyReverse (x:xs) = myReverse xs ++ [x]",
        starter_code="-- Write your myReverse function here\nmyReverse xs = undefined",
        tests=[
            TestCase(code="myReverse [1,2,3]", expected="[3,2,1]"),
            TestCase(code="myReverse \"hello\"", expected="\"olleh\""),
            TestCase(code="myReverse []", expected="[]"),
            TestCase(code="myReverse [1]", expected="[1]"),
        ]
    ),
}
