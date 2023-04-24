import pygame
import random
import os
import pickle

pygame.font.init()


To_Write=False
a=open("Highscore.bin","ab")
a.close()
a=open("Highscore.bin","rb")
try :content=pickle.load(a)
except:
    content=[]
    To_Write=True
a.close()
#

if To_Write==True:
    a=open("Highscore.bin","wb")
    pickle.dump(content,a)
    a.close()


used_font=pygame.font.SysFont("monospace",30)

FPS=7
POINT=0
body=[]
VEL=15
WIDTH,HIEGHT=605,600
SNAKE_FACE_WIDTH,SNAKE_FACE_HIEGHT=15,15
SNAKE_BODY_WIDTH,SNAKE_BODY_HIEGHT=15,15

win=pygame.display.set_mode((WIDTH,HIEGHT))
pygame.display.set_caption("snake game")

pygame.display.update()


clock = pygame.time.Clock()
current_orint="L"

POINT_IMAGE = pygame.image.load(os.path.join("assests","point.png"))
SNAKE_FACE_IMAGE = pygame.image.load(os.path.join("assests","face.png"))
SNAKE_BODY_IMAGE = pygame.image.load(os.path.join("assests","body.png"))
BORDER_IMAGE= pygame.image.load(os.path.join("assests","border.png"))
PLAY_IMAGE= pygame.image.load(os.path.join("assests","play.png"))
HIGHSCORE_IMAGE= pygame.image.load(os.path.join("assests","Highscore_icon.png"))
QUIT_IMAGE= pygame.image.load(os.path.join("assests","quit_icon.png"))
BACK_IMAGE= pygame.image.load(os.path.join("assests","back.png"))
BORDER_HORIZONTAL_IMAGE_USED=pygame.transform.rotate(pygame.transform.scale( BORDER_IMAGE,(20,600) ),270)
BORDER_VERTICLE_IMAGE_USED=pygame.transform.rotate(pygame.transform.scale( BORDER_IMAGE,(20,600) ),0)
SNAKE_BODY_IMAGE_USED=pygame.transform.rotate(pygame.transform.scale( SNAKE_BODY_IMAGE,(15,15) ),0)
SNAKE_FACE_IMAGE_USED=pygame.transform.rotate(pygame.transform.scale( SNAKE_FACE_IMAGE ,(15,15)),0)

def walls(): #Makes A List In Which Members Are The "Hitboxes" Of All The Walls
    WALLS=[]

    WALL_LEST_HAND=pygame.Rect(0,0,15,600)
    WALLS.append(WALL_LEST_HAND)
    WALL_UP=pygame.Rect(0,0,600,30)
    WALLS.append(WALL_UP)
    WALL_RIGHT_HAND=pygame.Rect(595,0,10,600)
    WALLS.append(WALL_RIGHT_HAND)
    WALL_DOWN=pygame.Rect(0,585,600,10)
    WALLS.append(WALL_DOWN)
    return WALLS

def draw(snake_face,point_obj,WALLS):#geneRates Image for snake face,body,point,walls
    

    win.fill((225,225,225))

    win.blit(SNAKE_FACE_IMAGE_USED,(snake_face.x,snake_face.y ))    #Snake Face
    
    for i in body:                                                  #Snake Body
        win.blit(SNAKE_BODY_IMAGE_USED,(i.x,i.y))
    
    win.blit(POINT_IMAGE,(point_obj.x,point_obj.y))                 #Point 
    
    win.blit(BORDER_VERTICLE_IMAGE_USED,(WALLS[0].x,WALLS[2].y))    #Walls
    win.blit(BORDER_VERTICLE_IMAGE_USED,(WALLS[2].x,WALLS[2].y))
    win.blit(BORDER_HORIZONTAL_IMAGE_USED,(WALLS[1].x,WALLS[1].y))
    win.blit(BORDER_HORIZONTAL_IMAGE_USED,(WALLS[3].x,WALLS[3].y))

    pygame.display.update()

def generate_point(snake_face,WALLS): #generates point object
    
    global point_obj
    satisfied=False
    while not satisfied :
        satisfied=True
        point_obj=pygame.Rect(random.randrange(5,490,8),random.randrange(5,590,8),9,9)


        for i in body:                                                  #If in body                            
            if i.colliderect(point_obj):
                satisfied=False
                print("Saved")

        if satisfied==True:
            if snake_face.colliderect(point_obj):                       #If in face
                 satisfied=False
                 print("Nerfed")


        for i in WALLS:                                                 #If in walls
            if i.colliderect(point_obj):
                satisfied=False
                print("new but saved")
                       
def collision(snake_face,WALLS,POINT): # check collision between Face-Body,Face-Wall,FAce-Wall

    global point_obj
    
    if point_obj.colliderect(snake_face):           #face-Point
        
        if len(body)==0:
            
               new_body=pygame.Rect(0,0,15,15)
        else:
            
               new_body=pygame.Rect(0,0,15,15)

        body.append(new_body)
        POINT+=1
        generate_point(snake_face,WALLS)

    for i in range(len(body)):                      #Face-Body
        
        if snake_face.colliderect(body[i]) :
             return False,POINT 
            
    for i in WALLS:                                 #Face-Wall
        if snake_face.colliderect(i):
            return False,POINT
    return True,POINT

def draw_pregame(tag,entry_field): #Draw Enter Name And Words On Screen
    win.fill((0,0,0))
    win.blit(tag,(75,250))
    win.blit(entry_field,(75,285))
    pygame.display.update()
    pass
        
