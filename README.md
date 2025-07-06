## 外星飞机大战

---

这个代码在《Python编程：从入门到实践》这本书里又详细介绍，这里只是将其进行了一些简单的改变，使其效果更好

在写代码之前，需要先下载`Pygame`库，使用`pip install pygame`命令，可以使用国内的镜像下载的会更快，下面这些是国内比较常用的镜像源，使用镜像源时需要在镜像源前加上`-i` 

|              | 镜像源                                   |
| ------------ | ---------------------------------------- |
| 豆瓣         | http://pypi.douban.com/simple            |
| 清华大学     | https://pypi.tuna.tsinghua.edu.cn/simple |
| 阿里云       | https://mirrors.aliyun.com/pypi/simple   |
| 中国科技大学 | https://pypi.mirrors.ustc.edu.cn/simple  |

```bash
pip install pygame -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### pygame库简单介绍

pygame时一个用于创建游戏的开源的Python库，它提供了一系列的模块用来处理游戏开发中的常见任务，比如图像显示，声音播放，事件处理等各种任务，一下是一些pygame模块中比较常用的方法：

| 方法             | 实现效果                                                     |
| ---------------- | ------------------------------------------------------------ |
| `pygame.display` | 用于管理显示屏幕，创建窗口，控制窗口的尺寸和标题，以及更新屏幕内容。 |
| `pygame.draw`    | 提供了基本的绘图函数，可以在屏幕上绘制线条，矩形，圆形等。   |
| `pygame.event`   | 用于处理事件，比如键盘输入，鼠标的移动和点击等。             |
| `pygame.image`   | 用于加载和处理图像，支持各种图像格式，如JPG，PNG，BMP等。    |
| `pygame.key`     | 提供了键盘按键的常量和一些键盘相关的函数，如K_SPACE(空格)，K_RIGHT(→)等。 |
| `pygame.time`    | 提供了时间相关的函数，如设置帧率、获取时间等。               |
| `pygame.font`    | 用于创建和渲染文本。                                         |
| `pygame.quit`    | 安全退出 Pygame。                                            |
| `pygame.sprite`  | 提供了精灵类和精灵组，用于组织和管理游戏中的多个对象。       |

接下来就开始编写代码

首先，我们需要先重建一个名为`alien_invasion.py`的主程序，然后将pygame模块导入

`alien_invasion.py` 

```python
import sys
import pygame

def run_game():
    # 初始化游戏窗口
    pygame.init() 
    # 设置游戏窗口大小
    screen=pygame.display.set_mode((1200,800))
    # 设置游戏窗口名字
    pygame.display.set_caption('外星飞机大战') 
    # 设置游戏背景
    background_image=pygame.image.load('外太空(游戏背景图).png') 
    # 开始游戏主循环
    while True:
        # 监视键盘和鼠标事件
        for event in pygame.event.get(): 
            if event.type==pygame.QUIT:
                # 当玩家点击游戏窗口关闭按钮时，调用sys.exit()退出游戏
                sys.exit() 
        # 游戏背景图
        screen.blit(background_image,(0,0))        
        # 让最近绘制的屏幕可见
        pygame.display.flip() 
     
run_game()
```

运行此代码，会出现带有背景图的游戏窗口

为了让主程序看起来更加简单明了，我们需要编写一个`setting.py`的模块，将所有的游戏设置放在此模块中，因为后期如果需要添加新功能，可以避免在代码中到处添加设置，在项目增大和修改游戏设置时只需修改在`setting.py`文件中的代码即可

`setting.py`

```py
class Settings():
    """存储游戏的所有设置"""
    
    def __init__(self):
        """初始化游戏设置"""
        # 屏幕设置
        self.screen_width=1200
        self.screen_hight=800
```

然后只需将`setting.py`模块导入到主程序中，再将主程序中相关代码修改即可

`alien_invasion.py`

```py
import sys
import pygame

form setting import Settings

def run_game():
    # 初始化游戏窗口
    pygame.init() 
    # 初始化设置对象St
    St=Settings()
    # 设置游戏窗口大小
    screen=pygame.display.set_mode((St.screen_width,St.screen_hight))
    # 设置游戏窗口名字
    pygame.display.set_caption('外星飞机大战') 
    # 设置游戏背景
    background_image=pygame.image.load('外太空(游戏背景图).png') 
    # 开始游戏主循环
    while True:
        # 监视键盘和鼠标事件
        for event in pygame.event.get(): 
            if event.type==pygame.QUIT:
                # 当玩家点击游戏窗口关闭按钮时，调用sys.exit()退出游戏
                sys.exit() 
        # 游戏背景图
        screen.blit(background_image,(0,0))
        # 让最近绘制的屏幕可见
        pygame.display.flip() 
     
run_game()
```

### 创建飞船

创建一个`ship.py`文件，编写`Ship`类用来管理飞船的行为

在这里我们需要用到`get_rect()`来获取战斗机图像的外接矩形，因为战斗机图像不是一个规则图形，所以用其外接矩形代替可以更加方便，在后续处理子弹与外星人战斗机的碰撞事件时，只需要判断子弹的外接矩形和敌人战斗机的外接矩形是否有重叠部分即可

`ship.py`

```py
import pygame


class Ship():
    """初始化飞船并设置飞船的开始位置"""
    def __init__(self,screen):
        self.screen = screen
    
        # 加载战斗机图像并获取其外接矩形
        self.image = pygame.image.load('战斗机.png')
        self.rect = self.image.get_rect()
        self.rect_screen = screen.get_rect()
    
        # 将战斗机的起始位置放置在游戏窗口底部中间
        self.rect.centerx = self.rect_screen.centerx
        self.rect.bottom = self.rect_screen.bottom

    def blitme(self):
        """在指定位置绘制战斗机"""
        self.screen.blit(self.image, self.rect)
```

我们将把战斗机放在游戏窗口底部中央，为此，首先将表示游戏窗口的矩形信息存储在`self.screen_rect` 中，再将`self.rect.centerx`（战斗机外接矩形中心的x 坐标）设置为表示游戏窗口的矩形属性`centerx`，并将`self.rect.bottom` （战斗机下边缘的y 坐标）设置为表示游戏窗口的矩形属性bottom ，Pygame将使用这些rect 属性来放置战斗机图像， 使其与屏幕下边缘对齐并水平居中。

接下来就是在游戏窗口上绘制战斗机，将`ship`模块导入到主程序

`alien_invasion.py`

```py
import sys
import pygame

from setting import Settings
from ship import Ship

def run_game():
    # 初始化游戏窗口
    pygame.init() 
    # 初始化设置对象St
    St=Settings()
    --此处代码省略--
    # 创建战斗机实例
    Sp=Ship(screen)
    # 开始游戏主循环
    while True:
        --此处代码省略--
        # 绘制战斗机
        Sp.blitme()
        # 让最近绘制的屏幕可见
        pygame.display.flip() 
     
run_game()
```

到这里可以先试着运行看是否可以，效果如下：

![image-20241013195741545](./image-20241013195741545.png)

如果感觉窗口太大，可以在`setting.py`中调整游戏窗口的宽高以达到合适的大小

### 创建`game_function`模块

在一些比较大的项目里面我们需要在添加新代码前重构既有代码，这样可以简化既有的代码，并且在后续添加新功能时更加方便，而且可以避免主程序太长，创建一个`game_function.py`文件，用来管理各种事件代码

我们先将主程序中管理键盘和鼠标的代码和更新屏幕的代码放进去，再将此模块导入主程序并重新命名为`g_f`

`game_function.py`

```py
import sys
import pygame

def check_events():
    """监视键盘和鼠标事件"""
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            # 当玩家点击游戏窗口关闭按钮时，调用sys.exit()退出游戏
            sys.exit()
def update_screen(Sp):
    """更新屏幕"""
    # 绘制战斗机
    Sp.blitme()
    # 让最近绘制的屏幕可见
    pygame.display.flip() 
```

`alien_invasion.py`

```python
import pygame
import game_function as g_f
from setting import Settings
from ship import Ship

def run_game():
    --此处代码省略--
    # 开始游戏主循环
    while True:
        # 鼠标和键盘事件
        g_f.check_events()
        # 更新屏幕
        g_f.update_screen(Sp)
     
run_game()
```

我们可以看出主程序的代码变得更加简介明了，注意：`update_screen()`需要进行传参，后面每一次修改代码都可能会进行传参，否则会报错

### 战斗机移动

下来我们开始实现让战斗机进行左右移动，这里我们需要响应键盘，因此我们需要在`check_events()`函数中添加响应键盘按键的代码

`game_function.py`

```py
import sys
import pygame


def check_events(Sp):
    """监视键盘和鼠标事件"""
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            # 当玩家点击游戏窗口关闭按钮时，调用sys.exit()退出游戏
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            # 当检测到玩家按下右箭头时，战斗机向右移动
            if event.key==pygame.K_RIGHT:
                Sp.rect.centerx+=1
            # 当检测到玩家按下左箭头时，战斗机向左移动
            elif event.key==pygame.K_LEFT:
                Sp.rect.centerx-=1
                
--此处代码省略--
```

当玩家按下右箭头时，战斗机的外接矩形中心坐标加1，则实现向右运动，同时要在`check_events()`中传入Sp参数，**_切记主程序中函数参数也要保持一致_**，运行主程序，按下左右箭头，发现战斗机可以初步实现左右移动

虽然战斗机现在可以左右移动，但是我们发现按一下移动一下，想要实现按住左右键不放就一直移动的效果，需要结合使用`KEYDOWN`和`KEYUP`事件来检查按键的按下和放开，同时命名一个`moving_right`来标志是否向右移动，如果其为`True`，则向右移动，`False`为不动，因为这属于战斗机的属性，所以我们将其放在`ship.py`文件中

`ship.py`

```py
import pygame


