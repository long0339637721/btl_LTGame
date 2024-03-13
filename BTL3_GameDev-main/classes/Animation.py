class Animation:
    def __init__(self, images, idleSprite=None, airSprite=None, attackSprite=None, deltaTime=7):
        self.images = images
        self.timer = 0
        self.index = 0
        self.image = self.images[self.index]
        self.idleSprite = idleSprite
        self.airSprite = airSprite
        self.attackSprite = attackSprite
        self.deltaTime = deltaTime
        self.attackTimer = 0
        self.state = 0      # 0: running, 1: idle, 2: inAir, 3: attacking

    def update(self):
        self.timer += 1
        if self.timer % self.deltaTime == 0:
            if self.index < len(self.images) - 1:
                self.index += 1
            else:
                self.index = 0
        self.image = self.images[self.index]
        self.state = 0

    def idle(self):
        self.state = 1
        self.image = self.idleSprite

    def inAir(self):
        self.state = 2
        self.image = self.airSprite
    
    def inAttack(self):
        self.state = 3
        self.image = self.attackSprite[self.index]


