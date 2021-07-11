#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import time
from datetime import date
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

delay = 10 # seconds
DESIRED_BET_COEFFICIENT_DIFFERENCE = 30
BET_AMOUNT_BGN = 1
TOTAL_AMOUNT_INVESTED = 0
PERCENTAGE_OF_BALANCE_TO_BET = 1
STARTING_BALANCE = 0

logging.basicConfig(level=logging.INFO)

class MatchBetDescription:
    def __init__(self, match_name, html_element, player_to_bet_on, bet_coefficient = 1):
        self.match_name = match_name
        self.html_element = html_element
        self.player_to_bet_on = player_to_bet_on
        self.bet_coefficient = bet_coefficient

def login(browser):
    browser.get('https://winbet.bg/bg/sport/')
    time.sleep(2)

    try:
        button_login = WebDriverWait(browser, delay).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-login')))
        button_login.click()
    except:
        logging.error("Could not find login button!")
        return 0
    
    try:
        username_input = WebDriverWait(browser, delay).until(EC.element_to_be_clickable((By.NAME, 'loginNameForLogin')))
        username_input.send_keys("USERNAME")
        
        password_input = WebDriverWait(browser, delay).until(EC.element_to_be_clickable((By.NAME, 'passwordForLogin')))
        password_input.send_keys("PASSWORD")
    except TimeoutException:
        logging.error("Could not find username or password input fields!")
        return -1
    
    try:
        button_submit = WebDriverWait(browser, delay).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.dark-green')))
        button_submit.click()
    except TimeoutException:
        logging.error("Could not find submit button!")
        return -1

def enter_live_betting(browser):
    browser.get("https://winbet.bg/bg/livebetting/")
    # enter the iframe and work there as if it were the original site
    try:
        iframe_tag = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
        browser.get(iframe_tag.get_property("src"))
    except TimeoutException:
        logging.error("Could not find iframe!")
        return -1

def get_bet_categories(browser):
    # Add this to filter empty tabs: .asb-nowrap
    bet_categories = []
    try:
        WebDriverWait(browser, delay).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[name=live-sports-scroller] .items-tabs-tab")))
        time.sleep(1)
        bet_categories = WebDriverWait(browser, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[name=live-sports-scroller] .items-tabs-tab")))
    except TimeoutException:
        logging.warning("could not find bet_categories!")
        return []
    
    return bet_categories

def expand_bet_events(browser):
    collapsed_bet_categories = []
    try:
        collapsed_bet_categories = WebDriverWait(browser, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".events-tree-table-node-CH .events-tree-table-node-CH--expansion-panel-title:only-child")))
    except TimeoutException:
        logging.debug("Could not expand bet_categories!")
        return -1
    
    for collapsed_bet_category in collapsed_bet_categories:
        collapsed_bet_category.find_element_by_xpath("..").click()

def submit_bet(browser, matches_to_bet_on):
    global TOTAL_AMOUNT_INVESTED
    global STARTING_BALANCE
    
    input_form = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".betslip-lines-accumulator")))
    text_input = WebDriverWait(input_form, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".asb-pos-wide.text-input-input")))
    text_input.clear()
    
    max_coefficient = max(match_info.bet_coefficient for match_info in matches_to_bet_on)
    current_bet_amount = BET_AMOUNT_BGN * max_coefficient
    
    if current_bet_amount > STARTING_BALANCE - TOTAL_AMOUNT_INVESTED:
        logging.warning("Current left balance is: " + str(STARTING_BALANCE - TOTAL_AMOUNT_INVESTED) + " BGN. We want to invest: " + str(current_bet_amount) + " BGN. But this is not possible!")
        return 0
    
    text_input.send_keys(str(int(current_bet_amount)))

    logging.info("Betting amount: " + str(current_bet_amount) + " BGN with price coeffiecient: " + str(max_coefficient) + " for:\n")
    for match in matches_to_bet_on:
        logging.info("    Match Name: " + match.match_name)
        logging.info("    Player to bet on: " + str(match.player_to_bet_on))
        logging.info("    Bet coefficient: " + str(match.bet_coefficient))

    time.sleep(1)

    # Accept changes in the bet coeffiecient after the bet was marked
    try:
        settings_button = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".betslip-odds-change-action-select")))
        action = webdriver.common.action_chains.ActionChains(browser)
        action.move_to_element_with_offset(settings_button, 5, 5)
        action.click()
        action.perform()    
        time.sleep(1)
        accept_bet_changes_button = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".betslip-odds-change-action-select--items-radio-item:first-child")))
        action = webdriver.common.action_chains.ActionChains(browser)
        action.move_to_element_with_offset(accept_bet_changes_button, 5, 5)
        action.click()
        action.perform()
    except:
        logging.info("Skipping Accept Bet changes step, because it failed...")
        
    # Actually press the BET button
    bet_button = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".betslip-place-btns-bet")))
    action = webdriver.common.action_chains.ActionChains(browser)
    action.move_to_element_with_offset(bet_button, 5, 5)
    action.click()
    action.perform()

    time.sleep(1)

    # Wait for operation to finish
    try:
        new_bet_button = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".betslip-recreate-btns-new-betslip-text")))
        action = webdriver.common.action_chains.ActionChains(browser)
        action.move_to_element_with_offset(new_bet_button, 5, 5)
        action.click()
        action.perform()
        
        TOTAL_AMOUNT_INVESTED = TOTAL_AMOUNT_INVESTED + current_bet_amount
    except TimeoutException:
        logging.warning("Bet failed!!!")
        return -1

