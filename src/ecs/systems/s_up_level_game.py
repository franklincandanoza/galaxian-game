

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
    
    if not len(components_enemy):
        #print("Se acabaron los enemigos")
        
        for _, (c_rl) in components: 
            pass #c_rl.start_config()
            
        create_enemy_spawner_new(world, level_data)
        pl_tp.level += 1
        print(f"Aumentando el jugador a nivel: {pl_tp.level}")
        ServiceLocator.sounds_service.play(path=game_start_cfg["up_level_sound"])

    