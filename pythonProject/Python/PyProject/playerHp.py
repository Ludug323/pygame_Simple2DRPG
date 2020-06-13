import pygame as pg

'''設定玩家血量條圖片'''
class PlayerHp(pg.sprite.Sprite):
    def __init__(self, x, y, surface):
        pg.sprite.Sprite.__init__(self)
        self.x = x  # 圖片載入x座標
        self.y = y  # 圖片載入y座標
        self.image = list()
        self.image_data = "playhp\\"  # 圖片放置處
        for img_num in range(6):
            self.image.append(pg.image.load(self.image_data + f"playerhp_{img_num}.png"))
            self.image[img_num].convert()
            self.rect = self.image[img_num].get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
