import pygame

from src.engine.scenes.scene import Scene
from src.create.prefab_creator_interface import TextAlignment, create_text,create_image
from src.ecs.components.c_input_command import CInputCommand 

class MenuScene(Scene):
    
    def do_create(self):
        create_image(self.ecs_world,"assets/img/invaders_logo_title.png",pygame.Vector2(186, 80))
        create_text(self.ecs_world, "MAIN MENU", 16, 
                    pygame.Color(50, 255, 50), pygame.Vector2(260, 150), TextAlignment.CENTER)
        create_text(self.ecs_world, "PRESS Z TO START GAME", 11, 
                    pygame.Color(255, 255, 0), pygame.Vector2(260, 210), TextAlignment.CENTER)
        create_text(self.ecs_world, "Arrows to MOVE(Left/Right) - Z to fire - P to PAUSE", 8, 
                    pygame.Color(150, 150, 255), pygame.Vector2(260, 250), TextAlignment.CENTER)
        
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("START_GAME", pygame.K_z))
        
    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            self.switch_scene(Scene.Scenes.LEVEL_01)
        