import pygame
import random
import time
from pygame.locals import *

# 飞机类
class BasePlane(object):
    def __init__(self,screen,hp,x,y,imagePath):
        '''
        :param screen: 主窗口对象
        :param imageName: 加载的图片
        '''
        self.screen = screen #主窗口
        self.image = pygame.image.load(imagePath) #加载的图片
        self.bullerList = [] #存储所有的子弹
        self.hp = hp
        self.x = x
        self.y = y
    def display(self):
        # 显示飞机
        if self.hp > 0:
            self.screen.blit(self.image, (self.x, self.y))
        else:
            print('游戏结束')
            exit()
        needDelitemList = [] # 需要删除的子弹
        # 检测越界的子弹
        for item in self.bullerList:
            if item.judge():
                needDelitemList.append(item)
        # 删除越界的子弹
        for i in needDelitemList:
            self.bullerList.remove(i)

# 子弹类
class CommonBullet(object):
    def __init__(self,x,y,screen,BulletType):
        self.screen = screen
        self.type = BulletType
        if self.type == 'hero':
            self.x = x+13
            self.y = y-20
            self.imagePath = './feiji/bullet.png'
        elif self.type == 'enemy':
            self.x = x
            self.y = y+10
            self.imagePath = './feiji/bullet1.png'
        self.image = pygame.image.load(self.imagePath)
    # 判断子弹是否越界
    def judge(self):
        if self.y < 0 or self.y > 500:
            return True
        else:
            return False
    # 显示子弹
    def display(self):
        self.screen.blit(self.image,(self.x,self.y))

# 我方子弹
class HeroBullet(CommonBullet):
    bulist1 = [0,0]
    # 子弹移动
    def move(self):
        self.y -= 1
        HeroBullet.bulist1.append(self.x)
        HeroBullet.bulist1.append(self.y)
        del HeroBullet.bulist1[:2]
        print('我方子弹坐标{}'.format(HeroBullet.bulist1))

# 敌方子弹
class EnemyBullet(CommonBullet):
    bulist2 = [0,0]
    # 子弹移动
    def move(self):
        self.y += 1
        EnemyBullet.bulist2.append(self.x)
        EnemyBullet.bulist2.append(self.y)
        del EnemyBullet.bulist2[:2]
        print('敌方子弹坐标{}'.format(EnemyBullet.bulist2))
# 我方类
class HeroPlane(BasePlane):
    herolist = [0,0]
    def __init__(self,screen):
        # 调用父类的初始化函数
        super().__init__(screen,100,150,450,'./feiji/hero.png')
    def display(self):
        super(HeroPlane, self).display()
        # 刷新子弹
        for bullet in self.bullerList:
            bullet.display()  # 显示子弹位置
            bullet.move()  # 移动子弹的位置
    # 上下左右移动
    def moveleft(self):
        if self.x > 0:
            self.x -= 1
            HeroPlane.herolist.append(self.x)
            HeroPlane.herolist.append(self.y)
            del HeroPlane.herolist[:2]
    def moveright(self):
        if self.x < 350-40:
            self.x += 1
            HeroPlane.herolist.append(self.x)
            HeroPlane.herolist.append(self.y)
            del HeroPlane.herolist[:2]
    def moveup(self):
        if self.y > 0:
            self.y -= 1
            HeroPlane.herolist.append(self.x)
            HeroPlane.herolist.append(self.y)
            del HeroPlane.herolist[:2]
    def movedown(self):
        if self.y < 500-40:
            self.y += 1
            HeroPlane.herolist.append(self.x)
            HeroPlane.herolist.append(self.y)
            del HeroPlane.herolist[:2]
    # 发射子弹
    def sheBuliet(self):
        # 创建一个新的子弹对象
        newBullet = HeroBullet(self.x,self.y,self.screen,'hero')
        self.bullerList.append(newBullet)