class Ship(object):
    """初始化飞船并设置飞船的开始位置"""
    def __init__(self,screen):
        self.screen = screen
        --此处代码省略--
        # 战斗机是否向右运动
        self.moving_right = False
        # 战斗机是否向左运动
        self.moving_left = False
    def blitme(self):
    """在指定位置绘制战斗机"""
        self.screen.blit(self.image, self.rect)
        
    def update(self):
        """更新战斗机的位置"""
        if self.moving_right:
            self.rect.centerx+=1
        elif self.moving_left:
            self.rect.centerx-=1
```

`game_inversion.py`

```py
import sys
import pygame


def check_events(Sp):
    """监视键盘和鼠标事件"""
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            # 当玩家点击游戏窗口关闭按钮时，调用sys.exit()退出游戏
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            # 当检测到玩家按下右箭头时，战斗机向右移动
            if event.key==pygame.K_RIGHT:
                Sp.moving_right=True
            # 当检测到玩家按下左箭头时，战斗机向左移动
            elif event.key==pygame.K_LEFT:
                Sp.moving_left=True
        elif event.type == pygame.KEYUP:
            # 当检测到玩家放开右箭头时，战斗机停止移动
            if event.key == pygame.K_RIGHT:
                Sp.moving_right = False
            # 当检测到玩家放开左箭头时，战斗机停止移动
            elif event.key == pygame.K_LEFT:
                Sp.moving_left = False

def update_screen(Sp):
   --此处代码省略--

```

最后在主程序中调用`update()`函数来更新战斗机位置

`alien_invasion.py`

```py
--此处代码省略--
    # 开始游戏主循环
    while True:
        g_f.check_events(Sp)
        # 更新屏幕
        g_f.update_screen(Sp)
        # 更新战斗机位置
        Sp.update()
        # 游戏背景图
        screen.blit(background_image, (0, 0))

run_game()
```

运行主程序，按下左右键，此时我们发现如果一直按住左或者右箭头，我们发现战斗机会跑出游戏窗口外面，想要解决这个问题，我们只需要在`update()`函数添加一个条件

`ship.py`

```py
--此处代码省略--        
    def update(self):
        """更新战斗机的位置"""
        # 当moving_right为True且战斗机最右边小于游戏窗口最右边时向右移动
        if self.moving_right and self.rect.right<self.rect_screen.right:
            self.rect.centerx+=1
        # 当moving_right为True且战斗机最左边大于游戏窗口最左边时向右移动
        elif self.moving_left and self.rect.left>self.rect_screen.left:
            self.rect.centerx-=1
```

再次运行主程序，发现战斗机不会跑出界面了

接下来让我们添加一个可以调整战斗机左右移动的速度的设置，想要改变移动速度，只需将每次移动的距离为1改为其他则可以实现速度改变

因为`rect` 只存储这个值的整数部分。为准确地存储飞船的位置，我们定义了一个可存储小数值的新属性`self.center` 我们使用函数`float()` 将`self.rect.centerx` 的值转换为小数，并将结果存储到`self.center` 中。

`setting.py`

```py
class Settings():
    """存储游戏的所有设置"""

    def __init__(self):
        """初始化游戏设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_hight = 600
        
        # 设置战斗机的移动速度
        self.ship_speed=1.5
```

`ship.py`

```py
import pygame


class Ship(object):
    """初始化飞船并设置飞船的开始位置"""
    def __init__(self,screen,St):
        --此处代码省略--
        self.St=St
        # 在战斗机属性center中存储小数值
        self.center=float(self.rect.centerx)
    def update(self):
        """更新战斗机的位置"""
        if self.moving_right and self.rect.right<self.rect_screen.right:
            self.center+=self.St.ship_speed
        elif self.moving_left and self.rect.left>self.rect_screen.left:
            self.center-=self.St.ship_speed
        self.rect.centerx = self.center

    def blitme(self):
        """在指定位置绘制战斗机"""
        self.screen.blit(self.image, self.rect)
```

`alien_invasion.py`

```python
import pygame
import game_function as g_f
from setting import Settings
from ship import Ship

def run_game():
    # 初始化游戏窗口
    pygame.init()
    # 初始化设置对象St
    St = Settings()
    # 设置游戏窗口大小
    screen = pygame.display.set_mode((St.screen_width, St.screen_hight))
    # 创建战斗机实例
    Sp = Ship(screen,St)
    # 设置游戏窗口名字
    pygame.display.set_caption('外星飞机大战')
    # 设置游戏背景
    background_image = pygame.image.load('外太空（游戏背景图）.png')
    # 开始游戏主循环
    while True:
        g_f.check_events(Sp)
        # 更新屏幕
        g_f.update_screen(Sp)
        # 更新战斗机位置
        Sp.update()
        # 游戏背景图
        screen.blit(background_image, (0, 0))


run_game()
```

将主程序中的战斗机实例`ship()`传参，运行主程序，发现当调整`ship_speed`的值变大时，战斗机的移动速度越大

### 射击

第一步我们需要在`setting`文件中添加子弹的属性设置，比如子弹的速度等

`setting.py`

```py
class Settings():
    """存储游戏的所有设置"""

    def __init__(self):
        """初始化游戏设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_hight = 600
        
        # 设置战斗机的移动速度
        self.ship_speed=1.5
        
        # 设置子弹的速度
        self.bullet_speed=1
```

第二部则需要创建一个存储`Bullet`类的文件`bullet.py`，用来管理子弹的行为和属性

和创建`ship`类差不多，找出一个子弹图片，得到其外接矩形

`bullet.py`

```py
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """管理发射出来的子弹"""
    def __init__(self,screen,Sp,St):
        super(Bullet,self).__init__()
        self.screen=screen
        self.bullet_image=pygame.image.load('导弹.png')
        # 获取子弹图片的外接矩形
        self.rect=self.bullet_image.get_rect()
        # 将子弹的位置放在战斗机的上边缘的中间作为子弹发射的起始位置
        self.rect.centerx=Sp.rect.centerx
        self.rect.top=Sp.rect.top
        
        self.centery=float(self.rect.y)
        
        # 子弹的速度属性
        self.speed=St.bullet_speed
```

> **注意：**代码倒数第二行和ship不同，战斗机是左右移动所以设置x，子弹是上下移动设置y

在这个代码中，因为子弹有许多个，所以我们这里用到了精灵`Sprite`类，这个类在`pygame`模块中，需要导入

Bullet 类继承了我们从模块pygame.sprite 中导入的Sprite 类。通过使用精灵，可将游戏中相关的元素编组，进而同时操作编组中的所有元素。为创建子弹实例，需要 向`__init__()`传递St 、screen 和ship 实例，还调用了super() 来继承Sprite 

下面是`bullet.py`的第二部分——方法`update()` 和`draw_b()`，其中`update()`负责更新子弹发射出去后的位置，`draw_b()`负责在游戏窗口绘制子弹图像

`bullet.py`

```py
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """管理发射出来的子弹"""
    def __init__(self,screen,Sp,St):
        --此处代码省略--
    
    def update(self):
        """更新子弹位置"""
        self.centery-=self.speed
        # 更新表示子弹的rect位置
        self.rect.y=self.centery
    
    def draw_b(self):
        """在游戏窗口绘制子弹图像"""
        self.screen.blit(self.bullet_image,self.rect)
```

定义Bullet 类和必要的设置后，就可以编写代码了，我们要实现当玩家每次按空格键时都射出一发子弹的效果。首先，我们将在`alien_invasion.py`中创建一个编组（group），用于存储所有发射出去的子弹，以便能够管理发射出去的所有子弹。这个编组将是`pygame.sprite.Group` 类的一个实例；`pygame.sprite.Group `类类似于列表，但提供了有助于开发游戏的额外功 能。在主循环中，我们将使用这个编组在屏幕上绘制子弹，以及更新每颗子弹的位置：

`alien_invasion.py`

```py
--此处代码省略--
from bullet import Bullet
from pygame.sprite import Group

def run_game():
    --此处代码省略--
    # 创建一个用来存储子弹的编组
    bullets=Group()
    # 开始游戏主循环
    while True:
        --此处代码省略--
        # 更新子弹的位置
        bullets.update()
        # 游戏背景图
        screen.blit(background_image, (0, 0))

run_game()
```

我们导入了`pygame.sprite` 中的`Group` 类，创建了一个`Group` 实例，并将其命名为`bullets` 。这个编组是在`while` 循环外面创建的，这样就无需每次运行该循环时都创建一个新的子弹编组。

### 发射子弹

目前我们已经定义好了子弹，现在需要发射出子弹，当玩家按下空格键时，发射一颗子弹，此时又需要用到之前的检测键盘按键，所以我们需要在`game_function.py`的`check_events()`中添加发射的代码：

`game_function.py`

```py
import sys
import pygame


def check_events(Sp,screen,St,bullets):
    """监视键盘和鼠标事件"""
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            # 当玩家点击游戏窗口关闭按钮时，调用sys.exit()退出游戏
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            --此处代码省略--
            elif event.key==pygame.K_SPACE:
                new_bullet = Bullet(screen,Sp,St)
                bullets.add(new_bullet)
        --此处代码省略--

def update_screen(Sp，bullets):
    """更新屏幕"""
    # 绘制子弹图像,将精灵组里的每个子弹绘制出来
    for bt in bullets.sprites():
        bt.draw_b()
    # 绘制战斗机
    Sp.blitme()
    # 让最近绘制的屏幕可见
    pygame.display.flip()
