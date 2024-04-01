class AttackTrait:
    def __init__(self, entity, animation=None, deltaTime=7 ):
        self.entity = entity
        self.timer = 0
        self.attackTimer = 0
        self.deltaTime = deltaTime
        self.animation = animation
    
    def update(self):
        self.timer += 1
        if self.timer % self.deltaTime == 0:
            if self.attackTimer < 7:
                self.attackTimer += 1
            else:
                self.reset()
    
    def attack(self, attacking):
        if attacking and self.entity.onGround:
            self.timer = 0
            self.entity.checkSwordMobCollision(self.animation.attackIndex)
            if self.entity.inAttack == False:
                self.entity.sound.play_sfx(self.entity.sound.bump)
                self.entity.inAttack = True
                
    def checkAttackBoss(self, boss):
        return self.entity.checkSwordBossCollision(self.animation.index, boss)
        
    def reset(self):
        self.entity.inAttack = False