# 敌机类
class EnemyPlane(BasePlane):
    enemylist = [0,0]
    def __init__(self,screen):
        super().__init__(screen,100,160,0,'./feiji/enemy0.png')
        # 默认设置一个方向
        self.direction = 'right'
    def display(self):
        super(EnemyPlane, self).display()
        # 刷新子弹
        for EnemyBullet in self.bullerList:
            EnemyBullet.display()  # 显示子弹位置
            EnemyBullet.move()  # 移动子弹的位置
    # 敌人随机发射子弹
    def sheBullet(self):
        num = random.randint(1,100)
        if num==3 :
            newBullet = EnemyBullet(self.x,self.y,self.screen,'enemy')
            self.bullerList.append((newBullet))
    # 敌人自动移动
    def move(self):
        if self.direction=='right':
            self.x += 1
            EnemyPlane.enemylist.append(self.x)
            EnemyPlane.enemylist.append(self.y)
            del EnemyPlane.enemylist[:2]
        elif self.direction=='left':
            self.x -= 1
            EnemyPlane.enemylist.append(self.x)
            EnemyPlane.enemylist.append(self.y)
            del EnemyPlane.enemylist[:2]
        if self.x >= 350-20:
            self.direction='left'
        elif self.x <= 0:
            self.direction='right'

# 键盘检测函数
def key_control(HeroObj):
    '''
    定义实现键盘检测的函数
    :param HeroObj:控制检测的对象
    :return:
    '''
    # 获取键盘事件
    eventlist = pygame.event.get()
    for event in eventlist:
        # 如果按下的是退出键
        if event.type == QUIT:
            print('退出')
            exit()
    pygame.key.set_repeat(100, 100)
    Key_pressed = pygame.key.get_pressed()
    if Key_pressed[K_UP]:
        print("上")
        HeroObj.moveup()  # 调用移动函数
    if Key_pressed[K_DOWN]:
        print("下")
        HeroObj.movedown()  # 调用移动函数
    if Key_pressed[K_LEFT]:
        print("左")
        HeroObj.moveleft()  # 调用移动函数
    if Key_pressed[K_RIGHT]:
        print("右")
        HeroObj.moveright()  # 调用移动函数
    if Key_pressed[K_SPACE]:
        print('空格')
        HeroObj.sheBuliet()
    if Key_pressed[K_ESCAPE]:
        print("退出")
        exit()

# 碰撞检测
def Pk(hero,enemy):
    if HeroBullet.bulist1 == EnemyPlane.enemylist:
        enemy.hp -= 10
        pass
    if EnemyBullet.bulist2 == HeroPlane.herolist:
        hero.hp -= 10
        pass
    pass

# 游戏主函数
def main():
    # 创建一个窗口
    screen = pygame.display.set_mode((350,500),depth=32)
    # 设置窗口标题
    pygame.display.set_caption("飞机大战")
    # 创建背景图片对象 './'表示当前目录
    background = pygame.image.load('./feiji/background.png')
    # 添加音乐
    pygame.mixer.init() # 初始化
    pygame.mixer.music.load('./feiji/background.mp3')
    pygame.mixer.music.set_volume(0.5) # 0.5是音量大小
    pygame.mixer.music.play(-1) # -1表示无限循环
    # 创建一个飞机对象
    hero = HeroPlane(screen)
    # 创建一个敌机对象
    enemyplane = EnemyPlane(screen)

    while True:
        # 显示背景图像
        screen.blit(background,(0,0))
        # 显示玩家飞机
        hero.display()
        # 显示敌人飞机
        enemyplane.display()
        enemyplane.move() #移动
        enemyplane.sheBullet() #发射子弹
        # 调用键盘检测函数
        key_control(hero)
        # 更新显示的内容
        pygame.display.update()
        print('玩家的血量:{}'.format(hero.hp))
        print('玩家的坐标:{},{}'.format(hero.x,hero.y))
        print('敌人的血量:{}'.format(enemyplane.hp))
        print('敌人的坐标:{},{}'.format(enemyplane.x, enemyplane.y))
        Pk(hero,enemyplane)

# 运行函数
if __name__ == '__main__':
    main()
