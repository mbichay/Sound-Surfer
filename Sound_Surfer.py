##################### Imports #####
import pygame                     #
import pygame._view               #
import sys                        #
import numpy as np                #
import math                       #
import array                      #
import os                         #
from random import randint        #
import pickle                     #
sys.path.append("res\\")          #
import eztext                     #
###################################


#######################Database Class#################
class database(object): #class that will manage all the music already seen once by the game
    def __init__(self):
        self.data=[] # array of game name
        self.datapath="save\\database.data" 
        if not os.path.exists('save'): # make save folder is save doesn't exist
            os.makedirs('save')
        if (os.path.isfile(self.datapath)==False): # if no file exist create one
            self.update_database()
        else: # else open the data file and update data
            with open(self.datapath, 'rb') as input:
                old_data = pickle.load(input)
            self += old_data # OVERLOADING MUHAHA (just concatenate the two list)

    def add_to_database(self,name): # add a name to the database
        self +=  name
        self.data.sort()
        self.update_database()

    def del_to_database(self,name): # del a name from the database
        self -= name
        self.data.sort()
        self.update_database()


    def check_database(self,name): # if name exist; return true, else return false
        for i in range (0,len(self.data)):
            if self.data[i]==name:
                return True
        return False


    def update_database(self): # overwrite the old data file with new data (or create the file)
        with open(self.datapath, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    def destroy_database(self):
        self.data=[]
        self.update_database()

        
    def remove_duplicate(self):
        self.data.sort()
        corr=0
        for i in range(0,len(self.data)-1):
            if (i==len(self.data)-corr):
                break
            while (self.data[i]==self.data[i+1]):
                del self.data[i]
                corr+=1
                i-=1
                if (i==len(self.data)-1):
                    break

    def __add__(self,other):
        if isinstance(other, self.__class__):
            self.data += other.data
        elif isinstance(other, str):
            self.data += [other]
        return self
    def __sub__(self,other):

        if isinstance(other, self.__class__):
            for i in range (0,len(other.data)):
                while (self.data.count(other.data[i])):
                    self.data.remove(other_date[i])

        elif isinstance(other, str):
            while (self.data.count(other)):
                self.data.remove(other) 
        return self


#######################Player Class#################
class player(object):
    def __init__(self):
        self.player_x = 20 ## starting X coordinate
        self.player_y = 200 ## starting Y coordinate
        self.player = pygame.image.load('res\\play-button.jpg')
        self.key = pygame.key.get_pressed() ## setting variable key = to input event key press
    """self.run_dist = 10 ## Obsolete way to move your character with keyboard

    def handle_keys(self,l):
        self.key = pygame.key.get_pressed() ## key press init
        if self.key[pygame.K_DOWN]: ## if down button is pressed
            self.player_y += self.run_dist
            if self.player_y >= (l-10): ## keeps your stupid square from leaving
                self.player_y = (l-10) ## the map, this is temporary
        elif self.key[pygame.K_UP]: ## same with this
            self.player_y -= self.run_dist
            if self.player_y <= 0:
                self.player_y = 0"""

    def mouse_movement(self):
        self.player_y = pygame.mouse.get_pos()[1] # get y axis value of the mouse
        pygame.mouse.set_pos([self.player_x,self.player_y])# set mouse to player position
    def collision(self,level,game):
        if (self.player_y<=level.left_energy[game.time+1]/level.rescale):
            return True;
        elif(self.player_y>=(game.l-level.right_energy[game.time+1]/level.rescale)):
            return True;
        else :
            return False;


    def draw(self, gameDisplay): 
        gameDisplay.blit(self.player, (self.player_x, self.player_y))

#######################################################



########################## Level Class ####################
class level(object): 
    def __init__(self,w):
        self.COLOR = (255,0,0) # Color of the wave
        self.left_energy=None # left energy value note : different from the beat value
        self.right_energy=None
        self.draw=int(w/20) # variable to avoid out of bound error at the very end of the elvel
        self.rescale=4.0 # rescale waves value to fit the screen (could do a calculus for better results)


    def draw_topbottom(self, game): # draw rectangle at the top and bottom of the game using pygame.draw.rect
        if (len(self.left_energy)<=(game.time + self.draw)) : # if less than self.draw elements left, draw one less
            self.draw-=1
        red=self.COLOR[0] # color is a tuple ,it's impossible to says color[0]=value
        green=self.COLOR[1]
        blue=self.COLOR[2]
        self.COLOR= (red,green,blue)
        if (game.time)%(255*6)<255 : # color pattern
            green+=1
        elif (game.time)%(255*6)<510 :
            red-=1
        elif (game.time)%(255*6)<765 :
            blue+=1
        elif (game.time)%(255*6)<1020 :
            green-=1
        elif (game.time)%(255*6)<1275 :
            red+=1
        else:
            blue-=1
        self.COLOR= (red,green,blue) # instead overwrite value each frame
        for i in range(0,self.draw): # draw rectangles
            pygame.draw.rect(game.gameDisplay, self.COLOR, [ 10 + 20*i,0 ,10, self.left_energy[game.time + i]/self.rescale]) ## this function call is for drawing the rectangle in updaed locations
            pygame.draw.rect(game.gameDisplay, self.COLOR, [ 10 + 20*i,(game.l - self.right_energy[game.time + i]/self.rescale ) ,10, self.right_energy[game.time + i]/self.rescale]) ## this function call is for drawing the rectangle in updaed locations

    def calculating_level(self,beat,game): # turn raw data of the music + beat calculus into a level, wich will be drawn part by part by the function above
        instant_e_sps = int(44032/(1024.0*game.difficulty_setting)) # 1 beat on that number of rectangles
        self.left_energy = beat.left_energy
        self.right_energy = beat.right_energy

        if game.difficulty_setting==1: # set different var for difficulty setting
            min_space=int(game.l*(1/3.5)) # min spacing between top and bottom (avoid walls)
            mult_height=self.rescale*4 # multiplication of the beat value
            sharpness=5 # sharpness of the sinwave created by beat
            RNG_ajust_value=2 # ajust RNG to avoid full up beat or full down beat
        elif game.difficulty_setting==2:
            min_space=int(game.l*(1/4.0))
            mult_height=self.rescale*3
            sharpness=3
            RNG_ajust_value=1
        else:
            min_space=int(game.l*(1/4.0))
            mult_height=self.rescale*2
            sharpness=1
            RNG_ajust_value=0
        old_random=randint(0,10)
        random=randint(0,10)
        RNG_ajust=0
        wait=0 # var to delay print of the next wall of two of them are super close
        ok=1 # print normally if ok==1 , delayed if ok ==0
        for i in range ( 43 , len(beat.beat_array[game.difficulty_setting-1,:])) :

                            
            if ((i+2*sharpness<len(beat.beat_array[game.difficulty_setting-1,:]))and(beat.beat_array[game.difficulty_setting-1,i+sharpness]==1)):# if not out of bound and there i a beat nearby
                old_random=random
                random=randint(0,10) + RNG_ajust
                if int(old_random/5)!=int(random/5):
                    RNG_ajust=0
                elif not int(random/5):
                    RNG_ajust+=1
                else :
                    RNG_ajust-1
                  
                for j in range(0,2*sharpness): # create the beat sin wave
                    if (random<5):
                        self.left_energy[i + j + wait]+=  mult_height*self.left_energy[i + j + wait]*math.sin(math.pi*j/(2*sharpness))
                        if ((self.left_energy[i + j + wait] + self.right_energy[i + j + wait])/self.rescale)>(game.l-min_space): # if not enought space
                            self.left_energy[i + j + wait]= self.rescale*(game.l-min_space) -(self.right_energy[i + j + wait] ) # crop the wave
                    else :
                        self.right_energy[i + j + wait]+=  mult_height*self.right_energy[i + j + wait]*math.sin(math.pi*j/(2*sharpness))
                        if ((self.left_energy[i + j + wait] + self.right_energy[i + j + wait])/self.rescale)>(game.l-min_space):
                            self.right_energy[i + j + wait]= self.rescale*(game.l-min_space) -(self.left_energy[i + j + wait] )
                if ok:
                    wait=int(instant_e_sps/2)
                    ok=0


            elif wait : 
                wait-=1
                if not wait :
                    ok=1

#######################################################



########################## Game Class ####################


class game(object): # main class, who will run the game
    def __init__(self,w,l):
        self.w=w # width
        self.l=l #lenght
        self.time=0 # where you are on the music
        self.gameDisplay=pygame.display.set_mode((self.w,self.l)) ## size of window
        self.difficulty_setting=1
        self.score=0
        self.BACKGROUND_COLOR = (0, 0, 0)
        self.TEXTCOLOR = (255,255,255)
        self.clock = 0
        self.fps=44100/1024.0 # =43
        myfont = pygame.font.SysFont("Comic Sans MS", int(self.w/25))
        self.txtbx = eztext.Input(maxlength=45, color=self.TEXTCOLOR,x = self.w/12,y = self.l*(3/4) , font = myfont,prompt = "Enter here: ")# textbox for the "GUI"



    def initialize(self): # initialize some variables for the game
        self.clock = pygame.time.Clock() # Clock for menu, callback, etc
        pygame.display.set_caption('Sound Surfer -- By: Maxime Hemion & Matthew Bichay') # lol
        dog = pygame.image.load('res\\dog.jpg') # AMAZING EASTER EGG HUEHUEHUEHUE
        pygame.display.set_icon(dog)
        self.gameDisplay.fill((self.BACKGROUND_COLOR))
        pygame.display.update()



    def game_states(self,beat,level,player,database,high_score): # int main(){ blablabla }
        self.initialize()
        game.main_menu(database) # menu displayed before game starts
        if not(beat.check_update_database(game,level,database)): # layer of protection that will quit the game if there is any problem + update the database if needed
            self.quit_game()
            return
        
        high_score.load_create_file(beat.name) # create highscore
        level.calculating_level(beat,self) # calculate the level (2 runs of the same music end on a different level (beat up or down)
        self.start_game() # press Enter menu
        restart=1
        while (restart==1):
            self.play(beat,level,player) # game running
            restart=high_score.display_highscore(self,self.update_hscr(high_score))
        self.quit_game()


    def play(self,beat,level,player):
        
        game.score=0 # restart some variable for replay
        level.draw=int(game.w/20)
        level.COLOR = (255,0,0)
        self.time=0
        player.player_y = 200
        musicfile=pygame.sndarray.make_sound(beat.audio)# make sound for audio samples
        pygame.mixer.Sound.play(musicfile)# play them
        endGame = False
        pygame.mouse.set_visible(0)
        while (endGame == False):
            for event in pygame.event.get(): #this checks for events, the quit one is for pressing X on the pygame window
                if (event.type == pygame.QUIT):
                    endGame = True
            pygame.event.get()
            if (pygame.key.get_pressed()[pygame.K_ESCAPE]):
                self.quit_game()
            if (len(beat.left_energy) + int(self.w/20) )<self.time:# EOF reached
                endGame = True
            self.gameDisplay.fill((self.BACKGROUND_COLOR)) #repaint the gamedisplay 
            player.mouse_movement() #mouse movement
            #player.handle_keys(self.l) ## call for checking movement - OBSOLETE
            if (self.time + 1 < len(beat.left_energy)):
                endGame=player.collision(level,self)
            player.draw(self.gameDisplay) ## draw new player location
            level.draw_topbottom(self)
            if ((self.time%15)==0): # regulate FPS because 44100/1024 !=43
                self.fps=44
            else:
                self.fps=43
            self.time+=1
            self.score+=self.difficulty_setting
            pygame.display.update() ## update display
            pygame.display.set_caption('Sound Surfer -- By: Maxime Hemion & Matthew Bichay -- [ Score: %d ]' %self.score) # lol
            self.clock.tick(self.fps) ## fps


         
    def display_message(self,label,pos_x,pos_y): # homemade function to display one message on the screen
        self.gameDisplay.fill((self.BACKGROUND_COLOR))
        self.gameDisplay.blit(label, (pos_x, pos_y))
        pygame.display.update()


    def start_game(self):
        myfont = pygame.font.SysFont("Comic Sans MS", int(self.w/20))
        label = myfont.render("Ready? [Press Enter]", 1, self.TEXTCOLOR)
        game.display_message(label,self.w/4,180)
        while (1):
            pygame.event.get()
            if (pygame.key.get_pressed()[pygame.K_RETURN]):
                break
            self.clock.tick(60)


    def main_menu(self, data): # main menu shown at the very beggining of the program, could be less hardcoded, sorry
        easy_color=(0,255,0) # green
        medium_color=(255,255,0)# yellow
        hard_color=(255,0,0)# red
        unused=(100,100,100)
        myfont = pygame.font.SysFont("Comic Sans MS", int(self.w/35))
        new_song_label = myfont.render("1. Input a new song!", 1, self.TEXTCOLOR)
        pick_song_label = myfont.render("2. Pick an already existing song!", 1, self.TEXTCOLOR)
        instruction_label =myfont.render("Use the keyboard to navigate the menu", 1, self.TEXTCOLOR)
        play_label =myfont.render("Press Enter when you are ready", 1, self.TEXTCOLOR)
        easy_label =myfont.render("EASY", 1, easy_color)
        medium_label =myfont.render("MEDIUM", 1, unused)
        hard_label =myfont.render("HARD", 1, unused)
        
        sound_name ="The sound you will choose will be displayed here"
        your_sound_label=myfont.render(sound_name, 1, self.TEXTCOLOR)
        self.gameDisplay.blit(new_song_label, (self.w/12, 100))
        self.gameDisplay.blit(pick_song_label, (self.w/12, 300))
        pygame.display.update()
        filename = ""
        come_from=0 # infos where you input the sound
        refresh=1
        while(1):
            if refresh: # does not to display all that stuff each tick of the clock
                self.gameDisplay.fill((self.BACKGROUND_COLOR))
                self.gameDisplay.blit(new_song_label, (self.w/12, self.l/5))
                self.gameDisplay.blit(pick_song_label, (self.w/12, 3*self.l/10))
                self.gameDisplay.blit(instruction_label, (self.w/12, self.l/10))
                self.gameDisplay.blit(easy_label, (self.w/12, 7*self.l/10))
                self.gameDisplay.blit(medium_label, (self.w/4 + self.w/12, 7*self.l/10))
                self.gameDisplay.blit(hard_label, (self.w/2 + self.w/12, 7*self.l/10))
                self.gameDisplay.blit(your_sound_label, (self.w/12, 8*self.l/10))
                self.gameDisplay.blit(play_label, (self.w/12, 9*self.l/10))
                pygame.display.update()
                refresh=0
                self.clock.tick(0) # 3 lines to pause the GUI for a bit when you press a button
                pygame.time.wait(100)
                self.clock.tick(30)

            pygame.event.get()
            
            if (pygame.key.get_pressed()[pygame.K_1]): 
                
                filename = game.write("Type your sound here","Attention : Your sound must be in the same folder as this program")
                come_from=0
                your_sound_label=myfont.render("Your sound is : " + filename, 1, self.TEXTCOLOR)
                refresh=1
            elif (pygame.key.get_pressed()[pygame.K_2]):
                come_from=1
                filename = game.main_menu_pick(data.data)
                your_sound_label=myfont.render("Your sound is : " + filename, 1, self.TEXTCOLOR)
                refresh=1
            elif (pygame.key.get_pressed()[pygame.K_e]):
                easy_label =myfont.render("EASY", 1, easy_color)
                medium_label =myfont.render("MEDIUM", 1, unused)
                hard_label =myfont.render("HARD", 1, unused)
                self.difficulty_setting=1
                refresh=1
            elif (pygame.key.get_pressed()[pygame.K_m])or(pygame.key.get_pressed()[pygame.K_SEMICOLON ]):
                easy_label =myfont.render("EASY", 1, unused)
                medium_label =myfont.render("MEDIUM", 1, medium_color)
                hard_label =myfont.render("HARD", 1, unused)
                self.difficulty_setting=2
                refresh=1
            elif (pygame.key.get_pressed()[pygame.K_h]):
                easy_label =myfont.render("EASY", 1, unused)
                medium_label =myfont.render("MEDIUM", 1, unused)
                hard_label =myfont.render("HARD", 1, hard_color)
                self.difficulty_setting=3
                refresh=1
            elif (pygame.key.get_pressed()[pygame.K_RETURN])and((os.path.isfile(filename + ".wav")) or (os.path.isfile("save\\" + filename  + ".level"))):
                beat.change_sound(filename)
                break
            elif (pygame.key.get_pressed()[pygame.K_RETURN])and not come_from and(not(os.path.isfile(filename + ".wav")) and not(os.path.isfile("save\\" + filename  + ".level"))):
                your_sound_label=myfont.render("Oops, it seems that the sound you asked is not readable", 1, self.TEXTCOLOR)
                refresh=1
            elif (pygame.key.get_pressed()[pygame.K_RETURN])and(not(os.path.isfile(filename + ".wav")) and not(os.path.isfile("save\\" + filename  + ".level"))):
                your_sound_label=myfont.render("Oops, the sound is absent from the database, I will delete it from the option menu", 1, self.TEXTCOLOR)
                data.del_to_database(filename)
                refresh=1
            elif (pygame.key.get_pressed()[pygame.K_ESCAPE]):
                self.quit_game()
                

        
    def main_menu_pick(self, data): # menu for choosing a music from the database, will print only 5 sound at the same time
        myfont = pygame.font.SysFont("Comic Sans MS", int(self.w/35))
        next_label = myfont.render("6. Next Page", 1, self.TEXTCOLOR)
        prev_label = myfont.render("0. Previous Page", 1, self.TEXTCOLOR)
        instructions_1 = myfont.render("Press 0 to 6 buttons of your keyboard to ", 1, self.TEXTCOLOR)
        instructions_2 = myfont.render("navigate the menu and choose a sound", 1, self.TEXTCOLOR)
        self.gameDisplay.fill((self.BACKGROUND_COLOR))
        self.gameDisplay.blit(next_label, (650, 430))
        self.gameDisplay.blit(prev_label, (25, 430))
        pygame.display.update()
        page = 0 # if there is more than 5 songs on the database, they will be displayed on differents pages, keys 0 and 6 allows to change pages
        maxpage = int(len(data)/5)
        change_page=1
        while (1):
            if (change_page) :
                self.clock.tick(0)
                pygame.time.wait(100)
                self.clock.tick(30)
                if not len(data):
                    return "database empty" # if the database is empty, return

                label_1=myfont.render("1. " + data[5*page], 1, self.TEXTCOLOR)
                if (5*page + 1)<len(data): # avoid out of bound 
                    label_2=myfont.render("2. " + data[5*page + 1], 1, self.TEXTCOLOR)
                else :
                    label_2=myfont.render(" " , 1, self.TEXTCOLOR)
                if (5*page + 2)<len(data):
                    label_3=myfont.render("3. " + data[5*page + 2], 1, self.TEXTCOLOR)
                else :
                    label_3=myfont.render(" " , 1, self.TEXTCOLOR)
                if (5*page + 3)<len(data):
                    label_4=myfont.render("4. " + data[5*page + 3], 1, self.TEXTCOLOR)
                else :
                    label_4=myfont.render(" " , 1, self.TEXTCOLOR)
                if (5*page + 4)<len(data):
                    label_5=myfont.render("5. " + data[5*page + 4], 1, self.TEXTCOLOR)
                else :
                    label_5=myfont.render(" " , 1, self.TEXTCOLOR)
                change_page=0
                self.gameDisplay.fill((self.BACKGROUND_COLOR))
                self.gameDisplay.blit(instructions_1, (self.w/8, 20))
                self.gameDisplay.blit(instructions_2, (self.w/8, 70))
                self.gameDisplay.blit(label_1, (self.w/4, 150))
                self.gameDisplay.blit(label_2, (self.w/4, 200))
                self.gameDisplay.blit(label_3, (self.w/4, 250))
                self.gameDisplay.blit(label_4, (self.w/4, 300))
                self.gameDisplay.blit(label_5, (self.w/4, 350))
                self.gameDisplay.blit(next_label, (650, 430))
                self.gameDisplay.blit(prev_label, (25, 430))
                pygame.display.update()
    
            pygame.event.get()
            if (pygame.key.get_pressed()[pygame.K_0]): # go the previous page or return to the main menu
                if page >= 1:
                    page-=1
                    change_page=1
                else:
                    return ""
            elif (pygame.key.get_pressed()[pygame.K_6]): # go the next page (if possible)
                if page < maxpage:
                    page +=1
                    change_page=1
            elif (pygame.key.get_pressed()[pygame.K_1]): # choose a data,if possible
                return data[5*page]
            elif (pygame.key.get_pressed()[pygame.K_2]) and (5*page + 1)<len(data):
                return data[5*page+1]
            elif (pygame.key.get_pressed()[pygame.K_3]) and (5*page + 2)<len(data):
                return data[5*page+2]
            elif (pygame.key.get_pressed()[pygame.K_4]) and (5*page + 3)<len(data):
                return data[5*page+3]
            elif (pygame.key.get_pressed()[pygame.K_5]) and (5*page + 4)<len(data):
                return data[5*page+4]


    def write(self,instruction1,instruction2): # function to input something from the keyboard using eztxt library, nasty bug force my to have the same function for all keyboard input
        myfont = pygame.font.SysFont("Comic Sans MS", int(self.w/35))
        instruction_label =myfont.render(instruction1, 1, self.TEXTCOLOR) # blablabla before typing
        instruction2_label =myfont.render(instruction2, 1, self.TEXTCOLOR)
        self.clock.tick(30)
        while(1):
            self.gameDisplay.fill((self.BACKGROUND_COLOR))
            self.gameDisplay.blit(instruction_label, (self.w/12, self.l/10))
            self.gameDisplay.blit(instruction2_label, (self.w/12, self.l/5))
            self.txtbx.update(pygame.event.get())
            self.txtbx.draw(self.gameDisplay)
            pygame.display.update()
            if (pygame.key.get_pressed()[pygame.K_RETURN]):
                return self.txtbx.value



    def update_hscr(self,highscore): # function that check if highscore need to be updated and manage the add name part for highscore
        pygame.mixer.stop()
        pygame.mouse.set_visible(1)
        index =len(highscore.value)
        for i in range(0,len(highscore.value)):
            if game.score>highscore.value[i]:
                index=i
                break
        if index!=len(highscore.value):
            ok=0
            while not ok:
                myfont = pygame.font.SysFont("Comic Sans MS", int(self.w/35))
                yes_label =  myfont.render("Y - Yes", 1, self.TEXTCOLOR)
                no_label = myfont.render("N - No", 1, self.TEXTCOLOR)


                your_name=self.write("Enter your name for the highscore leaderboard :"," ")
                for i in range(0,len(highscore.value)):
                    if your_name==highscore.name[i]:
                        instruction_label = myfont.render("There is already " + your_name +" on the leaderboard, is it you ?", 1, game.TEXTCOLOR)
                        self.gameDisplay.fill((self.BACKGROUND_COLOR))
                        self.gameDisplay.blit(instruction_label, (self.w/12, self.l/10))
                        self.gameDisplay.blit(yes_label, (self.w/12, self.l/2))
                        self.gameDisplay.blit(no_label, (self.w/2 + self.w/12, self.l/2))
                        pygame.display.update()
                        while(1):
                            pygame.event.get()
                            if (pygame.key.get_pressed()[pygame.K_y]):
                                ok = 1
                                win_quote=highscore.win_quote[i]
                                lose_quote=highscore.lose_quote[i]
                                break
                            elif (pygame.key.get_pressed()[pygame.K_n]):
                                break
                if ok==1:
                    break
                self.clock.tick(0)
                pygame.time.wait(100)
                self.clock.tick(30)
                instruction_label = myfont.render("Do you want to add a win quote to your name ?", 1, self.TEXTCOLOR)
                self.gameDisplay.fill((self.BACKGROUND_COLOR))
                self.gameDisplay.blit(instruction_label, (self.w/12, self.l/10))
                self.gameDisplay.blit(yes_label, (self.w/12, self.l/2))
                self.gameDisplay.blit(no_label, (self.w/2 + self.w/12, self.l/2))
                pygame.display.update()
                while (1) :
                    pygame.event.get()
                    if (pygame.key.get_pressed()[pygame.K_y]):
                        win_quote=self.write(" "," ")
                        break
                    elif (pygame.key.get_pressed()[pygame.K_n]) :
                        win_quote=""
                        break
                self.clock.tick(0)
                pygame.time.wait(100)
                self.clock.tick(30)
                instruction_label = myfont.render("Do you want to add a lose quote to your name ?", 1, self.TEXTCOLOR)
                game.gameDisplay.fill((self.BACKGROUND_COLOR))
                game.gameDisplay.blit(instruction_label, (self.w/12, self.l/10))
                game.gameDisplay.blit(yes_label, (self.w/12, self.l/2))
                game.gameDisplay.blit(no_label, (self.w/2 + self.w/12, self.l/2))
                pygame.display.update()                
                while (1) :
                    pygame.event.get()
                    if (pygame.key.get_pressed()[pygame.K_y]):
                        lose_quote=self.write(" "," ")
                        break
                    elif (pygame.key.get_pressed()[pygame.K_n]) :
                        lose_quote=""
                        break
                self.clock.tick(0)
                pygame.time.wait(100)
                self.clock.tick(30)
                instruction_label = myfont.render("Your informations are :", 1, game.TEXTCOLOR)
                name_label = myfont.render("Your name :" + your_name, 1, game.TEXTCOLOR)
                win_quote_label = myfont.render("Your win quote :" + win_quote, 1, game.TEXTCOLOR)
                lose_quote_label = myfont.render("Your lose quote :" + lose_quote, 1, game.TEXTCOLOR)
                game.gameDisplay.fill((game.BACKGROUND_COLOR))
                game.gameDisplay.blit(instruction_label, (self.w/12, self.l/10))
                game.gameDisplay.blit(name_label, (game.w/8, game.l/5))
                game.gameDisplay.blit(win_quote_label, (self.w/8, self.l*3/10))
                game.gameDisplay.blit(lose_quote_label, (self.w/8, game.l*4/10))
                game.gameDisplay.blit(yes_label, (self.w/12, self.l/2))
                game.gameDisplay.blit(no_label, (self.w/2 + self.w/12, self.l/2))
                pygame.display.update()
                while (1) :
                    pygame.event.get()
                    if (pygame.key.get_pressed()[pygame.K_y]):
                        ok=1
                        break
        
                    elif (pygame.key.get_pressed()[pygame.K_n]) :
                        ok=0
                        break
                
            highscore.value.pop()
            highscore.value.insert(index,game.score)
            highscore.name.pop()
            highscore.name.insert(index,your_name)            
            highscore.win_quote.pop()
            highscore.win_quote.insert(index,win_quote)            
            highscore.lose_quote.pop()
            highscore.lose_quote.insert(index,lose_quote)
            highscore.update_file()
        return index


   
    def quit_game(self): # function that stop the code if called
        pygame.quit()
        sys.exit()
        quit()

########################### Music class ##########################

class music_file(object): # class that contain all data from a musicfile
    def __init__(self,name):
        self.name=name
        pygame.mixer.quit() # rest the mixer fo a weird reason
        pygame.mixer.init(44100) # only work with 44,1khz music ( normal recording value, 22,05khz is low quality garbage)
        if (os.path.isfile("save\\" + self.name  + ".level")): # if file exist, import all the stuff on it
            with open("save\\" + self.name + ".level", 'rb') as input:
                    old_data = pickle.load(input)
            self.audio = old_data.audio # audio contains 2 lists of the right and left samples values
            self.beat_array= old_data.beat_array # beat contains 3 lists of 0 and 1 (0 for no beat and  1 for beat)
            self.left_energy = old_data.left_energy # left energy contains the sums of 1024 samples (left)
            self.right_energy = old_data.right_energy
        elif (os.path.isfile(self.name+ '.wav')):# elif wav file exist, prepare for calculus
            musicfile= pygame.mixer.Sound(self.name+ '.wav')
            self.audio = pygame.sndarray.samples(musicfile)
            instant_energy_samples=1024
            number_of_instant_energies = int(len(self.audio[:,0])/instant_energy_samples)
            self.beat_array=np.array([number_of_instant_energies*[0],number_of_instant_energies*[0],number_of_instant_energies*[0]])
            self.left_energy = number_of_instant_energies*[np.longdouble(0)]
            self.right_energy = number_of_instant_energies*[np.longdouble(0)]

        else :
            self.audio = None
            self.beat_array= None
            self.left_energy = None
            self.right_energy = None



    def check_update_database(self,game,level,database): # function who check if the music is reachable or not
        if (database.check_database(self.name)): # if file on the database
            if not (os.path.isfile("save\\" + self.name  + ".level")):
                database.del_to_database(self.name)
                return False
            else :

                return True
        else:
            if not (os.path.isfile(self.name  + ".wav")): 
                print ("Error, can't read your file")
                return False
            else :
                database.add_to_database(self.name)
                self.calculating_beat()
                with open("save\\" + self.name  +  ".level", 'wb') as f:
                    pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
                return True



    def change_sound(self,name): # doppleganger of the constructor, allows to change music during the program
        self.name=name
        pygame.mixer.quit()
        pygame.mixer.init(44100)
        if (os.path.isfile("save\\" + self.name  + ".level")):
            with open("save\\" + self.name + ".level", 'rb') as input:
                    old_data = pickle.load(input)
            self.audio = old_data.audio
            self.beat_array= old_data.beat_array
            self.left_energy = old_data.left_energy
            self.right_energy = old_data.right_energy
        elif (os.path.isfile(self.name+ '.wav')):
            musicfile= pygame.mixer.Sound(self.name+ '.wav')
            self.audio = pygame.sndarray.samples(musicfile)
            instant_energy_samples=1024
            number_of_instant_energies = int(len(self.audio[:,0])/instant_energy_samples)
            self.beat_array=np.array([number_of_instant_energies*[0],number_of_instant_energies*[0],number_of_instant_energies*[0]])
            self.left_energy = number_of_instant_energies*[np.longdouble(0)]
            self.right_energy = number_of_instant_energies*[np.longdouble(0)]
        else :
            print("Error, can't find your music file nor find it on the database")

    def calculating_beat(self): # "beat" calculus function
        left_channel= self.audio[:,0] # left chan
        right_channel= self.audio[:,1] #right chan
        instant_energy_samples=1024 # 1024 ~ 5millisecond with 44100 samples/second
        samples_in_one_second=44032 # rounded to 44032 instead of 44100 to have a round number with 1024
        number_of_instant_energies = int(len(left_channel)/instant_energy_samples) # number of instant energies is length of the song / 1024
        number_of_second=int(len(left_channel)/samples_in_one_second)
        #average_energy = number_of_second*[np.longdouble(0)] # <E>
        instant_energy = number_of_instant_energies*[np.longdouble(0)] # little e
        best_beat_index = 0
        loading_inc = number_of_second/100.0 ## incremental checker
        loading_perc = 0.0 ## starting percentage
        load_perc = 100.0/(number_of_second) ## percentage incrementer
        color =(255,255,255)
        myfont = pygame.font.SysFont("Comic Sans MS", int(game.w/20))
        label = myfont.render("Calculating Beat: %d%%" %loading_perc, 1, color) # percentage of work done indicator
        game.display_message(label,game.w/4,game.l/2)
        
        for j in range (0,3):
            best_beat_index = 0
            instant_e_sps = int(samples_in_one_second/(instant_energy_samples*(j+1))) # energy sample per second / diffulty ( ex : difficulty 1 number of samples in 1 sec, diffciulty 2 in half a second etc.)
            for i in range ( 0 , (j+1)*number_of_second) : # 0 - number of seconds
                pygame.event.get()
                best_beat_index = i*instant_e_sps#beat index
                if ((i + 1)*instant_e_sps>=len(self.left_energy)):# avoid going out of bound when j!=0 (calculus for difficulty medium and hard)
                    break
                for k in range (0,instant_e_sps) : # 0 - instant energy sample / second
                    if (j==0): # first time, make the calculus of sum of 1024 samples
                        for h in range (0 ,int(instant_energy_samples) ): # 0 - 1024
                            self.left_energy[i*instant_e_sps + k]+=abs(left_channel[i*int(samples_in_one_second/(j+1)) + k*int(instant_energy_samples/(j+1)) + h]/32768.0)
                            self.right_energy[i*instant_e_sps + k]+=abs(right_channel[i*int(samples_in_one_second/(j+1)) + k*int(instant_energy_samples/(j+1)) + h]/32768.0)
                        instant_energy[i*instant_e_sps + k] += pow(self.left_energy[i*instant_e_sps + k],2) + pow(self.right_energy[i*instant_e_sps + k],2)
                    #average_energy[int(i/difficulty_setting)] += instant_energy[i*int(instant_e_sps + k]/instant_e_sps
                    if (instant_energy[i*instant_e_sps + k]>instant_energy[best_beat_index]):
                        best_beat_index=i*instant_e_sps + k
                self.beat_array[j,best_beat_index] = 1
                if ((number_of_second)%loading_inc >= 0) and (j==0): # in fact it will reach 100% when easydifficulty will be finished, but because there is no need to calculate again the sum of all samples, the others difficultys are very fast to calculate
                    loading_perc += load_perc

                    label = myfont.render("Calculating Beat: %d%%" %loading_perc, 1, color)
                    game.display_message(label,game.w/4,180)


class highscore(object):
    def __init__(self):
        self.value=[5000,4500,4000,3500,3000,2500,2000,1500,1000,10]
        self.name=["Black Knight","Gandalf","Obama","Putin","Kim Jong Un","Sathya","GOT fan ","DD narrator","Definitely not Axel Banal ","Shadow of nothing"]
        self.win_quote=["I'm invincible","You shall not pass","No you can't "," . . .","My fantastic haircut remain unbeaten","You should improve your soft skills!","Winter is coming ","A trifling victory, but a victory none the less","You know !","How have you found me ?"]
        self.lose_quote=["It's just a flesh wound","Use the force Harry!","Thanks Obama "," . . . !","I will throw a nuclear bomb on you!","you will get an F!","I know nothing ","Remind yourself that overconfidence is a slow and insidious killer","Oh sh*t !"," "]
        self.sound_name = None

    def load_create_file(self,name):
        self.sound_name=name
        if not os.path.isfile("save\\" + self.sound_name  + ".hscr"):
            self.update_file()
        else:
            with open("save\\" + self.sound_name  + ".hscr", 'rb') as input:
                old_hscr = pickle.load(input)
                
            self.value=old_hscr.value
            self.name=old_hscr.name
            self.win_quote=old_hscr.win_quote
            self.lose_quote=old_hscr.lose_quote

    def update_file(self):
        with open("save\\" + self.sound_name  + ".hscr", 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

            
    def display_highscore(self,game,index):
        myfont = pygame.font.SysFont("Comic Sans MS", int(game.w/50))
        game.gameDisplay.fill((game.BACKGROUND_COLOR))
        display_lenght=0
        title_label =  myfont.render(" **** HIGHSCORE LEADERBOARD : ****", 1, game.TEXTCOLOR)
        game.gameDisplay.blit(title_label, (game.w/4, 0 ))
        pygame.display.update()
        score_label2 =  myfont.render( " . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . " , 1, game.TEXTCOLOR)
        for i in range (0,len(self.value)):
            score_label1 =  myfont.render(self.name[i], 1, game.TEXTCOLOR)
           
            score_label3 =  myfont.render(str(self.value[i]), 1, game.TEXTCOLOR)
            if index<i:
                quote_label = myfont.render(self.lose_quote[i], 1, (255,0,0))
            else :
                quote_label = myfont.render(self.win_quote[i], 1, (0,255,0))
                
            game.gameDisplay.blit(score_label1, (game.w/12,display_lenght + game.l/24 ))
            game.gameDisplay.blit(score_label2, (game.w/2,display_lenght + game.l/24 ))
            game.gameDisplay.blit(score_label3, (game.w*5/6,display_lenght + game.l/24 ))

            
            game.gameDisplay.blit(quote_label, (game.w/8,display_lenght + game.l/12 ))
            display_lenght+=game.l/12
            pygame.display.update()
        label = myfont.render("Restart [Press R], Quit [Press ESC]", 1, game.TEXTCOLOR)
        game.gameDisplay.blit(label, (game.w/4,game.l*11/12 ))
        pygame.display.update()
        game.clock.tick(30)
        while (1):
            pygame.event.get()
            if (pygame.key.get_pressed()[pygame.K_r]):
                return 1
            elif (pygame.key.get_pressed()[pygame.K_ESCAPE]):
                return 0
            
        
        
        
        


pygame.init()
pygame.mixer.pre_init(frequency=44100) #frequency of song, init mixer
pygame.mixer.init()


#######################MAIN#################################
game=game(900,500)
data = database()

#must go inbetween here
beat=music_file("")
player = player()
high_score=highscore()
#print (len(high_score.value),type(high_score.value),len(high_score.name),type(high_score.name),len(high_score.quote_win),type(high_score.quote_win),len(high_score.quote_lose),type(high_score.quote_lose))
level = level(game.w)

game.game_states(beat,level,player,data,high_score)
game.quit_game()

############################################################
