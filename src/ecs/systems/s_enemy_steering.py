import math
import pygame
import esper
from src.ecs.components.c_steering import CSteering

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity 
from src.ecs.components.tags.c_tag_enemy_new import CTagEnemyNew
from src.ecs.components.tags.c_tag_player import CTagPlayer 
 
def system_enemy_steering(world:esper.World, ball_cfg:dict, delta_time:float):
    components = world.get_components(CTransform, CVelocity, CSteering, CTagEnemyNew,CSurface)
    for _, (c_t, c_v, c_bs, _,c_s) in components:
        
       
        if c_bs.current_time==0:
            player_dist = _get_player_distance_pos(world,)
            
            # Follow Vector
            c_bs.follow_vector = player_dist - c_t.pos
            
            c_bs.follow_vector = pygame.Vector2( c_bs.follow_vector.x*c_bs.follow_vector.magnitude(),0)
            desired_good_length = 70 #ball_cfg["follow_force"]
            c_bs.follow_vector.scale_to_length(desired_good_length)
            final_vector = c_bs.follow_vector + c_bs.gravity_vector
            c_v.vel = c_v.vel.lerp(final_vector,1)           
            print(c_v.vel)
        elif c_bs.time_to_recalcule <= c_bs.current_time:
            c_bs.current_time = 0
            break
        c_bs.current_time += delta_time


def _get_player_distance_pos(world:esper.World) -> pygame.Vector2:

    components = world.get_components(CTransform, CSurface, CTagPlayer)
    for _, (c_t, c_s, c_bl) in components:
        return c_t.pos + c_s.area.center