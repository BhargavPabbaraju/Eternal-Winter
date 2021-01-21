from mapdata import *

from saveload import * 


class Game:
    def __init__(self,window,savedata):
        
        self.init_game()
        self.window = pg.display.get_surface()
    
    def init_game(self):
        self.menuExit = False

        self.paused = False
        self.inventory = False
        self.cutscene = False
        self.over = False
        self.sci = None
        self.tb = None
        self.coffee = None
        ##Sprite Groups
        
        self.init_groups()
        
        self.save = Savedata(saveData,self)
        self.clock = pg.time.Clock()

        
        

        self.save.load_state(self)

        ##Intializing map
        self.map = Map(self.mapid,self)

        ##Initializing player
        self.player = Player(*self.map.startpos,self)

        
        self.save.load_player(self)
        

        self.screen = pg.Surface((WIDTH,HEIGHT))
        #self.


        

        
        
        self.snow()
        self.all_sprites.add(self.map)
        
        self.window = pg.display.get_surface()

    def init_groups(self):
        self.all_sprites = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.tiles = pg.sprite.Group()
        self.snowballs = pg.sprite.Group()
        self.collectibles = pg.sprite.Group()
        self.warpholes = pg.sprite.Group()
        self.portals = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.camera = Camera(600,600)
        

    def snow(self):
        for i in range(100):
            snow=Snowball(self)
            self.snowballs.add(snow)
            self.all_sprites.add(snow)
    
    def sky(self):
        for i in range(50):
            cloud = Cloud(self)
            self.clouds.add(cloud)
            self.all_sprites.add(cloud)

    
    def check_collisions(self):
        for coll in self.collectibles:
            if self.player.gridx==coll.gridx and self.player.gridy==coll.gridy:
                coll.collect()

        for warp in self.warpholes:
            if self.player.gridx==warp.gridx and self.player.gridy==warp.gridy:
                warp.warp()
        
        for portal in self.portals:
            if self.player.gridx==portal.gridx and self.player.gridy==portal.gridy:
                portal.warp()
        
        if self.coffee:
            if self.player.gridx==self.coffee.gridx and self.player.gridy==self.coffee.gridy:
                    self.coffee.collect()
            
        
    
    def transition(self):
        for i in range(255,0,-50):
            self.screen2.set_alpha(i)
            self.all_sprites.update()
            self.window.blit(self.screen2,(0,0))
            pg.display.update()
            pg.time.wait(30)
            self.clock.tick(60)

        self.all_sprites.update()
        self.window.set_alpha(255)
        pg.display.update()
        self.clock.tick(60)

    def draw(self,over=0):
        pg.display.update()
        self.window.fill(1)
        self.screen.fill(1)
        if self.over:
            self.window.blit(SKY,(0,0))
            self.screen.blit(SKY,(0,0))
        ##Updates
        self.all_sprites.update()
        self.collectibles.update()
        self.player.update()
        self.warpholes.update()
        self.portals.update()
        self.camera.update(self.player)


        for sprite in self.all_sprites:
            self.screen.blit(sprite.image,self.camera.apply(sprite))
        for sprite in self.collectibles:
            self.screen.blit(sprite.image,self.camera.apply(sprite))
        for sprite in self.warpholes:
            self.screen.blit(sprite.image,self.camera.apply(sprite))
        for sprite in self.portals:
            self.screen.blit(sprite.image,self.camera.apply(sprite))
        
        
        if self.sci:
            self.sci.update()
            self.screen.blit(self.sci.image,self.camera.apply(self.sci))
        if self.coffee:
            self.coffee.update()
            self.screen.blit(self.coffee.image,self.camera.apply(self.coffee))

        self.screen.blit(self.player.image,self.camera.apply(self.player))
        self.screen2 = pg.transform.scale(self.screen,(WIDTH*2,HEIGHT*2))
        
        self.check_collisions()

        
        
        self.window.blit(self.screen2,self.camera.apply(self.screen2.get_rect()))
        
        if not over:
            pg.display.update()
        clock.tick(60)
    
    def alert(self):
        pg.quit()
        quit()

    def play_music(self,music):
        if music=="gamebgm":
            music=rd.choice(['gamebgm','gamebgm2'])
        pg.mixer.music.stop()
        pg.mixer.music.load('Audio/%s.wav'%music)
        pg.mixer.music.play(-1)

    def game_loop(self):
        self.play_music('gamebgm')
        while not self.paused and not self.inventory and not self.cutscene:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.alert()
            
            self.draw()

    
    
    def pausedraw(self):
        self.window.fill(1)
        self.snowballs.draw(self.window)
        self.snowballs.update()
        
        self.menu.draw(self.window)
        self.menu.update()
    
    def saved(self):
        self.saving = True
        txt = Text('Saving....',self,(300,300),0)
        txt.size = 72
        txt.update()
        while self.saving:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

            self.window.fill(1)
            self.snowballs.draw(self.window)
            self.snowballs.update()
            self.window.blit(txt.image,txt.rect)
            pg.display.update()
            self.clock.tick(60)
            self.save.save_state(self)
            pg.time.wait(400)
            txt.msg='Saved!'
            txt.update()
            self.window.fill(1)
            self.snowballs.draw(self.window)
            self.snowballs.update()
            
            self.window.blit(txt.image,txt.rect)
            pg.display.update()
            self.clock.tick(60)
            pg.time.wait(500)
            self.saving = False
            

    
    def pause_clicks(self):
        x,y = pg.mouse.get_pos()
        
        for i in self.menu:
            click = pg.mouse.get_pressed()
            if i.rect.collidepoint(x,y):
                i.color = GRAY
                i.active = True
                if click[0]:
                    #continue
                    if i.ind==0:
                        self.paused = False
                        self.play_music('gamebgm')
                    #inventory
                    elif i.ind==1:
                        self.inventory_loop()
                    #Save
                    if i.ind==2:
                        self.saved()
                    
                    #Quit
                    if i.ind==3:
                        self.alert()



            else:
                i.active = False

       
    
    def inventory_draw(self):
        self.window.fill(1)
        self.snowballs.draw(self.window)
        self.snowballs.update()

        self.gems.update()
        self.gems.draw(self.window)
        self.texts.update()
        self.texts.draw(self.window)

        x,y = pg.mouse.get_pos()
        if self.backbut.rect.collidepoint(x,y):
            self.backbut.active = True
            click = pg.mouse.get_pressed()
            if click[0]:
                self.inventory = False
        else:
            self.backbut.active = False




    def inventory_loop(self):
        self.inventory = True
        self.gems = pg.sprite.Group()
        self.texts = pg.sprite.Group()
        for i in range(7):
            gem = Collectible('vibgyor'[i],self,invpos[i])
            self.gems.add(gem)
            gem.scale = 2
            no = self.player.gems.get('vibgyor'[i],0)
            txt= Text('x%d'%no,self,(gem.rect.x+100,gem.rect.y+10),i)
            txt.color = COLORS[i]
            self.texts.add(txt)
            txt.inv = True
        
        txt = Text('Back to Pause Menu',self,(450,512),i)
        self.texts.add(txt)
        self.backbut = txt
            

        while self.inventory:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.alert()
            
            self.inventory_draw()
            pg.display.update()
            
            self.clock.tick(60)


    def pause(self):
        self.paused = True
        self.menu = pg.sprite.Group()
        self.play_music('menubgm')
        for i in range(len(pauseoptions)):
            self.menu.add(Text(pauseoptions[i],self,pausePositions[i],i))
        while self.paused:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.alert()

            pg.display.update()
            keys = pg.key.get_pressed()
            if keys[pg.K_KP_ENTER] or keys[pg.K_RETURN]:
                self.paused = False
                pg.time.wait(500)
                clock.tick(60)

            self.pausedraw()
            self.pause_clicks()
            pg.display.update()
            clock.tick(60)
    
    def menu_clicks(self):
        x,y = pg.mouse.get_pos()
        for txt in self.texts:
            if txt.rect.collidepoint(x,y):
                txt.active = True
                click = pg.mouse.get_pressed()
                if click[0]:
                    if txt.ind==0:
                        self.menuExit=True
                        self.save.file['exists'] = False
                        self.save.new_state(self)
                        self.game_loop()
                    if txt.ind==1:
                        self.menuExit=True
                        if self.save.file['exists']:
                            self.game_loop()
                        else:
                            self.menuExit=True
                            self.save_not_exist()

            else:
                txt.active = False

    def menu_draw(self):
        self.window.fill(1)
        self.snowballs.update()
        self.texts.update()

        self.snowballs.draw(self.window)
        self.texts.draw(self.window)

        pg.display.flip()

    def sne_clicks(self):
        self.window.fill(1)
        self.snowballs.update()
        self.texts.update()

        self.snowballs.draw(self.window)
        self.texts.draw(self.window)

        pg.display.flip()

        x,y = pg.mouse.get_pos()
        for txt in self.texts:
            if txt.rect.collidepoint(x,y):
                txt.active = True
                click = pg.mouse.get_pressed()
                if click[0]:
                    if txt.ind==1:
                        self.sne = False
                        self.menuExit=True
                        self.save.file['exists'] = False
                        self.save.new_state(self)
                        self.play_music('gamebgm')
                        self.game_loop()
                    if txt.ind==2:
                        self.sne = False
                        pg.quit()
                        quit()

            else:
                txt.active = False

        
    def save_not_exist(self):
        self.sne = True
        self.texts = pg.sprite.Group()
        self.texts.add(Text('Save File Does Not Exist',self,(WIDTH/2-44*7,150),0))
        self.texts.add(Text(options[0],self,(250,350),1))
        self.texts.add(Text(options[-1],self,(750,350),2))
        while self.sne:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                self.sne_clicks()


    def menu_loop(self):
    
        self.menuExit = False
        self.texts = pg.sprite.Group()
        for i in range(len(options)):
            self.texts.add(Text(options[i],self,optionPositions[i],i))
        
        self.play_music('menubgm')
        while not self.menuExit:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            self.menu_draw()
            self.menu_clicks()
            pg.display.update()
            clock.tick(60)
    
    def cutscenemove(self,dir):
        self.player.move(dir)
        self.draw()
        pg.display.update()
        self.clock.tick(60)
        pg.time.wait(100)
        
    def finalcutscene(self):
        self.cutscene = True
        self.play_music('bossmusic')
        moving = True
        self.sci = Sci(4,2,self)
        self.tb = Textbox(self,'sci')
        while self.cutscene:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            
            while moving:
                self.cutscenemove(2)
                self.cutscenemove(2)
                self.cutscenemove(0)
                self.cutscenemove(0)
                self.cutscenemove(0)
                self.cutscenemove(0)
                self.cutscenemove(3)
                self.cutscenemove(3)
                self.cutscenemove(3)
                self.cutscenemove(3)
                moving = False
            
            self.draw()
            if self.tb:
                self.tb.update()
                if not self.over:
                    self.cutscenemove(2)
                    self.cutscenemove(2)
                    self.cutscenemove(2)
                    self.cutscenemove(2)
                    self.cutscenemove(1)
                    self.cutscenemove(1)
                    self.cutscenemove(1)
                    self.cutscenemove(1)
                    self.cutscenemove(3)
                    self.cutscenemove(3)
                else:
                    self.cutscenemove(3)
                    self.cutscenemove(3)
                    self.cutscenemove(3)
                    self.cutscenemove(0)
                    self.cutscenemove(0)
                    self.cutscenemove(0)
                    self.cutscenemove(3)
                    self.tb=None
                self.sci=None
                self.cutscene=False
                if not self.over:
                    self.play_music('gamebgm')
                self.clock.tick(60)
                
                if self.mapid==OVERMAP:
                    self.gameover()
                
    def gameover(self):
        self.window2 = pg.display.get_surface()
        self.window.set_alpha(100)
        self.texts = pg.sprite.Group()
        self.draw()
        self.window2.blit(self.window,(0,0))
        txt = Text("Game Over",self,(256,128))
        txt.size = 72
        txt.color = BLACK
        self.texts.add(txt)
        i=0
        lu = pg.time.get_ticks()
        # for i in range(len(CREDITS)):
        #     txt = Text(CREDITS[i],self,creditpos[i],0)
        #     txt.size = 56
        #     txt.color = BLACK
        #     self.texts.add(txt)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.alert()

            self.draw(1)
            self.texts.update(1)
            self.texts.draw(self.window)
            pg.display.update()
            self.clock.tick(60)
            now = pg.time.get_ticks()
            if now - lu >500:
                if i<len(CREDITS):
                    if type(CREDITS[i])==str:
                        txt = Text(CREDITS[i],self,creditpos[i],0)
                        txt.size = 56
                        txt.color = BLACK
                        self.texts.add(txt)
                    else:
                        for j in range(2):
                            txt = Text(CREDITS[i][j],self,creditpos[i][j],0)

                            txt.color = BLACK
                            self.texts.add(txt)
                    i+=1
                lu = now
    
    def intro_draw(self):
        self.window = pg.display.get_surface()
        self.window.blit(introbg,(0,0))
        self.all_sprites.update()
        self.all_sprites.draw(self.window)
        
        pg.display.update()
        self.clock.tick(60)
    
    def intro_loop(self):
        self.introExit = False
        self.all_sprites = pg.sprite.Group()
        self.snow()
        txt = Text("Eternal",self,(530,240))
        txt.size = 72
        self.all_sprites.add(txt)
        txt = Text("Winter",self,(530,340))
        txt.size = 72
        self.all_sprites.add(txt)
        txt = Text("Press any key to continue",self,(500,510))
        txt.active=True
        txt.size = 30
        self.all_sprites.add(txt)
        for i in range(7):
            gem = Collectible('vibgyor'[i],self,intropos[i])
            gem.scale = 2
            self.all_sprites.add(gem)
        self.play_music('intro')
        while not self.introExit:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type ==  event.type == pg.KEYUP:
                    self.introExit = True
                    self.init_game()
                    self.menu_loop()
                    return


            self.intro_draw()


            

                

        



   




       
