import pygame
import random
import time
from pygame.locals import *

# 创建我方类
class HeroPlane(object):
    def __init__(self,screen):
        '''
        初始化函数
        :param screen: 窗口
        '''
        # 飞机的默认位置
        self.x = 150
        self.y = 450
        # 存储飞机子弹的列表
        self.bullerList = []
        # 飞机的血量
        self.hp = 100
        # 设置要显示内容的窗口
        self.screen = screen
        # 生成飞机的图片对象
        self.imageName = './feiji/hero.png'
        self.image = pygame.image.load(self.imageName)
    # 上下左右移动
    def moveleft(self):
        if self.x > 0:
            self.x -= 10
    def moveright(self):
        if self.x < 350-40:
            self.x += 10
    def moveup(self):
        if self.y > 0:
            self.y -= 10
    def movedown(self):
        if self.y < 500-40:
            self.y += 10
    # 发射子弹
    def sheBuliet(self):
        # 创建一个新的子弹对象
        newBullet = Bullet(self.x,self.y,self.screen)
        self.bullerList.append(newBullet)
    # 飞机和子弹在窗口中的显示
    def display(self):
        # 需要删除的子弹
        needDelitemList = []
        # 检测越界的子弹
        for item in self.bullerList:
            if item.judge():
                needDelitemList.append(item)
        # 删除越界的子弹
        for i in needDelitemList:
            self.bullerList.remove(i)
        # 刷新子弹
        for bullet in self.bullerList:
            bullet.display() # 显示子弹位置
            bullet.moveup() # 移动子弹的位置
        # 显示飞机
        if self.hp > 0:
            self.screen.blit(self.image,(self.x,self.y))
        else:
            print('游戏结束')
            exit()
# 创建敌机类
class EnemyPlane(object):
    def __init__(self,screen):
        # 默认设置一个方向
        self.direction = 'right'
        self.screen = screen
        # 飞机的默认位置
        self.x = 160
        self.y = 0
        # 存储飞机子弹的列表
        self.bullerList = []
        # 飞机的血量
        self.hp = 100
        # 设置要显示内容的窗口
        self.screen = screen
        # 生成飞机的图片对象
        self.imageName = './feiji/enemy0.png'
        self.image = pygame.image.load(self.imageName)
    def display(self):
        # 需要删除的子弹
        needDelitemList = []
        # 检测越界的子弹
        for item in self.bullerList:
            if item.judge():
                needDelitemList.append(item)
        # 删除越界的子弹
        for i in needDelitemList:
            self.bullerList.remove(i)
        # 刷新子弹
        for EnemyBullet in self.bullerList:
            EnemyBullet.display()  # 显示子弹位置
            EnemyBullet.movedown()  # 移动子弹的位置
        # 显示飞机
        if self.hp > 0:
            self.screen.blit(self.image, (self.x, self.y))
        else:
            print('游戏结束')
            exit()
    # 敌人随机发射子弹
    def sheBullet(self):
        num = random.randint(1,100)
        if num==3 :
            newBullet = EnemyBullet(self.x,self.y,self.screen)
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
# 我方子弹类
class Bullet(object):
    def __init__(self,x,y,screen):
        self.x = x+13
        self.y = y-20
        self.screen = screen
        self.imgage = pygame.image.load('./feiji/bullet.png')
    # 子弹显示
    def display(self):
        self.screen.blit(self.imgage,(self.x,self.y))
    # 子弹移动
    def moveup(self):
        self.y -= 1
    def movedown(self):
        self.y += 1
    # 判断子弹是否越界
    def judge(self):
        if self.y < 0 or self.y > 450:
            return True
        else:
            return False
# 敌方子弹类
class EnemyBullet(object):
    def __init__(self,x,y,screen):
        self.x = x
        self.y = y+10
        self.screen = screen
        self.imgage = pygame.image.load('./feiji/bullet1.png')
    # 子弹显示
    def display(self):
        self.screen.blit(self.imgage,(self.x,self.y))
    # 子弹移动
    def moveup(self):
        self.y -= 1
    def movedown(self):
        self.y += 1
    # 判断子弹是否越界
    def judge(self):
        if self.y < 0 or self.y > 480:
            return True
        else:
            return False
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
        # 如果按下的是键盘
        elif event.type == KEYDOWN:
            # 如果按下的是a键
            if event.key == K_a or event.key == K_LEFT:
                print('left')
                HeroObj.moveleft() # 调用移动函数
            # 如果按下的是d键
            elif event.key == K_d or event.key == K_RIGHT:
                print('right')
                HeroObj.moveright()
            # 如果按下的是w键
            elif event.key == K_w or event.key == K_UP:
                print('up')
                HeroObj.moveup()
            # 如果按下的是s键
            elif event.key == K_s or event.key == K_DOWN:
                print('down')
                HeroObj.movedown()
            # 如果按下的是空格键
            elif event.key == K_SPACE:
                print('space')
                HeroObj.sheBuliet()
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
# 运行函数
if __name__ == '__main__':
    main()
