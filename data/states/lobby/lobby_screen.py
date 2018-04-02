import math
import pygame as pg

from collections import OrderedDict

from data.core import tools, prepare
from data.components.labels import Button, ButtonGroup
from data.components.special_buttons import GameButton, NeonButton
from data.components.animation import Animation
from data.components.state_machine import _State


class LobbyScreen(_State):
    """
    This state represents the lobby where the player can choose
    which game they want to play or view their high scores. This is also
    the exit point for the game.
    """
    per_page = 6

    def __init__(self, controller):
        super(LobbyScreen, self).__init__(controller)
        self.animations = pg.sprite.Group()

    def update_screen_buttons(self, games):
        screen_rect = pg.Rect((0, 0), prepare.RENDER_SIZE)
        number_of_pages = int(math.ceil(len(games) / float(self.per_page)))
        self.loop_length = prepare.RENDER_SIZE[0] * number_of_pages
        self.game_buttons = self.make_game_pages(games, screen_rect, self.per_page)
        nav_buttons = self.make_navigation_buttons(screen_rect)
        main_buttons = self.make_main_buttons(screen_rect)
        self.buttons = ButtonGroup(nav_buttons, main_buttons)

    def make_game_pages(self, games, screen_rect, per):
        games_list = list(games.keys())
        groups = (games_list[i:i+per] for i in range(0, len(games), per))
        columns = 3
        width, height = GameButton.width, GameButton.height
        spacer_x, spacer_y = 50, 80
        start_x = (screen_rect.w - width * columns - spacer_x * (columns-1))//2
        start_y = screen_rect.top + 105
        step_x, step_y = width + spacer_x, height + spacer_y
        buttons = ButtonGroup()
        for offset,group in enumerate(groups):
            offset *= prepare.RENDER_SIZE[0]
            for i,game in enumerate(group):
                y, x = divmod(i, columns)
                pos = (start_x + step_x * x + offset, start_y + step_y * y)
                GameButton(pos, game, games[game], self.change_state, buttons)
        return buttons

    def make_navigation_buttons(self, screen_rect):
        sheet = prepare.GFX["nav_buttons"]
        size = (53, 50)
        y = 530
        from_center = 15
        icons = tools.strip_from_sheet(sheet, (0, 0), size, 4)
        buttons = ButtonGroup()
        l_kwargs = {"idle_image" : icons[0], "hover_image" : icons[1],
                    "call" : self.scroll_page, "args" : 1,
                    "bindings" : [pg.K_LEFT, pg.K_KP4]}
        r_kwargs = {"idle_image"  : icons[2], "hover_image" : icons[3],
                    "call" : self.scroll_page, "args" : -1,
                    "bindings" : [pg.K_RIGHT, pg.K_KP6]}
        left = Button(((0, y), size), buttons, **l_kwargs)
        left.rect.right = screen_rect.centerx - from_center
        right = Button(((0, y), size), buttons, **r_kwargs)
        right.rect.x = screen_rect.centerx + from_center
        return buttons

    def make_main_buttons(self, screen_rect):
        buttons = ButtonGroup()
        pos = (9, screen_rect.bottom-(NeonButton.height+11))
        NeonButton(pos, "Credits", 32, self.change_state, "credits", buttons)
        pos = (screen_rect.right-(NeonButton.width+10),
               screen_rect.bottom-(NeonButton.height+11))
        NeonButton(pos, "High Scores", 28, self.change_state, "high_scores",
                   buttons)
        pos = (screen_rect.centerx-(NeonButton.width//2),
               screen_rect.bottom-(NeonButton.height+11))
        NeonButton(pos, "Exit", 32, self.exit_game, None,
                   buttons, bindings=[pg.K_ESCAPE])
        rect_style = (screen_rect.left, screen_rect.top, 150, 95)
        return buttons

    def scroll_page(self, mag):
        if not self.animations and len(self.game_buttons) > self.per_page:
            for game in self.game_buttons:
                self.normalize_scroll(game, mag)
                fx, fy = game.rect.x+prepare.RENDER_SIZE[0]*mag, game.rect.y
                ani = Animation(x=fx, y=fy, duration=350.0,
                                transition='in_out_quint', round_values=True)
                ani.start(game.rect)
                self.animations.add(ani)
            prepare.SFX["cardplace4"].play()

    def normalize_scroll(self, game, mag):
        if game.rect.x < 0 and mag == -1:
            game.rect.x += self.loop_length
        elif game.rect.x >= prepare.RENDER_SIZE[0] and mag == 1:
            game.rect.x -= self.loop_length

    def startup(self, persistent):
        super(LobbyScreen, self).startup(persistent)
        games = self.controller.game_thumbs
        self.update_screen_buttons(games)

    def exit_game(self, *args):
        self.done = True
        self.quit = True

    def change_state(self, next_state):
        self.done = True
        self.next = next_state

    def get_event(self, event, scale=(1,1)):
        if event.type == pg.QUIT:
            self.exit_game()
        else:
            self.buttons.get_event(event)
            self.game_buttons.get_event(event)

    def update(self, surface, keys, current_time, dt, scale):
        mouse_pos = tools.scaled_mouse_pos(scale)
        self.buttons.update(mouse_pos)
        self.game_buttons.update(mouse_pos)
        self.animations.update(dt)
        self.draw(surface)

    def draw(self, surface):
        rect = surface.get_rect()
        surface.fill(prepare.BACKGROUND_BASE)
        self.buttons.draw(surface)
        for button in self.game_buttons:
            if button.rect.colliderect(rect):
                button.draw(surface)
