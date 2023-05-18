

import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState
from src.ecs.components.tags.c_tag_text import CTagText
from src.ecs.components.tags.c_tag_score_text import CTagScoreText
from src.create.prefab_creator import create_explosion_for_elimination, update_level_info
from src.engine.service_locator import ServiceLocator


def system_screen_info(world: esper.World, player_entity: int, explosion_info: dict, interface_info: dict):
    
    ## LEVEL
    components_text = world.get_components(CSurface, CTagText)
    pl_t = world.component_for_entity(player_entity, CTagPlayer)
    
    text_surface = ServiceLocator.fonts_service.get(font = interface_info["font"], size= interface_info["text_size"])
    
    for _, (c_s_t, ct_t) in components_text:
        c_s_t.surf = text_surface.render(f"{pl_t.level}", True, (interface_info["text_color"]["R"],interface_info["text_color"]["G"],interface_info["text_color"]["B"]))
    
    ## SCORE
    components_score = world.get_components(CSurface, CTagScoreText)
    
    text_surface_score = ServiceLocator.fonts_service.get(font = interface_info["font"], size= interface_info["text_size"])
    
    for _, (c_s_t_2, ct_t) in components_score:
        c_s_t_2.surf = text_surface_score.render(f"{pl_t.score}", True, (interface_info["score"]["R"],interface_info["score"]["G"],interface_info["score"]["B"]))
    
            

    