import pygame as pg
import random
from pygame.locals import *
from player import Player
from enemy import Enemy
from player_att import Attack
from enemy_att import Enemy_att
from playerHp import PlayerHp

pg.init()

'''--------------初始設定值-------------'''

pg.display.set_caption("2D RPG GAME")
width, height = 722, 714  # 圖片寬度,高度
screen = pg.display.set_mode((width, height))  # 設定主畫面
bg = pg.image.load("2D Pixel Dungeon Asset Pack\\background.jpg").convert()  # 載入主畫面背景圖,並且利用convert增加繪製速度
gameover = pg.image.load("image\\game.png").convert()  # 結束遊戲背景
clock = pg.time.Clock()
user_hp = 5  # 腳色的hp值
kill_flag = [1, 1]  # 設定殺死旗標
running = True  # 判斷執行畫面
allCount = 0  # 圖片陣列的計數器
enemy_hp = [3, 3]  # 記怪物的生命值 (攻擊一下扣一)
num = [4, 4]  # 紀錄是否為上下左右
follow_mode = [0, 0]  # enemy_left,enemy_top( 0為敵人自己看到玩家在他身邊,1為玩家攻擊他則自主跟蹤)
x = width / 2 + 2  # 角色初始X座標
y = height / 2 - 15  # 角色初始Y座標
att_count = 0  # 攻擊鍵按下去時間
delay_move = [0, 0]  # 怪物移動時間
delay_user = 0  # 用來延遲腳色移動速度
face_count = [0, 0]  # 用來計數敵人面相時間
eny_attImTime = [0, 0]  # 怪物攻擊圖片顯示時間
'''---------------創立怪物種類以及角色---------------'''
enemy_left = Enemy(27, 294, screen, [27, 123], [294, 390])  # 導入 Enemy, 設定enemy的初始值
enemy_top = Enemy(315, 102, screen, [267, 411], [54, 150])
enemy_rect = [enemy_left, enemy_top]  # 將怪物放入一個陣列裡
check_num = [enemy_left.check_num, enemy_top.check_num]  # 各種怪物的檢查碰撞值
eny_attLi = list()  # 各種類怪物攻擊圖片分類
user = Player(x, y, screen, enemy_rect)  # 導入Player,並且給其初始值
attack = Attack(user.x, user.y, screen)  # 導入攻擊方式
player_hp = PlayerHp(600, 50, screen)  # 初始化玩家血量條設定
'''--------------創立精靈類別並且加入物件-----------'''
allsprite = pg.sprite.Group()  # 創立所有精靈群組
allsprite.add(user)  # 將角色加入所有群組
allsprite.add(enemy_left)  # 將左邊怪物加進所有群組
allsprite.add(enemy_top)  # 將上面怪物加進所有群組
allsprite.add(attack)  # 將使用者攻擊方式放進所有群組
allsprite.add(player_hp)  # 將玩家生命條放進所有群組

def eny_atImg(enemy, eneNum):
    global eny_attLi
    for i in range(eneNum):
        eny_att = Enemy_att(enemy[i].x, enemy[i].y, screen)  # 放入怪物x,y初始化攻擊圖片座標
        eny_attLi.append(eny_att)
        allsprite.add(eny_attLi)


def gameWindow():  # 設定主畫面函式
    screen.blit(bg, (0, 0))  # 建立背景畫面
    print(f"player hp: {user_hp}")
    screen.blit(player_hp.image[user_hp], (500, 25))  # 建立玩家圖片以血量為取得元素
    '''-------------設定角色的(X,Y)座標--------------------------------'''
    font = pg.font.SysFont("Consoles", 28)  # 導入字體名稱,字體大小
    text = font.render(f"({user.x},{user.y})", True, (255, 255, 255), (0, 0, 0))
    # render(文字, 平滑(boolean), 字體顏色, 字體背景顏色)
    screen.blit(text, (0, 0))  # 建立文字


def character():
    global allCount, kill_flag  # 變數allcount宣告為global,在函式中改變其值

    if allCount < 11:  # 每張圖顯示3遍
        allCount += 1
    else:
        allCount = 0  # 重新記數

    character_dir()  # 角色跟怪物面對方向移動及建圖
    attack.update()
    user.update()


