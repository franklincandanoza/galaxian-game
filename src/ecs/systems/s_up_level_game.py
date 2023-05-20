

import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_ready_level import CReadyLevel
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_enemy_new import CTagEnemyNew
from src.engine.service_locator import ServiceLocator
from src.create.prefab_creator import create_enemy_explosion, create_enemy_spawner_new


def system_up_level_game(world: esper.World, explosion_info: dict, player_entity: int, game_start_cfg : dict, level_data: dict) -> None:
    """
    Deletes enemy and bullet entities when they collide and creates an explosion.
    
    Args:
    - world (esper.World): The World instance where the entities and their components are stored.
    - explosion_info (dict): A dictionary containing information about the explosion to be created.
    - player_entity (int): The entity ID of the player.
    
    Returns:
    - None
    """
    pl_tp = world.component_for_entity(player_entity, CTagPlayer)
    components_enemy = world.get_components(CSurface, CTransform, CTagEnemyNew)
    
    # Identificar si está ready el juego
    components = world.get_component(CReadyLevel)
    
    #print(f"hay ready {len(components)}")
    
    enemigos_ene_el_mundo = len(components_enemy)
    
    if not len(components_enemy):
        #print("Se acabaron los enemigos")
        
        for _, (c_rl) in components: 
            pass #c_rl.start_config()
            
        create_enemy_spawner_new(world, level_data)
        pl_tp.level += 1
        print(f"Aumentando el jugador a nivel: {pl_tp.level}")
        ServiceLocator.sounds_service.play(path=game_start_cfg["up_level_sound"])
    else:
        pass
        ##print(f"{enemigos_ene_el_mundo} enemigos en el mundo")
        
    """
    pl_t = world.component_for_entity(player_entity, CTagPlayer)
    
    for enemy_entity, (c_s, c_t, c_ene) in components_enemy:
        
        ene_rect = c_s.area.copy()
        ene_rect.topleft = c_t.pos
        for bullet_entity, (c_b_s, c_b_t, _) in components_bullet:
            bull_rect = c_b_s.area.copy()
            bull_rect.topleft = c_b_t.pos
            if ene_rect.colliderect(bull_rect):
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)
                pl_t.dead_enemies = pl_t.dead_enemies + 1
                create_enemy_explosion(world, c_t.pos, explosion_info)
    """