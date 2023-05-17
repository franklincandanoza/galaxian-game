

import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.create.prefab_creator import create_player_explosion


def system_collision_player_bullet(world: esper.World, player_entity: int,
                                  level_cfg: dict, explosion_info: dict):
    
    """Detects collision between the player and enemies in the game world.
    
    Args:
    - world (esper.World): The game world containing the entities and components.
    - player_entity (int): The entity ID of the player in the game world.
    - level_cfg (dict): A dictionary containing configuration information about the game level.
    - explosion_info (dict): A dictionary containing the information needed to create an explosion effect.
    """
    
    components = world.get_components(CSurface, CTransform, CTagEnemyBullet)
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)
    
    pl_tp = world.component_for_entity(player_entity, CTagPlayer)

    pl_rect = pl_s.area.copy()
    pl_rect.topleft = pl_t.pos

    for enemy_entity, (c_s, c_t, _) in components:
        ene_rect = c_s.area.copy()
        ene_rect.topleft = c_t.pos
        if ene_rect.colliderect(pl_rect):

            pl_tp.dead_enemies = 0
            pl_t.pos.x = level_cfg["player_spawn"]["position"]["x"] - pl_s.area.w / 2
            pl_t.pos.y = level_cfg["player_spawn"]["position"]["y"] - pl_s.area.h / 2
            create_player_explosion(world, pl_t.pos, explosion_info)