```

一定要注意在`update_screen()`中，子弹的绘制代码要放在最前面，否则子弹将会看不见，还有一个，如果出现错误并且错误显示说没有定义，则大概率是某个函数里面的参数没有传递完整，缺少了某一个参数或者是参数的顺序不对

此时运行程序，我们按下空格键发现子弹可以发射并且可以正常运行，则成功

但是如果时间越长，发射的子弹越多，会发现程序运行变得慢了，这是因为我们发射出去的子弹跑出界面后并没有消失，而是在不断的前进，这就导致随着子弹的增多，程序越来越慢，因此我们需要小小的修改一下代码，将那些跑出屏幕外的子弹删除，问题则会迎刃而解

我们在`game_function.py` 文件中添加一个函数来更新子弹，判断子弹是否跑出界面，是则删除

`game_function.py`

```py
import sys
import pygame


def check_events(Sp,screen,St,bullets):
    """监视键盘和鼠标事件"""
    --此处代码省略--

def update_screen(Sp，bullets):
    """更新屏幕"""
    --此处代码省略--
    
def update_bulllets(bullets):
    """删除屏幕之外的子弹"""
    bullets.update()
    # 先判断子弹的是否跑出屏幕外
    for bullet in bullets.copy():
        if bullet.rect.bottom==0:
            bullets.remove(bullet)
```

我们同时将`alien_invasion.py`中的`bullets.update()`代码也一起移到这个函数中，更加简化了主程序，最后在主程序中调用`update_bullets(bullets)`函数即可

`alien_invasion.py`

```py
--此处代码省略--

def run_game():
    --此处代码省略--
    # 开始游戏主循环
    while True:
        --此处代码省略--
        # 更新子弹并删除界外子弹
        g_f.update_bullets(bullets)
        # 游戏背景图
        screen.blit(background_image, (0, 0))

run_game()
```

目前删除屏幕外的子弹的代码已经完成

### 创建外星战斗机

因为外星人战斗机不是一个两个而是一群，所以我们还需要再次用到在创建子弹时的精灵`Sprite` ，用来包含所有的外星人战斗机，因此前面的代码类似

首先我们需要创建一个用来管理外星人战斗机的模块`alien.py`

`alien.py`

```py
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """负责管理外星人战斗机的行为和属性"""
    def __init__(self,screen,St):
        super(Alien,self).__init__()
        self.screen=screen
        self.St=St
        
        # 加载外星战斗机的图像并获取其外接矩形
        self.image=pygame.image.load("外星人战斗机.png")
        self.rect=self.image.get_rect()
        
    def blitme(self):
        """将外星人战斗机放在屏幕指定位置"""
        self.screen.blit(self.image,self.rect)
```

接下来我们便需要让这些外星人战斗机在屏幕顶部随机位置生成，这里就需要用到一个重要的模块`random`，这个模块中的`randint()`函数可以生成指定范围内的随机整数，在`alien.py`中导入`random`模块中的`randint()`函数

`alien_py`

```py
import pygame
from random import randint
from pygame.sprite import Sprite

class Alien(Sprite):
    """负责管理外星人战斗机的行为和属性"""
    def __init__(self,screen,St):
        super(Alien,self).__init__()
        self.screen=screen
        self.St=St
        
        # 加载外星战斗机的图像并获取其外接矩形
        self.image=pygame.image.load("外星人战斗机.png")
        self.rect=self.image.get_rect()
        
        # 在屏幕顶部随机位置生成外星人战斗机
        self.rect.x=randint(0,St.screen_width)
        self.rect.y=randint(0,10)
        
     def blitme(self):
        """将外星人战斗机放在屏幕指定位置"""
        self.screen.blit(self.image,self.rect)
```

同时我们需要在主程序中创建一个外星人战斗机的编组

`alien_invasion.py`

```py
--此处代码省略--
from alien import Alien

def run_game():
    --此处代码省略--
    # 创建外星人战斗机实例
    Al=Alien(screen,St)
    # 创建一个用来存储外星人战斗机的编组
    aliens=Group()
    # 开始游戏主循环
    while True:
        --此处代码省略--

run_game()
```

目前外星人战斗机编组中没有战斗机，因此我们需要将其中添加战斗机，在`game_function.py`中定义一个`create_alien()`函数来向编组中添加战斗机

`game_function.py`

```py
import sys
import pygame


def check_events(Sp,screen,St,bullets):
    """监视键盘和鼠标事件"""
    --此处代码省略--

def update_screen(Sp，bullets):
    """更新屏幕"""
    --此处代码省略--
    
def update_bulllets(bullets):
    """删除屏幕之外的子弹"""
    --此处代码省略--
    
def create_alien(St, screen, aliens):
    alien = Alien(screen, St)
    aliens.add(alien)
```

在主程序中调用这个函数

`alien_invasion.py`

```py
import pygame
import game_function as g_f
from setting import Settings
from ship import Ship
from alien import Alien
from pygame.sprite import Group

def run_game():
    --此处代码省略--
    # 开始游戏主循环
    while True:
        --此处代码省略--
        # 增加外星人战斗机
        g_f.create_alien(St,screen,aliens)
        # 更新屏幕
        g_f.update_screen(Sp,bullets,aliens,screen)
        # 游戏背景图
        screen.blit(background_image, (0, 0))


run_game()
```

下一步就是让外星人战斗机出现在游戏窗口上，为让外星人出现在屏幕上，我们在`update_screen()` 中调用方法`draw()`：

`game_function.py`

```py
import sys
import pygame


def check_events(Sp,screen,St,bullets):
    """监视键盘和鼠标事件"""
    --此处代码省略--

def update_screen(Sp,bullets,aliens,screen):
    """更新屏幕"""
    --此处代码省略--
    aliens.draw(screen)
    
def update_bulllets(bullets):
    """删除屏幕之外的子弹"""
    --此处代码省略--
    
def create_alien(St, screen, aliens):
    alien = Alien(screen, St)
    aliens.add(alien)
```

此时运行程序我们会发现外星人战斗机在（0，10）的范围内随机生成，产生大量的外星人战斗机，接下来我们开始实现外星人战斗机向下运动的行为，而不是一直呆在原地

首先在`setting.py`文件中设置外星人战斗机向下的速度`alien_speed`

`setting.py`

```py
class Settings():
    """存储游戏的所有设置"""

    def __init__(self):
        """初始化游戏设置"""
        --此处代码省略--
        
        # 设置外星人战斗机下落速度
        self.alien_speed=10
```

然后在`game_function.py`中实现外星人战斗机向下移动

`game_function.py`

```py
import sys
import pygame


def check_events(Sp,screen,St,bullets):
    """监视键盘和鼠标事件"""
    --此处代码省略--

def update_screen(Sp,bullets,aliens,screen):
    """更新屏幕"""
    --此处代码省略--
    
def update_bulllets(bullets):
    """删除屏幕之外的子弹"""
    --此处代码省略--
    
def create_alien(St, screen, aliens):
    """在编组中添加外星人战斗机"""
    --此处代码省略--
    
def change_fleet_direction(St, aliens):
    """将所有外星人战斗机往下移"""
    for alien in aliens.sprites():
        alien.rect.y += St.alien_speed
```

在主程序中调用该函数

`alien_invasion.py`

```py
import pygame
import game_function as g_f
from setting import Settings
from ship import Ship
from alien import Alien
from pygame.sprite import Group

def run_game():
    --此处代码省略--
    # 开始游戏主循环
    while True:
        --此处代码省略--
        # 让外星人战斗机向下移动
        g_f.change_fleet_direction(St,aliens)
        # 更新屏幕
        g_f.update_screen(Sp,bullets,aliens,screen)
        # 游戏背景图
        screen.blit(background_image, (0, 0))


run_game()
```

然后运行主程序，发现外星人战斗机都向下移动

### 射杀外星人战斗机

子弹和外星人战斗机都已经实现好之后，我们就要开始攻击外星人战斗机，需要我们实现当子弹与外星人战斗机接触的那一刻删除子弹和外星人战斗机的效果，对于子弹与外星人战斗机是否接触，在`sprite`中专门提供了检测两个编组是否重叠的方法`sprite.groupcollide()`，有了这个方法，问题就变得简单许多

`game_function.py`

```py
import sys
import pygame


def check_events(Sp,screen,St,bullets,Cl,aliens):
    """监视键盘和鼠标事件"""
    --此处代码省略--

def update_screen(Sp,bullets,aliens,screen):
    """更新屏幕"""
    --此处代码省略--
    
def update_bulllets(bullets):
    """删除屏幕之外的子弹"""
    --此处代码省略--
    
def create_alien(St, screen, aliens):
    """在编组中添加外星人战斗机"""
    --此处代码省略--
    
def change_fleet_direction(St, aliens):
    """将所有外星人战斗机往下移"""
    --此处代码省略--
    
def check_bullet_alien_collisions(aliens, bullets):
    """响应子弹和外星人战斗机的碰撞"""
    # 检查是否有子弹碰撞了外星人战斗机
    # 如果碰到了，则删除这颗子弹和被碰撞的外星人战斗机
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
```

每当有子弹和外星人的`rect`重叠时，`groupcollide()` 就在它返回的字典中添加一 个键-值对，两个实参`True` 告诉Pygame删除发生碰撞的子弹和外星人，（要模拟能够穿行到屏幕顶端的高能子弹——消灭它击中的每个外星人，可将第一个布尔实参设置 为False ，并让第二个布尔实参为True 。这样被击中的外星人将消失，但所有的子弹都始终有效，直到抵达屏幕顶端后消失。）

在主程序中调用该函数

`alien_invasion.py`

```py
import pygame
import game_function as g_f
from setting import Settings
from ship import Ship
from alien import Alien
from pygame.sprite import Group

