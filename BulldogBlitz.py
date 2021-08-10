import cv2
import pygame
import numpy as np
import copy

# gets pictures of players and stores them in files b%i.png
def getPic(num_players):

    cam = cv2.VideoCapture(0)
    cv2.startWindowThread()
    #cv2.namedWindow("Player Pictures", cv2.WND_PROP_FULLSCREEN)#cv2.WINDOW_NORMAL)
    cv2.namedWindow("Player Pictures", cv2.WINDOW_NORMAL)#WND_PROP_FULLSCREEN)#cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Player Pictures", cv2.WND_PROP_FULLSCREEN, cv2.WND_PROP_FULLSCREEN)#CV_WINDOW_FULLSCREEN);
    #cv2.setWindowProperty("Player Pictures", cv2.WND_PROP_FULLSCREEN,
    #                      cv2.WINDOW_FULLSCREEN)
    #cv2.setWindowProperty("Player Pictures", cv2.WND_PROP_FULLSCREEN, cv2.WND_PROP_FULLSCREEN)

    font                   = cv2.FONT_HERSHEY_SIMPLEX
    topLeftCornerOfText    = (10,25)
    bottomLeftCornerOfText = (10,700)
    fontScale              = 1
    fontColor              = (255,255,255)
    lineType               = 2
    


    # Start coordinate, here (0, 0)
    # represents the top left corner of image
    #start_point = (0, 0)
    ## represents the bottom right corner of image
    #end_point = (250, 250)
    # Green color in BGR
    color = (0, 255, 0)
    # Line thickness of 9 px
    thickness = 9
    
    frame = None
    pic_captured = False 
    decided = False
    img_counter = 1
    while True:
          
        k = cv2.waitKey(1)
        if not pic_captured and not decided:
            # capture pic and 
            ret, orig_frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            frame = copy.deepcopy(orig_frame)

            frame_width = frame.shape[1]
            frame_height = frame.shape[0]
            frame = cv2.line(frame, (int(frame_width*0.33), int(frame_height*.15)), (int(frame_width*0.67), int(frame_height*0.15)), color, thickness)
            frame = cv2.line(frame, (int(frame_width*0.33), int(frame_height*.85)), (int(frame_width*0.67), int(frame_height*0.85)), color, thickness)
            frame = cv2.line(frame, (int(frame_width*0.33), int(frame_height*.15)), (int(frame_width*0.33), int(frame_height*0.85)), color, thickness)
            frame = cv2.line(frame, (int(frame_width*0.67), int(frame_height*.15)), (int(frame_width*0.67), int(frame_height*0.85)), color, thickness)

            cv2.putText(frame,'Player %s'%img_counter, 
                topLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)
            cv2.putText(frame,'Capture (Press Space)', 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)
            cv2.imshow("Player %s Picture" % img_counter, frame)
            if k%256 == 32:
                # SPACE pressed
                pic_captured = True
                decided = False
                #cv2.imwrite("b%s.png"%img_counter, frame)
        elif pic_captured and not decided:
            cv2.imshow("Player %s Picture" % img_counter, orig_frame)
            cv2.putText(orig_frame,'Player %s'%img_counter, 
                topLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)
            cv2.putText(orig_frame,'Accept (Space) / Redo (Escape)', 
                bottomLeftCornerOfText, 
                font, 
                fontScale,
                fontColor,
                lineType)

            frame_width = frame.shape[1]
            frame_height = frame.shape[0]
            orig_frame = cv2.line(orig_frame, (int(frame_width*0.33), int(frame_height*.15)), (int(frame_width*0.67), int(frame_height*0.15)), color, thickness)
            orig_frame = cv2.line(orig_frame, (int(frame_width*0.33), int(frame_height*.85)), (int(frame_width*0.67), int(frame_height*0.85)), color, thickness)
            orig_frame = cv2.line(orig_frame, (int(frame_width*0.33), int(frame_height*.15)), (int(frame_width*0.33), int(frame_height*0.85)), color, thickness)
            orig_frame = cv2.line(orig_frame, (int(frame_width*0.67), int(frame_height*.15)), (int(frame_width*0.67), int(frame_height*0.85)), color, thickness)

            if k%256 == 27:
                pic_captured = False
                decided = False
            if k%256 == 32:
                # SPACE pressed
                cv2.imwrite("b%s.png"%img_counter, orig_frame)
                img_counter += 1
                pic_captured = False
                decided = False
                if img_counter==num_players+1:
                    break
    
    cam.release()
    cv2.destroyAllWindows()

