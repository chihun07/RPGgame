import random
import json
import pandas as pd
import locale
import sys

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
        print("\n장착된 아이템:")
        for item, tier_info in self.Mounted_inventory.items():
            item_name, item_tier = item.split('_')
            print(f"=-{item_name}: 등급 - {item_tier}-=")

        print("\n사용 가능한 아이템:")
        for item_name, details in self.Available_inventory.items():
            if isinstance(details, dict):
                quantity = details.get("quantity", 0)
                tier = details.get("grade", "Unknown")
                print(f"{item_name.split('_')[0]}: 갯수 X {quantity}, 등급 - {tier}")
            else:
                print(f"{item_name}: 잘못된 형식의 데이터입니다.")

    def move_to_mounted_inventory(self, item_name):
        if item_name in self.Available_inventory:
            available_item = self.Available_inventory[item_name]
            if item_name in self.Mounted_inventory:
                print("이미 장착중인 아이템입니다.")
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
                            del self.Available_inventory[item_name]
                            return
                else:
                    self.Mounted_inventory[item_name] = available_item
                    del self.Available_inventory[item_name]  # 아이템을 추가하기 전에 사용 가능한 인벤토리에서 삭제
                    print(f"{item_name}을(를) 장착 아이템으로 추가했습니다.")
        else:
            print(f"아이템 {item_name}이(가) 없습니다.")

                
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
        print("\n플레이어 프로필:")
        print(f"이름: {self.Name}")
        print(f"LV: {self.LV}")
        print(f"EXP: {self.EXP}")
        print(f"돈: {self.Money}")
        print(f"체력: {self.HP}/{self.Max_HP}")
        print(f"공격력: {self.STR}")
        print(f"방어력: {self.VIT}   -----10이 최대값-----")
        print(f"크리티컬: {self.Critical}-----1이 최대값------")
        print(f"회피력: {self.Avoid}  -----1이 최대값------\n")
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
    Player.STR += 5
    Player.Max_HP += 20
    print(f"레벨 업! 현재 레벨: {Player.LV}")
    print(f"공격력이 5 증가하였습니다.\n 새로운 공격력: {Player.STR}")
    print(f"최대 체력이 20 증가하였습니다.\n 새로운 최대 체력: {Player.Max_HP}")   #사용 방법 level_up(player)# player = (이름,체력,최대 체력,..등)

#플레이어가 데미지를 주는 함수
def attack(player, monster):
        # 플레이어의 공격력을 계산하고 방어력을 반영하여 대상의 체력을 감소시킴
        AKT = player.STR * (1 - monster.VIT / 10.0)
        monster.HP -= AKT
        print(f"{player.Name}이(가) {monster.Name}에게 {AKT}의 피해를 입혔습니다!")
#나가기
def Exit(user_input, player, store):
    if user_input == '나가기':
        print("\n마을로 돌아가는중 ...... \n")
        village_action(player, store)

# 아이템 사용 클래스
class Use_Item():
    def __init__(self, Name=None, Tier=None, Effect=None):
        self.Effect = Effect
        self.Tier = Tier

    def _u_item(self, Select_item):  # 만들어둔 사용 아이템 능력
        if self.Effect == "HP":  # 사용 효과 넣어야함
            print(f"{self.Name} : 체력 증가 X {self.Tier}")
        elif self.Effect == "Max_HP":
            print(f"{self.Name} : 최대 체력 증가 X {self.Tier}")
        elif self.Effect == "STR":
            print(f"{self.Name} : 공격력 증가 X {self.Tier}")
        elif self.Effect == "VIT":
            print(f"{self.Name} : 방어력 증가 X {self.Tier}")
        elif self.Effect == "Critical":
            print(f"{self.Name} : 크리티컬확율 증가 X {self.Tier}")
        elif self.Effect == "Avoid":
            print(f"{self.Name} : 회피율 증가 X {self.Tier}")
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

# 몬스터 드랍 아이템 클래스
'''
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