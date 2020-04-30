from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

"""
 Each character is either a knight or a knave. A knight will always tell the truth: if knight states a sentence,
  then that sentence is true. Conversely, a knave will always lie: if a knave states a sentence, then that sentence is false.
"""

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnave, AKnight),
    Biconditional(AKnight, Not(AKnave)),

    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))

)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    #Either A is Knight or Knave, Either B is knight or Knave
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),

    Biconditional(AKnight, And(BKnave,AKnave)),
    Biconditional(AKnave, Not(And(BKnave,AKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Either A is Knight or Knave, Either B is knight or Knave
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),

    Biconditional(AKnight,Or(And(AKnight,BKnight), And(AKnave,BKnave))),
    Biconditional(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),

    Biconditional(BKnight, Or(And(AKnight,BKnave),And(AKnave,BKnight))),
    Biconditional(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))))

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Either A is Knight or Knave, Either B is knight or Knave,
    # Either C is Knave or C is Knight
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Or(CKnave, CKnight),
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(CKnight, Not(CKnave)),

    #A says Either I am Knight Or I am Knave
    Or( Biconditional(AKnave,Not(Or(AKnight,AKnave))), Biconditional(AKnight, Or(AKnight , AKnave))),

    #B says "A said 'I am a Knave'
    Or(Implication(BKnight, Or(Implication(AKnight, AKnight), Implication(AKnave, Not(AKnight) ))) ,Implication(BKnave, Not(Or(Implication(AKnight, AKnight), Implication(AKnave,Not(AKnight)))))),

    Or(Biconditional(BKnight, CKnave), Biconditional(BKnave, Not(CKnave))),

    Or(Biconditional(CKnight, AKnight), Biconditional(CKnave, Not(AKnight)))

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()


# A says either "I am a knight." or "I am a knave.", but you don't know which.
"""
(Aknave <-> not(Aknight or Aknave) or (AKnight <-> Aknight or Aknave))
Or( Biconditional(Aknave,Not(Or(Aknight,Aknave))), Biconditional(AKnight, Or(Aknight , Aknave)))
"""

# B says "A said 'I am a knave'."
"""
Or(Bknight , Or(Implication(Aknight,Aknight), Implication(Aknave,Not(Aknight) ) , (BKnave, Not(Or(Implication(Aknight,Aknight), Implication(Aknave,Not(Aknight)) )
"""

