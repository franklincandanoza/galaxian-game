

import esper
import pygame
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_level import CTagLevel
from src.ecs.components.tags.c_tag_fixed_flag import CTagFixedFlag
from src.ecs.components.tags.c_tag_level_text import CTagLevelText
from src.engine.service_locator import ServiceLocator
from src.create.prefab_creator import create_sprite


def system_screen_level(world: esper.World, player_entity: int, explosion_info: dict, interface_info: dict):
    
    """
    Update the screen level information based on the current level.

    Args:
        world (esper.World): The world containing the entities and components.
        player_entity (int): The entity ID of the player.
        explosion_info (dict): A dictionary containing explosion information.
        interface_info (dict): A dictionary containing interface information.

    Returns:
        None

    Raises:
        None
    """
    
    ## LEVEL
    components = world.get_components(CSurface, CTagLevel)
    pl_t = world.component_for_entity(player_entity, CTagPlayer)
    
    # Obtenemos el nivel actual
    current_level = pl_t.level
    
    # Obtenemos el número de niveles requeridos para pintar el número
    level_to_show_number = interface_info["level_number_to_show_number"]
    
    # Validamos si ponemos el número del ninel actual
    pos : pygame.Vector2
    if current_level >= level_to_show_number:
        
        # Eliminamos las banderas
        for life_entity, (_, c_t) in components:
            pos = c_t.pos
            world.delete_entity(life_entity)
        
        components_text = world.get_components(CSurface, CTagLevelText)
        text_surface = ServiceLocator.fonts_service.get(font = interface_info["font"], size= interface_info["text_size"])
        if len(components_text)>0:
            for entity, (c_s, _) in components_text:
                c_s.surf = text_surface.render(f"{pl_t.level}", True, (interface_info["text_color"]["R"],interface_info["text_color"]["G"],interface_info["text_color"]["B"]))
                
        else: 
            
            create_fized_flag(x_pos = pos.x, world = world, interface_info=interface_info)
            
            new_pos = pygame.Vector2(pos.x + 15, pos.y)
            player_sprite = text_surface.render(f"{pl_t.level} ", True, (interface_info["text_color"]["R"],interface_info["text_color"]["G"],interface_info["text_color"]["B"]))
            
            vel = pygame.Vector2(0, 0)
            game_info_entity = create_sprite(world, new_pos, vel, player_sprite)
            world.add_component(game_info_entity, CTagLevelText(pos=pos))
            
            
        # Creamos la superficie para el texto
        
        
    else:
        
        if len(components) < current_level:
        
        # Pintamos el número de banderas del nivel
        #print("Pintando banderas")
            distance_x = 10
            start_x = interface_info["level_info_position"]["x"]
            start_x_current = start_x + (len(components) * distance_x)
            for i in range(1, current_level):
            
                create_flag(x_pos = start_x_current, world = world, interface_info=interface_info)
                start_x_current +=distance_x
       
                
def create_flag(x_pos : int, world: esper.World, interface_info: dict):
    
    """
    Create a flag entity at the specified x-position.

    Args:
        x_pos (int): The x-position where the flag entity should be created.
        world (esper.World): The world in which the flag entity will be added.
        interface_info (dict): A dictionary containing interface information.

    Returns:
        None

    Raises:
        None
    """
    
    player_sprite = ServiceLocator.images_service.get(path = interface_info["level_image"])
    
    pos = pygame.Vector2(x_pos,interface_info["level_info_position"]["y"])
    vel = pygame.Vector2(0, 0)
    game_info_entity = create_sprite(world, pos, vel, player_sprite)

    world.add_component(game_info_entity, CTagLevel(pos=pos))
    
def create_fized_flag(x_pos : int, world: esper.World, interface_info: dict):
    
    """
    Create a flag entity at the specified x-position.

    Args:
        x_pos (int): The x-position where the flag entity should be created.
        world (esper.World): The world in which the flag entity will be added.
        interface_info (dict): A dictionary containing interface information.

    Returns:
        None

    Raises:
        None
    """
    
    player_sprite = ServiceLocator.images_service.get(path = interface_info["level_image"])
    
    pos = pygame.Vector2(x_pos,interface_info["level_info_position"]["y"])
    vel = pygame.Vector2(0, 0)
    game_info_entity = create_sprite(world, pos, vel, player_sprite)

    world.add_component(game_info_entity, CTagFixedFlag(pos=pos))