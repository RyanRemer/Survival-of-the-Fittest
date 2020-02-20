import pygame


class TextBox:
    def __init__(self, text, color, coord: (int, int), center=False):
        self.font = pygame.font.SysFont('arial', 18)
        self.text = text
        self.color = color
        self.coord = coord
        self.is_center = center

        text_box = self.font.render(self.text, False, self.color)
        self.rect = text_box.get_rect()

    def set_sys_font(self, sysfont, size):
        self.font = pygame.font.SysFont(sysfont, size)

    def set_font(self, file_path, size):
        self.font = pygame.font.Font(file_path, size)

    def update_text(self, text):
        self.text = text

    def draw(self, screen):
        text_box = self.font.render(self.text, False, self.color)

        if self.is_center:
            center_rect = text_box.get_rect(center=(self.coord[0], self.coord[1]))
            screen.blit(text_box, center_rect)
        else:
            screen.blit(text_box, self.coord)


    def update(self):
        pass