# ask user how many players
print("How many players? (max 3)")
num_players = int(input())

# get pictures of players
getPic(num_players)

pygame.init()
bulldogs_font = pygame.font.Font('arial.ttf', 65)
bulldogs_textsurface = bulldogs_font.render('AHS BULLDOGS', False, (210, 210, 210))
bulldogs_textsurface = pygame.transform.rotate(bulldogs_textsurface, 270)

join_today_font = pygame.font.Font('arial.ttf', 28)
join_today_textsurface = join_today_font.render('Join Girls who Code Today!', False, (255, 255, 255))

# Set up the drawing window
#screen = pygame.display.set_mode([500, 500])
display_width = 800
display_height = 600

screen = pygame.display.set_mode((display_width,display_height), pygame.FULLSCREEN)
pygame.display.set_caption('Bulldog Blitz')


#players = [pygame.image.load('p1.png') for i in range(num_players)]
#players = [pygame.transform.scale(players[i], (50, 50)) for i in range(num_players)]

class Turtle:
    pass
class Player:
    pass

# load bulldog asset
bulldog = pygame.image.load('bulldog.png')
bulldog = pygame.transform.scale(bulldog, (175, 125))

# load in crown
crown = pygame.image.load('crown.png')
crown = pygame.transform.scale(crown, (300, 250))
crown = pygame.transform.rotate(crown, 45)

# load in frame
frame = pygame.image.load('frame.png')
frame = pygame.transform.scale(frame, (410, 410))

#x = (display_width * 0.45)
#y = (display_height * 0.8)

# game clock
clock = pygame.time.Clock()

# math to figure out placement of bulldogs and heads
screen_height_div_bulldogs = display_height // num_players 
excess_height = screen_height_div_bulldogs - bulldog.get_height()
face_vertical_offset = 32
assert excess_height > 0, "Too many players."
t = Turtle()
t_orig = Turtle()
t.x = [display_width * 0.05 for i in range(num_players)]
t_orig.y = [screen_height_div_bulldogs*i + 0.5*excess_height for i in range(num_players)]
t.y = [screen_height_div_bulldogs*i + 0.5*excess_height for i in range(num_players)]
p = Player()
p_orig = Player()
p.x = [display_width * 0.18 for i in range(num_players)]
p_orig.y = [screen_height_div_bulldogs*i + 0.5*excess_height + face_vertical_offset for i in range(num_players)]
p.y = [screen_height_div_bulldogs*i + 0.5*excess_height + face_vertical_offset for i in range(num_players)]
p.rate = [np.random.rand(1)*1.0+.0 for i in range(num_players)]

# load captured images
p.img_orig = [pygame.image.load('b%s.png'%(i+1)) for i in range(num_players)]

p_img_orig_width = p.img_orig[0].get_width()
p_img_orig_height = p.img_orig[0].get_height()
p.img_orig = [p.img_orig[i].subsurface((0.33*p_img_orig_width,0.15*p_img_orig_height, 0.35*p_img_orig_width, 0.71*p_img_orig_height)) for i in range(num_players)]
p.img = [pygame.transform.scale(p.img_orig[i], (50, 50)) for i in range(num_players)]

# audio assets
start_beep = pygame.mixer.Sound("beep_start.wav")
huffing = pygame.mixer.Sound("dog_panting.wav")
cheering = pygame.mixer.Sound("cheering.mp3")

