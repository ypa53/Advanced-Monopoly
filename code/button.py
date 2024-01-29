import pygame
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'  # Hide pygame support prompt


class state():
    disable = False

    def switch(self, state):
        self.__class__ = state


class avail(state):
    disable = False


class unavail(state):
    disable = True


class Button:
    def __init__(self, x, y, width, height, text, color=(255, 255, 255), hover_color=(200, 200, 200),
                 text_color=(0, 0, 0), font_size=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.font = pygame.font.SysFont("comicsansms", self.font_size)
        self.is_hovered = False
        self.state = avail()

    def change(self, state):
        self.state.switch(state)

    def draw(self, surface):
        if self.is_hovered or self.state.disable == True:
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)
        lines = self.text.split("\n")
        text_height = len(lines) * self.font_size
        y_offset = (self.rect.height - text_height) // 2  # Calculate the vertical offset for centering the text
        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, self.text_color)
            text_rect = text_surface.get_rect(
                center=(self.rect.centerx, self.rect.top + y_offset + (i + 0.5) * self.font_size))
            surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if self.state.disable == False:
            if event.type == pygame.MOUSEMOTION:
                self.is_hovered = self.rect.collidepoint(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_hovered and event.button == 1:  # Left mouse button
                    return True
            return False
        else:
            pass


class state():
    disable = False

    def switch(self, state):
        self.__class__ = state


class avail(state):
    disable = False


class unavail(state):
    disable = True


class img_Button:
    def __init__(self, x, y, width, height, image, color=(205, 230, 208), hover_color=(200, 200, 200)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.image = image
        self.is_hovered = False
        self.state = avail()

    def draw(self, surface):
        if self.is_hovered:
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.image, self.rect)

    def change(self, state):
        self.state.switch(state)

    def handle_event(self, event):
        if self.state.disable == False:
            if event.type == pygame.MOUSEMOTION:
                self.is_hovered = self.rect.collidepoint(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_hovered and event.button == 1:  # Left mouse button
                    return True
            return False
        else:
            pass


class img:
    def __init__(self, x, y, width, height, image):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image

    def draw(self, surface):
        surface.blit(self.image, self.rect)
