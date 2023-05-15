import esper
import pygame

from src.create.prefab_creator import create_enemy_square, create_enemy_hunter, create_enemy_new_by_type
from src.ecs.components.c_enemy_spawner_new import CEnemySpawnerNew, SpawnEventDataNew


def system_enemy_spawner_new(world: esper.World, enemies_data: dict, screen: pygame.Surface ):
    components = world.get_component(CEnemySpawnerNew)
    screen_rect = screen.get_rect()
                    
                    
    distancia = 15
    c_spw: CEnemySpawnerNew
    for _,  c_spw in components:
        spw_evt: SpawnEventDataNew
        for spw_evt in c_spw.spawn_event_data:
            
            if spw_evt.type == "Type01" and not spw_evt.triggered:
                space = 0
                izquierda = True
                for i in range(1,spw_evt.quantity+1): 
                    
                    #Calculamos espacio entre enemigos por línea
                    medium_screen = screen_rect.width / 2
                    
                    if izquierda:
                        x = medium_screen - (distancia * i)
                        izquierda = False
                    else:
                        x = medium_screen + (distancia * i)
                        izquierda = True
                    
                    print(f"Un enemigo Type01 en {x}")
                    position = pygame.Vector2(x, 50)
                    spw_evt.triggered = True
                    create_enemy_new_by_type(world, position, enemies_data[spw_evt.type], spw_evt.type)
                    space = x
            
            elif spw_evt.type == "Type02" and not spw_evt.triggered:
                space = 0
                for i in range(1,spw_evt.quantity+1): 
                    
                    
                    #Calculamos espacio entre enemigos por línea
                    medium_screen = screen_rect.width / 2
                    
                    if izquierda:
                        x = medium_screen - (distancia * i)
                        izquierda = False
                    else:
                        x = medium_screen + (distancia * i)
                        izquierda = True
                    
                    print(f"Un enemigo Type02 en {x}")
                    position = pygame.Vector2(x, 80)
                    spw_evt.triggered = True
                    create_enemy_new_by_type(world, position, enemies_data[spw_evt.type], spw_evt.type)
                    space = x
            elif spw_evt.type == "Type03" and not spw_evt.triggered:
                space = 0
                for i in range(2,spw_evt.quantity+1): 
                    
                    
                    #Calculamos espacio entre enemigos por línea
                    medium_screen = screen_rect.width / 2
                    
                    if izquierda:
                        x = medium_screen - (distancia * i)
                        izquierda = False
                    else:
                        x = medium_screen + (distancia * i)
                        izquierda = True
                    
                    print(f"Un enemigo Type03 en {x}")
                    position = pygame.Vector2(x, 110)
                    spw_evt.triggered = True
                    create_enemy_new_by_type(world, position, enemies_data[spw_evt.type], spw_evt.type)
                    space = x
            elif spw_evt.type == "Type04" and not spw_evt.triggered:
                space = 0
                #izquierda = True
                for i in range(1,spw_evt.quantity+1): 
                    
                    #Calculamos espacio entre enemigos por línea
                    medium_screen = screen_rect.width / 2
                    
                    if izquierda:
                        x = medium_screen - (distancia * i)
                        izquierda = False
                    else:
                        x = medium_screen + (distancia * i)
                        izquierda = True
                    
                    print(f"Un enemigo Type04 en {x}")
                    position = pygame.Vector2(x, 140)
                    spw_evt.triggered = True
                    create_enemy_new_by_type(world, position, enemies_data[spw_evt.type], spw_evt.type)
                    space = x
            else:
                pass
                #print("Type not supported")