from logic import *

# Define symbols
AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says: "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # If A is a knight, then the statement must be true
    Implication(AKnight, And(AKnight, AKnave)),

    # If A is a knave, then the statement must be false
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says: "We are both knaves."
knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says: "We are the same kind."
# B says: "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),

    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))))
)

# Puzzle 3
# A says: "I am a knight." or "I am a knave." (we don't know which)
# B says: "A said 'I am a knave.'"
# B says: "C is a knave."
# C says: "A is a knight."
# Puzzle 3
# A says: "I am a knight." OR "I am a knave." (unknown which)
# B says: "A said 'I am a knave.'" AND "C is a knave."
# C says: "A is a knight."

A_said_knight = Symbol("A says 'I am a Knight'")
A_said_knave = Symbol("A says 'I am a Knave'")

knowledge3 = And(
    # Characters are either Knight or Knave, not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # A said one of these two things, not both
    Or(A_said_knight, A_said_knave),
    Not(And(A_said_knight, A_said_knave)),

    # If A is a knight and says "I am a knight", that must be true
    Implication(A_said_knight, Implication(AKnight, AKnight)),
    Implication(A_said_knight, Implication(AKnave, Not(AKnight))),

    # If A says "I am a knave", and is a knight, then A is a knave (contradiction)
    Implication(A_said_knave, Implication(AKnight, AKnave)),
    Implication(A_said_knave, Implication(AKnave, Not(AKnave))),

    # B says: "A said 'I am a knave'"
    Implication(BKnight, A_said_knave),
    Implication(BKnave, Not(A_said_knave)),

    # B says: "C is a knave"
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),

    # C says: "A is a knight"
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)
