

import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState
from src.ecs.components.tags.c_tag_level import CTagLevel
from src.ecs.components.tags.c_tag_lifes import CTagLifes
from src.ecs.components.tags.c_tag_score_text import CTagScoreText
from src.engine.service_locator import ServiceLocator


def system_screen_info(world: esper.World, player_entity: int, explosion_info: dict, interface_info: dict):
    
    pl_t = world.component_for_entity(player_entity, CTagPlayer)
    ## LEVEL
    """components_text = world.get_components(CSurface, CTagLevel)
    
    
    text_surface = ServiceLocator.fonts_service.get(font = interface_info["font"], size= interface_info["text_size"])
    
    for _, (c_s_t, ct_t) in components_text:
        c_s_t.surf = text_surface.render(f"{pl_t.level}", True, (interface_info["text_color"]["R"],interface_info["text_color"]["G"],interface_info["text_color"]["B"]))
      """  
    
    ## LIFES
    components = world.get_components(CSurface, CTagLifes)
    for life_entity, (_, c_t) in components:
        if c_t.life_number > pl_t.current_lifes:
            world.delete_entity(life_entity)
    
    ## SCORE
    components_score = world.get_components(CSurface, CTagScoreText)
    
    text_surface_score = ServiceLocator.fonts_service.get(font = interface_info["font"], size= interface_info["text_size"])
    
    for _, (c_s_t_2, ct_t) in components_score:
        c_s_t_2.surf = text_surface_score.render(f"{pl_t.score}", True, (interface_info["score"]["color"]["R"],interface_info["score"]["color"]["G"],interface_info["score"]["color"]["B"]))
    
            

    