import MySQLdb
from config import host, userName, password, dbName
import os

Games = ['Inish', 'SpaceContact', 'Carcassonne', 'ThroughTheCenturies', 'Bullet', 'StarEmpires', '7WondersDuel', 'GameOfThrones', 'Root', 'Empires', 'Unmatched']

createLine = 60 * '#'



def statM(nowGame, rows):
    players, nowPlayers = list(), list()

    for row in rows:
        if row[5] == 'P':
            players.append(row[1])


    while players:
        print('Кто участвовал?')
        for i in range(len(players)):
            player = players[i]
            print(f'{i + 1} - {player}')
        print('5 - Все участники')
        print('6 - Всё')
        choice = input('Выберите: ')
        os.system('cls' if os.name == 'nt' else 'clear')

        if choice == '6':
            break
        elif choice == '5':
            nowPlayers = ['Vlad', 'Dima', 'Sasha', 'Nastya']
            break
        else:
            nowPlayers.append(players.pop(int(choice) - 1))

    if len(nowPlayers) < 2:
        print(createLine)
        print('Ошибка! Мало участников.')
        print(createLine)
        return

    print('Кто победил?')
    for i in range(len(nowPlayers)):
        player = nowPlayers[i]
        print(f'{i + 1} - {player}')
    choice = int(input('Выберите: '))
    os.system('cls' if os.name == 'nt' else 'clear')

    winner = nowPlayers[choice - 1]

    #############################----editing----########################################

    partiesGame = rows[0][2] + 1

    nowRow = [list(row) for row in rows if row[1] in nowPlayers]

    for row in nowRow:
        row[2] += 1
        if row[1] == winner:
            row[3] += 1
        row[4] = row[3] / row[2]

    #############################----recording----########################################
    with conn.cursor() as cursor:
        cursor.execute(f"UPDATE {nowGame} SET parties = {partiesGame} WHERE name = '{nowGame}'")
        conn.commit()

    for row in nowRow:
        with conn.cursor() as cursor:
            cursor.execute(
                f"UPDATE {nowGame} SET parties = '{row[2]}', vicrory = '{row[3]}', winrate = '{row[4]}' WHERE name = '{row[1]}'")
            conn.commit()




def statB(nowGame, rows):
    players, nowPlayers, factions, Pair = list(), list(), list(), dict()

    for row in rows:
        if row[5] == 'P':
            players.append(row[1])
        elif row[5] == 'F':
            factions.append(row[1])


    while players:
        print('Кто участвовал?')
        for i in range(len(players)):
            player = players[i]
            print(f'{i + 1} - {player}')
        print('6 - Всё')
        choiceP = input('Выберите: ')
        os.system('cls' if os.name == 'nt' else 'clear')

        if choiceP == '6':
            break
        else:
            print('Кем играл?')
            for i in range(len(factions)):
                faction = factions[i]
                print(f'{i + 1} - {faction}')
            choiceF = input('Выберите: ')
            os.system('cls' if os.name == 'nt' else 'clear')

            Pair[players[int(choiceP) - 1]] = factions[int(choiceF) - 1]
            del players[int(choiceP) - 1]
            del factions[int(choiceF) - 1]

    if len(Pair) < 2:
        print(createLine)
        print('Ошибка! Мало участников.')
        print(createLine)
        return

    print('Кто победил?')
    nowPlayers = [player for player in Pair.keys()]
    nowFactions = [faction for faction in Pair.values()]

    for i in range(len(nowPlayers)):
        player = nowPlayers[i]
        print(f'{i + 1} - {player}')
    choice = int(input('Выберите: '))
    os.system('cls' if os.name == 'nt' else 'clear')

    winner = nowPlayers[choice - 1]

    #############################----editing----########################################
    partiesGame = rows[0][2] + 1

    participants = nowPlayers + nowFactions
    nowRow = [list(row) for row in rows if row[1] in participants]

    for row in nowRow:
        row[2] += 1
        if row[1] == winner or row[1] == Pair[winner]:
            row[3] += 1
        row[4] = row[3] / row[2]

    #############################----recording----########################################
    with conn.cursor() as cursor:
        cursor.execute(f"UPDATE {nowGame} SET parties = {partiesGame} WHERE name = '{nowGame}'")
        conn.commit()

    for row in nowRow:
        with conn.cursor() as cursor:
            cursor.execute(f"UPDATE {nowGame} SET parties = '{row[2]}', vicrory = '{row[3]}', winrate = '{row[4]}' WHERE name = '{row[1]}'")
            conn.commit()

