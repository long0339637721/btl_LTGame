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

    def update(self, isCharacter = False, isInAir = False, isInAttack = False, isMoving = False):
        self.timer += 1
        if isCharacter: 
            if self.timer % self.deltaTime == 0:
                if isInAttack and not isMoving:
                    if self.index < len(self.attackSprite) - 1:
                        self.index += 1
                    else: self.index = 0
                else:
                    if self.index < len(self.images) - 1:
                        self.index += 1
                    else:
                        self.index = 0
        else:
            if self.timer % self.deltaTime == 0:
                if self.index < len(self.images) - 1:
                    self.index += 1
                else:
                    self.index = 0
        # Không cho set lại state = 0 và image running khi đang nhảy (hoặc tấn công)       
        if not (isCharacter and (isInAir or isInAttack)):
            self.image = self.images[len(self.images)-1 if self.index > len(self.images)-1 else self.index]  
            self.state = 0
        # Cho phép set lại trạng thái state = 0 và image running khi vừa giữ phím space vừa di chuyển
        if isCharacter and isInAttack and isMoving:
            self.image = self.images[len(self.images)-1 if self.index > len(self.images)-1 else self.index]  
            self.state = 0
        # else:
        #     self.image = self.images[self.index]  

    def idle(self):
        self.state = 1
        # self.image = self.idleSprite
        # if (self.idleSprite):
        self.image = self.idleSprite[self.index % len(self.idleSprite)]

    def inAir(self, jumpState):
        self.state = 2
        self.image = self.airSprite
        if (jumpState == 1):
            self.image = self.airSprite[0]
        if (jumpState == 2):
            self.image = self.airSprite[1]
    
    def inAttack(self):
        if self.state != 3:
            self.state = 3
            self.index = 0
        self.image = self.attackSprite[self.index]


