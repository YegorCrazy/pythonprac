class Spell:
    __match_args__ = 'type', 'strength'
    def __init__(self, type, strength):
        self.type = type
        self.strength = strength

LSpell = Spell('lightning', 3)
FSpell = Spell('fireball', 3)
LZSpell = Spell('lightning', 0)
FZSpell = Spell('fireball', 0)
USpell = Spell('aaa', 10)

def cast_spell(spell):
    match spell:
        case Spell(tp, 0):
            print('some spell with zero power')
        case Spell('lightning', pw):
            print(f'lightning with {pw} power')
        case Spell('fireball', pw):
            print(f'fireball with {pw} power')
        case _:
            print('somethings wrong i can feel it')

for sp in [LSpell, FSpell, LZSpell, FZSpell, USpell]:
    cast_spell(sp)



