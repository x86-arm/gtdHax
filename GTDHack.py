from os import system

libs = ["pycryptodome", "base64", "requests", "json"]

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    import base64
    import requests
    import json
except:
    for el in libs:
        system("pip install %s" % el)

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import requests
import json
import random
import math

BASE_URL = "http://211.253.26.47:8093/TOWERDEFENCE_"

SERVER = ""

USER_AGENT = random.choice(
    [
        "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S901U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S908U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; M2101K6G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; DE2118) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
    ]
)

# AES secret key and iv
key = b"gksekf1djrqjfwk!"
iv = b"towerdefence_amo"


def encrypt(string_to_encrypt: str) -> str:
    padded_data = pad(string_to_encrypt.encode("utf-8"), AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted_data).decode("utf-8")


def decrypt(encrypted_string: str) -> str:
    encrypted_data = base64.b64decode(encrypted_string)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data)
    unpadded_data = unpad(decrypted_data, AES.block_size)
    return unpadded_data.decode("utf-8")


def postWithEncryptedData(url: str, data: dict):
    return requests.post(
        BASE_URL + url,
        params={"DATA": encrypt(json.dumps(data))} if url.endswith("AES.php") else data,
        headers={
            "User-Agent": USER_AGENT,
            "X-Requested-With": "busidol.mobile.tower",
        },
    ).text


