import sys

import pygame
from pygame.math import Vector2 as vector
from pygame.mouse import get_pos as mouse_pos
from pygame.mouse import get_pressed as mouse_buttons

from settings import *


class Editor:
    def __init__(self):
        # Main setup.
        self.display_surface = pygame.display.get_surface()

        # Navigation.
        self.origin = vector()
        self.pan_active = False
        self.pan_offset = vector()

        # Support lines.
        self.support_line_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.support_line_surf.set_colorkey('green')
        self.support_line_surf.set_alpha(30)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.pan_input(event)

    def pan_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[1]:
            self.pan_active = True
            self.pan_offset = vector(mouse_pos()) - self.origin

        if not mouse_buttons()[1]:
            self.pan_active = False

        if self.pan_active:
            self.origin = vector(mouse_pos()) - self.pan_offset

        # Mouse wheel.
        if event.type == pygame.MOUSEWHEEL:
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                self.origin.y -= event.y * 50
            else:
                self.origin.x -= event.y * 50
            # print(event.y)

        return None

    def draw_tile_lines(self):
        cols = WINDOW_WIDTH // TILE_SIZE
        rows = WINDOW_HEIGHT // TILE_SIZE

        offset_vector = vector(
            x=self.origin.x - int(self.origin.x / TILE_SIZE) * TILE_SIZE,
            y=self.origin.y - int(self.origin.y / TILE_SIZE) * TILE_SIZE,
        )

        self.support_line_surf.fill('green')

        for col in range(cols + 1):
            x = offset_vector.x + col * TILE_SIZE
            pygame.draw.line(
                self.support_line_surf, LINE_COLOR, (x, 0), (x, WINDOW_HEIGHT)
            )

        for row in range(rows + 1):
            y = offset_vector.y + row * TILE_SIZE
            pygame.draw.line(
                self.support_line_surf, LINE_COLOR, (0, y), (WINDOW_WIDTH, y)
            )

        self.display_surface.blit(self.support_line_surf, (0, 0))

        return None

    def run(self, dt):
        self.event_loop()

        # Draw
        self.display_surface.fill('white')
        self.draw_tile_lines()
        pygame.draw.circle(self.display_surface, 'red', self.origin, 10)
