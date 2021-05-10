import hlt
import logging

game = hlt.Game("DJP")
logging.info("Starting...")

# Função para iteração e domínio dos
# navios inimigos que estão no ambiente
def get_all_enemy_ships(game_map):
    enemy_ships = []
    players = game_map.all_players()
    for player in players:
        if player == game_map.get_me():
            continue
        enemy_ships.extend(player.all_ships())
    return enemy_ships

# Função para verificar se esta sobre ataque e
# calcular a distância inimigo até o navio
def is_under_attack(game_map, ship):
    enemies = get_all_enemy_ships(game_map)
    for enemy in enemies:
        if ship.calculate_distance_between(enemy) <= 5:
            return True
    return False

# Função que itera com os inimigos e calcula a distância
# dos navios inimigos que estão atacando até o navio
def get_attackers(game_map, ship):
    attackers = []
    enemies = get_all_enemy_ships(game_map)
    for enemy in enemies:
        if ship.calculate_distance_between(enemy) <= 5:
            attackers.append(enemy)
    return attackers

# Método principal gerado automaticamente pelo starter kits
while True:
    game_map = game.update_map()
    command_queue = []

    for ship in game_map.get_me().all_ships():
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue

    for planet in game_map.all_planets():
        if planet.is_owned():
            continue

        if ship.can_dock(planet):
            command_queue.append(ship.dock(planet))
        else:
            navigate_command = ship.navigate(
                ship.closest_point_to(planet),
                game_map,
                speed=int(hlt.constants.MAX_SPEED / 2),
                ignore_ships=True,
            )
            if navigate_command:
                command_queue.append(navigate_command)
        break

    game.send_command_queue(command_queue)