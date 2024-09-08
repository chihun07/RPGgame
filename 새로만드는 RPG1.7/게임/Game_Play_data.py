import random
import json
import pandas as pd
import locale
import sys
import math
import time

Vam_AKT = 0
# 카테고리 목록
categories = [
    "회복물약"and "회복", 
    "최대 체력 증가 물약"and "최대", 
    "공격력 증가 물약"and "공격력", 
    "방어력 증가 물약"and "방어력", 
    "크리티컬 증가 물약"and "크리", 
    "회피율 증가 물약"and "회피",
    "머리 보호구"and "머리",
    "가슴 보호구"and "가슴",
    "손 보호구"and "손",
    "다리 보호구"and "다리",
    "발 보호구"and "발"
    "나가기"
]
Mounted_list = [
    "머리 보호구"and "머리",
    "가슴 보호구"and "가슴",
    "손 보호구"and "손",
    "다리 보호구"and "다리",
    "발 보호구"and "발"
]
#딜레이 프린트
def delayed_print(message, delay=0.03):
    for char in message:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()
# 플레이어 클래스
class Player:
    def __init__(self, Name, Money, HP, Max_HP, STR, VIT, Critical, Avoid, LV, EXP, 
                Available_inventory=None, Mounted_inventory=None):
        self.Name = Name  # 사용자 이름
        self.Money = Money
        self.HP = HP  # 현재 체력
        self.Max_HP = Max_HP  # 최대 체력
        self.STR = STR  # 공격력
        self.VIT = VIT  # 방어력
        self.Critical = Critical  # 크리티컬 확률 (0.0 ~ 1.0)
        self.Avoid = Avoid  # 회피 확률 (0.0 ~ 1.0)
        self.LV = LV  # 레벨
        self.EXP = EXP  # 경험치
        self.Mounted_inventory = Mounted_inventory if Mounted_inventory is not None else {}
        self.Available_inventory = Available_inventory if Available_inventory is not None else {}

    def set_Mounted_inventory(self, Mounted_inventory):
        self.Mounted_inventory = Mounted_inventory

    def set_Available_inventory(self, Available_inventory):
        self.Available_inventory = Available_inventory
        


    def add_Mounted_inventory(self, Mounted_item):
        # Mounted_inventory에 아이템 추가
        for item_name, (item_quantity, item_grade) in Mounted_item.items():
            if item_name in self.Mounted_inventory:
                self.Mounted_inventory[item_name]["quantity"] += item_quantity
            else:
                self.Mounted_inventory[item_name] = {"quantity": item_quantity, "grade": item_grade}

    def add_Available_inventory(self, Available_item):
        # Available_inventory에 아이템 추가
        for item_name, (item_quantity, item_grade) in Available_item.items():
            # 아이템 이름과 등급을 결합하여 새로운 아이템 이름 생성
            new_item_name = f"{item_name}_{item_grade}"
            if new_item_name in self.Available_inventory:
                self.Available_inventory[new_item_name]["quantity"] += item_quantity
            else:
                self.Available_inventory[new_item_name] = {"quantity": item_quantity, "grade": item_grade}

    def display_inventory(self):
        delayed_print("\n============장착된 아이템============")
        for item, tier_info in self.Mounted_inventory.items():
            item_name, item_tier = item.split('_')
            print(f"=-{item_name}: 등급 - {item_tier}-=")

        delayed_print("\n=========사용 가능한 아이템:=========")
        for item_name, details in self.Available_inventory.items():
            if isinstance(details, dict):
                quantity = details.get("quantity", 0)
                tier = details.get("grade", "Unknown")
                print(f"{item_name.split('_')[0]}: 갯수 X {quantity}, 등급 - {tier}")
        print("======================================")

    def move_to_mounted_inventory(self, item_name):
        if item_name in self.Available_inventory:
            available_item = self.Available_inventory[item_name]
            if item_name in self.Mounted_inventory:
                print("이미 장착중인 아이템입니다.")
                del self.Available_inventory[item_name]
            else:
                # 같은 아이템이 이미 Mounted_inventory에 있는지 확인하고, 등급을 비교하여 더 높은 것만 추가
                for mounted_item_name, mounted_item in self.Mounted_inventory.items():
                    if mounted_item_name.split('_')[0] == item_name.split('_')[0]:
                        if int(available_item["grade"]) > int(mounted_item["grade"]):
                            del self.Mounted_inventory[mounted_item_name]  # 기존에 장착된 아이템을 장착된 인벤토리에서 삭제
                            print(f"{mounted_item_name}을(를) 해제하고 {item_name}을(를) 장착 아이템으로 추가했습니다.")
                            self.Mounted_inventory[item_name] = available_item
                            del self.Available_inventory[item_name]
                            break
                        else:
                            print(f"{item_name}의 등급이 {mounted_item_name}보다 낮습니다. 추가할 수 없습니다.")
                            self.Available_inventory[item_name]
                            return
                else:
                    self.Mounted_inventory[item_name] = available_item
                    del self.Available_inventory[item_name]  # 아이템을 추가하기 전에 사용 가능한 인벤토리에서 삭제
                    print(f"{item_name}을(를) 장착 아이템으로 추가했습니다.")

            # 장착된 아이템에 따라 플레이어의 능력치 업데이트
            self.update_player_stats()
        else:
            print(f"아이템 {item_name}이(가) 없습니다.")
    
    def update_player_stats(self):
        # 플레이어의 기본 능력치
        self.Max_HP = 100 + (self.LV - 1) * 5  # 간단한 예시로 최대 체력이 레벨에 비례하여 증가하도록 설정
        self.STR = 10 + (self.LV - 1) * 3  # 레벨에 비례하여 공격력 증가
        self.VIT = 0.1 + (self.LV - 1) * 0.01  # 레벨에 비례하여 방어력 증가
        self.Critical = 0.1 + (self.LV - 1) * 0.01  # 레벨에 비례하여 크리티컬 확률 증가
        self.Avoid = 0.1 + (self.LV - 1) * 0.01  # 레벨에 비례하여 회피 확률 증가

        # 장착된 각 아이템의 능력치를 반영하여 플레이어의 능력치 업데이트
        for item_name, item_info in self.Mounted_inventory.items():
            number_grade = int(item_name.split('_')[-1])
            if item_name.split("_")[0] == "머리 보호구":
                self.Max_HP += 20 * number_grade
                self.VIT += 0.2 * number_grade
                self.Avoid += 0.02 * number_grade
            elif item_name.split("_")[0] == "가슴 보호구":
                self.Max_HP += 50 * number_grade
                self.VIT += 0.5 * number_grade
                self.Avoid += 0.02 * number_grade
            elif item_name.split("_")[0] == "손 보호구":
                self.Max_HP += 10 * number_grade
                self.VIT += 0.1 * number_grade
                self.Avoid += 0.02 * number_grade
            elif item_name.split("_")[0] == "다리 보호구":
                self.Max_HP += 30 * number_grade
                self.VIT += 0.3 * number_grade
                self.Avoid += 0.02 * number_grade
            elif item_name.split("_")[0] == "발 보호구":
                self.Max_HP += 10 * number_grade
                self.VIT += 0.1 * number_grade
                self.Avoid += 0.02 * number_grade
            elif item_name.split("_")[0] == "검":
                pass

                
    def remove_mounted_item(self, item_name):
        if item_name in self.Mounted_inventory:
            existing_item_grade = self.Mounted_inventory[item_name]["grade"]
            del self.Mounted_inventory[item_name]
            print(f"{item_name}을(를) 장착 아이템에서 삭제했습니다.")

            # 나머지 아이템들 중 등급이 낮은 아이템 삭제
            items_to_remove = []
            for mounted_item_name, mounted_item_info in self.Mounted_inventory.items():
                if mounted_item_info["grade"] < existing_item_grade:
                    items_to_remove.append(mounted_item_name)
            for item in items_to_remove:
                del self.Mounted_inventory[item]
                print(f"{item}을(를) 장착 아이템에서 삭제했습니다.")
                
            # 이름이 같은 아이템 삭제
            same_name_items = [name for name in self.Mounted_inventory if name.split('_')[0] == item_name.split('_')[0]]
            for item in same_name_items and item.split('')[1] < item_name.split('')[1]:
                if item != item_name:
                    del self.Mounted_inventory[item]
                    print(f"{item}을(를) 장착 아이템에서 삭제했습니다.")
        else:
            print(f"{item_name}이(가) 장착된 아이템 목록에 없습니다.")

    def display_stats(self): #스텟
        delayed_print("\n==========플레이어 프로필==========")
        print(f"이름: {self.Name}")
        print(f"LV: {int(self.LV)}")
        print(f"EXP: {int(self.EXP)}")
        print(f"돈: {int(self.Money)}")
        print(f"체력: {round(self.HP, 1)}/{int(self.Max_HP)}")
        print(f"공격력: {int(self.STR)}")
        print(f"방어력: {int(self.VIT)}   -----10이 최대값-----")
        print(f"크리티컬: {round(self.Critical, 1)}-----1이 최대값------")
        print(f"회피력: {round(self.Avoid, 1)}  -----1이 최대값------")
        print("==================================")

    def equip_armor(self, armor):
        # 해당 갑옷 종류가 이미 장착되어 있는지 확인
        if armor.name in self.Mounted_inventory:
            print(f"{self.Name}은(는) 이미 {armor.name}을(를) 장착하고 있습니다.")
        else:
            # 해당 갑옷 종류가 장착되어 있지 않다면 장착
            self.Mounted_inventory[armor.name] = armor
            # 플레이어의 능력치 업데이트
            self.Max_HP += armor.Max_HP_bonus
            self.STR += armor.STR_bonus
            self.VIT += armor.VIT_bonus
            self.Critical += armor.Critical_bonus
            self.Avoid += armor.Avoid_bonus
            print(f"{self.Name}이(가) {armor.name}을(를) 장착했습니다.\n 최대 체력이 {armor.Max_HP_bonus} 증가하고," +
                  f" 공격력이 {armor.STR_bonus} 증가하고, 방어력이 {armor.VIT_bonus} 증가합니다.")

