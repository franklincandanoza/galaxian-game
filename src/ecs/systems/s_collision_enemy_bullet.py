

import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_enemy_new import CTagEnemyNew
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.create.prefab_creator import create_enemy_explosion


def system_collision_enemy_bullet(world: esper.World, explosion_info: dict, player_entity: int) -> None:
    """
    Deletes enemy and bullet entities when they collide and creates an explosion.
    
    Args:
    - world (esper.World): The World instance where the entities and their components are stored.
    - explosion_info (dict): A dictionary containing information about the explosion to be created.
    - player_entity (int): The entity ID of the player.
    
    Returns:
    - None
    """
    components_enemy = world.get_components(CSurface, CTransform, CTagEnemyNew)
    components_bullet = world.get_components(CSurface, CTransform, CTagBullet)
    
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
                pl_t.score += c_ene.enemy_score
                create_enemy_explosion(world, c_t.pos, explosion_info)