def run_game():
    --此处代码省略--
    # 开始游戏主循环
    while True:
        --此处代码省略--
        # 检测子弹是否击中外星人战斗机
        g_f.check_bullet_alien_collisions(aliens,bullets)
        # 更新屏幕
        g_f.update_screen(Sp,bullets,aliens,screen)
        # 游戏背景图
        screen.blit(background_image, (0, 0))


run_game()
```

运行主程序，并发射子弹，发现已经实现预期的效果，但是我们会发现外星人战斗机的生成速度和下落速度非常快，虽然我们在之前已经设置了外星人战斗机的速度为10，但是那仅仅只是每次的下落距离，而且每次的间隔我们并没有设置，导致外星人战斗机会无间隔的每次向下移动10，所以我们为了让玩家有更好的体验，我们需要定义一个定时器，使每隔一段时间生成一个外星人战斗机和移动一次，这样效果会更好

新创建一个文件名为`clock.py`

`clock.py`

```py
import pygame

class Clocks(object):
    def __init__(self):
        # 每1000毫秒生成一个外星人
        self.ALIEN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ALIEN_EVENT, 1000)
        # 每150毫秒向下移动一下
        self.ALIEN_EVENT_1 = pygame.USEREVENT + 2
        pygame.time.set_timer(self.ALIEN_EVENT_1, 150)
```

然后在主程序中导入`clock`并定义一个`Clocks()`的实例，并且将外星人战斗机下落和生成函数全部放在`game_function.py`中的`check_events()`函数中，代码如下：

`alien_invasion.py`

```py
--此处代码省略--
from clock import Clocks



def run_game():
    # 初始化游戏窗口
    pygame.init()
    # 创建定时器对象
    Cl=Clocks()
    --此处代码省略--
    # 开始游戏主循环
    while True:
        g_f.check_events(Sp,screen,St,bullets,Cl,aliens)
        # 更新战斗机位置
        Sp.update()
        # 删除子弹
        g_f.update_bullets(bullets)
        # 检测子弹是否击中外星人战斗机
        g_f.check_bullet_alien_collisions(aliens,bullets)
        # 更新屏幕
        g_f.update_screen(Sp,bullets,aliens,screen)
        # 游戏背景图
        screen.blit(background_image, (0, 0))

run_game()
```

`game_function.py`

```py
import sys
import pygame


def check_events(Sp,screen,St,bullets,Cl,aliens):
    """监视键盘和鼠标事件"""
        for event in pygame.event.get():
        if event.type==pygame.QUIT:
            # 当玩家点击游戏窗口关闭按钮时，调用sys.exit()退出游戏
            sys.exit()
        elif event.type == Cl.ALIEN_EVENT:
            # 定时器事件触发，创建一个新的外星人
            create_alien(St, screen,aliens)
        elif event.type == Cl.ALIEN_EVENT_1:
            # 定时器事件触发，移动一下外星人
            change_fleet_direction(St, aliens)
        --此处代码省略--

def update_screen(Sp,bullets,aliens,screen):
    """更新屏幕"""
    --此处代码省略--
    
def update_bulllets(bullets):
    """删除屏幕之外的子弹"""
    --此处代码省略--
    
def create_alien(St, screen, aliens):
    """在编组中添加外星人战斗机"""
    --此处代码省略--
    
def change_fleet_direction(St, aliens):
    """将所有外星人战斗机往下移"""
    --此处代码省略--
    
def check_bullet_alien_collisions(aliens, bullets):
    """响应子弹和外星人战斗机的碰撞"""
    --此处代码省略--
```

运行主程序，看看是否达到了预期效果

![image-20241016200820958](./image-20241016200820958.png)

这就是运行成功的图片，战斗机和外星人战斗机的图片还有背景图片可以自己在网上找然后调整大小就行

### 游戏失败

当外星人战斗机与玩家战斗机碰撞或者外星人战斗机到达底部边缘时，玩家死亡，游戏失败，同时清空屏幕上的所有战斗机和子弹

首先来编写一个用于跟踪游戏统计信息的新类——GameStats ，并将其保存为文件`game_stats.py`

`game_stats.py`

```py
class GameStats(object):
    """跟踪游戏的统计信息"""

    def __init__(self,St):
        """初始化统计信息"""
        self.St=St
        self.reset_stats()
        
    def reset_stats(self):
        """初始化在游戏期间可能变化的统计信息"""
        self.ships_left=self.St.ship_limit
```

在这个游戏运行期间，我们只创建一个`GameStats` 实例，但每当玩家开始新游戏时，需要重置一些统计信息。为此，我们在方法`reset_stats()` 中初始化大部分统计信息

我们在游戏窗口左上角显示三个玩家战斗机，代表我们规定玩家每局游戏有三次复活机会，每次复活都清空屏幕，并且减少左上角的一个战斗机

`setting.py`

```py
class Settings():
    """存储游戏的所有设置"""

    def __init__(self):
        """初始化游戏设置"""
        --此处代码省略--
        
        # 设置玩家的复活次数为三次
        self.ship_limit=3
```

我们还需对`alien_invasion.py`做些修改，以创建一个`GameStats` 实例：

`alien_invasion.py`

```py
--此处代码省略--
from game_stats import GameStats



def run_game():
    --此处代码省略--
    # 设置游戏窗口大小
    screen = pygame.display.set_mode((St.screen_width, St.screen_hight))
    # 创建一个能够存储游戏统计信息的实例
    stats = GameStats(St)
    # 创建战斗机实例
    Sp = Ship(screen,St)
    --此处代码省略--
    # 开始游戏主循环
    while True:
        --此处代码省略--

run_game()
```

有外星人撞到飞船时，我们将余下的飞船数减1，创建一群新的外星人，并将飞船重新放置到屏幕底端中央（我们还将让游戏暂停一段时间，让玩家在新外星人群出现前注意到发 生了碰撞，并将重新创建外星人群）。 下面将实现这些功能的大部分代码放到`game_function.py`文件中的函数`ship_hit()` 中：

`game_function.py`

```py
import sys
import pygame
from time import sleep

def check_events(Sp,screen,St,bullets,Cl,aliens):
    """监视键盘和鼠标事件"""
    --此处代码省略--

def update_screen(Sp,bullets,aliens,screen):
    """更新屏幕"""
    --此处代码省略--
    
def update_bulllets(bullets):
    """删除屏幕之外的子弹"""
    --此处代码省略--
    
def create_alien(St, screen, aliens):
    """在编组中添加外星人战斗机"""
    --此处代码省略--
    
def change_fleet_direction(St, aliens):
    """将所有外星人战斗机往下移"""
    --此处代码省略--
    
def check_bullet_alien_collisions(aliens, bullets):
    """响应子弹和外星人战斗机的碰撞"""
    --此处代码省略--
    
def ship_hited(stats,aliens,bullets,Sp):
    """响应被外星人战斗机撞到的战斗机"""
    # 将ship_left减1（即战斗机的数量减一）,相当于玩家的三次复活机会
    stats.ships_left-=1

    # 清空子弹和外星人战斗机列表
    aliens.empty()
    bullets.empty()

    # 将玩家战斗机放置在屏幕底部中央
    Sp.ship_center()

    # 暂停
    sleep(0.5)
```

里面用到了`sleep()`函数，所以记得导入`time`模块，接下来在`ship.py`中编写`ship_center()`函数

`ship.py`

```py
import pygame


class Ship(object):
    """初始化飞船并设置飞船的开始位置"""
    def __init__(self,screen,St):
        --此处代码省略--

    def update(self):
        """更新战斗机的位置"""
        --此处代码省略--

    def blitme(self):
        """在指定位置绘制战斗机"""
        self.screen.blit(self.image, self.rect)

    def ship_center(self):
        """让玩家战斗机在屏幕上居中"""
        self.center=self.rect_screen.centerx
```

接下来就是检测外星人战斗机是否到达屏幕底部边缘，在`game_function.py`中定义`check_alien_bottom()`函数和`update_alien()`函数，在`update_alien()`函数中执行`ship_hited()`来响应外星人战斗机与玩家战斗机碰撞后

`game_function.py`

```py
import sys
import pygame
from time import sleep

def check_events(Sp,screen,St,bullets,Cl,aliens):
    """监视键盘和鼠标事件"""
    --此处代码省略--

def update_screen(Sp,bullets,aliens,screen):
    """更新屏幕"""
    --此处代码省略--
    
def update_bulllets(bullets):
    """删除屏幕之外的子弹"""
    --此处代码省略--
    
def create_alien(St, screen, aliens):
    """在编组中添加外星人战斗机"""
    --此处代码省略--
    
def change_fleet_direction(St, aliens):
    """将所有外星人战斗机往下移"""
    --此处代码省略--
    
def check_bullet_alien_collisions(aliens, bullets):
    """响应子弹和外星人战斗机的碰撞"""
    --此处代码省略--
    
def ship_hited(stats,aliens,bullets,Sp):
    """响应被外星人战斗机撞到的战斗机"""
    --此处代码省略--
    
def check_alien_bottom(screen,stats,bullets,aliens,Sp):
    """检查外星人战斗机有没有到达屏幕底部，有则视为与玩家战斗机碰撞"""
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            # 像玩家战斗机被撞到一样处理
            ship_hited(stats,aliens,bullets,Sp)
            break
            
