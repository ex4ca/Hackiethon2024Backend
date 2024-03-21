# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions

# primary skill can be defensive or offensive
# secondary skills involve summoning a projectile

# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Lasso, Boomerang, Ice Wall, Bear Trap

# currently unsure how to enforce this...
#TODO FOR USER: Set primary and secondary skill here
PRIMARY_SKILL = DashAttackSkill
SECONDARY_SKILL = Boomerang

#constants, for easier move return
# movements
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

# no move, aka no input
NOMOVE = "NoMove"

class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        
    def init_player_skills(self):
        return self.primary, self.secondary
    
    #MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):

        if get_landed(player):
            if self.get_x_distance(player, enemy) == 1:
                if not heavy_on_cooldown(player) and get_stun_duration(enemy) > 1:
                    return HEAVY
                return LIGHT
            else:
                return BLOCK
        
        elif self.get_x_distance(player, enemy) > 1:
            if not secondary_on_cooldown(player) and self.get_x_distance(player, enemy) <= seco_range(player):
                return SECONDARY
            
            elif (len(enemy_projectiles) and abs(get_proj_pos(enemy_projectiles[0])[0] - get_pos(player)[0]) < 3): #incoming projectile
                return JUMP

            if get_pos(player)[0] < get_pos(enemy)[0]:
                return FORWARD
            else:
                return BACK
        
        elif self.get_x_distance(player, enemy) == 1:
            if not primary_on_cooldown(player) and self.get_x_distance(player, enemy) <= prim_range(player):
                return PRIMARY
            if not heavy_on_cooldown(player) and get_stun_duration(enemy) > 1:
                    return HEAVY
            else:
                return LIGHT
            
        return LIGHT
            
    
    def get_x_distance(self, player, enemy):
        return abs(get_pos(player)[0] - get_pos(enemy)[0]) 