def draw_pause_menu(play,highscore,quit): #Draw Pause Menu
    win.fill((0,0,0))
    win.blit(PLAY_IMAGE,(play.x,play.y))
    win.blit(HIGHSCORE_IMAGE,(highscore.x,highscore.y))
    win.blit(QUIT_IMAGE,(quit.x,quit.y))

    pygame.display.update()

def Highscore(back_button):#Writes Highscrore Window Based On Previous Attempts
    win.fill((0,0,0))

    win.blit(BACK_IMAGE,(back_button.x,back_button.y))
    
    ex="Name"+" "*15+"Points"
    to_write=used_font.render(ex,1,(225,225,225))
    win.blit(to_write,(100,100))
    temp=1
    
    for i in content:
        
        ex=i[1]+" "*(25-(len(i[1])+len(str(i[0]))))+str(i[0])
        to_write=used_font.render(ex,1,(225,225,225))
        win.blit(to_write,(100,100+temp*30))
        temp+=1
        
    pygame.display.update()

    

name_list=[]
def main(WALL):#main thingy
    run=True
    POINT=0
    global SNAKE_FACE_IMAGE_USED,point_obj,current_orint,FPS,name_list
    
    high=False
    pause=False
    snake_face = pygame.Rect(250,300,SNAKE_FACE_WIDTH,SNAKE_FACE_HIEGHT)
    generate_point(snake_face,WALL)
    game_start=False
    user_text=" |"
    temp_list=[]
    
    

    
    #++++++++++++++++++++++++MAIN LOOP+++++++++++++++++++++++++++++++
    while run:
        clock.tick(FPS)

        if game_start==False:
            tag_text="Enter Your Name(15 Char Max)"
            tag=used_font.render(tag_text,1,(255,255,255))

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    run=False
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_BACKSPACE:
                        user_text=user_text[:-2]
                    elif event.key==pygame.K_RETURN:
                        for i in user_text:
                            name_list.append(i)
                        
                        FPS=15
                        game_start=True
                    elif len(user_text)<16:
                        user_text+=event.unicode

            if len(user_text)==0:user_text=" |"
            if user_text[-1]=="|":
                user_text=user_text[:-1]
                for i in user_text:
                    temp_list.append(i)
                times=temp_list.count("|")
                for i in range(times):
                    temp_list.remove("|")
                user_text=""
                for i in temp_list:
                    user_text+=i
                temp_list=[]
            else:
                user_text=user_text+"|"
            
            entry_field=used_font.render(user_text,1,(225,225,225))
                
            draw_pregame(tag,entry_field)
        
        elif high==True:
            back_button=pygame.Rect(200,350,250,100)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    run=False
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if back_button.collidepoint(event.pos):
                        high=False
                
            Highscore(back_button)

        elif pause==True:
        
            play=pygame.Rect(100,250,100,100)
            highscore=pygame.Rect(250,250,100,100)
            quit=pygame.Rect(400,250,100,100)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    run=False
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if play.collidepoint(event.pos):
                        pause=False
                    if quit.collidepoint(event.pos):
                        run=False
                    if highscore.collidepoint(event.pos):
                        high=True

            

            draw_pause_menu(play,highscore,quit)
            
        else:
          
          for i in range(len(body)-1,-1,-1):
              if i==0:
                  body[i].x=snake_face.x
                  body[i].y=snake_face.y
              else:
                  body[i].x=body[i-1].x
                  body[i].y=body[i-1].y

          for event in pygame.event.get():
              if event.type==pygame.QUIT:
                  
                  run=False

          keys_pressed=pygame.key.get_pressed()

          if keys_pressed[pygame.K_ESCAPE]:
              pause=True

          if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]: #up

              if current_orint=="L" or current_orint=="R":
                  SNAKE_FACE_IMAGE_USED=pygame.transform.rotate(pygame.transform.scale( SNAKE_FACE_IMAGE ,(15,15)),270)

                  current_orint="U"

          if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]: #left

              if current_orint=="U" or current_orint=="D":
                  SNAKE_FACE_IMAGE_USED=pygame.transform.rotate(pygame.transform.scale( SNAKE_FACE_IMAGE ,(15,15)),0)

                  current_orint="L"

          if keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]: #down
              if current_orint=="L" or current_orint=="R":
                  SNAKE_FACE_IMAGE_USED=pygame.transform.rotate(pygame.transform.scale( SNAKE_FACE_IMAGE ,(15,15)),90)

                  current_orint="D"

          if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]: #right
              if current_orint=="U" or current_orint=="D":
                  SNAKE_FACE_IMAGE_USED=pygame.transform.rotate(pygame.transform.scale( SNAKE_FACE_IMAGE ,(15,15)),180)

                  current_orint="R"

          if current_orint=="R":
              snake_face.x+=VEL

          elif current_orint=="L":
              snake_face.x-=VEL

          elif current_orint=="U":
              snake_face.y-=VEL
          elif current_orint=="D":
              snake_face.y+=VEL




          run,POINT=collision(snake_face,WALL,POINT)
          draw(snake_face,point_obj,WALL)

    return user_text,POINT
    pygame.quit()



def post_game_stuff(file_name,user_text,POINT):
    name=user_text[1:-1]
    if  len(content)!=5:
        content.append([POINT,name])
    elif POINT>content[-1][0]:
        content.pop()
        content.append([POINT,name])
    content.sort()
    content2=content[::-1]
    a=open(file_name,"wb")
    pickle.dump(content2,a)
    a.close()







if __name__=="__main__":
    WALL=walls()
    name,POINT=main(WALL)
    post_game_stuff("Highscore.bin",name,POINT)
    
    

