
import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_enemy_new import CTagEnemyNew
from src.ecs.components.tags.c_tag_grouped_enemy import CTagGroupEnemy


def system_synchronization_enemies(world: esper.World, screen: pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CVelocity, CTagEnemyNew,CTagGroupEnemy)

    delta = 16
    c_t: CTransform
    c_v: CVelocity
    #print(f"Enemigos encontrados {len(components)}")
    turn= False
    for _, (c_t, c_v, c_e,_) in components:
        
        # Consultamos la posiciòn original
        original_position = c_e.original_position
        
        # Position actual
        current_position = c_t.pos
        
        # Validamos que no haya llegado al límite por la derecha
        if original_position.x + delta < current_position.x:
            turn = True
        
        # Validamos que no haya llegado al límite por la izquierda
        elif original_position.x - delta > current_position.x:
            turn = True
        #print(f"vel {c_v.vel}")    
    for _, (c_t, c_v, c_e,_) in components:
            if turn:
                c_v.vel.x *= -1
                