class GTDHack:
    def __init__(self, id: str, server: str) -> None:
        self.id = id
        global SERVER
        global BASE_URL
        SERVER = server
        BASE_URL = "http://211.253.26.47:8093/TOWERDEFENCE_" +  server + "/"
        print(">> Counter server ++")
        postWithEncryptedData(
            "Counter/daily_run_count.php", {"UNIQ_ID": self.id}
        )  # Cái này để runcount lên server. Đại loại là để check in cho mỗi lần đăng nhập
        self.runCount = int(
            postWithEncryptedData(
                "../TOWERDEFENCE_COMMON/MOBILE_CONNECT/get_run_count_AES.php",
                {"PLATFORM": SERVER, "UNIQ_ID": self.id},
            )
        )  # Cái này để lấy số run count hiện tại rồi lưu vào self.runCount
        print(">> Get run count:", self.runCount)

    def getUserData(self):
        return postWithEncryptedData("get_user_data_all_AES.php", {"UNIQ_ID": self.id})

    def addCharbook(self, mode: str, number: int):
        currentUser = json.loads(
            self.getUserData()
        )  # Lấy số ruby, dia, gold, mileage hiện tại từ server

        currentUserCharbook = currentUser["VALUE"]["charbook"]["value"]

        print(">> Current user charbook value: ", currentUserCharbook)

        monster = currentUserCharbook["monster"]
        newHero = currentUserCharbook["hero"]
        newTower = currentUserCharbook["tower"]

        update = False

        if mode == "hero":
            temp = [*newHero]
            if temp[number - 1] == "0":
                temp[number - 1] = "1"
                newHero = "".join(temp)
                update = True

        if mode == "tower":
            rank = int(str(number)[0:1])
            type = int(str(number)[2:4])
            towersItem = newTower.split(",")

            temp1 = []
            for temp in towersItem:
                towers = [*temp.split(":")[0]]
                for index, tower in enumerate(towers):
                    if index >= (rank - 1) * 3 and index < rank * 3:
                        temp1.append(tower)

            if temp1[type - 1] == "0":
                temp1[type - 1] = "1"

                B = [
                    temp1[i * len(temp1) // 8 : (i + 1) * len(temp1) // 8]
                    for i in range(8)
                ]

                temp2 = []

                for jindex, temp in enumerate(towersItem):
                    towers = [*temp.split(":")[0]]
                    i = 0
                    for index, tower in enumerate(towers):
                        if index >= (rank - 1) * 3 and index < rank * 3:
                            if i < 3:
                                towers[index] = B[jindex][i]
                                i += 1

                    temp2.append("%s:%s" % ("".join(towers), temp.split(":")[1]))
                update = True
                newTower = ",".join(temp2)
        print("update charbook: %r" % update)
        if update:
            print(
                postWithEncryptedData(
                    "put_userinfo_charbook_AES.php",
                    {
                        "UNIQ_ID": self.id,
                        "TOWER": newTower,
                        "HERO": newHero,
                        "MONSTER": monster,
                        "RUN_COUNT": self.runCount,
                        "COMMENT": "도감추가:" if mode == "tower" else f"{number}영웅 획득",
                    },
                )
            )
            return

    def addRuby(self, amount: int):
        currentUser = json.loads(
            self.getUserData()
        )  # Lấy số ruby, dia, gold, mileage hiện tại từ server

        currentUserRubyDiaGold = currentUser["VALUE"]["rubydiagold"]["value"]

        print(">> Current user ruby dia gold value: ", currentUserRubyDiaGold)

        return postWithEncryptedData(
            "put_userinfo_rubydiagold_AES.php",
            {
                "UNIQ_ID": self.id,
                "CUR_RUBY": currentUserRubyDiaGold["RUBY"],
                "CUR_DIA": currentUserRubyDiaGold["DIA"],
                "CUR_GOLD": currentUserRubyDiaGold["GOLD"],
                "CUR_MILEAGE": currentUserRubyDiaGold["MILEAGE"],
                "RUBY_ADD": amount,
                "RUBY_WHY": random.choice(
                    ["신규사용자"]
                ),  # Lấy tạm lí do là nhận hộp thư và tạo acc mới
                "DIA_ADD": 0,
                "DIA_WHY": "",
                "GOLD_ADD": 0,
                "GOLD_WHY": "",
                "MILEAGE_ADD": 0,
                "MILEAGE_WHY": "",
                "RUN_COUNT": self.runCount,
            },
        )  # Không sửa code vì có thể lỗi không hack dc

    def addDia(self, amount: int):
        currentUser = json.loads(
            self.getUserData()
        )  # Lấy số ruby, dia, gold, mileage hiện tại từ server

        currentUserRubyDiaGold = currentUser["VALUE"]["rubydiagold"]["value"]

        print(">> Current user ruby dia gold value: ", currentUserRubyDiaGold)

        return postWithEncryptedData(
            "put_userinfo_rubydiagold_AES.php",
            {
                "UNIQ_ID": self.id,
                "CUR_RUBY": currentUserRubyDiaGold["RUBY"],
                "CUR_DIA": currentUserRubyDiaGold["DIA"],
                "CUR_GOLD": currentUserRubyDiaGold["GOLD"],
                "CUR_MILEAGE": currentUserRubyDiaGold["MILEAGE"],
                "RUBY_ADD": 0,
                "RUBY_WHY": "",
                "DIA_ADD": amount,
                "DIA_WHY": random.choice(
                    ["신규사용자"]
                ),  # Lấy tạm lí do là nhận hộp thư và tạo acc mới
                "GOLD_ADD": 0,
                "GOLD_WHY": "",
                "MILEAGE_ADD": 0,
                "MILEAGE_WHY": "",
                "RUN_COUNT": self.runCount,
            },
        )  # Không sửa code vì có thể lỗi không hack dc

    def addGold(self, amount: int):
        currentUser = json.loads(
            self.getUserData()
        )  # Lấy số ruby, dia, gold, mileage hiện tại từ server

        currentUserRubyDiaGold = currentUser["VALUE"]["rubydiagold"]["value"]

        print(">> Current user ruby dia gold value: ", currentUserRubyDiaGold)

        return postWithEncryptedData(
            "put_userinfo_rubydiagold_AES.php",
            {
                "UNIQ_ID": self.id,
                "CUR_RUBY": currentUserRubyDiaGold["RUBY"],
                "CUR_DIA": currentUserRubyDiaGold["DIA"],
                "CUR_GOLD": currentUserRubyDiaGold["GOLD"],
                "CUR_MILEAGE": currentUserRubyDiaGold["MILEAGE"],
                "RUBY_ADD": 0,
                "RUBY_WHY": "",
                "DIA_ADD": 0,
                "DIA_WHY": "",
                "GOLD_ADD": amount,
                "GOLD_WHY": random.choice(
                    ["신규사용자"]
                ),  # Lấy tạm lí do là nhận hộp thư và tạo acc mới
                "MILEAGE_ADD": 0,
                "MILEAGE_WHY": "",
                "RUN_COUNT": self.runCount,
            },
        )  # Không sửa code vì có thể lỗi không hack dc

    def addMileage(self, amount: int):
        currentUser = json.loads(
            self.getUserData()
        )  # Lấy số ruby, dia, gold, mileage hiện tại từ server

        currentUserRubyDiaGold = currentUser["VALUE"]["rubydiagold"]["value"]

        print(">> Current user ruby dia gold value: ", currentUserRubyDiaGold)

        return postWithEncryptedData(
            "put_userinfo_rubydiagold_AES.php",
            {
                "UNIQ_ID": self.id,
                "CUR_RUBY": currentUserRubyDiaGold["RUBY"],
                "CUR_DIA": currentUserRubyDiaGold["DIA"],
                "CUR_GOLD": currentUserRubyDiaGold["GOLD"],
                "CUR_MILEAGE": currentUserRubyDiaGold["MILEAGE"],
                "RUBY_ADD": 0,
                "RUBY_WHY": "",
                "DIA_ADD": 0,
                "DIA_WHY": "",
                "GOLD_ADD": 0,
                "GOLD_WHY": "",
                "MILEAGE_ADD": amount,
                "MILEAGE_WHY": random.choice(
                    ["신규사용자"]
                ),  # Lấy tạm lí do là nhận hộp thư và tạo acc mới
                "RUN_COUNT": self.runCount,
            },
        )  # Không sửa code vì có thể lỗi không hack dc

    def addHero(self, number: int, level: int, exp: int = 0):
        currentUser = json.loads(self.getUserData())  # Lấy số hero hiện tại từ server

        currentHero = currentUser["VALUE"]["hero"]["value"]

        print(">> Current user hero value: ", currentHero)

        heros = currentHero["bou_hero"].split(",")

        hero = heros[number - 1].split(":")

        hero[1] = level
        hero[2] = exp
        hero[3] = 1

        newHero = ":".join([str(el) for el in hero])

        heros[number - 1] = newHero

        newHeros = ",".join(heros)

        req = postWithEncryptedData(
            "put_userinfo_hero_AES.php",
            {
                "UNIQ_ID": self.id,
                "SELECTED_HERO": currentHero["selected_hero"],
                "SELECTED_HERO_MAX": currentHero["selected_hero_max"],
                "BOU_HERO": newHeros,
                "RUN_COUNT": self.runCount,
                "COMMENT": "%d번 영웅 레벱업" % number,
            },
        )  # Không sửa code vì có thể lỗi không hack dc

        self.addCharbook("hero", number)

        return req

    def addTower(self, number: int, level: int, card: int = 0, rainbowCard: int = 0):
        currentUser = json.loads(self.getUserData())  # Lấy số hero hiện tại từ server

        currentTower = currentUser["VALUE"]["tower"]["value"]
        currentTowers = currentUser["VALUE"]["tower"]["value"]["bou_tower"]

        print(">> Current user tower value: ", currentTowers)

        currentTowersList = currentTowers.split(",")

        newTowers = None

        newTower = ":".join([str(el) for el in [number, level, card]])

        if str(number) in currentTowers:
            for index, tower in enumerate(currentTowersList):
                if tower.find(str(number)) != -1:
                    currentTowersList[index] = newTower
                    break
        else:
            currentTowersList.append(newTower)

        newTowers = ",".join(currentTowersList)

        req = postWithEncryptedData(
            "put_userinfo_tower_AES.php",
            {
                "UNIQ_ID": self.id,
                "SELECTED_TOWER": currentTower["selected_tower"],
                "BOU_TOWER": newTowers,
                "RAINBOW_CARD": int(currentTower["rainbow_card"]) + rainbowCard,
                "RUN_COUNT": self.runCount,
                "COMMENT": random.choice(["고급(11장)", "고급(1장)"]),
            },
        )  # Không sửa code vì có thể lỗi không hack dc

        self.addCharbook("tower", number)

        return req

    def addItems(
        self, bomb: int, ice: int, nuclearBomb: int, heartBundle: int, mineral: int
    ):
        currentUser = json.loads(self.getUserData())  # Lấy số hero hiện tại từ server
        currentUserItems = currentUser["VALUE"]["item"]["value"]

        addItemsList = [bomb, ice, nuclearBomb, heartBundle, mineral]

        print(">> Current user item value: ", currentUserItems)

        newItemsList = [("%d:" % (index + 1)) for index in range(5)]

        for i, currentUserItem in enumerate(currentUserItems.split(",")):
            for j, oldItemValue in enumerate(currentUserItem.split(":")):
                if j == 1:
                    newItemsList[i] += str((addItemsList[i] + int(oldItemValue)))

        newItems = ",".join(newItemsList)

        return postWithEncryptedData(
            "put_userinfo_item_AES.php",
            {
                "UNIQ_ID": self.id,
                "DATA": newItems,
                "RUN_COUNT": self.runCount,
                "COMMENT": "%d번 아이템 우편함에서 수령" % random.choice(addItemsList),
            },
        )  # Không sửa code vì có thể lỗi không hack dc

    def addUpgrade(self, reinforcement: int, meteor: int, mineral: int, mode: str):
        currentUser = json.loads(self.getUserData())  # Lấy số hero hiện tại từ server
        currentUserUpgradeValue = currentUser["VALUE"]["upgrade"]["value"]

        currentUserUpgrades = currentUser["VALUE"]["upgrade"]["value"].split(",")
        print(">> Current user upgrade value: ", currentUserUpgradeValue)

        addUpgrades = ",".join(
            [
                str(upgrade)
                for upgrade in [
                    reinforcement + int(currentUserUpgrades[0]),
                    meteor + int(currentUserUpgrades[1]),
                    mineral + int(currentUserUpgrades[2]),
                ]
            ]
            if mode == "add"
            else (
                [
                    str(upgrade)
                    for upgrade in [
                        reinforcement,
                        meteor,
                        mineral,
                    ]
                ]
                if mode == "replace"
                else [
                    str(upgrade)
                    for upgrade in [
                        currentUserUpgrades[0],
                        currentUserUpgrades[1],
                        currentUserUpgrades[2],
                    ]
                ]
            )
        )

        fakeUpgradeType = random.choice(
            [
                (5, "Reinforcement Upgrade MAX"),
                (10, "Increase Meteor Power MAX"),
                (15, "Mineral Upgrade MAX"),
            ]
        )

        return postWithEncryptedData(
            "put_userinfo_upgrade_AES.php",
            {
                "UNIQ_ID": self.id,
                "DATA": addUpgrades,
                "RUN_COUNT": self.runCount,
                "COMMENT": "%d업그레이드:%s" % fakeUpgradeType,
            },
        )  # Không sửa code vì có thể lỗi không hack dc

    def addBlackList(self):
        return postWithEncryptedData(
            "put_blacklist.php",
            {
                "UNIQ_ID": self.id,
                "MESSAGE": "Detected abnormal access! so, You are blocked",
                "ETC": "영웅슬롯5 루비해킹:0",
            },
        )

