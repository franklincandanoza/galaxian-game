import esper
import pygame

from src.create.prefab_creator import create_enemy_square, create_enemy_hunter, create_enemy_new_by_type
from src.ecs.components.c_enemy_spawner_new import CEnemySpawnerNew, SpawnEventDataNew


def system_enemy_spawner_new(world: esper.World, enemies_data: dict, screen: pygame.Surface ):
    components = world.get_component(CEnemySpawnerNew)
    screen_rect = screen.get_rect()
    last_line = 50          
                    
    distancia = 15
    c_spw: CEnemySpawnerNew
    for _,  c_spw in components:
        spw_evt: SpawnEventDataNew
        for spw_evt in c_spw.spawn_event_data:
            
            if spw_evt.type == "Type01" and not spw_evt.triggered:
                last_line = create_enemy(quantity=spw_evt.quantity, distance_y=last_line, screen=screen,spw_evt= spw_evt, world = world, enemies_data=enemies_data)
            elif spw_evt.type == "Type02" and not spw_evt.triggered:
                last_line = create_enemy(quantity=spw_evt.quantity, distance_y=last_line, screen=screen,spw_evt= spw_evt, world = world, enemies_data=enemies_data)
            elif spw_evt.type == "Type03" and not spw_evt.triggered:
                last_line = create_enemy(quantity=spw_evt.quantity, distance_y=last_line, screen=screen,spw_evt= spw_evt, world = world, enemies_data=enemies_data)
            elif spw_evt.type == "Type04" and not spw_evt.triggered:
                last_line = create_enemy(quantity=spw_evt.quantity, distance_y=last_line, screen=screen,spw_evt= spw_evt, world = world, enemies_data=enemies_data)
            else:
                pass
                
def create_enemy(quantity: int, distance_y:int, screen: pygame.Surface, spw_evt: SpawnEventDataNew, world: esper.World, enemies_data: dict)-> int:
    
    delta_y = 20
    last_y = distance_y
    for y in range(0, spw_evt.lines):
        print(f"Type: {spw_evt.type} y linea: {y} con posicion en y {last_y}")
        distance_x = 15
        screen_rect = screen.get_rect()
        izquierda = True
        for i in range(1,quantity+1): 
            
            #Calculamos espacio entre enemigos por línea
            medium_screen = screen_rect.width / 2
            
            if izquierda:
                x = medium_screen - (distance_x * i)
                izquierda = False
            else:
                x = medium_screen + (distance_x * i)
                izquierda = True
            
            position = pygame.Vector2(x, last_y)
            
            spw_evt.triggered = True
            
            create_enemy_new_by_type(world, position, enemies_data[spw_evt.type], spw_evt.type)
        
        last_y = last_y + delta_y
            
    return last_y
        