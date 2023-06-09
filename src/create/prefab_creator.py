import random
import pygame
import esper

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_enemy_spawner_new import CEnemySpawnerNew
from src.ecs.components.c_enemy_steering_fire import CEnemySteeringFire
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_steering import CSteering
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.tags.c_tag_enemy_new import CTagEnemyNew 
from src.ecs.components.tags.c_tag_grouped_enemy import CTagGroupEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_score_text import CTagScoreText
from src.ecs.components.tags.c_tag_lifes import CTagLifes
from src.ecs.components.tags.c_tag_star import CTagStar
from src.ecs.components.tags.c_tag_level import CTagLevel
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState
from src.ecs.components.c_enemy_state import CEnemyState
from src.engine.service_locator import ServiceLocator


def create_square(world: esper.World, size: pygame.Vector2,
                  pos: pygame.Vector2, vel: pygame.Vector2, col: pygame.Color) -> int:
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity,
                        CSurface(size, col))
    world.add_component(cuad_entity,
                        CTransform(pos))
    world.add_component(cuad_entity,
                        CVelocity(vel))
    return cuad_entity


"""
def create_sprite(world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2,
                  surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity,
                        CTransform(pos))
    world.add_component(sprite_entity,
                        CVelocity(vel))
    world.add_component(sprite_entity,
                        CSurface.from_surface(surface))
    return sprite_entity
"""


def create_sprite(world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2,
                  surface: pygame.Surface) -> int:
    
    sprite_entity = world.create_entity()
    surf = CSurface.from_surface(surface)
    
    ene_rect = surf.area.copy()
    ene_rect.topleft = pos.copy()
                        
    world.add_component(sprite_entity,
                        CTransform(pos))
    world.add_component(sprite_entity,
                        CVelocity(vel))
    world.add_component(sprite_entity,
                        surf)
    return sprite_entity