def update_alien(aliens, St, Sp,stats,screen,bullets):
    """检查外星人战斗机是否碰到边缘并更新战斗机的位置"""
    # 响应战斗机与外星人战斗机碰撞
    if pygame.sprite.spritecollideany(Sp, aliens):
        ship_hited(stats,aliens,bullets,Sp)

    # 检查是否有外星人战斗机到达屏幕底端
    check_alien_bottom(screen,stats,bullets,aliens,Sp)
```

当外星人战斗机到达屏幕底部边缘，则将视为玩家失败，执行`ship_hited()`函数，清空屏幕

现在这个游戏看起来更完整了，但它永远都不会结束，只是`ships_left` 不断变成更小的负数。下面在`GameStats` 中添加一个作为标志的属性`game_active` ，以便在玩家的 飞船用完后结束游戏：

`game_stats.py`

```py
class GameStats(object):
    """跟踪游戏的统计信息"""

    def __init__(self, St):
        """初始化统计信息"""
        self.St = St
        self.reset_stats()

        # 游戏刚刚启动时处于活动状态
        self.game_active=True

    def reset_stats(self):
        """初始化在游戏期间可能变化的统计信息"""
        self.ships_left = self.St.ship_limit
```

现在在`ship_hited()` 中添加代码，在玩家的飞船都用完后将`game_active` 设置为`False` ：

`game_function.py`

```py
import sys
import pygame
from time import sleep

def check_events(Sp,screen,St,bullets,Cl,aliens):
    """监视键盘和鼠标事件"""
    --此处代码省略--

def update_screen(Sp,bullets,aliens,screen):
    """更新屏幕"""
    --此处代码省略--
    
def update_bulllets(bullets):
    """删除屏幕之外的子弹"""
    --此处代码省略--
    
def create_alien(St, screen, aliens):
    """在编组中添加外星人战斗机"""
    --此处代码省略--
    
def change_fleet_direction(St, aliens):
    """将所有外星人战斗机往下移"""
    --此处代码省略--
    
def check_bullet_alien_collisions(aliens, bullets):
    """响应子弹和外星人战斗机的碰撞"""
    --此处代码省略--
    
def ship_hited(stats,aliens,bullets,Sp):
    """响应被外星人战斗机撞到的战斗机"""
    if stats.ships_left>0:
        # 将ship_left减1（即战斗机的数量减一）,相当于玩家的三次复活机会
        stats.ships_left-=1

        # 清空子弹和外星人战斗机列表
        aliens.empty()
        bullets.empty()

        # 将玩家战斗机放置在屏幕底部中央
        Sp.ship_center()

        # 暂停
        sleep(0.5)
    
    # 三条命用完则将游戏状态设置为false，代表玩家死亡
    else:
        stats.game_active=False
    
def check_alien_bottom(screen,stats,bullets,aliens,Sp):
    """检查外星人战斗机有没有到达屏幕底部，有则视为与玩家战斗机碰撞"""
    --此处代码省略--
            
def update_alien(aliens, St, Sp,stats,screen,bullets):
    """检查外星人战斗机是否碰到边缘并更新战斗机的位置"""
    --此处代码省略--
```

`ship_hited()` 的大部分代码都没变。我们将原来的所有代码都移到了一个if 语句块中，这条if 语句检查玩家是否至少还有一艘飞船。如果是这样，就创建一群新的外星人，暂停一会儿，再接着往下执行。如果玩家没有飞船了，就将`game_active` 设置为False ，代表玩家死亡，游戏结束

在`alien_invasion.py`中，我们需要确定游戏的哪些部分在任何情况下都应运行，哪些部分仅在游戏处于活动状态时才运行：

`alien_invasion.py`

```py
--此处代码省略--

def run_game():
    --此处代码省略--
    # 开始游戏主循环
    while True:
        g_f.check_events(Sp,screen,St,bullets,Cl,aliens)
        if stats.game_active:
            # 更新战斗机位置
            Sp.update()
            # 删除子弹
            g_f.update_bullets(bullets,aliens)
            # 更新外星人战斗机
            g_f.update_alien(aliens,St,Sp,stats,screen,bullets)
        # 更新屏幕
        g_f.update_screen(Sp,bullets,aliens,screen)
        # 游戏背景图
        screen.blit(background_image, (0, 0))

run_game()
```

将原本主程序中的`check_bullet_alien_collisions()`函数添加在`game_function.py`中的`update_bullets()`中

`game_function.py`

```py
import sys
import pygame
from time import sleep

def check_events(Sp,screen,St,bullets,Cl,aliens):
    """监视键盘和鼠标事件"""
    --此处代码省略--

def update_screen(Sp,bullets,aliens,screen):
    """更新屏幕"""
    --此处代码省略--
    
