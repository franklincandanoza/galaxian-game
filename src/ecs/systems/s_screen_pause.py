import pygame
import esper
import random

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_star import CTagStar
from src.ecs.components.tags.messages.c_tag_pause_message import CTagPauseMessage
from src.ecs.components.tags.messages.c_tag_ready_message import CTagReadyMessage 



def system_screen_pause(world: esper.World, screen: pygame.Surface, delta_time:float):

    components = world.get_components(CSurface, CTagPauseMessage)
    
    c_s: CSurface
    c_tpm: CTagPauseMessage
    for _, (c_s, c_tpm) in components:
        
        c_tpm.current_time+=delta_time
        if c_tpm.is_showing:
            if c_tpm.time_show<=c_tpm.current_time:
                c_tpm.current_time = 0
                c_tpm.is_showing = False
        else:
            if c_tpm.time_hide<=c_tpm.current_time:
                c_tpm.current_time = 0
                c_tpm.is_showing = True
        
        if c_tpm.is_showing:
            alpha = 255
        else:
            alpha = 0
        c_s.surf.set_alpha(alpha)
