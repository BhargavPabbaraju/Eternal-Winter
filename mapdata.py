
import pygame as pg
import random as rd
from settings import *
from gametext import *

pg.init()

SKY = pg.image.load('Images/sky.png').convert()
introbg = pg.image.load('Images/introbg.png').convert()


class Spritesheet(pg.sprite.Sprite):
    def __init__(self,file):
        super().__init__()
        self.file =  pg.image.load(file).convert()
        
    
    def get(self,x,y,w,h,color):
        #self.file.set_colorkey()
        surf = pg.Surface((w,h))
        surf.set_colorkey(color)
        surf.blit(self.file,(0,0),[x,y,w,h])
        return surf
    
    def scale(self,x,y,w,h,color,scale=1):
        surf = self.get(x,y,w,h,color)
        surf = pg.transform.scale(surf,(int(w*scale),int(h*scale)))
        return surf





class Tile(pg.sprite.Sprite):
    def __init__(self,type,game,pos):
        self.type = type
        self.game = game
        super().__init__()
        self.sheet = Spritesheet('Images/tiles.png')
        self.no = rd.choice([0,1,2])
        self.w = 64
        self.h = 64
        self.get_image()
        self.pos=pos
        self.rect = self.image.get_rect()
    
    def get_image(self):
        id = ['s','i','f','g','0'].index(self.type)
        self.image = self.sheet.scale(self.no*self.w,id*self.h,self.w,self.h,(0,127,70))

    def passable(self):
        if self.type in ['s','f','i','g']:
            return True
        
        else:
            return False

class Coffee(pg.sprite.Sprite):
    def __init__(self,game,pos,x,y):
        super().__init__()
        self.game = game
        self.pos = pos
        self.gridx = x
        self.gridy = y
        self.rot = 0
        self.w = 40
        self.h = 64
        self.sheet = Spritesheet('Images/coffee.png')
        self.get_image()
        self.rot_speed = 200
        self.last_update = pg.time.get_ticks()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.rect.x+=13
        self.rect.y-=41
        
    
    def get_image(self):
        self.image = self.sheet.scale(self.rot*self.w,0,self.w,self.h,(0,127,70))
    
    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update >self.rot_speed:
            self.rot = (self.rot+1)%3
            self.get_image()
            self.last_update = now
    
    def collect(self):
        self.game.found = True
        gemfx.play()
        self.game.coffee = None
        self.kill()
        
        

    


