import pygame.font

class Button(object):
    """初始化按钮的属性"""
    def __init__(self,screen,msg):
        self.screen=screen
        self.rect_screen=self.screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width=100
        self.height=50
        self.button_color=(0,255,0)
        self.button_text_color=(255,255,255)
        self.font=pygame.font.SysFont(None,48)

        # 创建按钮的rect对象，并使其居中
        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.center=self.rect_screen.center

        self.prep_msg(msg)

    def prep_msg(self,msg):
        """将msg（也就是按钮的文本）渲染为图像，并使其在按钮上居中"""
        self.image_msg=self.font.render(msg,True,self.button_text_color,self.button_color)
        self.image_msg_rect=self.image_msg.get_rect()
        self.image_msg_rect.center=self.rect.center

    def draw_button(self):
        """在屏幕上绘制按钮"""
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.image_msg,self.image_msg_rect)