def addStat():
    #############################----survey----########################################
    print('Добавить.')
    print('В какую игру играли?')
    print('1 - Иниш')
    print('2 - Космический контакт')
    print('3 - Каркассон')
    print('4 - Сквозь века')
    print('5 - Bullet')
    print('6 - Звездные империи')
    print('7 - 7 Чудес:Дуэль')
    print('8 - Игра престолов')
    print('9 - Root')
    print('10 - Империи')
    print('11 - Unmatched')
    print('exit - Выход')
    choice = input('Выберите: ')
    os.system('cls' if os.name == 'nt' else 'clear')

    if choice == 'exit':
        return

    nowGame = Games[int(choice) - 1]

    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {nowGame}")
            rows = cursor.fetchall()

        if rows[0][5] == 'M':
            statM(nowGame, rows)
        else:
            statB(nowGame, rows)
    except:
        print(createLine)
        print('Ошибка! Нет такого варианта ответа.')
        print(createLine)

        return

    choice = Games.index(nowGame) + 1
    looStat(choice)
    input(createLine)
    os.system('cls' if os.name == 'nt' else 'clear')


def looStat(choice):
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {Games[int(choice) - 1]}")

            rows = cursor.fetchall()
            rows = [list(row) for row in rows]

            print(createLine)
            print(f'{rows[0][1]}:')
            print(f'Партий: {rows[0][2]}')
            print(createLine)

            nowGame = rows[0][5]
            #############################----sorted table----########################################
            del rows[0]

            def funcsort(x):
                return x[5], x[3], x[4],

            rows.sort(reverse=True, key=funcsort)

            #############################----Building table----########################################
            print(f'№ :' + ' ' + 'Player' + ' ' * (32 - len('Player')) + 'G' + ' ' * (5 - len('G')) + 'V' + ' ' * (6 - len('V')) + 'W' + '\n')
            for i in range(len(rows)):
                row = rows[i]

                if row[5] == 'F':
                    print(createLine)
                    break

                number = str(i + 1) + ' ' * (2 - len(str(i + 1)))
                name = row[1] + ' ' * (30 - len(row[1]))
                parties = str(row[2]) + ' ' * (3 - len(str(row[2])))
                victory = str(row[3]) + ' ' * (3 - len(str(row[3])))
                winrate = str(int(row[4] * 100))

                print(f'{number}: {name}  {parties}  {victory}  {winrate}%')
            if nowGame == 'B':
                for j in range(i, len(rows)):
                    row = rows[j]

                    number = str(j - i + 1) + ' ' * (2 - len(str(j - i + 1)))
                    name = row[1] + ' ' * (30 - len(row[1]))
                    parties = str(row[2]) + ' ' * (3 - len(str(row[2])))
                    victory = str(row[3]) + ' ' * (3 - len(str(row[3])))
                    winrate = str(int(row[4] * 100))

                    print(f'{number}: {name}  {parties}  {victory}  {winrate}%')

    except:
        print(createLine)
        print('Ошибка! Нет такого варианта ответа.')
        return
        print(createLine)


def watchStat():
    while True:
        print('Просмотр.')
        print('Какую игру?')
        print('1 - Иниш')
        print('2 - Космический контакт')
        print('3 - Каркассон')
        print('4 - Сквозь века')
        print('5 - Bullet')
        print('6 - Звездные империи')
        print('7 - 7 Чудес:Дуэль')
        print('8 - Игра престолов')
        print('9 - Root')
        print('10 - Империи')
        print('11 - Unmatched')
        print('exit - Выход')
        choice = input('Выберите: ')
        os.system('cls' if os.name == 'nt' else 'clear')

        if choice == 'exit':
            return

        looStat(choice)
        input(createLine)
        os.system('cls' if os.name == 'nt' else 'clear')



######################-----MAIN-----#########################
try:
    conn = MySQLdb.connect(host, userName, password, dbName)

    print('Добро пожаловать в статистику!')
    while True:
        print('Что желаете?')
        print('1 - Добавить')
        print('2 - Посмотреть')
        print('3 - Выход')
        choice = input('Выберите: ')

        os.system('cls' if os.name == 'nt' else 'clear')

        if choice == '1':
            addStat()
        elif choice == '2':
            watchStat()
        elif choice == '3':
            print(createLine)
            print('Работа завершена.')
            print(createLine)
            conn.close()
            break
        else:
            print(createLine)
            print('Ошибка! Нет такого варианта ответа.')
            print(createLine)

except:
    print(createLine)
    print('Ошибка')
    print(createLine)