# race variables
race_end = 700
# excess pixel beyond race_end to stop race
race_buffer = 10
running = True
racing_beep_time = False
make_crowd_cheer = False
almost_racing  = False
racing  = False
race_over = False
winner_num = -1

# run the game
while running:

    # check if it is times for sounds to start/stop
    if not race_over and almost_racing and racing_beep_time:
        pygame.mixer.Sound.play(start_beep)
        racing_beep_time = False

    if not race_over and almost_racing and not pygame.mixer.get_busy():
        almost_racing = False
        racing = True
        pygame.mixer.Sound.play(huffing)

    if make_crowd_cheer and not pygame.mixer.get_busy():
        pygame.mixer.Sound.play(cheering)
        make_crowd_cheer = False

    # collect user events and handle them
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not almost_racing and not racing and not race_over:
            almost_racing = True
            racing_beep_time = True
        elif event.type == pygame.KEYDOWN and not almost_racing and not racing and not race_over:
            if event.key == pygame.K_SPACE:
                almost_racing = True
                racing_beep_time = True
        elif event.type == pygame.MOUSEBUTTONDOWN and not almost_racing and not racing and race_over:
            running = False
        elif event.type == pygame.KEYDOWN and not almost_racing and not racing and race_over:
            if event.key == pygame.K_SPACE:
                running = False

    # fill the background with green
    screen.fill((  0, 120,   0))

    # detect if race over  
    for i in range(num_players):
    	if t.x[i]+bulldog.get_width() > race_end + race_buffer:
            racing = False
            race_over = True
            winner_num = i
            pygame.mixer.Sound.stop(huffing)
            make_crowd_cheer = True

    # if racing right now, move bulldogs / players
    if racing:
        #p.rate = [np.random.rand(1)*.6+.4 for i in range(num_players)]
        for i in range(num_players):
            p.x[i] += 1*p.rate[i]
            t.x[i] += 1*p.rate[i]
            clock_time = clock.get_time()/1000
            p.y[i] = p_orig.y[i] + np.sin(clock_time)
            t.y[i] = t_orig.y[i] + np.sin(clock_time)

    # draw end zone
    pygame.draw.rect(screen, [255, 255, 255], [race_end, 0, 5, display_height], False)
    pygame.draw.rect(screen, [0, 100, 0], [race_end+5, 0, display_width-(race_end+5), display_height], False)
    screen.blit(bulldogs_textsurface, 
                (race_end + 0.5*(display_width-race_end-bulldogs_textsurface.get_width()), 
                (0.5*(display_height-bulldogs_textsurface.get_height()))))


    # draw bulldogs
    t_bulldog = pygame.transform.flip(bulldog, True, False)
    [screen.blit(t_bulldog, (t.x[i],t.y[i])) for i in range(num_players)]

    # draw green rectangles
    #[pygame.draw.rect(screen, [0, 255, 0], [p.x[i], p.y[i], 50, 50], False) for i in range(num_players)]
  
    # draw heads
    for i in range(num_players):
    	screen.blit(p.img[i], (p.x[i], p.y[i]))

    if race_over:
        screen.blit(join_today_textsurface, 
                    (0.5*(race_end-join_today_textsurface.get_width()), 
                    (display_height*0.98-join_today_textsurface.get_height())))
        winner_img = pygame.transform.scale(p.img_orig[winner_num], (390, 390))
        screen.blit(winner_img, (110,110))
        screen.blit(frame, (100,100))
        screen.blit(crown, (-90,-95))


    #winner_img = pygame.transform.scale(p.img_orig[winner_num], (390, 390))
    #screen.blit(winner_img, (110,110))
    #screen.blit(frame, (100,100))
    #screen.blit(crown, (-90,-95))

    # update the display
    pygame.display.update()
    clock.tick(60)

# Done! Time to quit.
pygame.quit()
