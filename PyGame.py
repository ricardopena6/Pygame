import pygame as pg
import time
class Personagem(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 50
        self.y = ALTURA/2
        self.vel = 4
        self.largura = 100
        self.altura = 50

        # IMAGENS

        self.personagem1 = pg.image.load('personagem1.png')
        self.personagem2 = pg.image.load('personagem2.png')
        self.personagem1 = pg.transform.scale(self.personagem1, (self.largura, self.altura))
        self.personagem2 = pg.transform.scale(self.personagem2, (self.largura, self.altura))

        self.image = self.personagem1
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        self.movimento()
        self.correcao()
        self.batida()

        
        self.rect.center = (self.x, self.y)
    
    def movimento(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.x -= self.vel
            self.image = self.personagem2

        elif keys[pg.K_RIGHT]:
            self.x += self.vel
            self.image = self.personagem1

        if keys[pg.K_UP]:
            self.y -= self.vel

        elif keys[pg.K_DOWN]:
            self.y += self.vel


    def correcao(self):
        if self.x - self.largura /2<0:
            self.x = self.largura/2

        elif self.x + self.largura / 2  > LARGURA:
            self.x = LARGURA - self.largura / 2


        if self.y - self.altura /2 < 0:
            self.y = self.altura/2

        elif self.y + self.altura / 2 > ALTURA:
            self.y = ALTURA - self.altura / 2


    def batida(self):
        checa_bandeira = pg.sprite.spritecollide(self,grupo_band,False,pg.sprite.collide_mask)
        if checa_bandeira:
            explosao.explode(self.x, self.y)
class carro(pg.sprite.Sprite):
    def __init__(self, numero):
        super().__init__()
        if numero == 1:
            self.x = 190
            self.image =pg.image.load('carro_vermelho.png')
            self.vel = -4
            
            


        else:
            self.x = 460
            self.image = pg.image.load('carro_azul.png')
            self.vel = 5
            
        self.y = ALTURA / 2
        self.largura = 100
        self.altura = 150
        self.image = pg.transform.scale(self.image, (self.largura, self.altura))
        self.rect = self.image.get_rect()
        self.rect.x = 145
        self.rect.y = ALTURA / 2
        self.mask = pg.mask.from_surface(self.image)


    def update(self):
        self.movimento()
        self.rect.center = (self.rect.x, self.rect.y)


    def movimento(self):
        self.rect.y += self.vel

        if self.rect.y - self.altura / 2 < 0 :
            self.rect.y = self.altura / 2
            self.vel *= -1

        elif self.rect.y + self.altura / 2 > ALTURA:
            self.rect.y = ALTURA - self.altura / 2
            self.vel *= -1


class Tela(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img1 = pg.image.load('background.png')
        self.img2 = pg.image.load('venceu.png')
        self.img3 = pg.image.load('perdeu.png')

        self.img1 = pg.transform.scale(self.img1, (LARGURA, ALTURA))
        self.img2 = pg.transform.scale(self.img2, (LARGURA, ALTURA))
        self.img3 = pg.transform.scale(self.img3, (LARGURA, ALTURA))

        self.image = self.img1
        self.x = 0
        self.y = 0

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.topleft = (self.x, self.y)

class Bandeira(pg.sprite.Sprite):
    def __init__(self, numero):
        super().__init__()
        self.numero = numero
        if self.numero == 1:
            self.image = pg.image.load('bandeira_verde.png')
            self.visible = False
            self.x = 50
        else:
            self.image = pg.image.load('bandeira_branca.png')
            self.visible = True
            self.x = 580

        self.y = ALTURA / 2
        self.image = pg.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)


    def update(self):
        if self.visible:
            self.colisao()
            self.rect.center = (self.x, self.y)


    def colisao(self):
        global pontuacao, personagem

        bate_band = pg.sprite.spritecollide(self, grupo_personagem, False,pg.sprite.collide_mask)
        if bate_band:
            self.visible = False

            if self.number == 1:
                band_branca.visible = True
                if pontuacao < 5:
                    muda_nivel()
                else:
                    grupo_personagem.empty()
                    some_resto()

                    TelaFim(1)

            else:
                band_verde.visible = True


                
class explosao(object):
    def __init__(self):
        self.fantasia = 1
        self.largura = 140
        self.altura = 140
        self.image = pg.image.load('explosao'+str(self.fantasia)+'.png')
        self.image = pg.transform.scale(self.image,(self.largura,self.altura))

    def explode(self,x,y):
        x = x - self.largura/2
        y = y - self.altura/2
        some_personagem()

        while self.fantasia < 9:
            self.image = pg.image.load('explosao'+str(self.fantasia)+'.png')
            self.image = pg.transform.scale(self.image,(self.largura,self.altura))
            ganha.blit(self.image,(x,y))
            pg.display.update()

            self.fantasia+=1
            time.sleep(0.1)

        some_resto()
        TelaFim(0)




                

#def DisplayPontos():
#    global jogoS
#    if jogoS:
#        texto_pontos = pontos_fonte.render(str(PONTOS) + ' /5', True, (255, 255, 255))
#        ganha.blit(texto_pontos, (255, 10))

 
def checa_bandeira():
    for bandeira in bandeiras:
        if not bandeira.visible:
            bandeira.kill()

        else:
            if not bandeira.alive():
                grupo_Band.add(bandeira)

def muda_nivel():
    global pontuacao

    if band_vermelha.vel < 0:
        band_vermelha.vel -= 1

    else:
        band_vermelha.vel+=1

    if band_azul.vel < 0:
        band_azul.vel-=1

    else:
        band_azul.vel+=1

    pontuacao += 1 



def some_personagem():
    global personaem

    personagem.kill()
    grupo_tela.draw(ganha)
    grupo_band.draw(ganha)
    grupo_Band.draw(ganha)

    grupo_tela.update()
    grupo_band.update()
    grupo_Band.update()

    pg.display.update()


def some_resto():
    grupo_band.empty()
    grupo_Band.empty()
    bandeiras.clear()



def TelaFim(n):
    global jogoS

    jogoS == False

    if n == 0:
        tf.image = tf.img3
    elif n == 1:
        tf.image = tf.img2




LARGURA = 640
ALTURA = 480

pg.init()
ganha = pg.display.set_mode((LARGURA, ALTURA))
pg.display.set_caption("Atravessando a Rua")
tempo = pg.time.Clock()


PONTOS = 0
pontos_fonte = pg.font.SysFont('comicsans', 80, True)
tf = Tela()
grupo_tela = pg.sprite.Group()
grupo_tela.add(tf)


personagem = Personagem()
grupo_personagem = pg.sprite.Group()
grupo_personagem.add(personagem)



band_vermelha = carro(1)
band_azul = carro(2)
grupo_band = pg.sprite.Group()
grupo_band.add(band_vermelha,band_azul)

band_verde = Bandeira(1)
band_branca = Bandeira(2)
grupo_Band = pg.sprite.Group() 
grupo_Band.add(band_verde, band_branca)
bandeiras = [band_verde, band_branca]

explosao = explosao()

jogoS = True

corrida = True
while corrida:
    tempo.tick(60)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            corrida = False

    grupo_tela.draw(ganha)
#    DisplayPontos()
    checa_bandeira()





    
    grupo_band.draw(ganha)
    grupo_personagem.draw(ganha)
    grupo_Band.draw(ganha)
    
    

    
    grupo_personagem.update()
    grupo_Band.update()
    grupo_tela.update()
    

    pg.display.update()

pg.quit()