from GTDHack import GTDHack


def main() -> None:
    user = GTDHack("TDM28734", "AMO")

    # print(user.addHero(1, 50, 10000))

    # print(user.addBlackList())

    print(user.addDia(100))
    print(user.addGold(100))
    print(user.addRuby(1000))
    print(user.addMileage(100))
    print(user.addItems(999, 999, 999, 999, 999))
    print(user.addHero(1, 50, 10000))
    print(user.addTower(1001, 2, 2, 10))
    print(user.addUpgrade(100, 100, 100, "replace"))

    # Nếu acc không bị khoá nhưng lại trả về như này {"RESULT":"ERROR","VALUE":"(I)You are blocked!!","COMMENT":"empty"} thì là bị block ip


main()
