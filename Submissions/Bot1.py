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

        if distance == 1:
            if primary_on_cooldown(enemy) or secondary_on_cooldown(enemy):
                if heavy_on_cooldown(player):
                    return LIGHT
                return HEAVY

            # non damaging primaries:
            # if enemy has teleport or super jump, can expect to use it when distance = 1
            if enemy_primary == TeleportSkill and not primary_on_cooldown(enemy):
                if not primary_on_cooldown(player):
                    return PRIMARY
                if heavy_on_cooldown(player):
                    return LIGHT
                return HEAVY
                
            if enemy_secondary == JumpBoostSkill and not secondary_on_cooldown(enemy):
                if not primary_on_cooldown(player):
                    return PRIMARY
                if heavy_on_cooldown(player):
                    return LIGHT
                return HEAVY   

            # if enemy has any skill that attacks within one distance
            if enemy_primary == UppercutSkill and not primary_on_cooldown(enemy):
                if not primary_on_cooldown(player):
                    return PRIMARY
                return BLOCK
            
            if enemy_primary == OnePunchSkill and not primary_on_cooldown(enemy):
                return JUMP_BACKWARD        
            
            return PRIMARY

        # case where enemy has a projectile
        if enemy_projectiles:
            enemy_projectile_dist = abs(get_pos(player)[0] - get_proj_pos(enemy_projectiles[0])[0])
            if enemy_projectile_dist < 1:
                if not secondary_on_cooldown(player):
                    return SECONDARY
                return BLOCK
        
        # case where attack is a greater range than 1
        if get_primary_skill(enemy) == DashAttackSkill and not primary_on_cooldown(enemy):
            if distance <= prim_range(enemy) and not secondary_on_cooldown(player):
                return SECONDARY
                      
        return FORWARD