def update_bulllets(bullets,aliens):
    """删除屏幕之外的子弹"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom==0:
            bullets.remove(bullet)

    # 子弹与外星人战斗机碰撞
    check_bullet_alien_collisions(aliens, bullets)
    
def create_alien(St, screen, aliens):
    """在编组中添加外星人战斗机"""
    --此处代码省略--
    
def change_fleet_direction(St, aliens):
    """将所有外星人战斗机往下移"""
    --此处代码省略--
    
def check_bullet_alien_collisions(aliens, bullets):
    """响应子弹和外星人战斗机的碰撞"""
    --此处代码省略--
    
def ship_hited(stats,aliens,bullets,Sp):
    """响应被外星人战斗机撞到的战斗机"""
    --此处代码省略--
        
def check_alien_bottom(screen,stats,bullets,aliens,Sp):
    """检查外星人战斗机有没有到达屏幕底部，有则视为与玩家战斗机碰撞"""
    --此处代码省略--
            
def update_alien(aliens, St, Sp,stats,screen,bullets):
    """检查外星人战斗机是否碰到边缘并更新战斗机的位置"""
    --此处代码省略--
```

现在，你运行这个游戏时，会发现当三次复活用完时，外星人战斗机还在继续生成，所以我们要在`game_function.py`中生成外星人战斗机的代码前面加一个条件，即游戏处于活动状态时生成和移动

`game_function.py`

```py
import sys
import pygame
from time import sleep

def check_events(Sp,screen,St,bullets,Cl,aliens,stats):
    """监视键盘和鼠标事件"""
        for event in pygame.event.get():
        if event.type==pygame.QUIT:
            # 当玩家点击游戏窗口关闭按钮时，调用sys.exit()退出游戏
            sys.exit()
        elif event.type == Cl.ALIEN_EVENT:
            # 定时器事件触发，创建一个新的外星人
            if stats.game_active:  # 只在游戏活动状态下生成外星人
            	create_alien(St, screen,aliens)
        elif event.type == Cl.ALIEN_EVENT_1:
            # 定时器事件触发，移动一下外星人
            if stats.game_active:  # 只在游戏活动状态下移动外星人
                change_fleet_direction(St, aliens)
        --此处代码省略--

def update_screen(Sp,bullets,aliens,screen):
    """更新屏幕"""
    --此处代码省略--
    
def update_bulllets(bullets,aliens):
    """删除屏幕之外的子弹"""
    --此处代码省略
    
def create_alien(St, screen, aliens):
    """在编组中添加外星人战斗机"""
    --此处代码省略--
    
def change_fleet_direction(St, aliens):
    """将所有外星人战斗机往下移"""
    --此处代码省略--
    
def check_bullet_alien_collisions(aliens, bullets):
    """响应子弹和外星人战斗机的碰撞"""
    --此处代码省略--
    
def ship_hited(stats,aliens,bullets,Sp):
    """响应被外星人战斗机撞到的战斗机"""
    --此处代码省略--
        
def check_alien_bottom(screen,stats,bullets,aliens,Sp):
    """检查外星人战斗机有没有到达屏幕底部，有则视为与玩家战斗机碰撞"""
    --此处代码省略--
            
def update_alien(aliens, St, Sp,stats,screen,bullets):
    """检查外星人战斗机是否碰到边缘并更新战斗机的位置"""
    --此处代码省略--
```

此时，我们再次运行程序，当复活次数用完时，屏幕将处于静止状态

### 添加Play按钮

我们将添加一个Play按钮，它在游戏开始前出现，并在游戏结束后再次出现，让玩家能够开始新游戏。

当前，这个游戏在玩家运行`alien_invasion.py`时就开始了。下面让游戏一开始处于非活动状态，并提示玩家单击Play按钮来开始游戏。为此，在`game_stats.py`中将`game_active`改为False

`game_stats.py`

```py
class GameStats(object):
    """跟踪游戏的统计信息"""

    def __init__(self, St):
        """初始化统计信息"""
        self.St = St
        self.reset_stats()

        # 游戏刚刚启动时处于活动状态
        self.game_active=False

    def reset_stats(self):
        """初始化在游戏期间可能变化的统计信息"""
        self.ships_left = self.St.ship_limit
```

接下来让我们创建一个Button类，创建一个新文件`button.py`

`button.py`

```py
import pygame.font
class Button():
    """初始化按钮的属性"""
    def __init__(self, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.button_text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 按钮的标签只需创建一次
        self.prep_msg(msg)
        
        
    def prep_msg(self,msg):
        """将msg（也就是按钮的文本）渲染为图像，并使其在按钮上居中"""
        self.image_msg=self.font.render(msg,True,self.button_text_color,self.button_color)
        self.image_msg_rect=self.image_msg.get_rect()
        self.image_msg_rect.center=self.rect.center
```

首先，我们导入了模块`pygame.font` ，它让Pygame能够将文本渲染到屏幕上。方法`__init__()` 接受参数`self` ，对象`screen `，以及`msg`，其中`msg `是 要在按钮中显示的文本。我们设置按钮的尺寸，然后通过设置`button_color` 让按钮的rect 对象为亮绿色，并通过设置`button_text_color` 让文本为白色，实参`None `让Pygame 使用默认字体，而48 指定了文本的字号。为让按钮在屏幕上居中，我们创建一个表示按钮的`rect` 对 象，并将其`center `属性设置为屏幕的`center `属性。 Pygame通过将你要显示的字符串渲染为图像来处理文本。最后我们调用`prep_msg()` 来处理这样的渲染。

方法`prep_msg()` 接受实参`self` 以及要渲染为图像的文本（msg ）。调用`font.render()` 将存储在`msg` 中的文本转换为图像，然后将该图像存储在`msg_image `中。方法`font.render()` 还接受一个布尔实参，该实参指定开启还是关闭反锯齿功能（反锯齿让文本的边缘更平滑）。余下的两个实参分别是文本颜色和背景色。我们启用 了反锯齿功能，并将文本的背景色设置为按钮的颜色（如果没有指定背景色，Pygame将以透明背景的方式渲染文本），我们让文本图像在按钮上居中：根据文本图像创建一个`rect` ，并将其`center` 属性设置为按钮的`center` 属性。 最后，我们创建方法`draw_button()` ，通过调用它可将这个按钮显示到屏幕上：

`button.py`

```py
import pygame.font
class Button():
    """初始化按钮的属性"""
    def __init__(self, screen, msg):
        --此处代码省略--
        
    def prep_msg(self,msg):
        """将msg（也就是按钮的文本）渲染为图像，并使其在按钮上居中"""
        --此处代码省略--
        
    def draw_button(self):
        """在屏幕上绘制按钮"""
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.image_msg,self.image_msg_rect)
```

在屏幕上绘制按钮，我们将使用`Button` 类来创建一个`Play`按钮。鉴于只需要一个`Play`按钮，我们直接在`alien_invasion.py`中创建它，我们导入`Button` 类，并创建一个名为`play_bt` 的实例，然后我们将`play_bt` 传递给`update_screen()` ，以便能够在屏幕更新时显示按钮

`alien_invasion.py`

```py
--此处代码省略--
from button import Button


def run_game():
    # 初始化游戏窗口
    pygame.init()
    Cl=Clocks()
    # 初始化设置对象St
    St = Settings()
    # 设置游戏窗口大小
    screen = pygame.display.set_mode((St.screen_width, St.screen_hight))
    # 创建一个play按钮
    play_bt=Button(screen,'play')
    --此处代码省略--
    # 开始游戏主循环
    while True:
        --此处代码省略--

        # 更新屏幕
        g_f.update_screen(Sp, bullets, aliens, screen,play_bt,stats)


run_game()
```

接下来，修改`update_screen()` ，以便在游戏处于非活动状态时显示Play按钮

`game_function.py`

```py
import sys
import pygame
from time import sleep

def check_events(Sp,screen,St,bullets,Cl,aliens,stats):
    """监视键盘和鼠标事件"""
    --此处代码省略--

def update_screen(Sp,bullets,aliens,screen,play_bt,stats):
    """更新屏幕"""
    --此处代码省略--
    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_bt.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()
    
def update_bulllets(bullets,aliens):
    """删除屏幕之外的子弹"""
    --此处代码省略--
    
def create_alien(St, screen, aliens):
    """在编组中添加外星人战斗机"""
    --此处代码省略--
    
def change_fleet_direction(St, aliens):
    """将所有外星人战斗机往下移"""
    --此处代码省略--
    
def check_bullet_alien_collisions(aliens, bullets):
    """响应子弹和外星人战斗机的碰撞"""
    --此处代码省略--
    
def ship_hited(stats,aliens,bullets,Sp):
    """响应被外星人战斗机撞到的战斗机"""
    --此处代码省略--
        
def check_alien_bottom(screen,stats,bullets,aliens,Sp):
    """检查外星人战斗机有没有到达屏幕底部，有则视为与玩家战斗机碰撞"""
    --此处代码省略--
            
def update_alien(aliens, St, Sp,stats,screen,bullets):
    """检查外星人战斗机是否碰到边缘并更新战斗机的位置"""
    --此处代码省略--
```

为在玩家单击Play按钮时开始新游戏，需在`game_function.py`中添加新事件和新函数`check_play_button()`，以监视与这个按钮相关的鼠标事件

`game_function.py`

```py
import sys
import pygame
from time import sleep

def check_events(Sp,screen,St,bullets,Cl,aliens,stats,play_bt):
    """监视键盘和鼠标事件"""
    --此处代码省略--
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(stats,play_bt,mouse_x,mouse_y)

def update_screen(Sp,bullets,aliens,screen,play_bt,stats):
    """更新屏幕"""
    --此处代码省略--
    
def update_bulllets(bullets,aliens):
    """删除屏幕之外的子弹"""
    --此处代码省略--
    
def create_alien(St, screen, aliens):
    """在编组中添加外星人战斗机"""
    --此处代码省略--
    
def change_fleet_direction(St, aliens):
    """将所有外星人战斗机往下移"""
    --此处代码省略--
    
def check_bullet_alien_collisions(aliens, bullets):
    """响应子弹和外星人战斗机的碰撞"""
    --此处代码省略--
    
def ship_hited(stats,aliens,bullets,Sp):
    """响应被外星人战斗机撞到的战斗机"""
    --此处代码省略--
        
def check_alien_bottom(screen,stats,bullets,aliens,Sp):
    """检查外星人战斗机有没有到达屏幕底部，有则视为与玩家战斗机碰撞"""
    --此处代码省略--
            
def update_alien(aliens, St, Sp,stats,screen,bullets):
    """检查外星人战斗机是否碰到边缘并更新战斗机的位置"""
    --此处代码省略--
    
def check_play_button(stats,play_bt,mouse_x,mouse_y):
    """在玩家单击play的时候开始游戏"""
    if play_bt.rect.collidepoint(mouse_x,mouse_y) and not stats.game_active:
        # 在玩家点击play后，重置游戏信息，并开始游戏
        stats.game_active=True
```

无论玩家单击屏幕的什么地方，Pygame都将检测到一个`MOUSEBUTTONDOWN `事件，但我们只想让这个游戏在玩家用鼠标单击Play按钮时作出响应。为此，我们使用 了`pygame.mouse.get_pos()` ，它返回一个元组，其中包含玩家单击时鼠标的x 和y 坐标，我们将这些值传递给函数`check_play_button()`，而这个函 数使用`collidepoint()` 检查鼠标单击位置是否在Play按钮的`rect` 内，如果是这样的，我们就将`game_active` 设置为`True `，让游戏就此开始！

在`alien_invasion.py `中调用`check_events()` ，需要传递另外两个实参——`stats` 和`play_button` 

`alien_invasion.py`

```py
--此处代码省略--

def run_game():
    --此处代码省略--
    # 开始游戏主循环
    while True:
        g_f.check_events(Sp,screen,St,bullets,Cl,aliens,stats,play_bt)
        --此处代码省略--

run_game()
```

至此，应该能够开始这个游戏了。游戏结束时，`game_active` 应为`False` ，并重新显示Play按钮。

前面编写的代码只处理了玩家第一次单击Play按钮的情况，而没有处理游戏结束的情况，因为没有重置导致游戏结束的条件。 为在玩家每次单击Play按钮时都重置游戏，需要重置统计信息、删除现有的外星人和子弹、创建一群新的外星人，并让飞船居中，如下所示：

`game_function.py`

```py
def check_play_button(stats,play_bt,mouse_x,mouse_y,bullets,aliens,St,Sp):
    """在玩家单击play的时候开始游戏"""
    if play_bt.rect.collidepoint(mouse_x,mouse_y) and not stats.game_active:
        # 在玩家点击play后，重置游戏信息，并开始游戏
        stats.reset_stats()
        stats.game_active=True

        # 清空子弹和外星人战斗机列表
        bullets.empty()
        aliens.empty()

        # 创建一群新的外星人并让玩家战斗机居中
        Sp.ship_center()
```

注意，在`check_events()`函数中和`check_play_button()`函数参数要保持一致，记得补充完整，`alien_invasion.py`中的`check_events()`也需要补充

但是我们平时玩的游戏好歹也会有个难度或者难度递增，毕竟没有难度的游戏非常无聊，那么接下来，我们需要添加一些代码，实现一些效果：记分板，难度递增，同时限制玩家的复活次数

### 难度递增

我们在`setting.py`中添加一个设置，即`speed_up`，这个是外星人战斗机每次速度加快的倍数

`setting.py`

```py
class Settings():
    """存储游戏的所有设置"""

    def __init__(self):
        """初始化游戏设置"""
        --此处代码省略--

        # 速度加快倍数
        self.speed_up = 1.1
        
```

最后，我们定义并调用`initialize_settings()` ，以初始化随 游戏进行而变化的属性

`setting.py`

```py
class Settings():
    """存储游戏的所有设置"""

    def __init__(self):
        """初始化游戏设置"""
        --此处代码省略--

        self.initialize_setting()
        
    def initialize_setting(self):
        """初始化游戏设置"""
        self.alien_speed=10
        self.ship_speed=1.5
        self.bullet_speed=1
```

每当难度提高一个等级时，我们都使用`increase_speed()` 来提高外星人战斗机的速度：

`setting.py`

```py
class Settings():
    """存储游戏的所有设置"""

    def __init__(self):
        """初始化游戏设置"""
        --此处代码省略--
        
    def initialize_setting(self):
        """初始化游戏设置"""
        --此处代码省略--
        
    def increase_speed(self):
        """当游戏等级提升时，提高玩家，外星人战斗机"""
        self.alien_speed*=self.speed_up
```

那么游戏难度在什么情况下增加难度呢，我们规定每生成25个外星人战斗机难度增加一次，我们需要记录生成战斗机的个数，则需要在`game_function.py`的`create_alien()`中和`alien.py`中添加一行代码

`alien.py`

```py
import pygame
from random import randint
from pygame.sprite import Sprite

class Alien(Sprite):
    """管理外星人战斗机的行为和属性"""
    def __init__(self,screen,St):
        super(Alien,self).__init__()
        self.screen=screen
        self.St=St
        self.count=0

        --此处代码省略--

    def blitme(self):
        """将外星人战斗机放在屏幕指定位置"""
        self.screen.blit(self.image, self.rect)
```

`game_function.py`

```py
def create_alien(St, screen, aliens,Al):
    alien = Alien(screen, St)
    aliens.add(alien)
    Al.count+=1
```

这使得每次生成一个外星人战斗机时`count`加一，便可以记录战斗机个数，接下来就是让外星人战斗机速度加快

`game_function.py`

```py
def check_bullet_alien_collisions(aliens, bullets, St, stats,Sb,Al):
    """响应子弹和外星人战斗机的碰撞"""
    # 检查是否有子弹碰撞了外星人战斗机
    # 如果碰到了，则删除这颗子弹和被碰撞的外星人战斗机
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    # 检查是否消灭了25个外星人战斗机
    if Al.count==25:
        # 删除现有的所有子弹，加快游戏速度，并重新创建一群外星人战斗机，并提高等级
        bullets.empty()
        St.increase_speed()
        Al.count=0
```

这个代码实现了当消灭了25个外星人战斗机时，清空子弹，加快外星人战斗机速度，并将`count`重置为0，以便记录下一次生成的外星人战斗机

玩家开始新游戏时，我们都需要将发生了变化的设置重置为初始值，否则新游戏开始时，速度设置将是前一次游戏增加了的值

`game_function.py`

```py
def check_play_button(stats,play_bt,mouse_x,mouse_y,bullets,aliens,St,Sp):
    """在玩家单击play的时候开始游戏"""
    if play_bt.rect.collidepoint(mouse_x,mouse_y) and not stats.game_active:
        # 在玩家点击play后，重置游戏信息，并开始游戏
        --此处代码省略
        St.initialize_setting()

        --此处代码省略--
```

现在运行主程序，我们发现随着外星人战斗机生成的越多，速度越快，达到了我们的预期效果，记下来就是实现记分

### 记分

得分是游戏的一项统计信息，因此我们在`GameStats` 中添加一个`score` 属性：

`game_stats.py`

```py
class GameStats(object):
    """跟踪游戏的统计信息"""

    def __init__(self, St):
        """初始化统计信息"""
        --此处代码省略--

    def reset_stats(self):
        """初始化在游戏期间可能变化的统计信息"""
        self.ships_left = self.St.ship_limit
        self.score=0
```

为在每次开始游戏时都重置得分，我们在`reset_stats()` 而不是`__init__()` 中初始化score 

为在屏幕上显示得分，我们首先创建一个新类`Scoreboard` 。就当前而言，这个类只显示当前得分，但后面我们也将使用它来显示最高得分、等级和余下的飞船数。下面是这个 类的前半部分，它被保存为文件`scoreboard.py`，这里的步骤和play按钮的操作大差不差：

`scoreboard.py`

```py
import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard(object):
    """显示得分信息，记分板"""

    def __init__(self, St, screen, stats):
        self.screen = screen
        self.St = St
        self.stats = stats
        self.rect_screen = self.screen.get_rect()

        # 记分板字体颜色大小的设置
        self.score_color = (30, 30, 30)
        self.font = pygame.font.SysFont('华文宋体', 28)

        # 准备初始得分图像
        self.prep_score()
```

然后定义`prep_score()`函数

`scoreboard.py`

```py
import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard(object):
    """显示得分信息，记分板"""

    def __init__(self, St, screen, stats):
        --此处代码省略--
        
    def prep_score(self):
        """将记分板转换为图像"""
        round_score = int(round(self.stats.score, -1))
        self.score_str = '得分:' + '{:,}'.format(round_score)
        # print(pygame.font.get_fonts())
        # 上面这步是为了查看pygame支持什么字体，第一次写的时候’得分‘那两个字是乱码，就调用了这个函数
        self.score_image = self.font.render(self.score_str, True, self.score_color, (255,0,0))

        # 将记分板放在屏幕右上角
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.rect_screen.right
        self.score_image_rect.top = 20
```

在`prep_score()` 中，我们首先将数字值`stats.score` 转换为字符串，再将这个字符串传递给创建图像的`render()`。为在屏幕上清晰地显示得分，我们 向`render()` 传递了屏幕背景色，以及文本颜色。 我们将得分放在屏幕右上角，并在得分增大导致这个数字更宽时让它向左延伸。为确保得分始终锚定在屏幕右边，我们创建了一个名为`score_image_rect` 的`rect` ，让其右 边缘与屏幕右边缘相距20像素，并让其上边缘与屏幕上边缘也相距20像素。

 最后，我们创建方法`show_scoreboard()` ，用于显示渲染好的得分图像：

`scoreboard.py`

```py
import pygame.font


class Scoreboard(object):
    """显示得分信息，记分板"""

    def __init__(self, St, screen, stats):
        --此处代码省略--
        
    def prep_score(self):
        """将记分板转换为图像"""
        --此处代码省略--
        
    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_image_rect)
```

为显示得分，我们在`alien_invasion.py`中创建一个`Scoreboard` 实例：

`alien_invasion.py`

```py
--此处代码省略--
from scoreboard import Scoreboard


def run_game():
    --此处代码省略--
    # 创建一个记分板
    Sb = Scoreboard(St, screen, stats)
    # 开始游戏主循环
    while True:
        --此处代码省略--

        # 更新屏幕
        g_f.update_screen(Sp, bullets, aliens, screen,play_bt,stats,Sb)

run_game()
```

为显示得分，将`update_screen() `修改成下面这样：

`game_function.py`

```py
def update_screen(Sp,bullets,aliens,screen,play_bt,stats,Sb):
    """更新屏幕"""
    # 绘制子弹图像,将精灵组里的每个子弹绘制出来
    for bt in bullets.sprites():
        bt.draw_b()
    # 绘制战斗机
    Sp.blitme()
    # 显示得分
    Sb.show_score()
    --此处代码省略--
```

此时运行主程序，会发现屏幕左上角有个0

接下来就是规定消灭一个外星人战斗机能得多少分，随着游戏的进行，我们将提高每个外星人值的点数。为确保每次开始新游戏时这个值都会被重置，我们在`initialize_setting()` 中设置它，我们规定消灭一个得50分

`setting.py`

```py
    def initialize_setting(self):
        """初始化游戏设置"""
        # 打中每个外星人战斗机的得分
        self.alien_score=50
```

在`check_bullet_alien_collisions()` 中，每当有外星人被击落时，都更新得分：

`game_function.py`

```py
def check_bullet_alien_collisions(aliens, bullets, St, Al,stats,Sb):
    """响应子弹和外星人战斗机的碰撞"""
    # 检查是否有子弹碰撞了外星人战斗机
    # 如果碰到了，则删除这颗子弹和被碰撞的外星人战斗机
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # 如果子弹打到外星人战斗机，则分数加50
    if collisions:
        for alien in collisions.values():
            stats.score+=St.alien_score*len(alien)
            Sb.prep_score()
    # 检查所有外星人战斗机是否被消灭
    if Al.count==25:
        # 删除现有的所有子弹，加快游戏速度，并重新创建一群外星人战斗机，并提高等级
        bullets.empty()
        St.increase_speed()
        Al.count=0
```

注意修改相关函数的参数

游戏难度每提高一个等级，游戏都变得更难，因此处于较高的等级时，外星人战斗机的得分应更高。为实现这种功能，我们添加一些代码，以在游戏节奏加快时提高点数：

`setting.py`

```py
class Settings():
    """存储游戏的所有设置"""

    def __init__(self):
        """初始化游戏设置"""
        --此处代码省略--
        # 外星人战斗机的分数增大幅度
        self.alien_speed_score = 1.5

    def initialize_setting(self):
        """初始化游戏设置"""
        --此处代码省略--

    def increase_speed(self):
        """当游戏等级提升时，提高玩家，外星人战斗机"""
        self.alien_speed*=self.speed_up
        self.alien_score = int(self.alien_score * self.alien_speed_score)
```

下来让我们显示游戏最高得分，将其发在屏幕顶端中间

我们将最高得分存储在`GameStats` 中，鉴于在任何情况下都不会重置最高得分，我们在`__init__()` 中而不是`reset_stats()` 中初始化`high_score` 。

`game_stats.py`

```py
class GameStats(object):
    """跟踪游戏的统计信息"""

    def __init__(self, St):
        """初始化统计信息"""
        self.St = St
        self.reset_stats()
        
        # 最高得分，不能重置
        self.high_score=0

        # 游戏刚刚启动时处于活动状态
        self.game_active=False

    def reset_stats(self):
        """初始化在游戏期间可能变化的统计信息"""
        self.ships_left = self.St.ship_limit
        self.score=0
```

继续在`scoreboard.py`中添加`prep_high_score_most()`函数

`scoreboard.py`

```py
import pygame.font


class Scoreboard(object):
    """显示得分信息，记分板"""

    def __init__(self, St, screen, stats):
        --此处代码省略--

        self.prep_high_score_most()

    def prep_score(self):
        """将记分板转换为图像"""
        --此处代码省略--

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_image_rect)


    def prep_high_score_most(self):
        """将最高得分转换为图像并放在屏幕顶部中央"""
        # 将最高得分渲染为图像
        high_score = int(round(self.stats.high_score, -1))
        self.high_score_str = '最高记录:' + '{:,}'.format(high_score)
        self.high_score_image = self.font.render(self.high_score_str, True, self.score_color, (255,0,0))

        # 将最高得分图像放在屏幕顶部中央
        self.high_score_image_rect = self.high_score_image.get_rect()
        self.high_score_image_rect.centerx = self.rect_screen.centerx
        self.high_score_image_rect.top = self.rect_screen.top
```

最高分的显示和得分显示步骤一样，在这里，我们在最高分的显示上加了一行代码添加了用逗号表示的千分位分隔符隔开（比如：1000，000）

现在，方法`show_scoreboard()`需要在屏幕右上角显示当前得分，并在屏幕顶部中央显示最高得分：

`scoreboard.py`

```py
import pygame.font


class Scoreboard(object):
    """显示得分信息，记分板"""

    def __init__(self, St, screen, stats):
        --此处代码省略--

        self.prep_high_score_most()

    def prep_score(self):
        """将记分板转换为图像"""
        --此处代码省略--

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_image_rect)
        self.screen.blit(self.high_score_image, self.high_score_image_rect)


    def prep_high_score_most(self):
        """将最高得分转换为图像并放在屏幕顶部中央"""
        --此处代码省略--
```

为检查是否诞生了新的最高得分，我们在`game_function.py`中添加一个新函数`check_high_score()` ：

`game_function.py`

```py
def check_high_score(stats,Sb):
    """检查是否诞生了最高分"""
    if stats.score>stats.high_score:
        stats.high_score=stats.score
        Sb.prep_high_score_most()
```

在`check_bullet_alien_collisions()` 中，每当有外星人被消灭，都需要在更新得分后调用`check_high_score()` ：

`game_function.py`

```py
def check_bullet_alien_collisions(aliens, bullets, St, Al,stats,Sb):
    """响应子弹和外星人战斗机的碰撞"""
    # 检查是否有子弹碰撞了外星人战斗机
    # 如果碰到了，则删除这颗子弹和被碰撞的外星人战斗机
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # 如果子弹打到外星人战斗机，则分数加50
    if collisions:
        for alien in collisions.values():
            stats.score += St.alien_score * len(alien)
            Sb.prep_score()
        check_high_score(stats,Sb)

    --此处代码省略--
```

现在运行主程序，击败外星人战斗机后，我们可以发现得分和最高分都在正常变化，运行结果如下：

![image-20241019221240278](./image-20241019221240278.png)

### 显示难度等级

为在游戏中显示玩家的等级，首先需要在`GameStats` 中添加一个表示当前等级的属性。为确保每次开始新游戏时都重置等级，在`reset_stats()` 中初始化它：

`game_stats.py`

```py
    def reset_stats(self):
        """初始化在游戏期间可能变化的统计信息"""
        self.ships_left = self.St.ship_limit
        self.score=0
        # 游戏难度等级
        self.level = 1
```

为让`Scoreboard` 能够在当前得分下方显示当前等级，我们在`__init__()` 中调用了一个新函数`prep_level()`：

`scoreboard.py`

```py 
import pygame.font


class Scoreboard(object):
    """显示得分信息，记分板"""

    def __init__(self, St, screen, stats):
        --此处代码省略
        
        # 调用游戏难度等级显示
        self.prep_level()

    def prep_score(self):
        """将记分板转换为图像"""
        --此处代码省略--

    def show_score(self):
        """在屏幕上显示得分"""
        --此处代码省略--

    def prep_high_score_most(self):
        """将最高得分转换为图像并放在屏幕顶部中央"""
        --此处代码省略--

    def prep_level(self):
        """显示目前等级"""
        # 将等级显示渲染为图像
        level = self.stats.level
        self.level_str = '难度:' + str(level)
        self.level_image = self.font.render(self.level_str, True, self.score_color, (255,0,0))

        # 将等级显示图像放在记分板下方
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.right = self.rect_screen.right
        self.level_image_rect.top = self.score_image_rect.bottom + 10
```

游戏难度等级的显示与得分和最高分的显示步骤和代码基本相同，在这里就不再介绍了

我们还需要更新`show_scoreboard()` 

`scoreboard.py`

```py
    def show_scoreboard(self):
        """将记分板显示在屏幕上"""
        self.screen.blit(self.score_image, self.score_image_rect)
        self.screen.blit(self.high_score_image, self.high_score_image_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
```

我们在`check_bullet_alien_collisions()` 中提高等级，并更新等级图像：

`game_function.py`

```py
def check_bullet_alien_collisions(aliens, bullets, St, Al,stats,Sb):
    """响应子弹和外星人战斗机的碰撞"""
    --此处代码省略--

    # 检查所有外星人战斗机是否被消灭
    if Al.count==25:
        # 删除现有的所有子弹，加快游戏速度，并重新创建一群外星人战斗机，并提高等级
        bullets.empty()
        St.increase_speed()
        Al.count=0

        # 提高等级
        stats.level += 1
        Sb.prep_level()

```

如果外星人战斗机被消灭25个，我们就将stats.level 的值加1，并调用`prep_level()` ，以确保正确地显示新等级

为确保开始新游戏时更新记分和等级图像，在按钮Play被单击时触发重置：

`game_function.py`

```py
def check_play_button(stats,play_bt,mouse_x,mouse_y,bullets,aliens,St,Sp,Sb):
    """在玩家单击play的时候开始游戏"""
    if play_bt.rect.collidepoint(mouse_x,mouse_y) and not stats.game_active:
        # 在玩家点击play后，重置游戏信息，并开始游戏
        stats.reset_stats()
        stats.game_active=True
        St.initialize_setting()

        # 重置记分板和等级
        Sb.prep_level()
        Sb.prep_score()
        Sb.prep_high_score_most()

        --此处代码省略--
```

`check_play_button()`中的参数发生变化，记得修改相关函数的参数

现在我们就可以直到目前的游戏难度等级是多少了，运行结果如下图：

![image-20241019224038719](./image-20241019224038719.png)

### 显示剩余复活次数

在`scoreboard.py`中，定义一个`prep_ship()`函数在屏幕右上角显示三架战斗机，代表玩家的三次复活次数

`scoreboard.py`

```py
    def prep_ship(self):
        """显示剩余战斗机数量，即玩家的复活次数"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.screen, self.St)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
