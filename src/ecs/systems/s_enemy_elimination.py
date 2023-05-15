

import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_text import CTagText
from src.create.prefab_creator import create_explosion_for_elimination, update_dead_enemy_info
from src.engine.service_locator import ServiceLocator


def system_enemy_elimination(world: esper.World, player_entity: int, explosion_info: dict, interface_info: dict, actived_power: bool):
    components_enemy = world.get_components(CSurface, CTransform, CTagEnemy)
    
    components_text = world.get_components(CSurface, CTagText)
    
    pl_t = world.component_for_entity(player_entity, CTagPlayer)
    
    for enemy_entity, (c_s, c_t, c_ene) in components_enemy:
        
        text_surface = ServiceLocator.fonts_service.get(font = interface_info["font"], size= interface_info["text_size"])
        
        for text_entity, (c_s_t, ct_t) in components_text:
            if pl_t.dead_enemies > int(explosion_info["consecutive_enemies_to_eliminate_one"]) - 1:
                c_s_t.surf = text_surface.render(f"{interface_info['active_power']}", True, (interface_info["text_color_ready_power"]["R"],interface_info["text_color_ready_power"]["G"],interface_info["text_color_ready_power"]["B"]))
            else :
                c_s_t.surf = text_surface.render(f"{interface_info['dead_enemies_title']}: {pl_t.dead_enemies}", True, (interface_info["text_color"]["R"],interface_info["text_color"]["G"],interface_info["text_color"]["B"]))
        
        if pl_t.dead_enemies >int(explosion_info["consecutive_enemies_to_eliminate_one"]):
            print("Hay mas de 3  enemigos seguidos muertos. Eliminando")
            world.delete_entity(enemy_entity)   
            pl_t.dead_enemies = 0
            create_explosion_for_elimination(world, c_t.pos, explosion_info)
            return  
            

    