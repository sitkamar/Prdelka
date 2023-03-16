from random import randint, shuffle
from kivy.app import App

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

def getQuestions():
    with open('Vzorove_otazky.txt', 'r', encoding='utf-8') as questionsAll:
        line = questionsAll.readline()
        OpenQuestions = []
        ClosedQuestions = []
        while line:
            if line[0] == '^':
                ClosedQuestions[-1].append(line[1:])
                line = questionsAll.readline()
            else:
                if '. ' in line:
                    question = '. '.join(line.split('. ')[1:])
                    line = questionsAll.readline()
                    answers = []
                    while line and line[1] == ')':
                        answers.append(') '.join(line.split(') ')[1:]))
                        line = questionsAll.readline()
                    if len(answers) == 0:
                        OpenQuestions.append(question)
                    else:
                        ClosedQuestions.append([question, answers])
                else:
                    line = questionsAll.readline()
    for i in OpenQuestions:
        i = i.replace('\n', '')
    for i in ClosedQuestions:
        i[0]=i[0].replace('\n', '')
        for j in range(len(i[1])):
            i[1][j] = i[1][j].replace('\n', '')
    return OpenQuestions, ClosedQuestions
def getTest(OpenQuestions,ClosedQuestions):
    length = len(OpenQuestions)+len(ClosedQuestions)
    indexes = []
    for _ in range(37):
        x = randint(0, length-1)
        while x in indexes:
            x = randint(0, length-1)
        indexes.append(x) 
    print(indexes)
    with open('Test.txt', 'w', encoding='utf-8') as test:
        for x,i in enumerate(indexes):
            if i < len(OpenQuestions):
                test.write(str(x+1)+'. '+OpenQuestions[i])
            else:
                test.write(str(x+1)+'. '+ClosedQuestions[i-len(OpenQuestions)-1][0])
                answers = ClosedQuestions[i-len(OpenQuestions)-1][1][:]
                while len(answers) > 0:
                    index = randint(0, len(answers)-1)
                    answer = answers[index]
                    test.write('\t'+'abcd'[4-len(answers)]+') '+answer)
                    answers = answers[:index] + answers[index+1:]
    return indexes
class MyApp(App):
    OpenQuestions, ClosedQuestions = getQuestions()
    onOpenQuestion = False
    points = 0
    answer = ''
    correctness = ''
    wasRight = False
    question_label = Label(text='', font_size=30)
    points_label = Label(text='0', font_size=20)
    count = 0
    correct = Label(text='Correct', font_size=20)
    def generate_question(self):
        index = randint(0, len(self.OpenQuestions)+len(self.ClosedQuestions)-1)
        if index < len(self.OpenQuestions):
            question = self.OpenQuestions[index]
            self.OnOpenQuestion = True
            answers = []
        else:
            question = self.ClosedQuestions[index-len(self.OpenQuestions)-1][0]
            answers = self.ClosedQuestions[index-len(self.OpenQuestions)-1][1][:]
            print(self.ClosedQuestions[index-len(self.OpenQuestions)-1])
            self.correctness = answers['abcd'.index(self.ClosedQuestions[index-len(self.OpenQuestions)-1][2][0])]
            shuffle(answers)
        self.question_label.text = question
        return answers
    def myAnswer(self, instance):
        if not self.OnOpenQuestion:
            self.count += 1
            if instance.text == self.correctness:
                self.points += 1
                self.correct.text = 'Correct'
            else:
                self.correct.text = 'Wrong - ' + self.correctness
            self.points_label.text = str(self.points)+'/'+str(self.count)
            self.next_question()
    labelA = Button(text='A', font_size=30)
    labelB = Button(text='B', font_size=30)
    labelC = Button(text='C', font_size=30)
    labelD = Button(text='D', font_size=30)
    buttons = [labelD, labelC, labelB, labelA]
    def build(self):
        background = GridLayout(cols=1, padding=10, spacing=10)
        top = GridLayout(cols=3, row_force_default=True, row_default_height=40,padding=10, spacing=10)
        top.add_widget(self.points_label)
        top.add_widget(self.correct)
        next = Button(text='Submit', font_size=10,on_press=self.next)
        top.add_widget(next)
        background.add_widget(top)
        background.add_widget(self.question_label)
        for i in self.buttons:
            i.bind(on_press=self.myAnswer)
            background.add_widget(i)
        answers = self.generate_question()
        if len(answers) > 0:
            for i in range(len(answers)):
                self.buttons[i].text = answers[i]
            self.OnOpenQuestion = False
        else:
            self.OnOpenQuestion = True
        return background
    def next(self, instance):
        if self.OnOpenQuestion:
            self.count += 1
            if self.answer == self.correctness:
                self.points += 1
            self.points_label.text = str(self.points)+'/'+str(self.count)
        self.next_question()
    def next_question(self):
        answers = self.generate_question()
        if len(answers) > 0:
            for i in range(len(answers)):
                self.buttons[i].text = answers[i]
            self.OnOpenQuestion = False
        else:
            self.OnOpenQuestion = True
        self.wasRight = False
        self.answer = ''
    
MyApp().run()