#공격 함수
def attack(player, monster):
    # 방어력을 퍼센트 단위로 변환
    AKT = player.STR * (1 - monster.VIT / 10.0)
    # 크리티컬 확률 계산
    if random.random() < player.Critical:
        AKT *= 1.5  # 크리티컬 발생 시 데미지 두 배
        print("Critical Hit!!!")
    # 데미지 적용
    monster.HP -= AKT
    delayed_print(f"{player.Name}이(가) {monster.Name}에게 {round(AKT, 1)}의 피해를 입혔습니다!")


#불러오는 함수
def read_player(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        player_data = json.load(file)
        player = Player(player_data['Name'], player_data['Money'], player_data['HP'],
                        player_data['Max_HP'], player_data['STR'], player_data['VIT'],
                        player_data['Critical'], player_data['Avoid'], player_data['LV'],
                        player_data['EXP'])
        player.set_Mounted_inventory(player_data.get('Mounted_inventory', {}))
        player.set_Available_inventory(player_data.get('Available_inventory', {}))
        return player

# 사용자 프로필 정보를 JSON 형식으로 저장하는 함수
def save_player_data(player, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(player.__dict__, file, ensure_ascii=False, indent=4)

#게임 오버 함수
def over(player):
    if player.HP < 0:
        for _ in range(6):
            print("게임 오버!!")
        raise ValueError("플레이어의 체력이 0보다 작아서 게임이 종료됩니다.")

#레벨업 함수
def level_up(Player): #지정 능력치 증가 or 스텟 증가
    Player.LV += 1
    print(f"레벨 업! 현재 레벨: {Player.LV}")
    print(f"공격력이 3 증가하였습니다.\n 새로운 공격력: {Player.STR}")
    print(f"최대 체력이 5 증가하였습니다.\n 새로운 최대 체력: {Player.Max_HP}")   #사용 방법 level_up(player)# player = (이름,체력,최대 체력,..등)


#나가기
def Exit(user_input, player, store):
    if user_input == '나가기':
        print("\n마을로 돌아가는중 ...... \n")
        village_action(player, store)

# 아이템 사용 클래스

def Use_Item(player, Select_item, turn):  # 만들어둔 사용 아이템 능력
    item_turn = 3  # 아이템 효과 지속 턴 설정
    
    Useing_grade = int(Select_item.split('_')[-1]) 

    if Select_item in player.Available_inventory:  
        if "회복물약" in Select_item:  # 체력 회복 아이템인 경우
            print(f"{Select_item} : 체력 회복: {200 * Useing_grade}")
            player.HP += 200 * Useing_grade
            if player.HP > player.Max_HP:
                player.HP = player.Max_HP
        elif "공격력증가물약" in Select_item:  # 공격력 증가 아이템인 경우
            print(f"{Select_item} : 공격력 증가: {40 * Useing_grade}")
            player.STR += 40 * Useing_grade
        elif "방어력증가물약" in Select_item:  # 방어력 증가 아이템인 경우
            print(f"{Select_item} : 방어력 증가: {1.1 * Useing_grade}")
            player.VIT += 1.1 * Useing_grade
        elif "크리티컬증가물약" in Select_item:  # 크리티컬 증가 아이템인 경우
            print(f"{Select_item} : 크리티컬확률 증가: {1.1 * Useing_grade}")
            player.Critical += 1.1 * Useing_grade
        elif "회피율증가물약" in Select_item:  # 회피율 증가 아이템인 경우
            print(f"{Select_item} : 회피율 증가: {1.05 * Useing_grade}")
            player.Avoid += 1.05 * Useing_grade
        
        # 아이템 효과 지속 턴 감소
        turn += 1
        if turn >= item_turn:
            print(f"{Select_item}의 효과가 사라졌습니다.")
            # 아이템 효과 초기화
            if "회복물약" in Select_item:
                player.HP -= 200 * Useing_grade
                if player.HP < 0:
                    player.HP = 0
            elif "공격력증가물약" in Select_item:
                player.STR -= 40 * Useing_grade
            elif "방어력증가물약" in Select_item:
                player.VIT -= 1.1 * Useing_grade
            elif "크리티컬증가물약" in Select_item:
                player.Critical -= 1.1 * Useing_grade
            elif "회피율증가물약" in Select_item:
                player.Avoid -= 1.05 * Useing_grade
                
            # 사용한 아이템 인벤토리에서 제거
            del player.Available_inventory[Select_item]
    else:
        print(f"{Select_item}이(가) 인벤토리에 없습니다.")

# 상점 클래스
class Store:
    def __init__(self):
        self.products = pd.DataFrame(columns=['이름', '가격', '갯수', '등급'])

    def add_product(self, name, price, stock, tier):
        new_product = pd.DataFrame({'이름': [name], '가격': [price], '갯수': [stock], '등급': [tier]})
        self.products = pd.concat([self.products, new_product], ignore_index=True)

    def list_products(self):
        return self.products

    def list_products_by_category(self, category):
        print(f"\n{category} 항목 상품 목록:")
        return self.products[self.products['이름'].str.contains(category) | (self.products['이름'] == category)].reset_index(drop=True)

    def purchase_product(self, name, tier, quantity, player):
        product_index = self.products[(self.products['이름'] == name) & (self.products['등급'] == int(tier))].index
        if len(product_index) == 0:
            print("해당 상품이 상점에 없습니다.")
            return 0
        else:
            product_index = product_index[0]
            total_price = self.products.at[product_index, '가격'] * quantity
            if total_price <= player.Money:
                if self.products.at[product_index, '갯수'] >= quantity:
                    self.products.loc[product_index, '갯수'] -= quantity
                    print(f"{name} : 상품을 {quantity}개 구매하였습니다.")
                    player.add_Available_inventory({name: [quantity, tier]})  # 여기서 수정
                    player.Money -= total_price  # 구매 후 플레이어의 돈에서 상품 가격 차감
                    save_player_data(player, "{}.json".format(player.Name))
                    return total_price
                else:
                    print("재고가 부족하여 구매할 수 없습니다.")
                    return 0
            else:
                print("돈이 부족하여 구매할 수 없습니다.")
                return 0

# 구매 함수
def buy_store(player, store):  # store 매개변수 추가
    while True:
        print("사용 아이템----회복, 최대, 공격력, 방어력, 크리, 회피----\n")
        print("장착 아이템----------머리, 가슴, 손, 다리, 발----------")
        wish_list = input("\n나가기 / 원하는 항목을 말해주세요 : ")
        if wish_list in categories:
            select_product(store, wish_list)  # store 객체 전달
            buy_product(player, store)  # 상품 선택 후에 바로 구매 과정으로 이동
        elif wish_list == "나가기" :
            break
        else:
            print("해당하는 항목이 없습니다.")

# 상품 선택 함수ㅁ
def select_product(store, category):
    products = store.list_products_by_category(category)
    if products.empty:
        print("해당 항목에 대한 상품이 없습니다.")
    else:
        products.loc[:, '가격'] = products['가격'].map('{:,.0f}'.format)  # 가격 포맷 변경
        print(products.to_string(index=False, justify='center', col_space={'이름': 10, '가격': 10, '갯수': 10}))

# 구매 상품 함수
def buy_product(player, store):
    wish_name = input("\n나가기 / 구매할 상품을 입력하세요: ")
    # 사용자가 '나가기'를 입력했을 경우
    if wish_name == '나가기':
        print("구매를 취소합니다.")
        return player.Money
    wish_tier = input("나가기 / 원하는 등급를 입력해주세요 : ")
    wish_desired_number = int(input("원하는 갯수를 적어주세요 : "))
    total_price = store.purchase_product(wish_name, wish_tier, wish_desired_number, player)
    return player.Money

print("//정상//비정상시 출력 안됨")
# 몬스터 클래스
class Monster:
    def __init__(self, Name, LV, HP, Max_HP, STR, VIT, Critical, Avoid):
        self.Name = Name
        self.LV = LV
        self.HP = HP
        self.Max_HP = Max_HP
        self.STR = STR
        self.VIT = VIT
        self.Critical = Critical
        self.Avoid = Avoid

    def apply_damage(self, damage):
        self.HP -= damage
        if self.HP < 0:
            self.HP = 0

    def display_monster(self): #스텟
        print("\n=======몬스터 프로필=======")
        print(f"이름: {self.Name}")
        print(f"LV: {self.LV}")
        print(f"체력: {round(self.HP, 1)}/{self.Max_HP}")
        print(f"공격력: {self.STR}")
        print(f"방어력: {self.VIT}")
        print(f"크리티컬: {self.Critical}")
        print(f"회피력: {self.Avoid}")
        print("=============================")

    def __str__(self):
        return f"Monster(Name='{self.Name}', LV={self.LV}, HP={self.HP}, Max_HP={self.Max_HP}, STR={self.STR}, VIT={self.VIT}, Critical={self.Critical}, Avoid={self.Avoid})"
#몬스터 스킬 함수 mon_skill
def revive():
    if random.random(monster) > 0.3:
        print(f"{monster.Name}가 부활 했습니다.")
        monster.HP = monster.Max_HP / 2

def Transformation(monster):
    if monster.HP < monstr.Max_HP /2:
        print(f"{monster.Name}가 변신했습니다.")
        monster.Max_HP *= 2
        monster.HP = monster.Max_HP
        monster.STR *= 1.3
        monster.VIT *= 1.2
        monster.Critical = 0.3
#지속딜 
def DOT(monster, player):
    if random.random() < 0.4:
        delayed_print(f"{monster.Name}의 브래스에 의해 지속적인 데미지를 받고 있습니다.(현재체력의 %6: {player.Max_HP * 0.06})",0.05)
        player.HP -= player.Max_HP * 0.06
        
def Vam_AKT_Heal(monster, Vam_AKT):
    if random.random() < 0.1:
        heal_amount = Vam_AKT / 2
        delayed_print(f"{monster.Name}가 당신이 흘린 피를 가져갑니다 ({monster.Name}의 회복량: {monster.HP + (Vam_AKT / 2)})", 0.03)
        if monster.HP + heal_amount < monster.Max_HP:
            monster.HP += heal_amount
        else:
            monster.HP = monster.Max_HP

def Vam_Heal(monster):
    if random.random() < 0.1:
        delayed_print(f"{monster.Name}가 관작에 들어가 회복되었습니다 현재체력의 50% (회복량: {monster.HP / 2})")
        monster.HP += monster.HP / 2

def read_monster(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        monster_data = json.load(file)
        #print("Read monster data:", monster_data)  # 디버깅 출력 추가
        monster = Monster(monster_data['Name'], monster_data['LV'], monster_data['HP'],
                          monster_data['Max_HP'], monster_data['STR'], monster_data['VIT'],
                          monster_data['Critical'],monster_data['Avoid'])  # 키 수정
        return monster


def save_monster_data(monster, mon_file_path):
    with open(mon_file_path, 'w', encoding='utf-8') as file:
        json.dump(monster.__dict__, file, ensure_ascii=False, indent=4)

def create_monsters_from_file(mon_file_path):
    with open(mon_file_path, 'r', encoding='utf-8') as f:
        monster_names = f.readlines()
        for monster_name in monster_names:
            monster_name = monster_name.strip()  # 줄 바꿈 문자 제거
            monster = Monster(monster_name, 1, 100, 100, 10, 0.1, 0.1, 0.1)  # 새로운 몬스터 생성
            mon_file_path = "{}.json".format(monster_name)  # 몬스터 JSON 파일 경로 및 파일 이름
            save_monster_data(monster, mon_file_path)

def mon_attack(player, monster):
    # 방어력을 퍼센트 단위로 변환
    AKT = monster.STR * (1 - player.VIT / 10.0)
    # 크리티컬 확률 계산
    if random.random() < monster.Critical:
        AKT *= 1.5  # 크리티컬 발생 시 데미지 두 배
        delayed_print("Critical Hit!!!")
    # 데미지 적용
    player.HP -= AKT
    delayed_print(f"{monster.Name}가 플레이어 {player.Name}에게 {round(AKT, 1)}의 피해를 입혔습니다!")
    if monster.Name == "뱀파이어":#뱀파이어가 넣은 데미지는 저장
        Vam_AKT += AKT_rounded
        return Vam_AKT
def print_EXP(player, floor):
    player.EXP += 50*floor
    print(f"얻은 경험치: {50*floor} 경험치: {player.EXP}/{250*player.LV}")
    if player.EXP >= 250*player.LV:
        level_up(player)
        player.EXP = 0


'''
helmet = Armor("머리갑옷", 20, 0, 0)  # 머리 갑옷: 최대 체력 20 증가
chestplate = Armor("가슴갑옷", 50, 0, 10)  # 가슴 갑옷: 최대 체력 50 증가, 방어력 10 증가
leggings = Armor("다리갑옷", 30, 10, 0)  # 다리 갑옷: 최대 체력 30 증가, 공격력 10 증가
boots = Armor("발갑옷", 10, 0, 5)  # 발 갑옷: 최대 체력 10 증가, 방어력 5 증가
gloves = Armor("손갑옷", 15, 5, 5)  # 손 갑옷: 최대 체력 15 증가, 공격력 5 증가, 방어력 5 증가
gloves = Armor("손갑옷_2", 15, 5, 5)
# 플레이어 생성
player = Player("잉", 100, 100, 10,1,1,1,1,1,1)  # 초기 체력 100, 최대 체력 100, 공격력 10, 방어력 10

# 갑옷 장착
player.equip_armor(helmet)
player.equip_armor(chestplate)
player.equip_armor(leggings)
player.equip_armor(boots)
player.equip_armor(gloves)
print(f"{player.Name}의 체력: {player.HP}/{player.Max_HP}")  # 출력: 플레이어의 체력: 150/100

# 갑옷 해제

print(f"{player.Name}의 체력: {player.HP}/{player.Max_HP}")  # 출력: 플레이어의 체력: 100/100
# 몬스터 드랍 아이템 클래스
''''''
player = Player("John", 1000, 100, 100, 10, 5, 0.1, 0.1, 1, 0)

# 새로운 아이템 생성
new_item = {
    "Sword": {"attack": 20, "defense": 5}
}

# 플레이어의 장착된 아이템 목록에 새로운 아이템 추가
player.add_Mounted_inventory(new_item)


# 플레이어의 사용 가능한 아이템 목록에 새로운 아이템 추가
player.add_Available_inventory(another_new_item)

# 인벤토리 출력
player.display_inventory()

# 아이템 제거
player.remove_Mounted_inventory("Sword")
player.remove_Available_inventory("Potion")

# 인벤토리 출력
player.display_inventory()'''