import json
import monsters


def save_monster(file_path, monster):
    with open(os.path.join(MONSTER_FOLDER, file_path), 'w', encoding='utf-8') as file:
        json.dump(monster.__dict__, file, ensure_ascii=False, indent=4)
#save_monster("{}.json".format(monster.name), monster) #전투 데이터 저장

def read_monster(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        monster_data = json.load(file)
        print("Read monster data:", monster_data)  # 디버깅 출력 추가
        monster = Monster(monster_data['Name'], monster_data['LV'], monster_data['HP'],
                          monster_data['Max_HP'], monster_data['Damage'], monster_data['VIT'],
                          monster_data['Critical'], monster_data['Avoid'], monster_data['Tier'])
        return monster

monster_name = "고블린"

def load_monster(name):
    return read_monster("{}.json".format(name))

monster = load_monster(monster_name)