"""
This file contains the Control class which manages the primary control flow
for the entire program.
"""

import os
import pygame as pg

from collections import OrderedDict
from importlib import import_module

from data.core import constants
from data.components import state_machine


class Control(object):
    """
    Control class for entire project. Contains the game loop, and contains
    the event_loop which passes events to the state_machine as needed.
    Autodetection for both core states and game states is also handled here.
    """
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.render_surf = pg.Surface(constants.RENDER_SIZE).convert()
        self.set_scale()
        self.done = False
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.show_fps = False
        self.now = 0.0
        self.keys = pg.key.get_pressed()
        self.state_dict = OrderedDict()
        self.game_thumbs = OrderedDict()
        self.start_music()
        self.auto_discovery("states")
        self.auto_discovery("games")
        self.state_machine = state_machine.StateMachine()

    def start_music(self):
        pg.mixer.music.load(constants.TITLE_TRACK)
        pg.mixer.music.set_volume(0.2)
        if not constants.ARGS["music_off"]:
            pg.mixer.music.play(-1)

    def auto_discovery(self, scene_folder):
        """
        Scan a folder, load states found in it, and insert them in the
        state_dict.  If the scenefolder is "games" it will also load the
        lobby thumbnail for that game and place it in the game_thumbs dict.
        """
        scene_folder_path = os.path.join(".", "data", scene_folder)
        scene_package = "data.{}.".format(scene_folder)
        exclude_endings = (".py", ".pyc", "__pycache__")
        for folder in os.listdir(scene_folder_path):
            if any(folder.endswith(end) for end in exclude_endings):
                continue
            state = self.load_state_from_path(folder, scene_package)
            self.state_dict[folder] = state
            if scene_folder == "games":
                path = os.path.join(scene_folder_path, folder, "lobby_thumb.png")
                try:
                    thumb = pg.image.load(path).convert()
                except pg.error:
                    thumb = constants.GFX["default_image"]
                self.game_thumbs[folder] = thumb

    @staticmethod
    def load_state_from_path(folder, package="data.states."):
        """
        Load a state from disk, but do not register it
        """
        try:
            scene_module = import_module(package + folder)
            state = scene_module.Scene
            return state
        except Exception as e:
            template = "{} failed to load or is not a valid game package"
            print(e)
            print(template.format(folder))
            raise

    def start(self, start_state):
        """
        Setup the state machine with the states we autodetected.
        It also gives the state machine a copy of the game_thumbs dict
        for convenience.
        """
        self.state_machine.setup_states(self.state_dict)
        self.state_machine.game_thumbs = self.game_thumbs
        self.state_machine.start_state(start_state)

    def update(self, dt):
        """
        Checks if the state_machine is done and then updates the state_machine
        with the appropiate arguments.
        """
        self.now = pg.time.get_ticks()
        if self.state_machine.done:
            self.done = True
        machine_args = self.render_surf, self.keys, self.now, dt, self.scale
        self.state_machine.update(*machine_args)

    def render(self):
        """
        Scale the render surface if not the same size as the display surface.
        The render surface is then drawn to the screen.
        """
        if constants.RENDER_SIZE != self.screen_rect.size:
            scale_args = (self.render_surf, self.screen_rect.size, self.screen)
            pg.transform.smoothscale(*scale_args)
        else:
            self.screen.blit(self.render_surf, (0, 0))

    def event_loop(self):
        """
        Process all events and pass them down to the state_machine.
        The f5 key globally turns on/off the display of FPS in the caption.
        Screen resizes also handled here.
        """
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                self.keys = pg.key.get_pressed()
                self.toggle_show_fps(event.key)
                if event.key == pg.K_PRINT:
                    # Print screen for full render-sized screencaps.
                    pg.image.save(self.render_surf, "screenshot.png")
            elif event.type == pg.KEYUP:
                self.keys = pg.key.get_pressed()
            elif event.type == pg.VIDEORESIZE:
                self.on_resize(event.size)
                pg.event.clear(pg.VIDEORESIZE)
            self.state_machine.get_event(event, self.scale)

    def on_resize(self, size):
        """
        If the user resized the window, change to the next available
        resolution depending on if scaled up or scaled down.
        """
        if size == self.screen_rect.size:
            return
        res_index = constants.RESOLUTIONS.index(self.screen_rect.size)
        adjust = 1 if size > self.screen_rect.size else -1
        if 0 <= res_index + adjust < len(constants.RESOLUTIONS):
            new_size = constants.RESOLUTIONS[res_index + adjust]
        else:
            new_size = self.screen_rect.size
        self.screen = pg.display.set_mode(new_size, pg.RESIZABLE)
        self.screen_rect.size = new_size
        self.set_scale()

    def set_scale(self):
        """
        Reset the ratio of render size to window size.
        Used to make sure that mouse clicks are accurate on all resolutions.
        """
        w_ratio = constants.RENDER_SIZE[0] / float(self.screen_rect.w)
        h_ratio = constants.RENDER_SIZE[1] / float(self.screen_rect.h)
        self.scale = (w_ratio, h_ratio)

    def toggle_show_fps(self, key):
        """
        Press f5 to turn on/off displaying the framerate in the caption.
        """
        if key == pg.K_F5:
            self.show_fps = not self.show_fps
            if not self.show_fps:
                pg.display.set_caption(constants.CAPTION)

    def main(self):
        """
        Main loop for entire program.
        """
        while not self.done:
            time_delta = self.clock.tick(self.fps)
            self.event_loop()
            self.update(time_delta)
            self.render()
            pg.display.update()
            if self.show_fps:
                fps = self.clock.get_fps()
                with_fps = "{} - {:.2f} FPS".format(constants.CAPTION, fps)
                pg.display.set_caption(with_fps)