```

还需要导入一些模块，因为在这个函数中用到了`Group`

`scoreboard.py`

```py
import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard(object):
    """显示得分信息，记分板"""

    def __init__(self, St, screen, stats):
        --此处代码省略
        
        # 调用显示战斗机数量函数
        self.prep_ship()

    def prep_score(self):
        """将记分板转换为图像"""
        --此处代码省略--

    def show_score(self):
        """在屏幕上显示得分"""
        --此处代码省略--

    def prep_high_score_most(self):
        """将最高得分转换为图像并放在屏幕顶部中央"""
        --此处代码省略--

    def prep_level(self):
        """显示目前等级"""
        --此处代码省略--
        
    def prep_ship(self):
        """显示剩余战斗机数量，即玩家的复活次数"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.screen, self.St)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
```

因为调用了`ships.add()`，所以在`ship.py`中需要修改一些代码

`ship.py`

```py
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """初始化飞船并设置飞船的开始位置"""
    def __init__(self,screen,St):
        super(Ship, self).__init__()
        --此处代码省略--

    --此处代码省略--
```

我们导入了`Sprite`并且将`Ship(Object)`修改为`Ship(Sprite)`，并加了一行代码`super(Ship, self).__init__()`

为在游戏开始时让玩家知道他有多少艘飞船，我们在开始新游戏时调用`prep_ship()` 。这是在`game_function.py`的`check_play_button()` 中进行的：

`game_function.py`

```py
def check_play_button(stats,play_bt,mouse_x,mouse_y,bullets,aliens,St,Sp,Sb):
    """在玩家单击play的时候开始游戏"""
    --此处代码省略--

        # 重置记分板和等级
        Sb.prep_level()
        Sb.prep_score()
        Sb.prep_high_score_most()
        Sb.prep_ship()

        --此处代码省略--
```

我们还需要在战斗机被外星人撞到时调用`prep_ship()` ，从而在玩家复活一次时更新战斗机图像数量即复活次数：

`game_function.py`

```py
def ship_hited(stats,aliens,bullets,Sp,Sb):
    """响应被外星人战斗机撞到的战斗机"""
    # 将ship_left减1（即战斗机的数量减一）,相当于玩家的三条命
    if stats.ships_left>0:
        stats.ships_left-=1
        
        # 玩家复活时更新复活次数
        Sb.prep_ship()

        --此处代码省略--
```

因为我们往`ship_hited()`函数中传入了新的参数，因此许多调用了此函数的函数都需要传入新的参数，这里就不一个一个说了

最后我们在`show_score()`中显示战斗机图像

`scoreboard.py`

```py
    def show_score(self):
        """在屏幕上显示得分"""
        --此处代码省略--
        self.ships.draw(self.screen)
```

我们运行主程序，发现屏幕右上角会出现三架战斗机，当玩家每死亡一次，减少一个，用完的时候，再次死亡则游戏结束

运行结果如下：

![image-20241019231807719](./image-20241019231807719.png)

这个代码在原来那本书上做了一些改变，也可以在后续中为游戏添加爆炸效果和子弹发射的音乐和游戏背景音乐，也可以自己研究更多的功能，比如子弹的升级，添加大Boss，添加关卡等，该项目比较适合练手，到此该游戏代码结束。