def character_dir():
    global kill_flag, allCount, att_count, delay_user
    key = pg.key.get_pressed()
    pg.time.delay(50)

    # 若 沒有碰撞且kill_flag為True,則繼續繪出怪物
    if kill_flag[0] == 1:  # 若kill_flag[0](左邊的敵人)沒有被殺死
        enemy_group(enemy_left, 27, 294, 0)  # 將左邊怪物放入Group裡面
    if kill_flag[1] == 1:  # 若kill_flag[1](上面的敵人)沒有被殺死
        enemy_group(enemy_top, 263, 102, 1)
        ''' 怪物名稱, 初始x,初始y, 判斷碰撞陣列, 放入哪個怪物的kill flag'''
    if not user.move_count:
        user.move(kill_flag)
    else:
        delay_user += 1
        if delay_user == 5:
            user.move_count = False
            delay_user = 0
    attack.x = user.x  # 玩家移動完,攻擊座標跟著移動
    attack.y = user.y
    if user.x != x or user.y != y:  # 若目前角色(X,Y)不為初始值,則改變角色建立的位置
        if user.left:  # 判斷角色面相方向,以建立圖片
            screen.blit(user.image_left[allCount // 3], (user.x, user.y))
            if key[K_j]:  # 若面向左邊而且按下j鍵則建立左邊火焰
                screen.blit(attack.image_left[att_count // 3], (user.x - 48, user.y))
                if att_count == 11:
                    att_count = 0
                else:
                    att_count += 1
                attack.x = user.x - 48
            else:
                att_count = 0
        else:
            screen.blit(user.image_right[allCount // 3], (user.x, user.y))
            if key[K_j]:  # 若面向右邊而且按下j鍵則建立右邊火焰
                screen.blit(attack.image_right[att_count // 3], (user.x + 48, user.y))
                if att_count == 11:
                    att_count = 0
                else:
                    att_count += 1
                attack.x = user.x + 48
            else:
                att_count = 0
        pg.display.update()  # 畫面持續更新

    else:
        if user.left:
            screen.blit(user.image_left[allCount // 3], (x, y))
            if key[K_j]:  # 若面向左邊而且按下j鍵則建立左邊火焰
                screen.blit(attack.image_left[att_count // 3], (user.x - 48, user.y))
                if att_count == 11:
                    att_count = 0
                else:
                    att_count += 1
                attack.x = user.x - 48
            else:
                att_count = 0
        elif user.right:
            screen.blit(user.image_right[allCount // 3], (x, y))
            if key[K_j]:  # 若面向右邊而且按下j鍵則建立右邊火焰
                screen.blit(attack.image_right[att_count // 3], (user.x + 48, user.y))
                if att_count == 11:
                    att_count = 0
                else:
                    att_count += 1
                attack.x = user.x - 48
            else:
                att_count = 0
        pg.display.update()  # 畫面持續更新


# 怪物移動以及建立圖片的函示
'''follow_mode = [0, 0]  # enemy_left,enemy_top( 1為敵人自己看到玩家在他身邊,2為玩家攻擊他則自主跟蹤)'''


def enemy_group(enemy, x_point, y_point, kill_enemy):
    global kill_flag, allCount, enemy_rect, count, follow_mode, check_num, att_count
    if enemy_hp[kill_enemy] != 0 and kill_flag[kill_enemy]:  # 若未被碰撞以及殺死,則怪物持續顯示
        check_num[kill_enemy] = enemy.check_collide(user, enemy.rect)
        if follow_mode[kill_enemy] == 1:  # 1為敵人自己看到玩家在他身邊
            if enemy.left:
                enemy_follow_left(enemy, kill_enemy)  # if enemy left is True,do follow_left function
                '''用一個變數紀錄check的值,當變成4的時候則移動位置,靠近玩家'''
            elif enemy.right:
                enemy_follow_right(enemy, kill_enemy)  # if enemy right is True,do follow_left function
        elif follow_mode[kill_enemy] == 2:  # 2為玩家攻擊他則自主跟蹤
            if user.right:  # 敵人反向顯示
                follow_mode[kill_enemy] = 1  # 則轉換成模式1(敵人追隨模式)
                screen.blit(enemy.image_left[allCount // 3], (enemy.x, enemy.y))
            elif user.left:  # 敵人反向顯示
                follow_mode[kill_enemy] = 1
                screen.blit(enemy.image_right[allCount // 3], (enemy.x, enemy.y))
        else:  # 則都不是,為沒有被攻擊
            if enemy.x != 27 or enemy.y != 294:  # 判斷怪物面相方向,以建立圖片
                if enemy.right:
                    screen.blit(enemy.image_right[allCount // 3], (enemy.x, enemy.y))
                elif enemy.left:
                    screen.blit(enemy.image_left[allCount // 3], (enemy.x, enemy.y))
            else:
                if enemy.right:
                    screen.blit(enemy.image_right[allCount // 3], (x_point, y_point))
                elif enemy.left:
                    screen.blit(enemy.image_left[allCount // 3], (x_point, y_point))
            if allCount // 11 != 0:
                move_num = random.randint(0, 3)  # 給於敵人四個方向的整數亂數,使其移動
                enemy.move(move_num, user, enemy)  # 敵人移動
            if attack.x == enemy.x and attack.y == enemy.y and att_count == 4:  # 若被玩家攻擊,則模式轉成2
                enemy_hp[kill_enemy] -= 1  # 攻擊一下扣敵人血量
                follow_mode[kill_enemy] = 2
            if check_num[kill_enemy] == 2 or check_num[kill_enemy] == 3:  # 若被敵人自己看到,則模式轉成1
                follow_mode[kill_enemy] = 1
        enemy.update()  # 怪物持續更新
    else:  # 若enemy hp 歸0,則殺死怪物並且將旗標歸為False
        kill_flag[kill_enemy] = 0
        enemy.kill()  # 則殺死怪物

    ''' 敵人面相左邊所做的判斷函式'''


def enemy_follow_left(enemy, kill_enemy):
    global check_num, num, allCount, delay_move, att_count
    if attack.x == enemy.x and attack.y == enemy.y and att_count == 4:  # 若攻擊圖片座標跟敵人座標相同
        enemy_hp[kill_enemy] -= 1  # 攻擊一下扣敵人血量
    check_num[kill_enemy] = enemy.check_collide(user, enemy.rect)
    enemy.follow_move(4, user, enemy)
    if check_num[kill_enemy] != 4:  # 當 check_num 不為4(不能隨意走動),則紀錄其值,並且建立圖
        num[kill_enemy] = check_num[kill_enemy]
        if num[kill_enemy] == 2:  # 若檢查值=2(不能向左)
            enemy.left = True  # 則方向旗標左邊為True
            enemy.right = False  # 則方向旗標右邊為False
            screen.blit(enemy.image_left[allCount // 3], (enemy.x, enemy.y))  # num=2,so blit enemy image_left
        elif num[kill_enemy] == 3:  # 若檢查值=3(不能向右)
            enemy.left = False  # 則方向旗標左邊為False
            enemy.right = True  # 則方向旗標右邊為True
            screen.blit(enemy.image_right[allCount // 3], (enemy.x, enemy.y))
        elif enemy.left:  # if left is True,blit enemy image_left
            screen.blit(enemy.image_left[allCount // 3], (enemy.x, enemy.y))
        elif enemy.right:  # if right is True,blit enemy image_right
            screen.blit(enemy.image_right[allCount // 3], (enemy.x, enemy.y))
        enemy_attack(enemy, num[kill_enemy], kill_enemy)  # 使用怪物攻擊函式

    else:  # 怪物四方位,可以任意走動,則判斷是哪個方位不能前進
        if num[kill_enemy] == 2:  # 若檢查值=2(不能向左)
            enemy.left = True  # 則方向旗標左邊為True
            enemy.right = False  # 則方向旗標右邊為False
            screen.blit(enemy.image_left[allCount // 3], (enemy.x, enemy.y))  # num=2,so blit enemy image_left
        elif num[kill_enemy] == 3:  # 若檢查值=3(不能向右)
            enemy.left = False  # 則方向旗標左邊為False
            enemy.right = True  # 則方向旗標右邊為True
            screen.blit(enemy.image_right[allCount // 3], (enemy.x, enemy.y))
        elif enemy.left:  # if left is True,blit enemy image_left
            screen.blit(enemy.image_left[allCount // 3], (enemy.x, enemy.y))
        elif enemy.right:  # if right is True,blit enemy image_right
            screen.blit(enemy.image_right[allCount // 3], (enemy.x, enemy.y))
        if delay_move[kill_enemy] == 4:  # 怪物移動延遲到4,則移動座標
            enemy.follow_move(num[kill_enemy], user, enemy)  # 則跟隨腳色座標移動
            delay_move[kill_enemy] = 0
        else:
            delay_move[kill_enemy] += 1


''' 敵人面相右邊所做的判斷函式'''


def enemy_follow_right(enemy, kill_enemy):
    global check_num, num, allCount, delay_move
    if attack.x == enemy.x and attack.y == enemy.y and att_count == 4:  # 若攻擊圖片座標跟敵人座標相同
        enemy_hp[kill_enemy] -= 1  # 攻擊一下扣敵人血量
    check_num[kill_enemy] = enemy.check_num
    enemy.follow_move(4, user, enemy)
    if check_num[kill_enemy] != 4:  # 當 check_num 不為4(不能隨意走動),則紀錄其值,並且建立圖
        num[kill_enemy] = check_num[kill_enemy]
        if num[kill_enemy] == 3:  # if num == 3 (Did not go to right)
            enemy.left = False  # left flag is False
            enemy.right = True  # right flag is True
            screen.blit(enemy.image_right[allCount // 3], (enemy.x, enemy.y))  # And blit left image
        elif num[kill_enemy] == 2:  # if num == 2 (Did not go to left)
            enemy.left = True  # left flag is True
            enemy.right = False  # right flag is False
            screen.blit(enemy.image_left[allCount // 3], (enemy.x, enemy.y))  # And blit right image
        elif enemy.left:
            screen.blit(enemy.image_left[allCount // 3], (enemy.x, enemy.y))
        elif enemy.right:
            screen.blit(enemy.image_right[allCount // 3], (enemy.x, enemy.y))
        enemy_attack(enemy, check_num[kill_enemy], kill_enemy)
    else:  # 怪物四方位,可以任意走動,則判斷是哪個方位不能前進
        if num[kill_enemy] == 3:  # if num == 3 (Did not go to right)
            enemy.left = False  # left flag is False
            enemy.right = True  # right flag is True
            screen.blit(enemy.image_right[allCount // 3], (enemy.x, enemy.y))  # And blit left image
        elif num[kill_enemy] == 2:  # if num == 2 (Did not go to left)
            enemy.left = True  # left flag is True
            enemy.right = False  # right flag is False
            screen.blit(enemy.image_left[allCount // 3], (enemy.x, enemy.y))  # And blit right image
        elif enemy.left:
            screen.blit(enemy.image_left[allCount // 3], (enemy.x, enemy.y))
        elif enemy.right:
            screen.blit(enemy.image_right[allCount // 3], (enemy.x, enemy.y))
        if delay_move[kill_enemy] == 4:
            enemy.follow_move(num[kill_enemy], user, enemy)  # 則跟隨腳色座標移動
            delay_move[kill_enemy] = 0
        else:
            delay_move[kill_enemy] += 1


def enemy_attack(enemy, num, kill_enemy):
    global face_count, user_hp
    if num == 3 or num == 2:  # 3右邊, 2左邊
        eny_attMode(enemy, kill_enemy, face_count[kill_enemy], num)
        face_count[kill_enemy] += 1  # 若在條件內,則繼續加時間
        if face_count[kill_enemy] == 8:  # 若加到8,則對玩家造成傷害
            user_hp -= 1  # 玩家生命減一
            face_count[kill_enemy] = 0  # 並且重新計算時間
    else:
        face_count[kill_enemy] = 0


# enemy攻擊圖片函式,放入怪物、元素、面相時間、判斷怪物面向的方向
def eny_attMode(enemy, kill_enemy, face_time, face_chknum):
    global eny_attLi, eny_attImTime
    if face_chknum == 2:  # 2為無法向左邊移動,則讀取左邊攻擊圖片
        if face_time >= 2:  # 若怪物面相時間大於等於3時,則載入怪物攻擊圖片
            screen.blit(eny_attLi[kill_enemy].image_left[eny_attImTime[kill_enemy] // 2],
                        (enemy.x - 48, enemy.y))  # 怪物面相左邊所以圖片x必須減掉48
            if eny_attImTime[kill_enemy] == 7:  # 7為最圖片顯示次數(4*2=8)
                eny_attImTime[kill_enemy] = 0
            else:
                eny_attImTime[kill_enemy] += 1
        else:
            eny_attImTime[kill_enemy] = 0
    elif face_chknum == 3:  # 3為無法向右邊移動,則讀取右邊攻擊圖片
        if face_time >= 2:  # 若怪物面相時間大於等於2時,則載入怪物攻擊圖片
            screen.blit(eny_attLi[kill_enemy].image_right[eny_attImTime[kill_enemy] // 2],
                        (enemy.x + 48, enemy.y))  # 怪物面相右邊所以圖片x必須加48
            if eny_attImTime[kill_enemy] == 7:  # 7為最圖片顯示次數(4*2=8)
                eny_attImTime[kill_enemy] = 0
            else:
                eny_attImTime[kill_enemy] += 1
        else:
            eny_attImTime[kill_enemy] = 0
    pg.display.update()  # 畫面持續更新


eny_atImg(enemy_rect, len(enemy_rect))  # 將各個怪物放入eny_atImg,初始化各個怪物攻擊圖片

if __name__ == "__main__":
    while running:
        clock.tick(60)
        pg.time.delay(20)  # 畫面刷新延遲
        for event in pg.event.get():  # 畫面持續顯示在螢幕上,判斷按鈕是否結束
            if event.type == KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            if event.type == pg.QUIT:
                running = False
        if user_hp == 0:  # 若玩家生命歸0,則結束遊戲
            screen.blit(gameover, (0, 0))  # 顯示結束遊戲圖片
            pg.display.update()     # 將畫面更新為結束圖片
        else:  # 若不為0,則繼續遊戲
            gameWindow()
            character()
pg.quit()