def click_on_matches(browser, matches):
    for match in matches:
        price_block_content_count = len(match.html_element)
        element_to_be_clicked = None
        if match.player_to_bet_on == 1:
            element_to_be_clicked = match.html_element[0]
        elif match.player_to_bet_on == 2:
            element_to_be_clicked = match.html_element[price_block_content_count-1]
        # Bet on Draw
        elif match.player_to_bet_on == 0:
            element_to_be_clicked = match.html_element[1]
        else:
            logging.warning("Invalid player! " + match.player_to_bet_on)
            return -1
        
        # Select match winner
        action = webdriver.common.action_chains.ActionChains(browser)
        action.move_to_element_with_offset(element_to_be_clicked, 5, 5)
        action.click()
        action.perform()

def bet_on_matches(browser, matches_to_bet_on):
    global BET_AMOUNT_BGN
    
    try:
        click_on_matches(browser, matches_to_bet_on)
    except:
        logging.warning("Could not select one of the matches:")
        for match in matches_to_bet_on:
            logging.warning(match.match_name)
        logging.warning("Skipping them...")
    
    if submit_bet(browser, matches_to_bet_on) == -1:
        # Unselect matches
        try:
            click_on_matches(browser, matches_to_bet_on)
        except:
            logging.warning("Could not unselect matches!!!")

def bet_on_good_matches(browser, good_matches):
    # TODO: Write a better algorithm to pair the matches to get higher win
    
    # Bet 1 by 1
    for good_match in good_matches:
        if good_match.bet_coefficient > 1:
            matches_to_bet_on = [good_match]
            bet_on_matches(browser, matches_to_bet_on)

    # Bet 2 by 2
    for i in range(len(good_matches)):
        for j in range(i + 1, len(good_matches)):
            if good_matches[i].bet_coefficient == 1 and good_matches[j].bet_coefficient == 1:
                bet_on_matches(browser, [good_matches[i], good_matches[j]])


def calc_bet_coefficient(coef_relation, score_diff, match_time_since_start):
    if match_time_since_start >= 85 and coef_relation > 70:
        return 30 + (10 if score_diff > 1 else 0)
    if match_time_since_start >= 85 and coef_relation > 60:
        return 25 + (10 if score_diff > 1 else 0)
    if match_time_since_start >= 85 and coef_relation > 50:
        return 20 + (10 if score_diff > 1 else 0)
    if match_time_since_start >= 80 and coef_relation > 50:
        return 15 + (10 if score_diff > 1 else 0)
    if match_time_since_start >= 80 and coef_relation > 40:
        return 10 + (10 if score_diff > 1 else 0)
    elif coef_relation > 50:
        return 5
    else:
        return 1