class Warphole(pg.sprite.Sprite):
    def __init__(self,game,pos,x,y,wx,wy):
        super().__init__()
        self.game = game
        self.sheet = Spritesheet('Images/warp.png')
        self.w = 64
        self.h = 64
        self.rot = 0
        self.get_image()
        self.pos=pos
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

        self.rot_speed = 150
        self.last_update = pg.time.get_ticks()
        self.gridx = x
        self.gridy = y
        self.warpx = wx
        self.warpy = wy
        self.origin = (WIDTH//2 - BLOCKSIZE,100)
        self.warppos = self.warpto(wx,wy)
        
        
    def get_image(self):
        self.image = self.sheet.get(self.rot*self.w,0,self.w,self.h,(148,157,158))

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update >self.rot_speed:
            self.rot = (self.rot+1)%3
            self.get_image()
            self.last_update = now
    
    def warpto(self,x,y):
        ix=self.origin[0]+(x-y)*30
        iy=self.origin[1]+(x+y)*15
        return ix,iy

    def warp(self):
        if self.game.player.warping:
            return
        self.game.player.rect.x = self.warppos[0] + 12
        self.game.player.rect.y = self.warppos[1] - 77
        self.game.player.gridx = self.warpx
        self.game.player.gridy = self.warpy
        self.game.player.warping = True
        warpfx.play()
        self.game.transition()
        
class Portal(pg.sprite.Sprite):

    def __init__(self,game,pos,x,y,dir,id):
        super().__init__()
        self.game = game
        self.rot = 0
        self.w =62
        self.h = 153
        self.facing = dir
        self.sheet = Spritesheet('Images/portals.png')
        self.get_image()
        self.pos=pos
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        if self.facing%3!=0:
            self.rect.x-=6
            self.rect.y-=121
        else:
            self.rect.x+=8
            self.rect.y-=121
        
        self.rot_speed = 100
        self.last_update = pg.time.get_ticks()
        self.gridx = x
        self.gridy = y
        self.mapto = id
        self.origin = (WIDTH//2 - BLOCKSIZE,100)
        self.dir = 1
        
        
    
    def get_image(self):
        self.image = self.sheet.get(self.rot*self.w,self.facing*self.h,self.w,self.h,(148,157,158))
    
    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update >self.rot_speed:
            if self.rot==0:
                self.dir = (self.dir+1)%2

            if self.dir==1:
                self.rot = (self.rot-1)%9
            else:
                self.rot = (self.rot+1)%9
            
            self.get_image()
            self.last_update = now
    

    def warp(self):
        if self.game.player.warping:
            return
        self.game.mapid = self.mapto
        b=1
        if self.facing>1:
            b=2

            
    
        self.game.save.new_state(self.game,b)
        self.game.player.warping = True
        portalfx.play()
        self.game.transition()
        
        
        



class Collectible(pg.sprite.Sprite):
    def __init__(self,type,game,pos):
        super().__init__()
        self.id = type
        self.game = game
        self.pos = pos
        self.sheet = Spritesheet('Images/gems.png')
        self.col = 'vibgyor'.index(type[0])
        self.w = 34
        self.h = 34
        self.rot = 0
        self.scale = 1
        self.get_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.rect.x+=16
        self.rect.y-=16
        self.last_update = pg.time.get_ticks()
        self.rot_speed = 200
        
        
        
  
    def get_image(self):
        self.image = self.sheet.scale(self.rot*self.w,self.col*self.h,self.w,self.h,(148,157,158),self.scale)

    
    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update >self.rot_speed:
            self.rot = (self.rot+1)%3
            self.get_image()
            self.last_update = now
        
     


    def collect(self):
        self.game.collected[self.id]=True
        self.game.player.gems[self.id[0]]+=1
        gemfx.play()
        self.kill()
    
    
       
            
        
    
    






class Map(pg.sprite.Sprite):
    def __init__(self,id,game):
        self.game = game
        super().__init__()
        self.id = str(id).zfill(3)
        self.game.mapid = self.id
        self.tilegrid=[]
        self.collgrid = []
        self.grid = self.gridify()
        self.rows=len(self.grid)
        self.columns=len(self.grid[0])
        #self.max_height = MAX_HEIGHTS[self.id]
        self.origin = (WIDTH//2 - BLOCKSIZE,100)
        #self.origin = (100,0)
        self.image=pg.Surface((WIDTH,HEIGHT))
        self.image.set_colorkey((0,0,0))
        
        self.create_map()
        self.rect = self.image.get_rect()
        
        
        

    def gridify(self):
        self.portals=[]
        self.facing=[]
        file = open('Maps/map'+self.id+'.txt')
        grid=[]
        lines=file.readlines()
        x,y = map(int,lines[1].split())
        self.startpos = [x,y]
        
        curline = 3
        for line in lines[curline:curline+10]:
            grid.append(line.split())
            self.tilegrid.append([0]*len(grid[-1]))
            self.collgrid.append([0]*len(grid[-1]))
        
        curline+=11
        n_collect = int(lines[curline])
        curline+=1
        for line in lines[curline:curline+n_collect]:
            t,x,y = line.split()
            x,y=int(x),int(y)
            self.collgrid[x][y]=t
        
        curline+=n_collect+1
        n_warps = int(lines[curline])
        curline +=1
        for line in lines[curline:curline+n_warps]:
            x,y,wx,wy = map(int,line.split())
            self.collgrid[x][y]=[wx,wy]
        
        ###curline+n_warps - Portals
        curline = curline+n_warps+1
        for i in range(2):
            x,y,d,to = lines[curline+i].split()
            if to!='X':
                x,y = map(int,(x,y))
                d=int(d)
                self.collgrid[x][y]=[d,to]
                self.portals.append([x,y])
                self.facing.append(d)
            else:
                self.portals.append(self.startpos)
                self.facing.append(1)
        
        return grid



    def create_map(self):
        for y in range(self.rows):
            for x in range(self.columns):
                #if self.grid[y][x]=='s':
                    ix = self.origin[0] - 30*x
                    iy = self.origin[1] + 15*x
                    iy += 15*y
                    ix += 30*y
                    tile = Tile(self.grid[y][x],self.game,(ix,iy))
                    self.tilegrid[y][x] = tile
                    self.image.blit(tile.image,(ix,iy))
                    self.game.tiles.add(tile)
                    
                    if self.collgrid[y][x]:
                        t=self.collgrid[y][x]
                        if type(t)==str:
                            if not self.game.collected.get(t,False):
                                coll = Collectible(t,self.game,(ix,iy))
                                coll.gridx=y
                                coll.gridy=x
                                self.game.collectibles.add(coll)
                                
                        else:
                            if type(t[1]) == str:
                                portal = Portal(self.game,(ix,iy),y,x,*t)
                                self.game.portals.add(portal)
                                
                            
                            else:
                                warp = Warphole(self.game,(ix,iy),y,x,*t)
                                self.game.warpholes.add(warp)
            
        if self.game.hunting and not self.game.found and self.game.hunting==self.id:
            
            x,y = rd.choice(coffee_locs[self.game.hunting])
            ix=self.origin[0]+(x-y)*30
            iy=self.origin[1]+(x+y)*15
            cof = Coffee(self.game,(ix,iy),x,y)
            self.game.coffee = cof
            
            

                        
                        

            








class Snowball(pg.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.sheet = Spritesheet('Images/snowball.png')
        self.scale = rd.choice([1/3,1/2,1,2])
        self.get_image()
        self.image.set_colorkey((0,0,0))
        self.game = game
        self.rect = self.image.get_rect()
        self.form()
        self.velx=20
        self.vely = 30
    
    def get_image(self):
        self.image = self.sheet.scale(0,0,8,8,(0,0,0),self.scale)
    
    def form(self):
        self.limy = self.game.player.rect.y
        self.limx = self.game.player.rect.x
        self.rect.y = rd.randint(self.limy-800,self.limy+800)
        self.rect.x = rd.randint(self.limx-800,self.limx+800)

    
    def update(self):
        if self.game.over:
            self.kill()
        self.rect.x+=rd.choice([self.velx,-self.velx])
        self.rect.y+=self.vely
        if self.rect.y>640:
            self.form()


class Cloud(pg.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.sheet = Spritesheet('Images/clouds.png')
        self.scale = rd.choice([1/4,1/3,1/2,1])
        self.get_image()
        self.image.set_colorkey((230,255,170))
        self.game = game
        self.rect = self.image.get_rect()
        self.form()
        self.velx=10
        #self.vely = 30
    
    def get_image(self):
        r = rd.choice([0,1,2])
        self.image = self.sheet.scale(r*128,0,128,128,(230,255,170),self.scale)
    
    def form(self):
        self.limy = self.game.player.rect.y
        self.limx = self.game.player.rect.x
        self.rect.y = rd.randint(self.limy-800,self.limy+800)
        self.rect.x = rd.randint(self.limx-800,self.limx+800)

    
    def update(self):
        self.rect.x+=rd.randint(1,self.velx)
        if self.rect.x>WIDTH:
            self.form()


###PLAYER
class Player(pg.sprite.Sprite):
    def __init__(self,x,y,game):
        super().__init__()
        
        self.w=40
        self.h = 104
        self.sheet = Spritesheet('Images/player.png')
        self.facing = 1
        self.last_update = pg.time.get_ticks()
        self.update_threshold = 150
        self.speedx = 30
        self.speedy = 15
        self.get_image()
        self.rect = self.image.get_rect()
        self.gridx=x
        self.gridy=y
        self.game = game
        x=self.game.map.origin[0]+(self.gridx-self.gridy)*30
        y=self.game.map.origin[1]+(self.gridx+self.gridy)*15
        self.rect.x = x+12
        self.rect.y = y-77
        self.vx = 0
        self.vy = 0
        self.last_faded = pg.time.get_ticks()
        self.fade_threshold = 75
        #self.gems={}
        self.warping = False
        # for i in 'vibgyor':
        #     self.gems[i]=0
    
    def get_image(self):
        if self.facing<2:
            fx=0
        else:
            fx=1
        fy = self.facing%2
        self.image = self.sheet.scale(self.w*fy,self.h*fx,self.w,self.h,(230,255,170))
        
    
    def change_direction(self,dir):
        ##Moving Right
        self.warping = False
        if dir==1:
            self.facing =1 
            self.get_image()
            
   
        ##Moving Left
        elif dir==0:
            self.facing = 3
            self.get_image()
           
        ##Moving Down
        elif dir==2:
            self.facing = 0
            self.get_image()
        
        ##Moving Up
        elif dir==3:
            self.facing = 2
            self.get_image()

        self.image.set_alpha(150)
    
   


    def move(self,dir):
        ##Right
        if dir==1 and self.gridx<self.game.map.rows-1:
            tile = self.game.map.tilegrid[self.gridx+1][self.gridy]
            if  tile.passable():
                    self.change_direction(1)
                    self.rect.x+=self.speedx
                    self.rect.y+=self.speedy
                    self.gridx+=1
        
        ##Left
        elif dir==0 and self.gridx>0:
            tile = self.game.map.tilegrid[self.gridx-1][self.gridy]
            if  tile.passable():
                    self.change_direction(0)
                    self.rect.x-=self.speedx
                    self.rect.y-=self.speedy
                    self.gridx-=1
        
        ###Down
        elif dir==2 and self.gridy<self.game.map.columns-1:
           

            tile = self.game.map.tilegrid[self.gridx][self.gridy+1]
            if tile.passable():
                    self.change_direction(2)
                    self.rect.x-=self.speedx
                    self.rect.y+=self.speedy
                    self.gridy+=1


        ##Up
        elif dir==3 and self.gridy>0:
            tile = self.game.map.tilegrid[self.gridx][self.gridy-1]
            if  tile.passable():
                    self.change_direction(3)
                    self.rect.x+=self.speedx
                    self.rect.y-=self.speedy
                    self.gridy-=1



    
    def update(self):
        now = pg.time.get_ticks()
        if now-self.last_faded>self.fade_threshold:
            self.image.set_alpha(255)
            self.last_faded = now
        if now - self.last_update>self.update_threshold and not self.game.cutscene:


            keys = pg.key.get_pressed()
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.move(1)
                
                
            elif keys[pg.K_LEFT] or keys[pg.K_a]:
                self.move(0)
                
                
                
            elif keys[pg.K_DOWN] or keys[pg.K_s]:
                self.move(2)
                
            elif keys[pg.K_UP] or keys[pg.K_w]:
                self.move(3)
            
            elif keys[pg.K_h]:
                #self.game.savedata['game'] = self.game
                #print(self.gridx,self.gridy)
                pg.image.save(self.game.window,r"C:\Users\bharg\OneDrive\Desktop\pygame\newyearjam\dist\ss.png")
                
            
            
            elif keys[pg.K_p] or keys[pg.K_SPACE]:
                if not self.game.over:
                    self.game.pause()
                

            self.last_update = now
            
            return
        
    


    

##Scientist
class Sci(pg.sprite.Sprite):
    def __init__(self,x,y,game):
        super().__init__()
        self.w=40
        self.h = 104
        self.sheet = Spritesheet('Images/scientist.png')
        self.facing = 0
        self.last_update = pg.time.get_ticks()
        self.update_threshold = 150
        self.get_image()
        self.rect = self.image.get_rect()
        self.gridx=x
        self.gridy=y
        self.game = game
        x=self.game.map.origin[0]+(self.gridx-self.gridy)*30
        y=self.game.map.origin[1]+(self.gridx+self.gridy)*15
        self.rect.x = x+12
        self.rect.y = y-77

    def get_image(self):
        if self.facing<2:
            fx=0
        else:
            fx=1
        fy = self.facing%2
        self.image = self.sheet.scale(self.w*fy,self.h*fx,self.w,self.h,(230,255,170))



class Text(pg.sprite.Sprite):
    def __init__(self,msg,game,pos,i=0):
        super().__init__()
        self.msg = msg
        self.size = 44
        
        self.color = WHITE
        self.active = False
        self.inv = False
        self.update()
        #self.image = self.font.render(msg,True,self.color)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.topleft = pos
        self.last_update = pg.time.get_ticks()
        self.threshold = 1000
        self.ind = i
        self.speed = 3

    def update(self,over=0):
        if not self.inv and not over:
            if self.active:
                self.color = GRAY
            else:
                self.color = WHITE
        self.font = pg.font.Font('Halo3.ttf',self.size)
        self.image = self.font.render(self.msg,True,self.color)
        if over:
            now = pg.time.get_ticks()
            if now - self.last_update>self.threshold:
                if self.rect.y<-100:
                    self.kill()
                self.rect.y-=self.speed
                now = self.last_update

       
class Gem(pg.sprite.Sprite):
    def __init__(self,type,pos,game,i):
        super().__init__()
        self.col = type
        self.pos = pos
        self.game = game 
        self.ind = i
        self.images=[]
        self.rot = 1
        # for i in range(3):
        #     self.images.append(pg.image.load('.png'%(,i)).convert())

class Textbox(pg.sprite.Sprite):
    def __init__(self,game,msg):
        super().__init__()
        self.msg = msg
        self.game = game
        self.sheet = Spritesheet("Images/textbox.png")
        self.limit = 900
        self.w = 1020
        self.h = 164
        self.get_image()
        self.speed = TEXTSPEED
        self.last_update = pg.time.get_ticks()
        self.cur = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = TEXTBOXPOSITIONS[self.msg]
        self.wl = 24
        self.space = 1
    
    def all_collected(self):
        for i in 'vibgyor':
            if self.game.player.gems[i]<6:
                return False
        return True

    

    def get_image(self):
        self.image = self.sheet.get(0,0,self.w,self.h,(0,0,0))
    
    def find_cur(self):
        if self.msg=='sci': 
            if not self.game.met:
                self.cur = 0
                self.game.met = True
            elif not self.all_collected():
                self.cur = 1
            else:
                if not self.game.hunting:
                    self.cur = 2
                    self.game.hunting = rd.choice(list(coffee_locs.keys()))

                elif self.game.found:
                    self.cur= 4
                    self.sci(4)
                    self.sci(5)
                    self.cur = 6
                    self.game.over = True
                    self.game.sky()
                    self.game.play_music('overbgm')

                else:
                    self.cur = 3
                    
        
        
            self.sci(self.cur)
            self.game.player.warping = True
        
        
    
    def sci(self,cur):
        lines = texts[self.msg][cur].split('\n')
        for line in lines[:-1]:
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    pg.quit()
                    quit()
            self.render(line)
            self.game.draw()
            self.game.window.blit(self.image,self.rect)
            pg.display.update()
            pg.time.wait(self.speed)
            self.game.clock.tick(60)

        
        
    
    def render(self,msg):
        pos=[100,25]
        color=(0,0,1)
        font = pg.font.Font('pkmndp.ttf',36)
        size=36
        words = msg.split(' ')
        self.get_image()
        tx=pos[0]
        ty=pos[1]
        for word in words:
            l=len(word)
            if tx+l*self.wl+self.space>self.limit:
                tx=pos[0]
                ty+=40
            
      

            font_surface = font.render(word, True, color)

           
            self.image.blit(font_surface, (tx, ty))
            tx+=l*self.wl+self.space
        nextfx.play()

        
        
        
    
    def update(self):
        if self.msg=='sci':
            self.find_cur()
        elif self.msg=='intro':
            self.intro()
        
        

coffee_locs={
    '001':[(2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (3, 5), (3, 6), (3, 7), (3, 8), (4, 5), (4, 6), (4, 7), (4, 8), (5, 5), (5, 6), (5, 8), (6, 5), (6, 6), (6, 7), (6, 8), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8)],
    '002':[(1, 6), (1, 7), (1, 8), (1, 11), (2, 1), (2, 6), (2, 7), (2, 8), (2, 10), (2, 11), (3, 1), (3, 6), (3, 7), (3, 8), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (4, 1), (4, 2), (4, 6), (4, 8), (4, 10), (4, 13), (5, 2), (5, 6), (5, 7), (5, 8), (5, 9), (5, 10), (5, 13), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 9), (6, 10), (6, 13), (6, 14), (6, 15), (7, 2), (7, 3), (7, 9), (7, 10), (7, 13), (8, 9), (8, 11), (8, 12)],
    '003':[(0, 3), (1, 4), (1, 5), (1, 11), (1, 12), (2, 3), (2, 9), (2, 11), (2, 13), (3, 9), (3, 11), (3, 13), (4, 6), (4, 9), (4, 10), (4, 13), (4, 14), (5, 6), (5, 13), (6, 4), (6, 6), (6, 13), (7, 4), (7, 5), (7, 6), (7, 7), (8, 13), (8, 14), (8, 15)],
    '004':[(1, 6), (1, 7), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (2, 1), (2, 15), (3, 1), (3, 7), (3, 15), (4, 1), (4, 7), (4, 15), (5, 1), (5, 2), (5, 3), (5, 15), (6, 3), (6, 7), (6, 11), (6, 14), (6, 15), (7, 3), (7, 7), (7, 11), (7, 12), (7, 13), (8, 3), (8, 4), (8, 5), (8, 7), (8, 8), (8, 10)],
    '005':[(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 12), (0, 13), (1, 13), (2, 13), (4, 2), (4, 10), (4, 13), (5, 13), (5, 15), (6, 2), (6, 13), (7, 4), (7, 13), (7, 14), (7, 15), (8, 3), (8, 14)],
    '006':[(1, 8), (1, 9), (1, 10), (1, 11), (2, 14), (2, 15), (3, 1), (3, 14), (4, 0), (4, 2), (5, 1), (5, 2), (6, 0), (6, 2), (6, 15), (7, 1), (7, 2), (7, 3), (7, 4), (7, 12), (7, 13), (7, 15), (8, 0), (8, 1), (8, 2), (8, 3), (8, 13), (8, 14), (8, 15)]


}
