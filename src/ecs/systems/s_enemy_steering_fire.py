import math
import pygame
import esper
from src.create.prefab_creator import create_enemy_bullet
from src.ecs.components.c_enemy_steering_fire import CEnemySteeringFire
from src.ecs.components.c_steering import CSteering

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity 
from src.ecs.components.tags.c_tag_enemy_new import CTagEnemyNew
from src.ecs.components.tags.c_tag_player import CTagPlayer 
 
def system_enemy_steering_fire(world:esper.World, delta_time:float,enemy_bullet_info: dict):
    components = world.get_components(CTransform, CVelocity, CSteering, CSurface, CEnemySteeringFire)
    for _, (c_t, c_v, c_bs, c_s,c_sf) in components:
        
        c_sf:CEnemySteeringFire
        c_sf.current_time +=delta_time
       
        if c_sf.current_time > c_sf.time_to_fire:
            c_sf.bullet_current_time +=delta_time
            if c_sf.bullet_current_time >c_sf.time_between_bullets:
                c_sf.current_bullets-=1
                c_sf.bullet_current_time=0
                if c_sf.current_bullets == 0:
                    c_sf.current_time =0 
                    c_sf.current_bullets = c_sf.bullets  
                player_dist = _get_player_distance_pos(world)
                direction_version = player_dist - c_t.pos
                direction = direction_version.normalize()
                print("disparando")
                create_enemy_bullet(world=world,
                        enemy_pos = c_t.pos.copy(),
                        enemy_size= c_s.area,
                        enemy_bullet_info=enemy_bullet_info,
                        direction=direction)
                
 



 
 
def _get_player_distance_pos(world:esper.World) -> pygame.Vector2:

    components = world.get_components(CTransform, CSurface, CTagPlayer)
    for _, (c_t, c_s, c_bl) in components:

        return c_t.pos + c_s.area.center