class Area:
    def __init__(self, encounter, encounters, pre_enemy_states, post_player_states, post_enemy_states, player_damage_given, player_damage_taken, ):
        self.turn = turn
        self.pre_player_states = pre_player_states
        self.pre_enemy_states = pre_enemy_states
        self.post_player_states = post_player_states
        self.post_enemy_states = post_enemy_states

    def __repr__(self):
        return "<Encounter |Turn:%s |Player:%s |Enemy:%s >" % (self.turn, self.pre_player_states[0], self.pre_enemy_states[0])
    def __str__(self):
        return "<Encounter |Turn:%s |Player:%s |Enemy:%s >" % (self.turn, self.pre_player_states[0], self.pre_enemy_states[0])
    def __eq__(self, other):
        if isinstance(other, Encounter):
            return self.turn == other.turn and self.pre_player_states == other.pre_player_states