def bet_on_category_inner(browser, bet_on_winner_column):
    expand_bet_events(browser)
    leagues = []
    try:
        leagues = WebDriverWait(browser, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".expansion-panel.events-tree-table-node-CH")))
    except TimeoutException:
        logging.debug("This category doesn't have available bets!")
        return -1
    
    good_matches = []
    
    for league in leagues:
        try:
            league_name = WebDriverWait(league, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".asb-pos-wide.asb-text.events-tree-table-node-CH-name"))).get_attribute("innerHTML")
        except:
            logging.info("Couldn't get league_name for some reason...")
            continue
        logging.debug("Bet Event League: " + league_name)
        
        matches = WebDriverWait(league, delay).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".events-table-row-event-info")))
        
        for match in matches:
            start_time = datetime.now()
            
            match_name = match.get_property("title")
            logging.info("Match name: " + match_name)
            match = match.find_element_by_xpath("../..")
            players = WebDriverWait(match, 1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".events-table-row-competitor-name .asb-text")))
            bet_markets = WebDriverWait(match, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".asb-flex.asb-unshrink.events-table-row-markets")))
            match_time_since_start = WebDriverWait(match, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".events-table-row--start-datetime div"))).get_property("innerHTML")
            try:
                match_time_since_start = int(match_time_since_start[:-1])
            except:
                match_time_since_start = 0
            
            if bet_on_winner_column == 0:
                bet_market_fields = WebDriverWait(bet_markets, 1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".asb-flex.prices-market")))[bet_on_winner_column]
            else:
                bet_market_fields = WebDriverWait(bet_markets, 1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".asb-flex-col")))[bet_on_winner_column]
            
            is_empty = False
            try:
                WebDriverWait(bet_market_fields, 0).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".price-block-empty")))
                is_empty = True
            except TimeoutException:
                is_empty = False
            
            if is_empty == True:
                logging.info("Not betting on this match...")
                continue
            
            checkpoint1_time = datetime.now()
            logging.info("Time it took to get whether match is empty: " + str(checkpoint1_time - start_time))
            try:
                price_block_contents = WebDriverWait(bet_market_fields, 1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".prices-markets--price-block.price-block")))
                price_block_texts = WebDriverWait(bet_market_fields, 1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".price-block-content span")))
            except TimeoutException:
                logging.debug("Skipping this match. It has some advanced settings!")
                continue
            price_block_content_count = len(price_block_contents)
            
            coefficient1 = float(price_block_texts[0].get_property("innerHTML"))
            coefficient2 = float(price_block_texts[price_block_content_count-1].get_property("innerHTML"))
            coefficientX = float(price_block_texts[1].get_property("innerHTML"))
            coef_relation = max(coefficient1, coefficient2) / min(coefficient1, coefficient2)
            
            # decide whether to bet on DRAW
            
            match_scores = WebDriverWait(match, 1).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".events-table-row-competitor-score div")))
            score_player1 = int(match_scores[0].get_property("innerHTML"))
            score_player2 = int(match_scores[1].get_property("innerHTML"))
            score_diff = abs(score_player2 - score_player1)
            is_match_draw_now = score_diff == 0
            
            if match_time_since_start <= 45:
                continue

            bet_coefficient = calc_bet_coefficient(coef_relation, score_diff, match_time_since_start)
            
            if is_match_draw_now and match_time_since_start >= 85:
                logging.info("Betting on DRAW - match_time_since_start: " + str(match_time_since_start))
                
                good_matches.append(MatchBetDescription(match_name, price_block_contents, 0, 1.5 if coef_relation < 1.5 else 1))
            elif is_match_draw_now and match_time_since_start >= 80 and coef_relation < 1.5:
                logging.info("Betting on DRAW - match_time_since_start: " + str(match_time_since_start))
                
                good_matches.append(MatchBetDescription(match_name, price_block_contents, 0, 1))
            elif coefficient1 * DESIRED_BET_COEFFICIENT_DIFFERENCE < coefficient2:
                logging.info("Checking out bet market field (coefficient1, coefficient2): (" + str(coefficient1) + ", " + str(coefficient2) + ")")
                logging.info("Betting on player 1 (" + players[0].get_attribute("innerHTML") +") with coefficient: " + str(coefficient1))
                
                good_matches.append(MatchBetDescription(match_name, price_block_contents, 1, bet_coefficient))
            elif coefficient2 * DESIRED_BET_COEFFICIENT_DIFFERENCE < coefficient1:
                logging.info("Checking out bet market field (coefficient1, coefficient2): (" + str(coefficient1) + ", " + str(coefficient2) + ")")
                logging.info("Betting on player 2 (" + players[1].get_attribute("innerHTML") +") with coefficient: " + str(coefficient2))
                
                good_matches.append(MatchBetDescription(match_name, price_block_contents, 2, bet_coefficient))
            else:
                logging.debug("Not betting...")

            checkpoint2_time = datetime.now()
            logging.info("Time it took to see whether and what to bet: " + str(checkpoint2_time - start_time))
    
    if len(good_matches) > 0:
        bet_on_good_matches(browser, good_matches)

