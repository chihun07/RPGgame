class Armor:
    def __init__(self, name, hp_bonus, str_bonus, vit_bonus):
        self.name = name  # 갑옷 이름
        self.hp_bonus = hp_bonus  # 최대 체력 증가량
        self.str_bonus = str_bonus  # 공격력 증가량
        self.vit_bonus = vit_bonus  # 방어력 증가량


class Player:
    def __init__(self, name, max_hp, strength, vitality):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.vitality = vitality
        self.equipped_armor = {}  # 장착한 갑옷을 저장할 딕셔너리

    def equip_armor(self, armor):
        # 해당 갑옷 종류가 이미 장착되어 있는지 확인
        if armor.name in self.Mounted_inventory:
            print(f"{self.name}은(는) 이미 {armor.name}을(를) 장착하고 있습니다.")
        else:
            # 해당 갑옷 종류가 장착되어 있지 않다면 장착
            self.equipped_armor[armor.name] = armor
            # 플레이어의 능력치 업데이트
            self.max_hp += armor.hp_bonus
            self.strength += armor.str_bonus
            self.vitality += armor.vit_bonus
            print(f"{self.name}이(가) {armor.name}을(를) 장착했습니다. 최대 체력이 {armor.hp_bonus} 증가하고,"+
            " 공격력이 {armor.str_bonus} 증가하고, 방어력이 {armor.vit_bonus} 증가합니다.")

    def unequip_armor(self):
        if self.equipped_armor:
            # 갑옷 해제
            unequipped_armor = self.equipped_armor.popitem()[1]
            # 플레이어의 능력치 업데이트
            self.max_hp -= unequipped_armor.hp_bonus
            self.strength -= unequipped_armor.str_bonus
            self.vitality -= unequipped_armor.vit_bonus
            print(f"{self.name}이(가) {unequipped_armor.name}을(를) 해제했습니다.")



helmet = Armor("머리갑옷", 20, 0, 0)  # 머리 갑옷: 최대 체력 20 증가
chestplate = Armor("가슴갑옷", 50, 0, 10)  # 가슴 갑옷: 최대 체력 50 증가, 방어력 10 증가
leggings = Armor("다리갑옷", 30, 10, 0)  # 다리 갑옷: 최대 체력 30 증가, 공격력 10 증가
boots = Armor("발갑옷", 10, 0, 5)  # 발 갑옷: 최대 체력 10 증가, 방어력 5 증가
gloves = Armor("손갑옷", 15, 5, 5)  # 손 갑옷: 최대 체력 15 증가, 공격력 5 증가, 방어력 5 증가
gloves = Armor("손갑옷_2", 15, 5, 5)
# 플레이어 생성
player = Player("플레이어", 100, 100, 10)  # 초기 체력 100, 최대 체력 100, 공격력 10, 방어력 10

# 갑옷 장착
player.equip_armor(helmet)
player.equip_armor(chestplate)
player.equip_armor(leggings)
player.equip_armor(boots)
player.equip_armor(gloves)
print(f"{player.name}의 체력: {player.hp}/{player.max_hp}")  # 출력: 플레이어의 체력: 150/100

# 갑옷 해제
player.unequip_armor()
player.unequip_armor()
player.unequip_armor()
player.unequip_armor()
print(f"{player.name}의 체력: {player.hp}/{player.max_hp}")  # 출력: 플레이어의 체력: 100/100
