# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN


# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = OnePunchSkill
SECONDARY_SKILL = SuperArmorSkill

#constants, for easier move return
#movements
JUMP = ("move", (0,1))
FORWARD = ("move", (1,0))
BACK = ("move", (-1,0))
JUMP_FORWARD = ("move", (1,1))
JUMP_BACKWARD = ("move", (-1, 1))

# attacks and block
LIGHT = ("light",)
HEAVY = ("heavy",)
BLOCK = ("block",)

PRIMARY = get_skill(PRIMARY_SKILL)
SECONDARY = get_skill(SECONDARY_SKILL)
CANCEL = ("skill_cancel", )

# no move, aka no input
NOMOVE = "NoMove"
# for testing
moves = SECONDARY,
moves_iter = iter(moves)

# TODO FOR PARTICIPANT: WRITE YOUR WINNING BOT
class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    
    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        distance = abs(get_pos(player)[0] - get_pos(enemy)[0])
        enemy_primary = get_primary_skill(enemy)
        enemy_secondary = get_secondary_skill(enemy)
        is_melee = False
        unblockable_skills = [DashAttackSkill, OnePunchSkill, Grenade, BearTrap]

        # is player under immediate threat
        if (prim_range(enemy) > 0 and not primary_on_cooldown(enemy)) or (seco_range(enemy) > 0 and secondary_on_cooldown(enemy)): 
            # TODO: better conditions to check if player is under threat
            if prim_range(enemy) < distance:
                return JUMP
            if enemy_projectiles:
                # once projectile is distance 1 away, can treat as a close range attack
                enemy_projectile_dist = abs(get_pos(player)[0] - get_proj_pos(enemy_projectiles[0])[0])
                if enemy_projectile_dist == 1:
                    is_melee = True
            if prim_range(enemy) == 1:
                is_melee = True
            if is_melee:
                is_melee = False
                # block if blockable, else return secondary
                if get_primary_skill(enemy) in unblockable_skills:
                    if secondary_on_cooldown(player):
                        return JUMP_BACKWARD
                    else:
                        return SECONDARY
                else:
                    if get_block_status(player) < 2:
                        return BLOCK
                    return JUMP_BACKWARD
                    
        # if player is NOT under immediate threat
        else:
            if distance <= 1:
                if not primary_on_cooldown(player):
                    return PRIMARY
                else:
                    if heavy_on_cooldown(player):
                        return LIGHT
                    return HEAVY
            else:
                return FORWARD