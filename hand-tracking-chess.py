import cv2
from pynput.keyboard import Key, Controller
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from stockfish import Stockfish
import sys
from win32com.client import Dispatch
import time
import random
from criticize import criticizer
import chess
speak = Dispatch("SAPI.SpVoice").Speak

sf=Stockfish('stockfish-windows-2022-x86-64-avx2.exe')
sf.set_elo_rating(5000)
#sf.make_moves_from_current_position(["g4d7", "a8b8", "f1d1"])
# NOTE COMPUTER IS ON LEFT FOR WHITE

keyboard = Controller()
cap = cv2.VideoCapture(0)

whitetime=5*60
blacktime=5*60

topen=0
tclose=0
curr=1

detector = HandDetector(detectionCon= .8, maxHands = 1)
p=0 #calibration points
points1 = np.zeros((4,2))
points2 = np.float32([[0, 0], [700, 0], [700, 700], [0, 700]])
command=["now \"A\" 1", "now H 1", "now H 8", "calibration complete"]
speak("hold \"A\" 8")
loc=[0,0]
transloc=[[[0,0]]]
sticky=5
redx=5
redy=5
closedist=18 # defines closed hand range
store=[[[0,0,0] for i in range(10)] for i in range(10)]
cursorloc=[0,0]
try:
#for i in range(1):
    origboard=cv2.imread("chess_sprites\chessboard.png")
    chessboard=origboard
    while cap.isOpened():

        ret, frame = cap.read()
        height, width, layers = frame.shape

        frame = cv2.resize(frame, ( width//2, height//2))

        hands, image = detector.findHands(frame)

        if hands:
            lmList = hands[0]["lmList"]

#            print(lmList)
           
            coord1 = [lmList[4][0], lmList[4][1]]
            coord2 = [lmList[8][0], lmList[8][1]]
            coord3 = [lmList[12][0], lmList[12][1]]

            length1, info, image  = detector.findDistance( coord1, coord2, image)
            length2, info, image  = detector.findDistance( coord1, coord3, image)
#            hold=(length1<closedist) or (length2<closedist)
            hold=(length1<closedist)
            lim=length1
            loc=[(coord1[i]+coord2[i])/2 for i in range(len(coord1))]
            cursorloc=[(cursorloc[i]+loc[i])/2 for i in range(len(loc))]
#            if length1<length2:
#                lim=length1
#                loc=[(coord1[i]+coord2[i])/2 for i in range(len(coord1))]
#            else:
#                lim=length2
#                loc=[(coord1[i]+coord3[i])/2 for i in range(len(coord1))]
           
            if hold:
                tclose+=1
                if tclose>sticky:
                    topen=0
                    if curr==1:
                        print("picked up")
#                        start=loc
                        start=cursorloc
                        if p>=4:
                            original = np.array([[start]], dtype=np.float32)
                            transloc=cv2.perspectiveTransform(original, resultimage)
                            square1=[int(round(transloc[0][0][0],-2)/100+1),int(round(transloc[0][0][1],-2)/100+1)]
                            startsquare=str(chr(96+square1[1]))+str(9-square1[0])
                            speak("picked up at "+startsquare)
                        else:
                            speak("release")
#                        print(loc)
                    curr=0
                if curr==0:
                    topen=0
            else:
                topen+=1
                if topen>sticky:
                    tclose=0
                    if curr==0:
                        print("put down")
#                        print(loc)
                        if p<4:
#                            points1[p]=loc
                            points1[p]=cursorloc
                            speak(command[p])
                            p+=1
                            print(points1)
                            if p==4:
                                points1=np.float32(points1)
                                resultimage = cv2.getPerspectiveTransform(points1, points2)
                                starttime=time.time()
#                                finalimage = cv2.warpPerspective(frame, resultimage, (500, 500))
#                                cv2.imshow('reproject', finalimage)
                        else:
#                            original = np.array([[loc]], dtype=np.float32)
                            whitetime=whitetime-(time.time()-starttime)
                            if whitetime<0:
                                speak("you lost on time!")
                                print("you lost on time!")
                                break
                            original = np.array([[cursorloc]], dtype=np.float32)
                            transloc=cv2.perspectiveTransform(original, resultimage)
                            square2=[int(round(transloc[0][0][0],-2)/100+1),int(round(transloc[0][0][1],-2)/100+1)]
                            endsquare=str(chr(96+square2[1]))+str(9-square2[0])
                            speak("moved to "+endsquare)
                            if whitetime<60:
                                speak("you have " +str(round(whitetime,2))+" seconds left")
                            move=startsquare+endsquare
                            try:
                                insult = criticizer(sf, move, chess.Board(sf.get_fen_position()))
                                speak(insult)
                            except:
                                print("oops that didn't work... try again?")
                                speak("try again?")
                                curr=1
                                continue
                            print("You moved:" +move)
                            print("You have "+time.strftime('%M:%S', time.gmtime(whitetime)))
                            print("Stockfish has "+time.strftime('%M:%S', time.gmtime(blacktime)))
                            starttime=time.time()
                            sfmove=sf.get_best_move()
                            blacktime=blacktime-(time.time()-starttime)
                            if blacktime<0:
                                speak("stockfish lost on time!")
                                print("stockfish lost on time!")
                                break
                            print("stockfish moves: " +sfmove)
                            speak("stockfish moves: " +sfmove)
                            speak("press space when ready")
                            sf.make_moves_from_current_position([sfmove])
                            print(sf.get_board_visual())
                            print("You have "+time.strftime('%M:%S', time.gmtime(whitetime)))
                            print("Stockfish has "+time.strftime('%M:%S', time.gmtime(blacktime)))
                            while True:
                                k = cv2.waitKey(1)
                                if k==ord(' ') or k==ord('q'):
                                    starttime=time.time()
                                    break
                    curr=1
                if curr==1:
                    tclose=0
            if p>=4:
#                original = np.array([[loc]], dtype=np.float32)
                original = np.array([[cursorloc]], dtype=np.float32)
                cursor=cv2.perspectiveTransform(original, resultimage)
                redx=int((cursor[0][0][0]+50)*612/800)
                redy=int((cursor[0][0][1]+50)*612/800)
                color=[0,255,0] # red color
                if curr==1:
                    color=[0,0,255]
                origboard=cv2.imread("chess_sprites\chessboard.png")
                chessboard=origboard
                chessboard[redx-5:redx+5,redy-5:redy+5]=color
#                chessboard[oredx-5:oredx+5,oredy-5:oredy+5]=[0,0,0]
                cv2.imshow("board", origboard)
                #implement logic to show sprites on top of origboard, can do something with enlargening when hand is over the sprite

        cv2.imshow('Frame', image)
        k = cv2.waitKey(1)
        if k == ord('h'):
            for m in sf.get_top_moves(3):
                speak( 'suggested move is ' + m.get('Move'))
        if k == ord('q'):
            break
        if k==ord('c'):
            speak("hold \"A\" 8")
            p=0
except Exception as e:
    print(e)
    exception_type, exception_object, exception_traceback = sys.exc_info()
    filename = exception_traceback.tb_frame.f_code.co_filename
    line_number = exception_traceback.tb_lineno

    print("Exception type: ", exception_type)
    print("File name: ", filename)
    print("Line number: ", line_number)
cap.release()
cv2.destroyAllWindows()
