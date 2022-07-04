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
    # 子弹移动
    def move(self):
        if self.type == 'hero':
            self.y -= 1
        elif self.type == 'enemy':
            self.y += 1
    # 判断子弹是否越界
    def judge(self):
        if self.y < 0 or self.y > 500:
            return True
        else:
            return False
    # 显示子弹
    def display(self):
        self.screen.blit(self.image,(self.x,self.y))

# 我方类
class HeroPlane(BasePlane):
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
    def moveright(self):
        if self.x < 350-40:
            self.x += 1
    def moveup(self):
        if self.y > 0:
            self.y -= 1
    def movedown(self):
        if self.y < 500-40:
            self.y += 1
    # 发射子弹
    def sheBuliet(self):
        # 创建一个新的子弹对象
        newBullet = CommonBullet(self.x,self.y,self.screen,'hero')
        self.bullerList.append(newBullet)
        return newBullet

# 敌机类
class EnemyPlane(BasePlane):
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
            newBullet = CommonBullet(self.x,self.y,self.screen,'enemy')
            self.bullerList.append((newBullet))
    # 敌人随机移动
    def move(self):
        if self.direction=='right':
            self.x += 1
        elif self.direction=='left':
            self.x -= 1
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
    # # 通过set_reoeat设置连续检测按键
    # pygame.key.set_repeat(20,50)
    for event in eventlist:
        # 如果按下的是退出键
        if event.type == QUIT:
            print('退出')
            exit()
        # 如果按下的是键盘
        elif event.type == KEYDOWN:
            # # 如果按下的是a键
            # if event.key == K_a or event.key == K_LEFT:
            #     print('left')
            #     HeroObj.moveleft() # 调用移动函数
            # # 如果按下的是d键
            # elif event.key == K_d or event.key == K_RIGHT:
            #     print('right')
            #     HeroObj.moveright()
            # # 如果按下的是w键
            # elif event.key == K_w or event.key == K_UP:
            #     print('up')
            #     HeroObj.moveup()
            # # 如果按下的是s键
            # elif event.key == K_s or event.key == K_DOWN:
            #     print('down')
            #     HeroObj.movedown()
            # 如果按下的是空格键
            if event.key == K_SPACE:
                print('space')
                HeroObj.sheBuliet()
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
    # if Key_pressed[K_SPACE]:
    #     print("发射子弹")
    #     HeroObj.sheBuliet()
    if Key_pressed[K_ESCAPE]:
        print("退出")
        exit()


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
        # 碰撞检测
        # if hero.x and hero.y:

# 运行函数
if __name__ == '__main__':
    main()
