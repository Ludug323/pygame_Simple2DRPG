import pygame as pg
from pygame.locals import *


'''設定玩家座標以及大小物件'''
class Player(pg.sprite.Sprite):
    # 宣告全域變數初始化
    x = 0
    y = 0
    img_data = ""

    '''定義玩家所需的初始值'''
    def __init__(self, x, y, surface, enemy_rect):
        pg.sprite.Sprite.__init__(self)
        self.image_right = list()  # 角色圖片陣列
        self.image_left = list()
        self.move_count = False
        self.right = True  # 判斷角色面向左或右, 初始為向左
        self.left = False   # 判斷角色面向左或右
        self.right_count = 0  # 判斷角色 是否面向 "右" 邊 0為沒有面向此方向,1為面相此方向
        self.left_count = 0    # 判斷角色 是否面向 "左" 邊 0為沒有面向此方向,1為面相此方向
        self.x = x  # 定義x值
        self.y = y  # 定義y值
        self.enemy_rect = enemy_rect
        self.img_data = "2D Pixel Dungeon Asset Pack/user/"  # 圖片位置
        for img_ind in range(0, 4):
            self.image_right.append(pg.image.load(self.img_data + f"img_right_{img_ind}.png"))  # 載入向"右"圖片
            self.image_right[img_ind].convert()  # 增加圖片繪製速度
            self.image_left.append(pg.image.load(self.img_data + f"img_left_{img_ind}.png"))  # 載入向"左"圖片
            self.image_left[img_ind].convert()  # 增加圖片繪製速度
            self.rect = self.image_right[img_ind].get_rect()  # 取得目前圖片的範圍大小
            self.rect.x = self.x  # rect.x 取得現在x座標
            self.rect.y = self.y  # rect.y 取得現在y座標
            try:  # 若可以執行,則畫出來
                pg.draw.rect(surface, (0, 255, 0), self.rect, 1)  # 利用矩形,畫出圖片範圍大小
            except Exception as e:
                print("ERROR :", e)

    '''玩家判斷可移動位置,而改變座標'''
    def move(self, kill_flag):
        keyboard = pg.key.get_pressed()  # 取得鍵盤按鍵
        if kill_flag[0] != 0:
            check_collide_1 = Player.check_collide(self, self.rect, self.enemy_rect, 0)  # 回傳碰撞數字(0,4)
            '''檢查腳色面向位置,並且給於碰撞判定'''
            if check_collide_1 == 3:   # 檢查是否面向右邊
                if self.right_count == 1:  # 若面向右邊且碰撞條件符合,則不能前進
                    check_collide_1 = 3
                else:
                    check_collide_1 = 4    # 反之,則朝向右邊
            elif check_collide_1 == 2:  # 檢查是否面向左邊
                if self.left_count == 1:  # 若面向左邊且碰撞條件符合,則不能前進
                    check_collide_1 = 2
                else:                       # 反之,則朝向左邊
                    check_collide_1 = 4
        else:
            check_collide_1 = 4
        if kill_flag[1] != 0:
            check_collide_2 = Player.check_collide(self, self.rect, self.enemy_rect, 1)  # 回傳碰撞數字(0,4)
            if check_collide_2 == 3:
                if self.right_count == 1:
                    check_collide_2 = 3
                else:
                    check_collide_2 = 4
            elif check_collide_2 == 2:
                if self.left_count == 1:
                    check_collide_2 = 2
                else:
                    check_collide_2 = 4
        else:
            check_collide_2 = 4

        check_collGroup = [check_collide_1, check_collide_2]
        try:
            if check_collGroup == [4, 4]:
                Player.move_direction(self, keyboard, [1, 1, 1, 1])
            else:
                # 判斷左邊怪物位置
                if check_collGroup[0] == 0:  # 若為0,則無法向上   #上,下,左,右
                    Player.move_direction(self, keyboard, [0, 1, 1, 1])
                elif check_collGroup[0] == 1:   # 若為1,則無法向下
                    Player.move_direction(self, keyboard, [1, 0, 1, 1])
                elif check_collGroup[0] == 2:    # 若為2,則無法向右
                    Player.move_direction(self, keyboard, [1, 1, 0, 1])
                elif check_collGroup[0] == 3:    # 若為3,則無法向左
                    Player.move_direction(self, keyboard, [1, 1, 1, 0])
                # 判斷上面怪物位置
                if check_collGroup[1] == 0:  # 若為0,則無法向上   #上,下,左,右
                    Player.move_direction(self, keyboard, [0, 1, 1, 1])
                elif check_collGroup[1] == 1:  # 若為1,則無法向下
                    Player.move_direction(self, keyboard, [1, 0, 1, 1])
                elif check_collGroup[1] == 2:  # 若為2,則無法向右
                    Player.move_direction(self, keyboard, [1, 1, 0, 1])
                elif check_collGroup[1] == 3:  # 若為3,則無法向左
                    Player.move_direction(self, keyboard, [1, 1, 1, 0])

        except Exception as e:
            print("error keyboard:", e)
        # print(f"x : {self.x}, y: {self.y}")
        self.rect.x = self.x  # 更新rect(x,y)　
        self.rect.y = self.y
        pg.time.delay(50)  # 鍵盤回饋延遲

    '''判斷角色與怪物是否碰撞'''
    def check_collide(self, user, enemy, enemy_num):
        if user.bottom - 48 == enemy[enemy_num].rect.bottom and \
                user.right >= enemy[enemy_num].rect.left and \
                user.left <= enemy[enemy_num].rect.right:  # 向上
            return 0
        elif user.top + 48 == enemy[enemy_num].rect.top and \
                user.right >= enemy[enemy_num].rect.left and \
                user.left <= enemy[enemy_num].rect.right:  # 向下
            return 1
        elif user.left - 48 == enemy[enemy_num].rect.left and \
                user.bottom == enemy[enemy_num].rect.bottom and \
                user.top == enemy[enemy_num].rect.top:  # 向左
            return 2
        elif user.right + 48 == enemy[enemy_num].rect.right and \
                user.bottom == enemy[enemy_num].rect.bottom and \
                user.top == enemy[enemy_num].rect.top:  # 向右
            return 3
        else:
            return 4

    '''得到方向回傳值,0為不可往前,1為可移動方向'''
    def move_direction(self, keyboard, num):  # 正常動作
        time = 0
        if keyboard[K_a] and self.left_count == 1:  # 若按下a鍵而且腳色是面向左邊,則往前移動
            self.move_count = True                  # move_count為面相方向是否跟按鍵相同
        elif keyboard[K_d] and self.right_count == 1:  # 若按下d鍵而且腳色是面向左邊,則往前移動
            self.move_count = True
        elif keyboard[K_w] or keyboard[K_s]:  # 若是按ｗｓ鍵,則move_count為True
            self.move_count = True
        else:
            self.move_count = False
        '''left_count and right_count 來判斷玩家面相是否跟按鍵相同,若相同則改變座標,若不同則改變面向'''
        if num == [1, 1, 1, 1]:  # 四個方向都可以前進
            if keyboard[K_w]:  # 若按W(往上)
                Player.time_delay(self, time)
                if 294 < self.y <= 390:
                    self.y -= 48
                elif self.y > 54:
                    if 267 <= self.x <= 411:
                        self.y -= 48
            elif keyboard[K_s]:  # 若按S(往下)
                Player.time_delay(self, time)
                if 294 <= self.y < 390:
                    self.y += 48
                elif self.y < 630:
                    if 267 <= self.x <= 411:
                        self.y += 48
            elif keyboard[K_a]:  # 若按A(往左)
                Player.time_delay(self, time)
                self.left = True
                self.right = False
                if self.left_count == 1:
                    if 267 < self.x <= 411:
                        self.x -= 48
                    elif self.x > 27:
                        if 294 <= self.y <= 390:
                            self.x -= 48
                else:
                    self.left_count += 1
                    self.right_count = 0
            elif keyboard[K_d]:  # 若按D(往右)
                Player.time_delay(self, time)
                self.left = False
                self.right = True
                if self.right_count == 1:
                    if 267 <= self.x < 411:
                        self.x += 48
                    elif self.x < 651:
                        if 294 <= self.y <= 390:
                            self.x += 48
                else:
                    self.right_count += 1
                    self.left_count = 0
        elif num == [0, 1, 1, 1]:  # 上方無法前進
            if keyboard[K_s]:  # 若按S(往下)
                Player.time_delay(self, time)
                if 294 <= self.y < 390:
                    self.y += 48
                elif self.y < 630:
                    if 267 <= self.x <= 411:
                        self.y += 48
            elif keyboard[K_a]:  # 若按A(往左)
                Player.time_delay(self, time)
                self.left = True
                self.right = False
                if self.left_count == 1:
                    if 267 < self.x <= 411:
                        self.x -= 48
                    elif self.x > 27:
                        if 294 <= self.y <= 390:
                            self.x -= 48
                else:
                    self.left_count += 1
                    self.right_count = 0
            elif keyboard[K_d]:  # 若按D(往右)
                Player.time_delay(self, time)
                self.left = False
                self.right = True
                if self.right_count == 1:
                    if 267 <= self.x < 411:
                        self.x += 48
                    elif self.x < 651:
                        if 294 <= self.y <= 390:
                            self.x += 48
                else:
                    self.right_count += 1
                    self.left_count = 0

        elif num == [1, 0, 1, 1]:  # 下方無法前進
            if keyboard[K_w]:  # 若按W(往上)
                Player.time_delay(self, time)
                if 294 < self.y <= 390:
                    self.y -= 48
                elif self.y > 54:
                    if 267 <= self.x <= 411:
                        self.y -= 48
            elif keyboard[K_a]:  # 若按A(往左)
                Player.time_delay(self, time)
                self.left = True
                self.right = False
                if self.left_count == 1:
                    if 267 < self.x <= 411:
                        self.x -= 48
                    elif self.x > 27:
                        if 294 <= self.y <= 390:
                            self.x -= 48
                else:
                    self.left_count += 1
                    self.right_count = 0
            elif keyboard[K_d]:  # 若按D(往右)
                Player.time_delay(self, time)
                self.left = False
                self.right = True
                if self.right_count == 1:
                    if 267 <= self.x < 411:
                        self.x += 48
                    elif self.x < 651:
                        if 294 <= self.y <= 390:
                            self.x += 48
                else:
                    self.right_count += 1
                    self.left_count = 0
        elif num == [1, 1, 0, 1]:  # 左邊無法前進
            if keyboard[K_w]:  # 若按W(往上)
                Player.time_delay(self, time)
                if 294 < self.y <= 390:
                    self.y -= 48
                elif self.y > 54:
                    if 267 <= self.x <= 411:
                        self.y -= 48
            elif keyboard[K_s]:  # 若按S(往下)
                Player.time_delay(self, time)
                if 294 <= self.y < 390:
                    self.y += 48
                elif self.y < 630:
                    if 267 <= self.x <= 411:
                        self.y += 48
            elif keyboard[K_d]:  # 若按D(往右)
                Player.time_delay(self, time)
                self.left = False
                self.right = True
                if self.right_count == 1:
                    if 267 <= self.x < 411:
                        self.x += 48
                    elif self.x < 651:
                        if 294 <= self.y <= 390:
                            self.x += 48
                else:
                    self.right_count += 1
                    self.left_count = 0
        elif num == [1, 1, 1, 0]:  # 右邊無法前進
            if keyboard[K_w]:  # 若按W(往上)
                Player.time_delay(self, time)
                if 294 < self.y <= 390:
                    self.y -= 48
                elif self.y > 54:
                    if 267 <= self.x <= 411:
                        self.y -= 48
            elif keyboard[K_s]:  # 若按S(往下)
                pg.time.delay(40)
                if 294 <= self.y < 390:
                    self.y += 48
                elif self.y < 630:
                    if 267 <= self.x <= 411:
                        self.y += 48
            elif keyboard[K_a]:  # 若按A(往左)
                Player.time_delay(self, time)
                self.left = True
                self.right = False
                if self.left_count == 1:
                    if 267 < self.x <= 411:
                        self.x -= 48
                    elif self.x > 27:
                        if 294 <= self.y <= 390:
                            self.x -= 48
                else:
                    self.left_count += 1
                    self.right_count = 0

    def time_delay(self, time):
        return pg.time.delay(time)