class Camera:
    def __init__(self,width,height):
        self.camera = pg.Rect(0,0,width,height)
        self.width = width
        self.height = height
    

    def apply(self,object):
        try:
            return object.rect.move(self.camera.topleft)
        except:
            return object.move(self.camera.topleft)
    
    def update(self,target):
        x = -target.rect.x + WIDTH/4
        y = -target.rect.y + target.rect.height
        self.camera = pg.Rect(x,y,self.width,self.height)



class Savedata:
    def __init__(self,file,game):
        self.file = file
        

    
    def save_state(self,game):
        self.file['exists'] = True
        ####Save Player
        newpl = Empty()
        player = game.player
        newpl.facing = player.facing
        newpl.rect = player.rect
        newpl.gridx = player.gridx
        newpl.gridy = player.gridy
        newpl.collected = game.collected
        newpl.gems = player.gems
        newpl.met = game.met
        newpl.found = game.found
        newpl.mapid = game.mapid
        newpl.hunting = game.hunting
        self.file['player'] = newpl


        ##Collected gems
        newpl.collected = game.collected
        

       

       
    
    def load_state(self,game):
        if not self.file['exists']:
            self.new_state(game)
            return

        
        newpl = self.file['player']
        game.collected = newpl.collected
        game.met = newpl.met 
        game.found = newpl.found
        game.hunting = newpl.hunting
        game.mapid = newpl.mapid
       
    
    def load_player(self,game):
        if not self.file['exists']:
            self.new_state(game)
            return

        ####Load Player
        newpl = self.file['player']
        game.player.facing = newpl.facing
        game.player.rect = newpl.rect
        game.player.gridx = newpl.gridx
        game.player.gridy = newpl.gridy
        game.player.gems = newpl.gems
        
        
        
       
    

    def new_state(self,game,portal=0):
        if portal:
            gems = game.player.gems
        
            
            
        else:
            gems={}
            for i in 'vibgyor':
                gems[i]=0
            game.collected = {}
            game.mapid ='001'
            game.met = False
            game.found = False
            game.hunting = False
            
        
       
        game.init_groups()
        ##New Map
        game.map = Map(game.mapid,game)
        

        game.all_sprites.add(game.map)
        if portal==2:
            game.map.startpos = game.map.portals[0]
        else:
            game.map.startpos = game.map.portals[1]

        game.player = Player(*game.map.startpos,game)

        if portal:
            if game.map.facing[0]%3==0:
                game.player.facing = 0
            else:
                game.player.facing = 1
            game.player.get_image()

        game.player.gems = gems
        
        game.cutscene = False
        
        if game.over:
            game.sky()
        else:
            game.snow()
        if game.mapid==FINALMAP:
            game.finalcutscene()
        if game.mapid==OVERMAP:
            game.over = True
        
        

        

        

        


    #def load_player(self,)


class Empty:
    def __init__(self):
        pass



game = Game(window,saveData)
game.intro_loop()