def create_enemy_square(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    enemy_surface = ServiceLocator.images_service.get(path = enemy_info["image"])
    vel_max = enemy_info["velocity_max"]
    vel_min = enemy_info["velocity_min"]
    vel_range = random.randrange(vel_min, vel_max)
    velocity = pygame.Vector2(random.choice([-vel_range, vel_range]),
                              random.choice([-vel_range, vel_range]))
    enemy_entity = create_sprite(world, pos, velocity, enemy_surface)
    world.add_component(enemy_entity, CTagEnemy("Bouncer"))
    ServiceLocator.sounds_service.play(path=enemy_info["sound"])


def create_enemy_new_by_type(world: esper.World, pos_in: pygame.Vector2, enemy_info: dict, type: str):
    enemy_surface = ServiceLocator.images_service.get(path = enemy_info["image"])
    
    #new_size = (15, 15)
    #scaled_surface = pygame.transform.scale(enemy_surface, new_size)
    size = enemy_surface.get_size()
    size = (size[0] / enemy_info["animations"]["number_frames"], size[1])
    pos = pygame.Vector2(pos_in.x - (size[0] / 2),
                         pos_in.y - (size[1] / 2))
    
    
    velocity = pygame.Vector2(32, 0) 
    enemy_entity = create_sprite(world, pos, velocity, enemy_surface)
    world.add_component(enemy_entity, CEnemyState(pos))
    world.add_component(enemy_entity,
                        CAnimation(enemy_info["animations"]))
    
    world.add_component(enemy_entity, CTagEnemyNew(type, pos.copy(), enemy_info["score"]))

    world.add_component(enemy_entity, CTagGroupEnemy())
 

def create_enemy_hunter(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    enemy_surface = ServiceLocator.images_service.get(path = enemy_info["image"])
    velocity = pygame.Vector2(0, 0)
    enemy_entity = create_sprite(world, pos, velocity, enemy_surface)
    world.add_component(enemy_entity, CEnemyHunterState(pos))
    world.add_component(enemy_entity,
                        CAnimation(enemy_info["animations"]))
    world.add_component(enemy_entity, CTagEnemy("Hunter"))
    
def create_text_dead_enemies(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    enemy_surface = ServiceLocator.images_service.get(path = enemy_info["image"])
    velocity = pygame.Vector2(20, 0)
    enemy_entity = create_sprite(world, pos, velocity, enemy_surface)
    world.add_component(enemy_entity, CEnemyHunterState(pos))
    world.add_component(enemy_entity,
                        CAnimation(enemy_info["animations"]))
    world.add_component(enemy_entity, CTagEnemy("Hunter"))

def create_enemy_spawner_new(world: esper.World, level_data: dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity,
                        CEnemySpawnerNew(level_data["enemies"]))


def create_input_player(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()

    input_z = world.create_entity()
    steering = world.create_entity()
    
    world.add_component(input_left,
                        CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    world.add_component(input_right,
                        CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
    world.add_component(input_z,
                        CInputCommand("PLAYER_Z", pygame.K_z))

    world.add_component(input_z,
                        CInputCommand("PLAYER_Z", pygame.K_z))
    
    world.add_component(steering,
                        CInputCommand("TOGGLE_STEERING_DEBUG", pygame.K_LCTRL))

def create_start(world: esper.World,
                 star_pos: pygame.Vector2,
                 star_info: dict)->None:
    
    color = star_info["star_colors"][(random.randint(0, len(star_info["star_colors"])-1))]
    
    size = pygame.Vector2(star_info["size"]["x"],
                          star_info["size"]["y"])
    color = pygame.Color(color["r"],
                         color["g"],
                         color["b"])
    vel_max = star_info["vertical_speed"]["max"]
    vel_min = star_info["vertical_speed"]["min"]
    
    vel_range = random.randrange(vel_min, vel_max)
    
    
    
    # Calculamos la velocidad de la bala (Vector)
    velocity = (pygame.Vector2(star_pos.x, star_pos.y+10) - star_pos)
    velocity = velocity.normalize() * vel_range
    
    
    enemy_entity = create_square(world, size, star_pos, velocity, color)
    world.add_component(enemy_entity, CTagStar())
    
    """
    # Cargamos la superficie (imagen)
    start_surface = ServiceLocator.images_service.get(path = star_info["image"])
    start_velocity = star_info["vertical_speed"]["max"]
    
    # Calculamos la velocidad de la bala (Vector)
    vel = (pygame.Vector2(star_pos.x, star_pos.y+10) - star_pos)
    vel = vel.normalize() * vel_max

    # Creamos la bala
    bullet_entity = create_sprite(world, star_pos, vel, start_surface)
    
    # Añadimos el componente al mundo
    world.add_component(bullet_entity, CTagStar())
    """

def create_bullet(world: esper.World,
                  player_pos: pygame.Vector2,
                  player_size: pygame.Vector2,
                  bullet_info: dict):
    
    # Cargamos la superficie (imagen)
    bullet_surface = ServiceLocator.images_service.get(path = bullet_info["image"])
    
    # Obtenemos el tamaño de la superficie (imagen)
    bullet_size = bullet_surface.get_rect().size
    
    # Calculamos la posición en que debe aparecer la bala(pos es un vector)
    pos = pygame.Vector2(player_pos.x + (player_size[0] / 2) - (bullet_size[0] / 2),
                         player_pos.y + (player_size[1] / 2) - (bullet_size[1] / 2))
    
    # Calculamos la velocidad de la bala (Vector)
    vel = (pygame.Vector2(player_pos.x, player_pos.y-10) - player_pos)
    vel = vel.normalize() * bullet_info["velocity"]

    # Creamos la bala
    bullet_entity = create_sprite(world, pos, vel, bullet_surface)
    
    # Añadimos el componente al mundo
    world.add_component(bullet_entity, CTagBullet())
    ServiceLocator.sounds_service.play(path= bullet_info["sound"] )
    
    
    
def create_enemy_bullet(world: esper.World,
                  enemy_pos: pygame.Vector2,
                  enemy_size: pygame.Vector2,
                  enemy_bullet_info: dict,
                  direction: pygame.Vector2 =pygame.Vector2(0,1) ):
     
         
    # Calculamos la posición en que debe aparecer la bala(pos es un vector)
    pos = pygame.Vector2(enemy_pos.x + (enemy_size[0] / 2) - (enemy_bullet_info["size"]["w"] / 2),
                         enemy_pos.y + (enemy_size[1] / 2) - (enemy_bullet_info["size"]["h"] / 2))   
 
    
    col=pygame.Color(enemy_bullet_info["color"]["r"],enemy_bullet_info["color"]["g"],enemy_bullet_info["color"]["b"])
    vel = direction*enemy_bullet_info["velocity"]
    bullet_entity = create_square(world, size=pygame.Vector2(enemy_bullet_info["size"]["w"], enemy_bullet_info["size"]["h"]),
                  pos=pos, vel=vel, col=col)

    
    # Añadimos el componente al mundo
    world.add_component(bullet_entity, CTagEnemyBullet())
       
    
def create_enemy_explosion(world: esper.World, pos: pygame.Vector2, explosion_info: dict):
    explosion_surface = ServiceLocator.images_service.get(path = explosion_info["image_enemy"])
    vel = pygame.Vector2(0, 0)

    explosion_entity = create_sprite(world, pos, vel, explosion_surface)
    world.add_component(explosion_entity, CTagExplosion())
    world.add_component(explosion_entity,
                        CAnimation(explosion_info["animations"]))
    ServiceLocator.sounds_service.play(path= explosion_info["sound_enemy_die"] )
    return explosion_entity

def create_player_explosion(world: esper.World, pos: pygame.Vector2, explosion_info: dict):
    explosion_surface = ServiceLocator.images_service.get(path = explosion_info["image_player"])
    vel = pygame.Vector2(0, 0)

    explosion_entity = create_sprite(world, pos, vel, explosion_surface)
    
    world.add_component(explosion_entity, CTagExplosion())
    world.add_component(explosion_entity,
                        CAnimation(explosion_info["animations"]))
    ServiceLocator.sounds_service.play(path= explosion_info["sound_player_die"] )
    return explosion_entity

def create_explosion_for_elimination(world: esper.World, pos: pygame.Vector2, explosion_info: dict):
    explosion_surface = ServiceLocator.images_service.get(path = explosion_info["image_enemy"])
    vel = pygame.Vector2(0, 0)

    explosion_entity = create_sprite(world, pos, vel, explosion_surface)
    world.add_component(explosion_entity, CTagExplosion())
    world.add_component(explosion_entity,
                        CAnimation(explosion_info["animations"]))
    ServiceLocator.sounds_service.play(path= explosion_info["sound_for_elimination"] )
    return explosion_entity

def create_score_info(world: esper.World, interface_info: dict) -> int:
    
    text_surface = ServiceLocator.fonts_service.get(font = interface_info["font"], size= interface_info["text_size"])
    
    player_sprite = text_surface.render(interface_info["score_lavel"]["text"], True, (interface_info["score_lavel"]["color"]["R"],interface_info["score_lavel"]["color"]["G"],interface_info["score_lavel"]["color"]["B"]))
    
    pos = pygame.Vector2(interface_info["score_lavel"]["position"]["x"],interface_info["score_lavel"]["position"]["y"])
    vel = pygame.Vector2(0, 0)
    game_info_entity = create_sprite(world, pos, vel, player_sprite)

    world.add_component(game_info_entity, CPlayerState())
    return game_info_entity

def create_score_value(world: esper.World, interface_info: dict) -> int:
    
    text_surface = ServiceLocator.fonts_service.get(font = interface_info["font"], size= interface_info["text_size"])
    
    player_sprite = text_surface.render("0      ", True, (interface_info["score"]["color"]["R"],interface_info["score"]["color"]["G"],interface_info["score"]["color"]["B"]))
    
    pos = pygame.Vector2(interface_info["score_lavel"]["position"]["x"],interface_info["score_lavel"]["position"]["y"]+20)
    vel = pygame.Vector2(0, 0)
    game_info_entity = create_sprite(world, pos, vel, player_sprite)

    world.add_component(game_info_entity, CTagScoreText())
    return game_info_entity

def create_lifes_info(world: esper.World, interface_info: dict, player_info : dict) -> None:
    
    player_sprite = ServiceLocator.images_service.get(path = interface_info["life_image"])
    distance_x = 10
    start_x = 300

    lifes = player_info["lifes"]
    for i in range(1, lifes+1):
        
        pos = pygame.Vector2(start_x,10)
        vel = pygame.Vector2(0, 0)
        game_info_entity = create_sprite(world, pos, vel, player_sprite)
        print(f"Creando vida {i}")
        world.add_component(game_info_entity, CTagLifes(life_number=i))
        start_x +=distance_x


def create_instructions_info(world: esper.World, interface_info: dict, explosion_info: dict) -> int:
    
    text_surface = ServiceLocator.fonts_service.get(font = interface_info["font"], size= interface_info["text_size"])
    
    player_sprite = text_surface.render(f"{interface_info['instructions']}{explosion_info['consecutive_enemies_to_eliminate_one']} ", True, (interface_info["text_color"]["R"],interface_info["text_color"]["G"],interface_info["text_color"]["B"]))
    
    pos = pygame.Vector2(200,20)
    vel = pygame.Vector2(0, 0)
    game_info_entity = create_sprite(world, pos, vel, player_sprite)
    world.add_component(game_info_entity, CPlayerState())
    return game_info_entity

def create_level_info(world: esper.World, interface_info: dict, dead_enemies: int) -> int:
    
    player_sprite = ServiceLocator.images_service.get(path = interface_info["level_image"])
    
    pos = pygame.Vector2(interface_info["level_info_position"]["x"],interface_info["level_info_position"]["y"])
    vel = pygame.Vector2(0, 0)
    game_info_entity = create_sprite(world, pos, vel, player_sprite)

    world.add_component(game_info_entity, CTagLevel(pos=pos))
    return game_info_entity


def create_player_square(world: esper.World, player_info: dict, player_lvl_info: dict) -> int:
    print(f"creando jugador con vidas {player_info['lifes']}")
    player_sprite = ServiceLocator.images_service.get(path = player_info["image"])
    new_size = (50, 50)
    
    scaled_surface = pygame.transform.scale(player_sprite, new_size)
    
    size = player_sprite.get_size()
    size = (size[0] / player_info["animations"]["number_frames"], size[1])

    pos = pygame.Vector2(player_lvl_info["player_spawn"]["position"]["x"] - (size[0] / 2),
                         player_lvl_info["player_spawn"]["position"]["y"] - (size[1] / 2))
    vel = pygame.Vector2(0, 0)
    player_entity = create_sprite(world, pos, vel, player_sprite)
    world.add_component(player_entity, CTagPlayer(lifes = player_info["lifes"]))
    world.add_component(player_entity,
                        CAnimation(player_info["animations"]))
    world.add_component(player_entity, CPlayerState())
    
    
    return player_entity

def create_level_square(world: esper.World, interface_info: dict) -> int:
    player_sprite = ServiceLocator.images_service.get(path = interface_info["level_image"])
    
    pos = pygame.Vector2(420,10)
    vel = pygame.Vector2(0, 0)
    player_entity = create_sprite(world, pos, vel, player_sprite)
    world.add_component(player_entity, CPlayerState())
    return player_entity

