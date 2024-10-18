import cv2
import numpy as np
from math import ceil, floor

poligonos = []
vertices = []
b, g, r = 0, 0, 0
ba, ga, ra = (0,255,255)
encontrou = False
nova_cor_selecionada = False
eliminado = False

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        vertices.append((x, y)) #pega x e y

        cv2.circle(image, (x, y), 3, (0, 0, 0), 10) #desenha uma bolinha no vertice
        
        cv2.imshow('Poligonos', image) #atualiza a imagem



def draw_line(p1, p2, image):
    cv2.line(image, p1, p2, (ba, ga, ra), 5)
    

def paleta():
    paleta = np.ones((400, 400, 3), dtype=np.uint8) * 255
    
    for y in range(400):
        for x in range(400):
            b = x * 255 // 400
            g = y * 255 // 400
            r = 255 - b - g
            r = np.clip(r, 0, 255) 

            paleta[y, x] = [b, g, r]
    
    return paleta

def cor_arestas(event, x, y, flags, param):
    global ba, ga, ra
    if event == cv2.EVENT_LBUTTONDOWN:
        paletaimg = param
        ba, ga, ra = paletaimg[y, x]
        ba = int(ba)
        ga = int(ga)
        ra = int(ra)
        cv2.destroyWindow('selecione a cor das arestas:')

def cor(event, x, y, flags, param):
    global b, g, r
    if event == cv2.EVENT_LBUTTONDOWN:
        paletaimg = param
        b, g, r = paletaimg[y, x]
        b = int(b)
        g = int(g)
        r = int(r)
        cv2.destroyWindow('selecione a cor do poligono:')

def nova_cor(event, x, y, flags, param):
    global b, g, r, nova_cor_selecionada, temp_list
    if event == cv2.EVENT_LBUTTONDOWN:
        nova_cor_selecionada = True
        paletaimg = param
        b, g, r = paletaimg[y, x]
        b = int(b)
        g = int(g)
        r = int(r)
        temp_list['color'] = (b, g, r)
    
def click_poligono_recolor(event, x, y, flags, param):
    global vertices, encontrou, temp_list
    if event == cv2.EVENT_LBUTTONDOWN:
        

        
        for k in reversed(range(len(poligonos))):
            poligono = poligonos[k]
            dist = cv2.pointPolygonTest(np.array(poligono['points']), (x, y), False)
                
            if dist >= 0:
                
                encontrou = True
                
                temp_list = poligono
                
                vertices = poligono['points']
                
                poligonos.pop(k)
               
                cv2.imshow('selecione a nova cor do poligono:', paletaimg)
                cv2.setMouseCallback('selecione a nova cor do poligono:', nova_cor, param=paletaimg)
                break

def click_poligono_deletar(event, x, y, flags, param):
    global eliminado
    if event == cv2.EVENT_LBUTTONDOWN:
        for k in reversed(range(len(poligonos))):
            poligono = poligonos[k]
            dist = cv2.pointPolygonTest(np.array(poligono['points']), (x, y), False)
            
            if dist >= 0:
                eliminado = True
                poligonos.pop(k)
                break                    

def fill():

    ymin = vertices[0][1]
    ymax = vertices[0][1]

    #ymin e ymax
    for p in vertices:
        ymin = min(ymin, p[1])
        ymax = max(ymax, p[1])

    dicionario_xy = {}

    #iniciando o dicionario para cada ymin até ymax
    for y in range(ymin, ymax + 1):
        dicionario_xy[y] = []

    #pegando par de vertices (rotação circular)
    for i in range(len(vertices)):
        A = vertices[i]
        B = vertices[(i + 1) % len(vertices)]

        #invertendo para gantantir que o primeiro vertice estéja acima
        if B[1] < A[1]:
            A, B = B, A

        if B[1] == A[1]: #ignorando linhas orizontais
            continue

        #dy e dx do par de vertices
        dy = B[1] - A[1]
        dx = B[0] - A[0]

        #faco dx/dy para nao ter q ter m
        tx = dx / dy

        #iniciando yline e xline com o primeiro vertice
        yline = A[1]
        xline = A[0]
        

        #while até passar por todos os y (do primeiro vertice até o segundo)
        while yline < B[1]:
            dicionario_xy[yline].append(xline) #adicionando os X a cada yline (arrendondando usando round)
            yline += 1 #itenrando os y
            xline += tx #calculando os X
            

    #aqui eu tenho meu dicionario pronto, e vou ordenar os X
    for keyss, itemss in dicionario_xy.items():
        dicionario_xy[keyss] = sorted(itemss)

    #desenhando as linhas
    for y, x_coords in dicionario_xy.items(): #para cada Y (keys do dicionario)
        for i in range(0, len(x_coords) - 1, 2): #Para cada parzinho de X (itens do dicionario)
                    cv2.line(image, (ceil(x_coords[i]), y), (floor(x_coords[i+1]), y), (b, g, r), 1) #desenhando
                

    cv2.imshow('Poligonos', image) #mostrando



