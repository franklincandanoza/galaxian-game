

import esper
from src.ecs.components.c_enemy_steering_fire import CEnemySteeringFire
from src.ecs.components.c_steering import CSteering, State
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_enemy_new import CTagEnemyNew
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.create.prefab_creator import create_enemy_explosion
import pygame

def system_collision_enemy_screen(world: esper.World, 
                                  screen: pygame.Surface) -> None:
    """
    Deletes enemy and bullet entities when they collide and creates an explosion.
    
    Args:
    - world (esper.World): The World instance where the entities and their components are stored.
    - explosion_info (dict): A dictionary containing information about the explosion to be created.
    - player_entity (int): The entity ID of the player.
    
    Returns:
    - None
    """
    components_enemy = world.get_components(CSurface, CTransform, CSteering,CVelocity)
    
    for enemy_entity, (c_s, c_t, c_st,c_v) in components_enemy:
        
        ene_rect = c_s.area.copy()
        ene_rect.topleft = c_t.pos
        if not ene_rect.colliderect(screen.get_rect()):
            print("no contiene")
            c_st.state=State.RETURNING
            c_t.pos=pygame.Vector2(c_t.pos.x,0)
            c_v.vel=pygame.Vector2(0,0)
            world.remove_component(enemy_entity,CEnemySteeringFire)
            world.remove_component(enemy_entity,CSteering)
            