
import random
import math
import pygame
from pygame import mixer

#Menginisialisasi pygame
pygame.init()


#Membuat layar Width dan Height 800x600 pixel
layar = pygame.display.set_mode((800, 600))

#Ubah icon game
icon = pygame.image.load("image/alien.png")
icon = pygame.transform.scale(icon, (32, 32))

pygame.display.set_icon(icon)

#Background Sound
mixer.music.load("sound/bg_sound.wav")
mixer.music.play(-1)

#Memberi latar belakang layar
bg = pygame.image.load("image/bg.jpg")
bg = pygame.transform.scale(bg, (800, 600))

#Memberikan Judul pada pygame saat running
pygame.display.set_caption("Space Ranger")
    

#Player
playerimg = pygame.image.load("image/ship.png")
playerX = 370
playerY = 480
kecepatan = 0.3

#Enemy
enemyimg = []
enemyX = []
enemyY = []
kecepatan_enemy = []
enemyY_maju = []
jumlah_enemies = 6
for i in range(jumlah_enemies):
    enemyimg.append(pygame.image.load("image/enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    kecepatan_enemy.append(0.2)
    enemyY_maju.append(30)

#Peluru
#Ready = Peluru tidak tampil di layar
#Tembak = Peluru baru muncul dan bergerak
peluruimg = pygame.image.load("image/peluru.png")
peluruX = 0
peluruY = 480
status_peluru = "ready"

#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10


#Game Over
score_value = 0
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score = font.render("Score : " + str(score_value), True, (255,255,255))
    layar.blit(score, (x,y))

def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255,255,255))
    layar.blit(game_over_text, (200,250))

def player(x,y):
    layar.blit(playerimg, (x, y))


def enemy(x,y,i):
    layar.blit(enemyimg[i], (x, y))


def tembak_peluru(x,y):
    global status_peluru
    status_peluru = "tembak"
    layar.blit(peluruimg, (x + 16,y + 10))#Munculkan peluru dilayar
kecepatan_peluru = 0.2
peluruY_maju = 1

def isCollision(enemyX, enemyY, peluruX, peluruY):
    jarak = math.sqrt((math.pow(enemyX - peluruX, 2)) + (math.pow(enemyY - peluruY, 2)))#Jarak menggunakan rumus aljabar
    if jarak < 27:
        return True
    else:
        return False

running = True
while running :#Meloopping run yang bernilai True agar tidak keluar ketika dirun
    for event in pygame.event.get():#Memeriksa setiap aktivitas yang terjadi dan menentukan tidakan yang harus diambil oleh aplikasi
        if event.type == pygame.QUIT:#Jika tindakan yang diambil adalah samadengan event QUIT, maka run akan diubah ke false, dan akan menutup aplikasi yang berjalan
            running = False#Menutup aplikasi dengan memberikan nilai run menjadi false
    layar.blit(bg, (0, 0))
    #Membuat Enemy bergerak
    #enemyX -= kecepatan
    for i in range(jumlah_enemies):

            #Game Over
            if enemyY[i] > 400:
                for j in range(jumlah_enemies):
                    enemyY[j] = 2000
            
                game_over()
                break

            enemyX[i] += kecepatan_enemy[i]
            if enemyX[i] <= 0:
                kecepatan_enemy[i] = 0.2
                enemyY[i] += enemyY_maju[i]
                
            elif enemyX[i] >= 736:
                kecepatan_enemy[i] = -0.2
                enemyY[i] += enemyY_maju[i]

             #Collision
            coll = isCollision(enemyX[i], enemyY[i], peluruX, peluruY)
            if coll:
                suara_ledakan = mixer.Sound("sound/ledakan_sound.wav")
                suara_ledakan.play()
                peluruY = 480
                status_peluru = "ready"
                score_value += 1
                print (score_value)
                enemyX[i] = random.randint(0, 800)
                enemyY[i] = random.randint(50, 150)  

            enemy(enemyX[i], enemyY[i] , i)

   #Membuat movement key ditekan left, right, up, down
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
         playerX -= kecepatan
    if key[pygame.K_RIGHT]:
        playerX += kecepatan
    if key[pygame.K_UP]:
        playerY -= kecepatan
    if key[pygame.K_DOWN]:
        playerY += kecepatan
    if status_peluru == "ready":
        if key[pygame.K_SPACE]:
            suara_peluru = mixer.Sound("sound/peluru_sound.wav")
            suara_peluru.play()
            peluruY = playerY
            peluruX = playerX
            tembak_peluru(playerX, peluruY)
    


    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    elif playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

 

    # untuk menampilkan perubahan yang terjadi pada layar. Dalam aplikasi Pygame, setiap perubahan pada layar (seperti menggambar objek baru, memindahkan objek, mengubah warna latar belakang, dll.) 
    
    player(playerX, playerY)
 
    
   #Movement Peluru
    if peluruY <= 0:#Jika peluruY kurang dari / sama dengan 0 (berati jadi negatif keatas, maka peluruY diset jadi 480)
        peluruY = 480
        status_peluru = "ready"# Dan Statusnya belum tampil lagi
        

    if status_peluru is "tembak":
        tembak_peluru(peluruX, peluruY)
        peluruY -= peluruY_maju

   
    show_score(textX, textY)
    # game_over()
    pygame.display.update()#Diletakkan didalam loop, dan digunakan untuk update yang terjadi seperti ubah background dsb

pygame.quit()