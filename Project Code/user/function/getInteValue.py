import random


def getInteValue(hotelsInState):
    d = {ni: indi for indi, ni in enumerate(set(hotelsInState))}
    listno = [d[ni] for ni in hotelsInState]
    randomno = random.choice(listno)
    while randomno > 461:
        randomno = randomno - 30
    return randomno
