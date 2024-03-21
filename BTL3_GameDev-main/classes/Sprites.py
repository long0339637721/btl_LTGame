import json

from classes.Animation import Animation
from classes.Sprite import Sprite
from classes.Spritesheet import Spritesheet


class Sprites:
    def __init__(self):
        self.spriteCollection = self.loadSprites(
            [
                "./sprites/CharacterIdle/CharacterIdle1.json",
                "./sprites/CharacterIdle/CharacterIdle2.json",
                "./sprites/CharacterIdle/CharacterIdle3.json",
                "./sprites/CharacterIdle/CharacterIdle4.json",
                "./sprites/CharacterIdle/CharacterIdle5.json",
                "./sprites/CharacterIdle/CharacterIdle6.json",
                "./sprites/CharacterIdle/CharacterIdle7.json",
                "./sprites/CharacterIdle/CharacterIdle8.json",
                "./sprites/CharacterRun/CharacterRun1.json",
                "./sprites/CharacterRun/CharacterRun2.json",
                "./sprites/CharacterRun/CharacterRun3.json",
                "./sprites/CharacterRun/CharacterRun4.json",
                "./sprites/CharacterRun/CharacterRun5.json",
                "./sprites/CharacterRun/CharacterRun6.json",
                "./sprites/CharacterRun/CharacterRun7.json",
                "./sprites/CharacterRun/CharacterRun8.json",
                "./sprites/CharacterAttack/CharacterAttack1.json",
                "./sprites/CharacterAttack/CharacterAttack2.json",
                "./sprites/CharacterAttack/CharacterAttack3.json",
                "./sprites/CharacterAttack/CharacterAttack4.json",
                "./sprites/CharacterAttack/CharacterAttack5.json",
                "./sprites/CharacterAttack/CharacterAttack6.json",
                "./sprites/CharacterAttack/CharacterAttack7.json",
                "./sprites/CharacterAttack/CharacterAttack8.json",
                "./sprites/CharacterAttack/CharacterAttack9.json",
                "./sprites/CharacterAttack/CharacterAttack10.json",
                "./sprites/CharacterAttack/CharacterAttack11.json",
                "./sprites/CharacterAttack/CharacterAttack12.json",
                "./sprites/CharacterAttack/CharacterAttack13.json",
                "./sprites/CharacterAttack/CharacterAttack14.json",
                "./sprites/CharacterAttack/CharacterAttack15.json",
                "./sprites/CharacterAttack/CharacterAttack16.json",
                "./sprites/CharacterAttack/CharacterAttack17.json",
                "./sprites/CharacterAttack/CharacterAttack18.json",
                "./sprites/CharacterAttack/CharacterAttack19.json",
                "./sprites/CharacterAttack/CharacterAttack20.json",
                "./sprites/CharacterAttack/CharacterAttack21.json",
                "./sprites/CharacterAttack/CharacterAttack22.json",
                "./sprites/CharacterAttack/CharacterAttack23.json",
                "./sprites/CharacterAttack/CharacterAttack24.json",
                "./sprites/CharacterAttack/CharacterAttack25.json",
                "./sprites/CharacterAttack/CharacterAttack26.json",
                "./sprites/CharacterAttack/CharacterAttack27.json",
                "./sprites/CharacterAttack/CharacterAttack28.json",
                "./sprites/CharacterJump/CharacterJump2.json",
                "./sprites/CharacterJump/CharacterJump16.json",
                "./sprites/CharacterDie/CharacterDie1.json",
                "./sprites/CharacterDie/CharacterDie2.json",
                "./sprites/CharacterDie/CharacterDie3.json",
                "./sprites/CharacterDie/CharacterDie4.json",
                "./sprites/CharacterDie/CharacterDie5.json",
                "./sprites/CharacterDie/CharacterDie6.json",
                "./sprites/CharacterDie/CharacterDie7.json",
                "./sprites/CharacterDie/CharacterDie8.json",
                "./sprites/CharacterDie/CharacterDie9.json",
                "./sprites/CharacterDie/CharacterDie10.json",
                "./sprites/CharacterDie/CharacterDie11.json",
                "./sprites/CharacterDie/CharacterDie12.json",
                "./sprites/CharacterDie/CharacterDie13.json",
                # "./sprites/CharacterIdle.json",
                # "./sprites/CharacterRun.json",
                # "./sprites/CharacterJump.json",
                # "./sprites/CharacterAttack.json",
                "./sprites/Mario.json",
                "./sprites/Goomba.json",
                "./sprites/Koopa.json",
                "./sprites/Animations.json",
                "./sprites/BackgroundSprites.json",
                "./sprites/BackgroundSprites2.json",
                "./sprites/ItemAnimations.json",
                "./sprites/RedMushroom.json",
                "./sprites/Rock.json",
            ]
        )

    def loadSprites(self, urlList):
        resDict = {}
        for url in urlList:
            with open(url) as jsonData:
                data = json.load(jsonData)
                mySpritesheet = Spritesheet(data["spriteSheetURL"])
                dic = {}
                if data["type"] == "background":
                    for sprite in data["sprites"]:
                        try:
                            colorkey = sprite["colorKey"]
                        except KeyError:
                            colorkey = None
                        dic[sprite["name"]] = Sprite(
                            mySpritesheet.image_at(
                                sprite["x"],
                                sprite["y"],
                                sprite["scalefactor"],
                                colorkey,
                            ),
                            sprite["collision"],
                            None,
                            sprite["redrawBg"],
                        )
                    resDict.update(dic)
                    continue
                elif data["type"] == "animation":
                    for sprite in data["sprites"]:
                        images = []
                        for image in sprite["images"]:
                            images.append(
                                mySpritesheet.image_at(
                                    image["x"],
                                    image["y"],
                                    image["scale"],
                                    colorkey=sprite["colorKey"],
                                )
                            )
                        dic[sprite["name"]] = Sprite(
                            None,
                            None,
                            animation=Animation(images, deltaTime=sprite["deltaTime"]),
                        )
                    resDict.update(dic)
                    continue
                elif data["type"] == "character" or data["type"] == "item":
                    for sprite in data["sprites"]:
                        try:
                            colorkey = sprite["colorKey"]
                        except KeyError:
                            colorkey = None
                        try:
                            xSize = sprite['xsize']
                            ySize = sprite['ysize']
                        except KeyError:
                            xSize, ySize = data['size']
                        dic[sprite["name"]] = Sprite(
                            mySpritesheet.image_at(
                                sprite["x"],
                                sprite["y"],
                                sprite["scalefactor"],
                                colorkey,
                                True,
                                xTileSize=xSize,
                                yTileSize=ySize,
                            ),
                            sprite["collision"],
                        )
                    resDict.update(dic)
                    continue
        return resDict
