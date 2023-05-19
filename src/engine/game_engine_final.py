import json
import pygame

from src.ecs.components.c_input_command import CInputCommand
from src.engine.scenes import scene
from src.game.game_over_scene import GameOverScene
from src.game.menu_scene import MenuScene
from src.game.play_scene import PlayScene
from src.game.win_scene import WinScene
import asyncio
class GameEngine:
    def __init__(self) -> None:
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self._window_cfg = json.load(window_file)

        pygame.init()
        pygame.display.set_caption(self._window_cfg["title"])
        self.screen = pygame.display.set_mode(
            (self._window_cfg["size"]["w"], self._window_cfg["size"]["h"]),
            pygame.SCALED)

        self._clock = pygame.time.Clock()
        self._framerate = self._window_cfg["framerate"]
        self._delta_time = 0
        self._bg_color = pygame.Color(self._window_cfg["bg_color"]["r"],
                                     self._window_cfg["bg_color"]["g"],
                                     self._window_cfg["bg_color"]["b"])
        self.is_running = False
        self.is_paused = False
        self.actived_power = False
        self._scenes:dict[scene.Scene.Scenes, scene.Scene] = {}
        
        self._scenes[scene.Scene.Scenes.MENU_SCENE] = MenuScene(self.screen)
        self._scenes[scene.Scene.Scenes.LEVEL_01] = PlayScene("assets/cfg/level_01.json", self.screen)
        self._scenes[scene.Scene.Scenes.WIN_SCENE] = WinScene(self.screen)
        self._scenes[scene.Scene.Scenes.GAME_OVER_SCENE] = GameOverScene(self.screen)
        self._current_scene:scene.Scene = None
        self._scene_name_to_switch:str = None

    async def run(self, start_scene_name:scene.Scene.Scenes = scene.Scene.Scenes.MENU_SCENE) -> None:
        self.is_running = True
        self._current_scene = self._scenes[start_scene_name]
        self._create()
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            self._handle_switch_scene()
            await asyncio.sleep(0)
        self._do_clean()
    
    def _create(self):
        self._current_scene.do_create()

    def _calculate_time(self):
        self._clock.tick(self._framerate)
        self._delta_time = self._clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            self._current_scene.do_process_events(event)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        self._current_scene.simulate(self._delta_time)

    def _draw(self):
        self.screen.fill(self._bg_color)        
        self._current_scene.do_draw(self.screen)
        pygame.display.flip()

    def _handle_switch_scene(self):
        if scene.scene_name_to_switch is not None:
            self._current_scene.clean()
            self._current_scene = self._scenes[scene.scene_name_to_switch]
            self._current_scene.do_create()
            scene.scene_name_to_switch = None

    def _do_action(self, action:CInputCommand):        
        self._current_scene.do_action(action)

    def _do_clean(self):
        if self._current_scene is not None:
            self._current_scene.clean()
        pygame.quit()
        