def bet_on_category(browser, category_name):
    global DESIRED_BET_COEFFICIENT_DIFFERENCE
    
    if category_name.lower() == "футбол":
        DESIRED_BET_COEFFICIENT_DIFFERENCE = 20
        bet_on_category_inner(browser, 0)
    # elif category_name.lower() == "тенис":
        # bet_on_category_inner(browser, 0)
    # elif category_name.lower() == "баскетбол":
        # DESIRED_BET_COEFFICIENT_DIFFERENCE = 6
        # bet_on_category_inner(browser, 2)
    # elif category_name.lower() == "тенис на маса":
        # bet_on_category_inner(browser, 0)
    # elif category_name.lower() == "волейбол":
        # bet_on_category_inner(browser, 0)
    else:
        logging.debug("Skipping category... I don't want to play this!")        

def do_live_betting(browser, CURRENT_BALANCE):
    global BET_AMOUNT_BGN
    global PERCENTAGE_OF_BALANCE_TO_BET
    
    bet_categories = get_bet_categories(browser)
    bet_categories_count = len(bet_categories)
    
    BET_AMOUNT_BGN = CURRENT_BALANCE / 100.0 * PERCENTAGE_OF_BALANCE_TO_BET
    
    logging.info("Current Balance is: " + str(CURRENT_BALANCE))
    logging.info("Bet amount per match is: " + str(BET_AMOUNT_BGN))
    
    for i in range(bet_categories_count-1):
        if i == 0:
            # Skip "Любими"
            continue
        categories = get_bet_categories(browser)
        category = categories[i]
        
        category_name = category.get_property("title")
        
        logging.info("\n=============== Category name: " + category_name + " ==================")
        try:
            category.click()
        except:
            logging.debug("Bet category not clickable! Skipping it...")
            continue
        
        bet_on_category(browser, category_name)
        
        logging.info("\n================================================================\n")
    
    # Go to placed bets page
    placed_bets_button = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mybets-selector-button--redirect-button")))
    action = webdriver.common.action_chains.ActionChains(browser)
    action.move_to_element_with_offset(placed_bets_button, 5, 5)
    action.click()
    action.perform()

    logging.info("Total amount invested: " + str(TOTAL_AMOUNT_INVESTED))

def get_current_balance(browser):
    global STARTING_BALANCE
    current_balance = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".user-balance")))
    result = float(current_balance.get_property("innerHTML").split()[0])
    STARTING_BALANCE = result
    return result

def log_info_file(log_line):
    current_date = date.today().strftime("%d-%m-%Y")
    current_date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    with open("C:\\GoogleDrive\\PythonScripts\\" + current_date + '.log', 'a') as f:
        f.write(current_date_time + ": " + log_line + '\n')

if __name__ == "__main__":
    options = Options()
    options.headless = True
    browser = webdriver.Chrome(options=options)
    browser.set_window_position(0, 0)
    
    while True:
        browser.set_window_size(900, 720)
        
        if login(browser) == -1:
            logging.error("Login failed!")
            exit(-1)
        logging.info("Login Success!!")
        
        # for some reason, we DONT want resizing before logging (it just doesn't find the buttons
        # But we want resizing for the betting, because the right context menu in WinBet doesn't 
        browser.set_window_size(1920, 1080)
    
        CURRENT_BALANCE = get_current_balance(browser)
        enter_live_betting(browser)
        do_live_betting(browser, CURRENT_BALANCE)
        
        log_info_file("Balance:" + str(CURRENT_BALANCE) + ",BetAmount=" + str(TOTAL_AMOUNT_INVESTED))
        
        # wait before the next bet
        time.sleep(5)
    
    logging.info("That's all, thanks!")