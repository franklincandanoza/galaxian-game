
import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_enemy_new import CTagEnemyNew
from src.ecs.components.tags.c_tag_grouped_enemy import CTagGroupEnemy


def system_synchronization_enemies(world: esper.World, screen: pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CTransform, CVelocity, CSurface, CTagEnemyNew,CTagGroupEnemy)

    delta = 20
    c_t: CTransform
    c_v: CVelocity
    c_s: CSurface
    #print(f"Enemigos encontrados {len(components)}")
    for enemy_entity, (c_t, c_v, c_s, c_e,_) in components:
        
        # Consultamos la posiciòn original
        original_position = c_e.original_position
        
        # Position actual
        current_position = c_t.pos
        
        # Validamos que no haya llegado al límite por la derecha
        if original_position.x + delta < current_position.x:
            c_v.vel.x *= -1
        
        # Validamos que no haya llegado al límite por la izquierda
        if original_position.x - delta > current_position.x:
            c_v.vel.x *= -1