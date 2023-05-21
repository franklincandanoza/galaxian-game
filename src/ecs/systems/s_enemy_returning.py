import math
import pygame
import esper 
from src.ecs.components.c_steering_state import CSteeringState,State

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity 
from src.ecs.components.tags.c_tag_enemy_new import CTagEnemyNew
from src.ecs.components.tags.c_tag_grouped_enemy import CTagGroupEnemy
from statistics import mode
def system_enemy_returning(world:esper.World, enemy_sterling_info:dict):
    components = world.get_components(CTransform, CVelocity, CSteeringState, CTagEnemyNew,CSurface)
    
    for enemy_entity, (c_t, c_v, c_ss, c_ten,_) in components:
       if c_ss.state == State.RETURNING:
            
            follow_vector = c_ss.original_pos - c_t.pos
            vel = follow_vector.normalize()*enemy_sterling_info["returning_vel"]    
            c_v.vel = vel
            
            dist_to_origin = c_t.pos.distance_squared_to(c_ss.original_pos)
            
            if dist_to_origin<20*20:
                c_t.pos=pygame.Vector2(c_ss.original_pos.x-_get_position_from(world,c_ten.enemy_type), c_ss.original_pos.y)
                velx=_get_mode(world,c_ten.enemy_type)
                c_v.vel=pygame.Vector2(velx, 0)
                world.remove_component(enemy_entity,CSteeringState)
                world.add_component(enemy_entity, CTagGroupEnemy())
                
    
    
def _get_mode(world:esper.World, enemy_type:str):
    componets = world.get_components( CVelocity, CTagGroupEnemy,CTagEnemyNew) 
    if not componets:
        return 32
    l = [x[0].vel.x for _,x in componets if enemy_type == x[2].enemy_type]
    if not l:
        return 32
    return mode(l)


def _get_position_from(world:esper.World, enemy_type:str):
    print(enemy_type)
    componets = world.get_components( CTransform, CTagGroupEnemy,CTagEnemyNew) 
    if not componets:
        return 0
    lists=[x[2].original_position.x - x[0].pos.x for _,x in componets if enemy_type == x[2].enemy_type]
    if  not lists:
        return 0
    return mode(lists )