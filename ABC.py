import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
from pynput.keyboard import Controller
from tkinter import *


class Buttonn():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


def transparent_layout(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[0]), 20, rt=0)

        cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]), (255, 144, 30), cv2.FILLED)
        # cv2.rectangle(img, start_pos, end_pos, color, animation)

        cv2.putText(imgNew, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)
        # cv2.putText(img, text, position, font, fontScale, color, thickness)

    out = img.copy()
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, 0.5, imgNew, 1-0.5, 0)[mask]
    return out


def main_program():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    detector = HandDetector(detectionCon=1)

    keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "Dl"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
            ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
            ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]]

    final_text = ""

    keyboard = Controller()

    buttonList = []
    for k in range(len(keys)):
        for x, key in enumerate(keys[k]):
            buttonList.append(Buttonn([100 * x + 25, 100 * k + 50], key))

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList, bboxInfo = detector.findPosition(img)
        img = transparent_layout(img, buttonList)

        if lmList:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 255), cv2.FILLED)

                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)

                    l, _, _ = detector.findDistance(8, 12, img, draw=False)
                    print(l)

                    if l < 25:
                        keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)

                        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)

                        final_text += button.text
                        sleep(0.3)

        cv2.rectangle(img, (25, 750), (1250, 650), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, final_text, (30, 710), cv2.FONT_HERSHEY_PLAIN, 4, (0, 0, 0), 4)

        cv2.imshow("Main Interface", img)
        w = cv2.waitKey(1)
        if w == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


scr = Tk()
scr.geometry("1920x1031")
bg = PhotoImage(file=r'06.png')
label1 = Label(scr, image=bg)
label1.place(x=0, y=0)
scr.title("Final Project")
bt_Run = Button(scr, text="Run Program", font = ("Arial", 14, "bold"), bg="cyan", fg="blue", command=main_program)
bt_Run.place(x=1350, y=600)
scr.mainloop()