image = np.ones((800, 800, 3), dtype=np.uint8) * 255
HELP = np.ones((500, 1200, 3), dtype=np.uint8) * 255
ALERT = np.ones((200, 1000, 3), dtype=np.uint8) * 255
ALERT2 = np.ones((200, 800, 3), dtype=np.uint8) * 255

cv2.putText(HELP, "Selecione a cor inicial e desenhe o poligono livremente.", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(HELP, "Aperte 'q' para indicar que terminou o poligono.", (50, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(HELP, "Aperte 'a' caso deseje desenhar com uma outra cor para a aresta.", (50, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(HELP, "Aperte 'l' caso deseje desenhar com uma outra cor para o poligono.", (50, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(HELP, "Aperte 'p' caso deseje alterar a cor de um poligono existente.", (50, 220), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(HELP, "Aperte 'd' caso deseje excluir um poligono existente.", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(HELP, "Caso deseje ver novamente essa mensagem aperte 'h'.", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

cv2.putText(ALERT, "poligono menor que 2 vertices, continue desenhando...", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),  2, cv2.LINE_AA)
cv2.putText(ALERT2, "Selecione o poligono para recolorir...", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0),  2, cv2.LINE_AA)

cv2.imshow('Poligonos', image)
cv2.setMouseCallback('Poligonos', mouse_callback)

paletaimg = paleta()
cv2.imshow('selecione a cor do poligono:', paletaimg)
cv2.setMouseCallback('selecione a cor do poligono:', cor, param=paletaimg)


cv2.imshow('Como usar', HELP)


while True:
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        
        if len(vertices) >= 3:
            
            poligonos.append({'points': vertices.copy(), 'color': (b, g, r), 'color_aresta': (ba, ga, ra)})
    
            for i in range(len(vertices)):
                
                draw_line(vertices[i], vertices[(i + 1) % len(vertices)], image)
                cv2.imshow('Poligonos', image)    
            fill() 
            vertices = []

            
        else:
            cv2.imshow('ALERT', ALERT)

    if key == ord('l'):
        cv2.imshow('selecione a cor do poligono:', paletaimg)
        cv2.setMouseCallback('selecione a cor do poligono:', cor, param=paletaimg)
    
    if key == ord('a'):
        cv2.imshow('selecione a cor das arestas:', paletaimg)
        cv2.setMouseCallback('selecione a cor das arestas:', cor_arestas, param=paletaimg)
    
    if key == ord('p'):
        cv2.imshow('ALERT2', ALERT2)
        cv2.setMouseCallback('Poligonos', click_poligono_recolor)
        

    if encontrou and nova_cor_selecionada:
        poligonos.append(temp_list)
        fill()
        vertices = []
        encontrou = False
        nova_cor_selecionada = False
        cv2.destroyWindow('selecione a nova cor do poligono:')
        cv2.setMouseCallback('Poligonos', mouse_callback)

    if key == ord('d'):
        cv2.setMouseCallback('Poligonos', click_poligono_deletar)
        

    if eliminado == True:
        image = np.ones((800, 800, 3), dtype=np.uint8) * 255
        cv2.imshow('Poligonos', image)
        
        for poligono in poligonos:
            vertices = poligono['points']
            color = poligono['color']
            color_aresta = poligono['color_aresta']
            
            b, g, r = color
            ba, ga, ra = color_aresta
            
            for i in range(len(vertices)): 
                cv2.circle(image, (vertices[i][0], vertices[i][1]), 3, (0, 0, 0), 10)
            for i in range(len(vertices)):
                draw_line(vertices[i], vertices[(i + 1) % len(vertices)], image)
                
            fill()
            vertices = []
            cv2.setMouseCallback('Poligonos', mouse_callback)
        
        eliminado = False
        cv2.setMouseCallback('Poligonos', mouse_callback)
        
            
    if key == ord('h'):
        cv2.imshow('Como usar', HELP)


    if key == 27:
        break

cv2.imshow('Poligonos', image)     
cv2.destroyAllWindows()