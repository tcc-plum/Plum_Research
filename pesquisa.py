import cv2
import datetime
import os

class Pesquisa:
    
    PASTA_FRAMES = 'frames'
    PASTA_CARTAZES = 'cartazes'
    CARTAZ_NOME = 'cartaz'
    CARTAZ_ORDEM = 0
    
    def data(self, tipo='datetime'):
        resultado = ''
        if tipo == 'datetime':
            resultado = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        elif tipo == 'date':
            resultado = datetime.datetime.now().strftime('%Y%m%d')
        return resultado
    
    def showNextPoster(self):
        if os.path.exists(self.PASTA_CARTAZES):
            try:
                cartaz = cv2.imread(self.PASTA_CARTAZES + '/'+ self.CARTAZ_NOME + '_' + str(self.CARTAZ_ORDEM) + '.jpg')
                cartaz_redimensionado = cv2.resize(cartaz, (466,659))
                video_cartaz_nome = 'Plum - Cartaz'
                cv2.namedWindow(video_cartaz_nome) 
                cv2.resizeWindow(video_cartaz_nome, 466, 659)
                cv2.moveWindow(video_cartaz_nome, 40, 30)   
                cv2.imshow(video_cartaz_nome, cartaz_redimensionado)
            except:
                print('[ERRO] Ocorreu um erro ao exibir a imagem: '+ self.PASTA_CARTAZES + '/'+ self.CARTAZ_NOME + '_' + str(self.CARTAZ_ORDEM))
        else:
            print('[ERRO] A pasta com as fotos não existe')

    def faceStreaming(self):
        modelo = cv2.CascadeClassifier('models/frontal/haarcascade_frontalface_default.xml')
        
        video_captura = cv2.VideoCapture(0)
        
        while True:
            ret, frame = video_captura.read()
            cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = modelo.detectMultiScale(cinza, flags=cv2.CASCADE_SCALE_IMAGE)
            
            for face in faces:
                x_axis, y_axis, width, height = [vertice for vertice in face]
                
                cv2.rectangle(frame, (x_axis, y_axis), (x_axis+width, y_axis+height), (255,0,222), 2)
                
                sub_face = frame[y_axis: y_axis+height, x_axis:x_axis+width]
                
                if not os.path.exists(self.PASTA_FRAMES):
                    os.makedirs(self.PASTA_FRAMES)
                
                foto_nome = 'face_' + self.data('datetime') + '_' + self.CARTAZ_NOME + '_' + str(self.CARTAZ_ORDEM) + '_.jpg'
                foto_arquivo = self.PASTA_FRAMES + '/' + foto_nome
                
                if self.CARTAZ_ORDEM > 0:
                    cv2.imwrite(foto_arquivo, sub_face)
            
            video_captura_nome = 'Plum - Video Streaming'
            cv2.namedWindow(video_captura_nome)
            cv2.moveWindow(video_captura_nome, 520, 30)         
            cv2.imshow(video_captura_nome, frame)

            tecla_seta_esquerda = 2424832
            tecla_seta_direita = 2555904
            tecla_esc = 27
            
            tecla = cv2.waitKeyEx(30)
            if tecla == tecla_seta_direita and self.CARTAZ_ORDEM <= len(os.listdir(self.PASTA_CARTAZES)):
                self.CARTAZ_ORDEM = self.CARTAZ_ORDEM + 1
                self.showNextPoster()
            elif tecla == tecla_seta_esquerda and self.CARTAZ_ORDEM > 1:
                self.CARTAZ_ORDEM = self.CARTAZ_ORDEM - 1
                self.showNextPoster()
            elif tecla == tecla_esc:
                break

        video_captura.release()
        cv2.destroyAllWindows()