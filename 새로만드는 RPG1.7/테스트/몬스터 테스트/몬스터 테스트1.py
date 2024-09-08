import json
import os

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
        print(f"체력: {self.HP}/{self.Max_HP}")
        print(f"공격력: {self.STR}")
        print(f"방어력: {self.VIT}")
        print(f"크리티컬: {self.Critical}")
        print(f"회피력: {self.Avoid}\n")
        print("=============================")

    def __str__(self):
        return f"Monster(Name='{self.Name}', LV={self.LV}, HP={self.HP}, Max_HP={self.Max_HP}, STR={self.STR}, VIT={self.VIT}, Critical={self.Critical}, Avoid={self.Avoid})"

def read_monster(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        monster_data = json.load(file)
        print("Read monster data:", monster_data)  # 디버깅 출력 추가
        monster = Monster(monster_data['Name'], monster_data['LV'], monster_data['HP'],
                          monster_data['Max_HP'], monster_data['STR'], monster_data['VIT'],
                          monster_data['Critical'],monster_data['Avoid'])  # 키 수정
        return monster


def save_monster_data(monster, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(monster.__dict__, file, ensure_ascii=False, indent=4)

def create_monsters_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        monster_names = f.readlines()
        for monster_name in monster_names:
            monster_name = monster_name.strip()  # 줄 바꿈 문자 제거
            monster = Monster(monster_name, 1, 100, 100, 10, 0.1, 0.1, 0.1)  # 새로운 몬스터 생성
            file_path = "{}.json".format(monster_name)  # 몬스터 JSON 파일 경로 및 파일 이름
            save_monster_data(monster, file_path)

# 현재 디렉토리에서 monsters 폴더 내의 파일을 읽어올 수 있도록 경로 수정
monN = input("몬스터 이름: ")
file_path = f"monsters/{monN}.json"


# read_monster() 함수 호출하여 몬스터 데이터 가져오기

monster = read_monster(file_path)
#monster.apply_damage(damage)
monster.display_monster()
print(monster)
save_monster_data(monster, file_path)
