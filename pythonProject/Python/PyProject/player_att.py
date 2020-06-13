import pygame as pg

'''設定玩家攻擊圖片'''
class Attack(pg.sprite.Sprite):
    def __init__(self, x, y, surface):
        pg.sprite.Sprite.__init__(self)
        self.x = x  # 攻擊圖片座標x為怪物x座標
        self.y = y  # 攻擊圖片座標y為怪物y座標
        self.image_left = list()
        self.image_right = list()
        self.image_data = "2D Pixel Dungeon Asset Pack/userattack/"
        for ima_num in range(0, 4):
            self.image_left.append(pg.image.load(self.image_data + f"flame_left_{ima_num}.png"))
            self.image_left[ima_num].convert()
            self.image_right.append(pg.image.load(self.image_data + f"flame_right_{ima_num}.png"))
            self.image_right[ima_num].convert()
            self.rect = self.image_left[ima_num].get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            print(self.rect)
            try:  # 若可以執行,則畫出來
                pg.draw.rect(surface, (0, 255, 0), self.rect, 1)  # 利用矩形,畫出圖片範圍大小
            except Exception as e:
                print("ERROR :", e)
