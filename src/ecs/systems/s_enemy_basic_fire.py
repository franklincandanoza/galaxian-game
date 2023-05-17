


import esper
from src.ecs.components.c_enemy_basic_fire import CEnemyBasicFire
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_enemy_new import CTagEnemyNew
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.create.prefab_creator import create_enemy_bullet, create_enemy_explosion
import random

def system_basic_enemy_fire(world: esper.World,delta_time:float, enemy_basic_fire:dict,enemy_bullet_info: dict) -> None:
    
    component_enemy_basic_fire = world.get_component(CEnemyBasicFire)[0][1]
    component_enemy_basic_fire.time += delta_time
    if  component_enemy_basic_fire.time< component_enemy_basic_fire.frequency_fire:
        return
    component_enemy_basic_fire.time=0
    
    bullets = random.randrange(*component_enemy_basic_fire.bullets)

    components_enemy = world.get_components(CSurface,CTransform, CTagEnemyNew)
    
    bullets=min(bullets,len(components_enemy))
    
    enemies_to_fire = random.sample(range(0, len(components_enemy)), bullets) 
    
    for index,(enemy_entity, (c_s, c_t, c_ene)) in enumerate(components_enemy):
        
        if index in enemies_to_fire:
            create_enemy_bullet(world=world,
                    enemy_pos = c_t.pos.copy(),
                    enemy_size= c_s.area,
                    enemy_bullet_info=enemy_bullet_info)
        
 


