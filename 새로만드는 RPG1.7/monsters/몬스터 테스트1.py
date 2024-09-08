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

# "MonsterName.txt" 파일에서 몬스터 이름을 읽어와서 몬스터 생성 및 저장
file_path = "MonsterName.txt"  # 몬스터 이름이 담긴 파일 경로
create_monsters_from_file(file_path)
'''
# 현재 디렉토리에서 monsters 폴더 내의 파일을 읽어올 수 있도록 경로 수정
    file_path = "monsters/고블린.json"

    # read_monster() 함수 호출하여 몬스터 데이터 가져오기
    goblin = read_monster(file_path)

    # 변수명 수정
    monster_name = "고블린"  # monster_name 변수 정의

    print(f"{monster_name} 몬스터 프로필:")
    print(f"LV: {goblin.LV}, HP: {goblin.HP}, STR: {goblin.STR}, VIT: {goblin.VIT}")'''
