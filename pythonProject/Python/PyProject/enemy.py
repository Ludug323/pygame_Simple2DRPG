import pygame as pg


'''設定怪物初始化位置及大小'''
class Enemy(pg.sprite.Sprite):
    x = 0
    y = 0

    def __init__(self, x, y, surface, x_range, y_range):
        # 初始化怪物 : x,y(怪物初始化座標),x_range,y_range(限制怪物跑動範圍)
        pg.sprite.Sprite.__init__(self)
        self.image_right = list()  # 怪物圖片向右陣列
        self.image_left = list()  # 怪物圖片向左陣列
        self.check_num = 0
        self.right = True  # 判斷怪物面向左或右, 初始為向左
        self.left = False  # 判斷怪物面向左或右
        self.right_count = 0  # 判斷怪物 是否面向 "右" 邊 0為沒有面向此方向,1為面相此方向
        self.left_count = 0  # 判斷怪物 是否面向 "左" 邊 0為沒有面向此方向,1為面相此方向
        self.x = x  # 定義x值
        self.y = y  # 定義y值
        self.x_range = x_range
        self.y_range = y_range
        self.img_data = "2D Pixel Dungeon Asset Pack/enemy/"  # 圖片位置
        for img_ind in range(0, 4):
            self.image_right.append(pg.image.load(self.img_data + f"skeleton_right_{img_ind}.png"))  # 載入向右圖片
            self.image_right[img_ind].convert()  # 增加圖片繪製速度
            self.image_left.append(pg.image.load(self.img_data + f"skeleton_left_{img_ind}.png"))  # 載入向左圖片
            self.image_left[img_ind].convert()  # 增加圖片繪製速度
            self.rect = self.image_right[img_ind].get_rect()  # 取得目前圖片的範圍大小
            self.rect.x = self.x  # rect.x 取得現在x座標
            self.rect.y = self.y  # rect.y 取得現在y座標
            try:  # 若可以執行,則畫出來
                pg.draw.rect(surface, (0, 255, 0), self.rect, 1)  # 利用矩形,畫出圖片範圍大小
            except Exception as e:
                print("ERROR :", e)

    '''怪物針對移動位置,來改變座標位置'''
    def move(self, move_num, user, enemy):
        check_collide = Enemy.check_collide(self, user, enemy.rect)
        if check_collide == 3:  # 3為無法向右移動,檢查是否面向右邊
            if self.right_count == 1:  # 若面向右邊且碰撞條件符合,則不能前進
                check_collide = 3
            else:
                check_collide = 4  # 反之,則朝向右邊
        elif check_collide == 2:  # 2為無法向左移動,檢查是否面向左邊
            if self.left_count == 1:  # 若面向左邊且碰撞條件符合,則不能前進
                check_collide = 2
            else:  # 反之,則朝向左邊
                check_collide = 4
        try:
            '''
                move_num = 怪物隨機跑動位置(0,1,2,3)(上,下,左,右)
                self.y_range, self.x_range = 限定怪物跑動位置'''
            if check_collide == 0:
                if move_num == 1:
                    if self.y_range[0] <= self.y < self.y_range[1]:
                        self.y += 48
                elif move_num == 2:
                    if self.x_range[0] < self.x:
                        self.left = True
                        self.right = False
                        if self.left_count == 1:  # 判斷是否重複面向 左邊
                            self.x -= 48
                        else:
                            self.left_count += 1
                            self.right_count = 0
                elif move_num == 3:
                    if self.x < self.x_range[1]:
                        self.left = False
                        self.right = True
                        if self.right_count == 1:  # 判斷是否重複面向 右邊
                            self.x += 48
                        else:
                            self.right_count += 1
                            self.left_count = 0
            elif check_collide == 1:
                if move_num == 0:
                    if self.y_range[0] < self.y <= self.y_range[1]:
                        self.y -= 48
                elif move_num == 2:
                    if self.x_range[0] < self.x:
                        self.left = True
                        self.right = False
                        if self.left_count == 1:  # 判斷是否重複面向 左邊
                            self.x -= 48
                        else:
                            self.left_count += 1
                            self.right_count = 0
                elif move_num == 3:
                    if self.x < self.x_range[1]:
                        self.left = False
                        self.right = True
                        if self.right_count == 1:  # 判斷是否重複面向 右邊
                            self.x += 48
                        else:
                            self.right_count += 1
                            self.left_count = 0
            elif check_collide == 2:
                if move_num == 0:
                    if self.y_range[0] < self.y <= self.y_range[1]:
                        self.y -= 48
                elif move_num == 1:
                    if self.y_range[0] <= self.y < self.y_range[1]:
                        self.y += 48
                elif move_num == 3:
                    if self.x < self.x_range[1]:
                        self.left = False
                        self.right = True
                        if self.right_count == 1:  # 判斷是否重複面向 右邊
                            self.x += 48
                        else:
                            self.right_count += 1
                            self.left_count = 0
            elif check_collide == 3:
                if move_num == 0:
                    if self.y_range[0] < self.y <= self.y_range[1]:
                        self.y -= 48
                elif move_num == 1:
                    if self.y_range[0] <= self.y < self.y_range[1]:
                        self.y += 48
                elif move_num == 2:
                    if self.x_range[0] < self.x:
                        self.left = True
                        self.right = False
                        if self.left_count == 1:  # 判斷是否重複面向 左邊
                            self.x -= 48
                        else:
                            self.left_count += 1
                            self.right_count = 0
            else:
                if move_num == 0:
                    if self.y_range[0] < self.y <= self.y_range[1]:
                        self.y -= 48
                elif move_num == 1:
                    if self.y_range[0] <= self.y < self.y_range[1]:
                        self.y += 48
                elif move_num == 2:
                    if self.x_range[0] < self.x:
                        self.left = True
                        self.right = False
                        if self.left_count == 1:  # 判斷是否重複面向 左邊
                            self.x -= 48
                        else:
                            self.left_count += 1
                            self.right_count = 0
                elif move_num == 3:
                    if self.x < self.x_range[1]:
                        self.left = False
                        self.right = True
                        if self.right_count == 1:  # 判斷是否重複面向 右邊
                            self.x += 48
                        else:
                            self.right_count += 1
                            self.left_count = 0
        except Exception as e:
            print("error keyboard:", e)
            # print(f"x : {self.x}, y: {self.y}")
        self.rect.x = self.x  # 更新rect(x,y)　
        self.rect.y = self.y
        self.check_num = check_collide
        pg.time.delay(50)

    '''若為跟隨模式,則單純移動跟玩家相同位置'''
    def follow_move(self, num, user, enemy):
        check = Enemy.check_collide(self, user, enemy.rect)

        if num == 0:  # 向上
            self.y -= 48
        elif num == 1:  # 向下
            self.y += 48
        elif num == 2:  # 向左
            self.x -= 48
        elif num == 3:  # 向右
            self.x += 48

        self.rect.x = self.x
        self.rect.y = self.y
        self.check_num = check

    '''檢查怪物的可移動方向,來回傳相對值'''
    def check_collide(self, user, enemy):
        if enemy.bottom - 48 == user.rect.bottom and \
                enemy.right >= user.rect.left and \
                enemy.left <= user.rect.right:  # 向上
            return 0
        elif enemy.top + 48 == user.rect.top and \
                enemy.right >= user.rect.left and \
                enemy.left <= user.rect.right:  # 向下
            return 1
        elif enemy.left - 48 == user.rect.left and \
                enemy.bottom == user.rect.bottom and \
                enemy.top == user.rect.top:  # 向左
            return 2
        elif enemy.right + 48 == user.rect.right and \
                enemy.bottom == user.rect.bottom and \
                enemy.top == user.rect.top:  # 向右
            return 3
        else:
            return 4
