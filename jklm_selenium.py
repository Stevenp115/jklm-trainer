# -*- coding: utf-8 -*-

# Selenium Import
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Constant Definitions
DICT_FILENAME = "dict.txt"
DRIVER_PATH = [[ENTER DRIVER PATH HERE]]
INITIAL_LIVES = 2
MAX_LIVES = 10
ALPHABET_INFO = True  # Display current alphebet?

# Bot class


class JKLM_Bot:
    def __init__(self, name, priority, code):
        self.name = name
        self.priority = priority
        self.code = code

    def connect(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")  # Optional.
        self.driver = webdriver.Chrome(DRIVER_PATH)
        self.driver.get(f'https://jklm.fun/{self.code}')
        time.sleep(1)

        # Input name
        name_box = self.driver.find_element_by_css_selector(
            "body > div.pages > div.setNickname.page > form > div.line > input")
        name_box.send_keys(self.name)

        # OK BUTTON
        l = self.driver.find_element(By.XPATH, '//button[text()="OK"]')
        self.driver.execute_script("arguments[0].click();", l)

    def join(self, reframe=True):
        time.sleep(5)
        if reframe:
            self.driver.switch_to.frame(0)
        # JOIN BUTTON
        l = self.driver.find_element(By.XPATH, '//button[text()="Join game"]')
        self.driver.execute_script("arguments[0].click();", l)

    def play(self):
        # Play the bot.
        alpha = set("abcdefghijklmnopqrstuvwy".upper())

        hadTurn = 0  # Keeps track if it was your turn in the previous loop.
        lives = INITIAL_LIVES

        while True:
            current_player = self.driver.find_element_by_class_name(
                "player").get_attribute('innerHTML')
            hadTurn = 0
            # Run syllable checks and play a word if it is your turn.
            if current_player == self.name:
                if hadTurn:
                    print("ALERT! Word must have failed!")
                    time.sleep(0.1)
                    continue
                time.sleep(0.30)
                answer_box = self.driver.find_element_by_css_selector(
                    "body > div.main.page > div.bottom > div.round > div.selfTurn > form > input")
                prompt = self.driver.find_element_by_css_selector(
                    "body > div.main.page > div.middle > div.canvasArea > div.round > div").text
                time.sleep(0.10)
                # Finds matching word
                word = word_finder(prompt, self.priority, alpha)
                basic_type(word, 0.03, answer_box)  # Type the word.
                intersect = alpha.intersection(set(word.upper()))
                # Remove letters from alphabet.
                alpha = alpha.difference(intersect)

                if ALPHABET_INFO:  # This will print the letters to remove and alphabet.
                    print(f"Alphabet: {alpha}")
                    print(f"Intersect: {intersect}")
                    print(sorted(list(alpha)))

                if not alpha:  # If alphabet has been used up, reset alphabet.
                    alpha = set("abcdefghijklmnopqrstuvwxyz".upper())
                    print("New life!")
                    if lives < MAX_LIVES:
                        lives += 1

                print(f"Lives: {lives}")
                time.sleep(1.5)
                hadTurn = 1

## The main function for playing.

## Connect several bots at once.


def connect_bots(arr_of_bots):
    for bot in arr_of_bots:
        bot.connect()

## Join several bots at once.


def join_bots(arr_of_bots):
    for bot in arr_of_bots:
        bot.join()

## Play several bots at once. More complicated.


def play_bots(arr_of_bots):
    for bot in arr_of_bots:
        bot.alpha = set("ABCDEFGHIJKLMNOPQRSTUVWY")
        bot.hadTurn = 0


###############################################################################
######################### ALL THE WORD DECISION LOGIC #########################
###############################################################################


# Get dictionary data
wordDict = []
with open("dict.txt", 'r') as fp:
    wordDict = fp.readlines()
wordDict = [word.strip() for word in wordDict]


def basic_type(string, delay, obj):
    """ Types a string to an object with a delay of "delay" seconds. """
    for ch in string:
        obj.send_keys(ch)
        time.sleep(delay)
    obj.send_keys(Keys.ENTER)


def word_finder(string, priority=0, args="", pop=True):
    """ Takes in a substring, 'string', then according to a sorting priority and
        letters to optimise for, 'args', returns a word in the dictionary containing
        that substring. 

        Priority descriptions =
            0: "First in ALPHABET",
            1: "Longest Word",
            2: "Shortest Word",
            3: "ALPHABET Optimised"
    """
    print("Finding a word...")
    candidates = [word for word in wordDict if string in word]

    if not candidates:
        return "No word was found..."
    elif len(candidates) == 1:
        return candidates[0]

    if priority == 0:  # Gets a 'random' word that an average human would choose.
        sort = sorted(candidates, key=len)
        word = random.choice(sort[:len(sort) // 2])
    elif priority == 1:  # Gets largest word.
        word = sorted(candidates, key=len)[-1]
    elif priority == 2:  # Gets shortest word.
        word = sorted(candidates, key=len)[0]
    elif priority == 3:  # Gets word which uses the most amount of letters possible.
        def my_key(x): return len([s for s in set(x) if s in args])
        word = sorted(candidates, key=my_key)[-1]

    if pop:
        wordDict.pop(wordDict.index(word))

    print(word)
    return word

###############################################################################
############################# WEB BOT OPERATIONS ##############################
###############################################################################


name = input("Enter the bot name: ")
code = input("Enter the lobby code: ")
priority = int(input(
    "Enter the priority (0 = Alphabetical Order, 1 = Longest Word, 2 = Shortest Word, 3 = Alphabet Optimised): "))
bot = JKLM_Bot(name, priority, code)
bot.connect()
bot.join()
bot.play()
