from enum import Enum

class type(Enum):
    INTEGGER = 1
    FLOAT = 2
    BOOLEAN = 3
    CHAR = 4
    STRING = 5
    NULL = 6
    ARRAY = 7

class Arithmetic_Operator(Enum):
    ADDITION = 1
    SUBSTRACTION = 2
    MULTIPLICATION = 3
    DIVISION = 4
    POWER = 5
    MODULS = 6
    UMINUS = 7


class Relational_Operators(Enum):
    EQUAL = 1
    UNEQUAL = 2
    GREATER = 3
    GREATEREQUAL = 4
    LESS = 5
    LESSEQUAL = 6


class Logical_Operators(Enum):
    AND = 1
    OR = 2
    NOT = 3