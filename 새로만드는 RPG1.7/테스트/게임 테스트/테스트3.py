from 테스트4 import *
# 아이템 생성
another_new_items = []  # 만들어둔 사용 아이템들
for i in range(1, 6):
    another_new_items.append(Use_Item("회복물약", "티어 : " + str(i), "HP"))
    another_new_items.append(Use_Item("최대_체력_증가_물약", "티어 : " + str(i), "Max_HP"))
    another_new_items.append(Use_Item("공격력_증가_물약", "티어 : " + str(i), "STR"))
    another_new_items.append(Use_Item("방어력_증가_물약", "티어 : " + str(i), "VIT"))
    another_new_items.append(Use_Item("크리티컬_증가_물약", "티어 : " + str(i), "Critical"))
    another_new_items.append(Use_Item("회피율_증가_물약", "티어 : " + str(i), "Avoid"))
#상점 생성
store = Store()
for i in range(1, 6):
    store.add_product('회복물약', 1000 * i, 10, i)
    store.add_product('최대 체력 증가 물약', 500 * i, 20, i)
    store.add_product('공격력 증가 물약', 800 * i, 15, i)
    store.add_product('방어력 증가 물약', 1500 * i, 10, i)
    store.add_product('크리티컬 증가 물약', 600 * i, 20, i)
    store.add_product('회피율 증가 물약', 1000 * i, 15, i)
    store.add_product('머리 보호구', 2000 * i^2, 1, i)
    store.add_product('가슴 보호구', 3000 * i^2, 1, i)
    store.add_product('손 보호구', 1400 * i^2, 1, i)
    store.add_product('다리 보호구', 2500 * i^2, 1, i)
    store.add_product('발 보호구', 1300 * i^2, 1, i)


#로그인 및 메인
def main(player, monster):
    Name_list = load_player_names("PlayerName.txt")
    inputplayerName = input_player_name(Name_list)

    if inputplayerName == "없음":
        newplayer = create_new_player(Name_list)
        save_player(newplayer, "{}.json".format(newplayer.Name))  # 수정된 부분
        inputplayerName = newplayer.Name
    else:
        player = load_player(inputplayerName)
    
    # 상점 생성
    store = Store()  # 상점 객체 생성


    while True:
        worldmap = input("--메인 메뉴--\n나가기 / 저장 / 마을 / 던전: ")
        if worldmap == "나가기":
            print("저장하고 종료하는 중...")
            save_player(player, "{}.json".format(player.Name))  # 수정된 부분
            break
        elif worldmap == "저장":
            save_player(player, "{}.json".format(player.Name))  # 수정된 부분
        elif worldmap == "마을":
            village_action(player, store)  # 수정된 부분
        elif worldmap == "던전":
            Dungeon(player, monster)


#플레이어 확인 함수들
def load_player_names(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f]

def input_player_name(name_list):
    input_name = input("전에 플레이 하던 데이터가 있다면 이름을 입력해 주세요\n(없다면 없음): ")
    if input_name in name_list:
        return input_name
    else:
        print("존재 하지 않는 이름입니다.")
        return "없음"

def create_new_player(name_list):
    new_name = input("새로운 닉네임을 생성해주세요: ")
    while new_name in name_list:
        print("이미 존재하는 이름입니다.")
        new_name = input("다시 입력해주세요: ")
    with open("PlayerName.txt", 'a', encoding='utf-8') as f:
        f.write(new_name + '\n')
    return Player(new_name, 2000, 100, 100, 10, 0.1, 0.1, 0.1, 1, 0)

def load_player(name):
    return read_player("{}.json".format(name))

def save_player(player, file_path):
    save_player_data(player, file_path)  # save_player_data를 호출할 때 file_path를 전달
    print("플레이어 데이터가 저장되었습니다.")
