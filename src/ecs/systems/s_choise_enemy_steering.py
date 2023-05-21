


import esper
import random
import pygame
from src.ecs.components.c_enemy_choose_steering import CEnemyChooseSteering
from src.ecs.components.c_enemy_steering_fire import CEnemySteeringFire
from src.ecs.components.c_steering import CSteering
from src.ecs.components.c_steering_state import CSteeringState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_grouped_enemy import CTagGroupEnemy
from src.engine.service_locator import ServiceLocator
def system_choose_enemy_steering(world:esper.World,enemy_steering_info:dict, delta_time:float):

    component = world.get_component(CEnemyChooseSteering)
 
    for _, (c_cs) in component: 
        if world.get_components(CSteeringState):
            continue
        c_cs.current_time += delta_time
        if c_cs.current_time>=c_cs.time_steering:
            c_cs.current_time = 0
            number_of_enemies = random.randint(c_cs.enemies_to_steering_min,c_cs.enemies_to_steering_max)
            components_enemy = world.get_component(CTagGroupEnemy)
            component_enemy_list = [enemy_entity for enemy_entity,_ in components_enemy]
                           
            if not component_enemy_list:
                break
            if len(component_enemy_list)<number_of_enemies:
                number_of_enemies=len(component_enemy_list)
            components_enemy = random.sample(component_enemy_list,number_of_enemies)
            for entity in components_enemy:
                c_t=world.component_for_entity(entity,CTransform)
                world.remove_component(entity,CTagGroupEnemy)
                world.add_component(entity,CSteering(enemy_steering_info))
                world.add_component(entity,CSteeringState(c_t.pos.copy()))
                world.add_component(entity,CEnemySteeringFire(enemy_steering_info["fire"]))
                ServiceLocator.sounds_service.play(enemy_steering_info["enemy_launch"])
                
 