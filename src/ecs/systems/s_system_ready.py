import pygame
import esper
import random
from src.ecs.components.c_ready_level import CReadyLevel

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_star import CTagStar
from src.ecs.components.tags.messages.c_tag_ready_message import CTagReadyMessage
from src.engine.service_locator import ServiceLocator

def text_objects(text, font,start_game_info:dict):
    c = start_game_info["color"]
    color = (c["r"],c["g"],c["b"])
    text_surface = font.render(text, True, color)
    return text_surface

def system_ready_level(world: esper.World,delta_time:float,start_game_info:dict,screen:pygame.Surface):
    components = world.get_component(CReadyLevel)
    
    c_rl: CReadyLevel
    
    for _, (c_rl) in components: 
        component = world.get_component(CTagReadyMessage) 
        c_rl.time +=delta_time
        
        if c_rl.time >= c_rl.time_to_ready:
            c_rl.ready = True
        elif c_rl.time >= start_game_info["time_to_hide_ready"]:

            if not len(component):
                return
            world.delete_entity(component[0][0])
            
        elif c_rl.time >= start_game_info["time_to_show_ready"]:

            if len(component):
                return
            
                    
            largeText = ServiceLocator.fonts_service.get(start_game_info["font"],start_game_info["size"])

            text_surf = text_objects(start_game_info["text"], largeText,start_game_info) 
            
            ready_message = world.create_entity()
            world.add_component(ready_message, CSurface.from_surface(text_surf))
            world.add_component(ready_message, CTagReadyMessage())
            world.add_component(ready_message,CTransform(pygame.Vector2(screen.get_rect().w/2-text_surf.get_width()/2 , screen.get_rect().h/2)))
            