#마을 함수
def village_action(player, store):
    save_player(player, "{}.json".format(player.Name))
    print("==마을==\n나가기 - 메뉴로 나간다")
    print("프로필 - 프로필 확인")
    print("아이템 - 아이템 장착")
    print("휴식 - 체력 회복")
    print("상점 - 상점으로 이동")
    action = input("이동: ")
    if action == "나가기":
        return
    elif action == "프로필":
        print("_"*10)
        player.display_stats()
        print("_"*10)
        player.display_inventory()
        print("_"*10)
        village_action(player, store)  # 수정된 부분
    elif action == "아이템":
        print("==보호구==/==검==")
        category = input("장착할 아이템 카테고리: ")
        if category =="보호구":
            equip_item(player)  # 수정된 부분
        elif categories == "검":
            pass
        else:
            village_action(player, store)
    elif action == "휴식":
        print("휴식끝")
        village_action(player, store)  # 수정된 부분
    elif action == "상점":
        buy_store(player, store) 
    else:
        print("잘못된 입력")
        village_action(player, store)  # 수정된 부분


#아이템 장착 함수
def equip_item(player):
    while True:
        player.display_stats()
        print("\n========= 장착된 아이템: =========")
        for item_name, item_info in player.Mounted_inventory.items():
            delayed_print(f"=-{item_name}: 등급 - {item_info['grade']}=-")

        print("\n=========사용 가능한 아이템: =========")
        for item_name, item_info in player.Available_inventory.items():
            print(f"{item_name}:  등급 - {item_info['grade']}")

        print("\n===장착할 아이템을 선택하세요===")
        print("머리 보호구_1, 머리 보호구_2 등등")
        choose = input("나가기 / 장착할 아이템: ")
        
        player.move_to_mounted_inventory(choose)
        if choose.lower() == "나가기":
            break

def Dungeon(player, monster):
    delayed_print("숫자만 입력해 주세요.\n1층~~6층까지 존재하는 던전..../스페셜:0층")
    floor = int(input("몇층으로 이동하시겠습니까?: "))

    monsters_floor_tier = {
        0: ["미믹"],
        1: ["슬라임", "파란달팽이", "빨간달팽이", "초록달팽이"],
        2: ["고블린", "늑대", "좀비", "스켈레톤","켄타오로스", "트롤", "미라",],
        3: ["골렘", "오크", "하피", "예티", "늑대인간"],
        4: ["파이어 드래곤", "아이스 드래곤", "포이즌 드래곤", "메두사"],
        5: ["뱀파이어", "히드라", "바실리스크","크라켄"],
        6: ["각성 크라켄", "푸른 눈의 백룡"]
    }

    if floor in monsters_floor_tier: # 선택한 층이 유효한지 확인
        delayed_print(f"{floor}층에 오신걸 환영합니다")
        
        # 해당 층의 몬스터 목록 출력
        print("이 층에서 만날 수 있는 몬스터 목록:")
        for i, monster_names in enumerate(monsters_floor_tier[floor], 1):
            print(f"{i}. {monster_names}")

        # 사용자에게 몬스터 선택 받기
        monster_choice = int(input("원하는 몬스터의 번호를 선택하세요: ")) - 1

        if 0 <= monster_choice < len(monsters_floor_tier[floor]):
            selected_monster = monsters_floor_tier[floor][monster_choice]
            delayed_print(f"선택된 몬스터: {selected_monster}")
            mon_file_path = f"monsters/{selected_monster}.json"
            monster = read_monster(mon_file_path)
        else:
            print("올바르지 않은 몬스터 번호입니다.")
    else:
        print("존재하지 않는 층입니다.")
    monster.display_monster()
    while True:
        save_player(player, "{}.json".format(player.Name))
        save_monster_data(monster, mon_file_path)
        if monster.HP <= 0:
            delayed_print(f"\n======{monster.Name}이(가) 쓰러졌습니다!======\n")
            #이자리에 처치 보상 나오게
            delayed_print("=====처리 보상=====")
            Dungeon(player, monster)
        Dungeon_action = input("어떤 행동을 하시겠습니까?\n/ 나가기 / 공격 / 아이템 사용 /\n입력 : ")  # 던전 액션을 행동에서 받는다
        if Dungeon_action == "공격" or "2":
            attack(player, monster)
        elif Dungeon_action == "아이템 사용" or "3":
            print("아이템 사용")
        elif Dungeon_action == "나가기" or "1":
            break
        else:
            print("알수 없는 입력입니다.")
        monster.display_monster()
        mon_attack(player, monster)
        player.display_stats()

  

player = ""
if __name__ == "__main__":
    main(player, Monster)