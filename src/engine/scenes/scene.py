import pygame
import esper

from src.ecs.components.c_input_command import CInputCommand
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_rendering import system_rendering
import enum


scene_name_to_switch = None



class Scene:
    
    class Scenes(enum.Enum):
        MENU_SCENE="MENU_SCENE"
        LEVEL_01="LEVEL_01"
        WIN_SCENE="WIN_SCENE"
        GAME_OVER_SCENE="GAME_OVER_SCENE"
        RETRY_GAME="RETRY_GAME"
        QUIT_TO_MENU="QUIT_TO_MENU"

    
    def __init__(self, screen:pygame.Surface) -> None:
        self.ecs_world = esper.World()
        self.screen = screen

    def do_process_events(self, event:pygame.event):
        system_input_player(self.ecs_world, event, self.do_action)

    def simulate(self, delta_time):
        self.do_update(delta_time)
        self.ecs_world._clear_dead_entities()

    def clean(self):
        self.ecs_world.clear_database()
        self.do_clean()
    
    def switch_scene(self, new_scene_name:"Scene.Scenes"):
        global scene_name_to_switch
        scene_name_to_switch=new_scene_name

    def do_create(self):
        pass

    def do_update(self, delta_time:float):
        pass

    def do_draw(self, screen):
        system_rendering(self.ecs_world, screen)

    def do_action(self, action:CInputCommand):
        pass
    
    def do_clean(self):
        pass
