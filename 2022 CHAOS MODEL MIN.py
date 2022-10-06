import selenium.webdriver as webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException, UnexpectedAlertPresentException, WebDriverException, NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
import math
import random as rdm
import statistics as stats
import scipy.stats
import numpy as np
import time


CONFINTVLS = [0.99, 0.98, 0.97, 0.96, 0.95, 0.93, 0.9, 0.85, 0.8, 0.75]
NMP = 15
FORM_VALUE = 0.6
POS_DIFF = 5
BAY_DIFF = 0.5
POS_MARK = 4
YEAR = 22
DSCRM_H_A = 9
DSCRM_BT = 4


start_time = time.time()
FLASH_SCORE = "https://www.flashscore.com/football/"

chrome_path = "C:\Development\chromedriver_win33\chromedriver.exe"
service = Service(chrome_path)
options = webdriver.ChromeOptions()
options.add_extension("AdblockPlus.crx")
options.add_argument("start-maximized")


driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(2)
driver.get(FLASH_SCORE)
sleep(5)

window_before = driver.window_handles[0]

accept_cookies = driver.find_element(By.ID, "onetrust-accept-btn-handler")
accept_cookies.click()
sleep(1.5)

driver.find_element(By.CSS_SELECTOR, '[title="Next day"]').click()
sleep(2)
driver.find_element(By.CSS_SELECTOR, ".filters__group .filters__tab:last-child").click()
sleep(2)


def team_data():
    try:
        country = driver.find_element(By.CSS_SELECTOR, '.tournamentHeaderDescription .tournamentHeader__country').text.split(':')[0]
        league = driver.find_element(By.CSS_SELECTOR, '.tournamentHeaderDescription .tournamentHeader__country').text.split(':')[1].split(' - ')[0]
        home_team = driver.find_element(By.CSS_SELECTOR, '.duelParticipant__home  .participant__participantName a').text
        away_team = driver.find_element(By.CSS_SELECTOR, '.duelParticipant__away  .participant__participantName a').text
    except NoSuchElementException:
        driver.refresh()
        sleep(0.1)
        country = driver.find_element(By.CSS_SELECTOR, '.tournamentHeaderDescription .tournamentHeader__country').text.split(':')[0]
        league = driver.find_element(By.CSS_SELECTOR, '.tournamentHeaderDescription .tournamentHeader__country').text.split(':')[1].split(' - ')[0]
        home_team = driver.find_element(By.CSS_SELECTOR, '.duelParticipant__home  .participant__participantName a').text
        away_team = driver.find_element(By.CSS_SELECTOR, '.duelParticipant__away  .participant__participantName a').text
    leagues.append(league)
    countries.append(country)
    away_teams.append(away_team)
    home_teams.append(home_team)


def pts_pos_mp():
    if selected_teams_names[0].text == home_teamx:
        try:
            home_t_position = driver.find_elements(By.CSS_SELECTOR, ".table__row--selected .tableCellRank")[0].text.split('.')[0].strip()
            home_t_mp = driver.find_elements(By.CSS_SELECTOR, '[class="ui-table__row table__row--selected "] [class=" table__cell table__cell--value   "]')[0].text.strip()
            home_t_point = driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--points ')[0].text.strip()
            home_positions.append(int(home_t_position))
            home_points.append(int(home_t_point))
            home_nums_matches_played.append(int(home_t_mp))
        except IndexError:
            home_positions.append(0)
            home_nums_matches_played.append(0)
            home_points.append(0)
    else:
        try:
            away_t_position = driver.find_elements(By.CSS_SELECTOR, ".table__row--selected .tableCellRank")[0].text.split('.')[0].strip()
            away_t_mp = driver.find_elements(By.CSS_SELECTOR, '[class="ui-table__row table__row--selected "] [class=" table__cell table__cell--value   "]')[0].text.strip()
            away_t_point = driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--points ')[0].text.strip()
            away_positions.append(int(away_t_position))
            away_points.append(int(away_t_point))
            away_nums_matches_played.append(int(away_t_mp))
        except IndexError:
            pass
            away_positions.append(0)
            away_nums_matches_played.append(0)
            away_points.append(0)

    if selected_teams_names[1].text == away_teamx:
        try:
            away_t_position = driver.find_elements(By.CSS_SELECTOR, ".table__row--selected .tableCellRank")[1].text.split('.')[0].strip()
            away_t_mp = driver.find_elements(By.CSS_SELECTOR, '[class="ui-table__row table__row--selected "] [class=" table__cell table__cell--value   "]')[4].text.strip()
            away_t_point = driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--points ')[1].text.strip()
            away_positions.append(int(away_t_position))
            away_points.append(int(away_t_point))
            away_nums_matches_played.append(int(away_t_mp))
        except IndexError:
            pass
            away_positions.append(0)
            away_nums_matches_played.append(0)
            away_points.append(0)

    else:
        try:
            home_t_position = driver.find_elements(By.CSS_SELECTOR, ".table__row--selected .tableCellRank")[1].text.split('.')[0].strip()
            home_t_mp = driver.find_elements(By.CSS_SELECTOR, '[class="ui-table__row table__row--selected "] [class=" table__cell table__cell--value   "]')[4].text.strip()
            home_t_point = driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--points ')[1].text.strip()
            home_positions.append(int(home_t_position))
            home_points.append(int(home_t_point))
            home_nums_matches_played.append(int(home_t_mp))
        except IndexError:
            pass
            home_positions.append(0)
            home_nums_matches_played.append(0)
            home_points.append(0)


def teams_form_checker():
    global H_form_L
    global H_form_W
    global H_form_D
    global A_form_D
    global A_form_W
    global A_form_L
    form_length = len(driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--form .wld'))
    if form_length == 12:
        if selected_teams_names[0].text == home_teamx:
            for j in range(1, (int(form_length / 2)), 1):
                if driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--form .wld')[j].text == "D":
                    H_form_D += 1
                elif driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--form .wld')[j].text == "L":
                    H_form_L += 1
                elif driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--form .wld')[j].text == "W":
                    H_form_W += 1
        else:
            for j in range(1, (int(form_length / 2)), 1):
                if driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--form .wld')[j].text == "D":
                    A_form_D += 1
                elif driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--form .wld')[j].text == "L":
                    A_form_L += 1
                elif driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--form .wld')[j].text == "W":
                    A_form_W += 1
        if selected_teams_names[1].text == away_teamx:
            for m in range((int(form_length / 2) + 1), form_length, 1):
                if driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--form .wld')[m].text == "D":
                    A_form_D += 1
                elif driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--form .wld')[m].text == "L":
                    A_form_L += 1
                elif driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--form .wld')[m].text == "W":
                    A_form_W += 1
        else:
            for m in range((int(form_length / 2) + 1), form_length, 1):
                if driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--form .wld')[m].text == "D":
                    H_form_D += 1
                elif driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--form .wld')[m].text == "L":
                    H_form_L += 1
                elif driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--form .wld')[m].text == "W":
                    H_form_W += 1
        h_form_W.append(round((H_form_W / 5), 4))
        h_form_D.append(round((H_form_D / 5), 4))
        h_form_L.append(round((H_form_L / 5), 4))
        a_form_W.append(round((A_form_W / 5), 4))
        a_form_D.append(round((A_form_D / 5), 4))
        a_form_L.append(round((A_form_L / 5), 4))


def z_scorer(htpts, atpts):
    teams_pts = driver.find_elements(By.CSS_SELECTOR, '.ui-table__row  .table__cell--points ')
    team_pts = []
    for t in range(len(teams_pts)):
        pts = int(teams_pts[t].text.strip())
        team_pts.append(pts)

    mean_ = stats.mean(team_pts)
    stdv = stats.pstdev(team_pts)
    if mean_ > 0 and stdv > 0:
        home_zsc = scipy.stats.norm.cdf(htpts, loc=mean_, scale=stdv)
        away_zsc = scipy.stats.norm.cdf(atpts, loc=mean_, scale=stdv)
        diff_zsc = abs(home_zsc - away_zsc)
        home_z_prob.append(home_zsc)
        away_z_prob.append(away_zsc)
        diff_z_prob.append(diff_zsc)
    else:
        home_z_prob.append(0.01)
        away_z_prob.append(0.01)
        diff_z_prob.append(0.01)


def append_zeroes():
    away_positions.append(0)
    away_nums_matches_played.append(0)
    away_points.append(0)
    home_positions.append(0)
    home_nums_matches_played.append(0)
    home_points.append(0)
    home_z_prob.append(0.01)
    away_z_prob.append(0.01)
    diff_z_prob.append(0.01)


def h2h_aggregator(m):
    global valid_games
    global count_HW
    global count_AW
    global count_GG
    global count_1_5
    global count_2_5

    global count_12
    valid_games += 1
    sleep(0.5)
    if (int(home_score[m].text) > int(away_score[m].text)) and (home_x[m].text == home_teamx):
        count_HW += 1
    if (int(home_score[m].text) > int(away_score[m].text)) and (home_x[m].text == away_teamx):
        count_AW += 1
    if (int(away_score[m].text) > int(home_score[m].text)) and (away_x[m].text == away_teamx):
        count_AW += 1
    if (int(away_score[m].text) > int(home_score[m].text)) and (away_x[m].text == home_teamx):
        count_HW += 1
    if int(home_score[m].text) == int(away_score[m].text) and (int(home_score[m].text) > 0 and int(away_score[m].text) > 0):
        count_HW += 0.5
        count_AW += 0.5
    if int(home_score[m].text) == int(away_score[m].text) and (int(home_score[m].text) == 0 and int(away_score[m].text) == 0):
        count_HW += 0
        count_AW += 0
    if (int(home_score[m].text) > 0 and int(away_score[m].text) > 0) and (int(home_score[m].text) > 1 or int(away_score[m].text) > 1):
        count_GG += 1
    if (int(home_score[m].text) + int(away_score[m].text)) >= 2:
        count_1_5 += 1
    if (int(home_score[m].text) + int(away_score[m].text)) >= 3:
        count_2_5 += 1
    if int(home_score[m].text) != int(away_score[m].text):
        count_12 += 1


def h2h_prob_calc():
    global valid_games
    global count_HW
    global count_AW
    global count_GG
    global count_1_5
    global count_2_5
    global count_12
    prob_GG1 = float(count_GG / valid_games)
    prob_1_5i = float(count_1_5 / valid_games)
    prob_2_5i = float(count_2_5 / valid_games)
    prob_12i = float(count_12 / valid_games)
    prob_HW = float(count_HW / valid_games)
    prob_AW = float(count_AW / valid_games)

    if prob_HW == 1.0:
        prob_HW -= 0.01
    if prob_AW == 1.0:
        prob_AW -= 0.01
    if prob_GG1 == 1.0:
        prob_GG1 -= 0.01
    if prob_1_5i == 1.0:
        prob_1_5i -= 0.01
    if prob_2_5i == 1.0:
        prob_2_5i -= 0.01
    if prob_12i == 1.0:
        prob_12i -= 0.01

    if prob_GG1 == 0.0:
        prob_GG1 += 0.01
    if prob_1_5i == 0.0:
        prob_1_5i += 0.01
    if prob_2_5i == 0.0:
        prob_2_5i += 0.01
    if prob_12i == 0.0:
        prob_12i += 0.01
    if prob_HW == 0.0:
        prob_HW += 0.01
    if prob_AW == 0.0:
        prob_AW += 0.01
    return [prob_HW, prob_AW, prob_GG1, prob_1_5i, prob_2_5i, prob_12i]


def h2h_appender(prb_HW, prb_AW, prb_GG, prb_1_5, prb_2_5, prb_12):
    prob_HWs.append(prb_HW)
    prob_AWs.append(prb_AW)
    prob_GGs.append(prb_GG)
    prob_1_5s.append(prb_1_5)
    prob_2_5s.append(prb_2_5)
    prob_12s.append(prb_12)


def ht_indp_aggregator(k):
    global valid_games_H_indp
    global count_HW_H_indp
    global count_GG_H_indp
    global count_1_5_H_indp
    global count_2_5_H_indp
    global count_12_H_indp

    valid_games_H_indp += 1
    if (int(home_score[k].text) > int(away_score[k].text)) and (home_x[k].text == home_teamx):
        count_HW_H_indp += 1
    if (int(away_score[k].text) > int(home_score[k].text)) and (away_x[k].text == home_teamx):
        count_HW_H_indp += 1
    if int(home_score[k].text) == int(away_score[k].text) and (int(home_score[k].text) > 0 and int(away_score[k].text) > 0):
        count_HW_H_indp += 0.5
    if int(home_score[k].text) == int(away_score[k].text) and (int(home_score[k].text) == 0 and int(away_score[k].text) == 0):
        count_HW_H_indp += 0
    if (int(home_score[k].text) > 0 and int(away_score[k].text) > 0) and int(home_score[k].text) > 1 and (home_x[k].text == home_teamx):
        count_GG_H_indp += 1
    if (int(home_score[k].text) > 0 and int(away_score[k].text) > 0) and int(away_score[k].text) > 1 and (away_x[k].text == home_teamx):
        count_GG_H_indp += 1
    if (int(home_score[k].text) + int(away_score[k].text)) >= 2 and (home_x[k].text == home_teamx) and int(home_score[k].text) >= 1:
        count_1_5_H_indp += 1
    if (int(home_score[k].text) + int(away_score[k].text)) >= 2 and (away_x[k].text == home_teamx) and int(away_score[k].text) >= 1:
        count_1_5_H_indp += 1
    if (int(home_score[k].text) + int(away_score[k].text)) >= 3 and (home_x[k].text == home_teamx) and int(home_score[k].text) >= 2:
        count_2_5_H_indp += 1
    if (int(home_score[k].text) + int(away_score[k].text)) >= 3 and (away_x[k].text == home_teamx) and int(away_score[k].text) >= 2:
        count_2_5_H_indp += 1
    if int(home_score[k].text) != int(away_score[k].text) and int(home_score[k].text) >= 1 and (home_x[k].text == home_teamx):
        count_12_H_indp += 1
    if int(away_score[k].text) != int(home_score[k].text) and int(away_score[k].text) >= 1 and (away_x[k].text == home_teamx):
        count_12_H_indp += 1


def ht_indp_prob_calc():
    global valid_games_H_indp
    global count_HW_H_indp
    global count_GG_H_indp
    global count_1_5_H_indp
    global count_2_5_H_indp
    global count_12_H_indp

    prob_HW_H_indp = float(count_HW_H_indp / valid_games_H_indp)
    prob_AW_H_indp = 1 - prob_HW_H_indp
    prob_GG_H_indp = float(count_GG_H_indp / valid_games_H_indp)
    prob_1_5_H_indp = float(count_1_5_H_indp / valid_games_H_indp)
    prob_2_5_H_indp = float(count_2_5_H_indp / valid_games_H_indp)
    prob_12_H_indp = float(count_12_H_indp / valid_games_H_indp)

    if prob_HW_H_indp == 1.0:
        prob_HW_H_indp -= 0.01
    if prob_AW_H_indp == 1.0:
        prob_AW_H_indp -= 0.01
    if prob_GG_H_indp == 1.0:
        prob_GG_H_indp -= 0.01
    if prob_1_5_H_indp == 1.0:
        prob_1_5_H_indp -= 0.01
    if prob_2_5_H_indp == 1.0:
        prob_2_5_H_indp -= 0.01
    if prob_12_H_indp == 1.0:
        prob_12_H_indp -= 0.01

    if prob_GG_H_indp == 0.0:
        prob_GG_H_indp += 0.01
    if prob_1_5_H_indp == 0.0:
        prob_1_5_H_indp += 0.01
    if prob_2_5_H_indp == 0.0:
        prob_2_5_H_indp += 0.01
    if prob_12_H_indp == 0.0:
        prob_12_H_indp += 0.01
    if prob_HW_H_indp == 0.0:
        prob_HW_H_indp += 0.01
    if prob_AW_H_indp == 0.0:
        prob_AW_H_indp += 0.01
    return [prob_HW_H_indp, prob_AW_H_indp, prob_GG_H_indp, prob_1_5_H_indp, prob_2_5_H_indp, prob_12_H_indp]


def ht_indp_appender(prb_HW_H_indp, prb_AW_H_indp, prb_GG_H_indp, prb_1_5_H_indp, prb_2_5_H_indp, prb_12_H_indp):
    prob_HW_H_indps.append(prb_HW_H_indp)
    prob_AW_H_indps.append(prb_AW_H_indp)
    prob_GG_H_indps.append(prb_GG_H_indp)
    prob_1_5_H_indps.append(prb_1_5_H_indp)
    prob_2_5_H_indps.append(prb_2_5_H_indp)
    prob_12_H_indps.append(prb_12_H_indp)


def at_indp_aggregator(n):
    global valid_games_A_indp
    global count_AW_A_indp
    global count_GG_A_indp
    global count_1_5_A_indp
    global count_2_5_A_indp
    global count_12_A_indp

    valid_games_A_indp += 1
    if (int(home_score[n].text) > int(away_score[n].text)) and (home_x[n].text == away_teamx):
        count_AW_A_indp += 1
    if (int(away_score[n].text) > int(home_score[n].text)) and (away_x[n].text == away_teamx):
        count_AW_A_indp += 1
    if int(home_score[n].text) == int(away_score[n].text) and (int(home_score[n].text) > 0 and int(away_score[n].text) > 0):
        count_AW_A_indp += 0.5
    if int(home_score[n].text) == int(away_score[n].text) and (int(home_score[n].text) == 0 and int(away_score[n].text) == 0):
        count_AW_A_indp += 0
    if (int(home_score[n].text) > 0 and int(away_score[n].text) > 0) and int(home_score[n].text) > 1 and (home_x[n].text == away_teamx):
        count_GG_A_indp += 1
    if (int(home_score[n].text) > 0 and int(away_score[n].text) > 0) and int(away_score[n].text) > 1 and (away_x[n].text == away_teamx):
        count_GG_A_indp += 1
    if (int(home_score[n].text) + int(away_score[n].text)) >= 2 and (home_x[n].text == away_teamx) and int(home_score[n].text) >= 1:
        count_1_5_A_indp += 1
    if (int(home_score[n].text) + int(away_score[n].text)) >= 2 and (away_x[n].text == away_teamx) and int(away_score[n].text) >= 1:
        count_1_5_A_indp += 1
    if (int(home_score[n].text) + int(away_score[n].text)) >= 3 and (home_x[n].text == away_teamx) and int(home_score[n].text) >= 2:
        count_2_5_A_indp += 1
    if (int(home_score[n].text) + int(away_score[n].text)) >= 3 and (away_x[n].text == away_teamx) and int(away_score[n].text) >= 2:
        count_2_5_A_indp += 1
    if int(home_score[n].text) != int(away_score[n].text) and int(home_score[n].text) >= 1 and (home_x[n].text == away_teamx):
        count_12_A_indp += 1
    if int(away_score[n].text) != int(home_score[n].text) and int(away_score[n].text) >= 1 and (away_x[n].text == away_teamx):
        count_12_A_indp += 1


def at_indp_prob_calc():
    global valid_games_A_indp
    global count_AW_A_indp
    global count_GG_A_indp
    global count_1_5_A_indp
    global count_2_5_A_indp
    global count_12_A_indp

    prob_GG_A_indp = float(count_GG_A_indp / valid_games_A_indp)
    prob_1_5_A_indp = float(count_1_5_A_indp / valid_games_A_indp)
    prob_2_5_A_indp = float(count_2_5_A_indp / valid_games_A_indp)
    prob_12_A_indp = float(count_12_A_indp / valid_games_A_indp)
    prob_AW_A_indp = float(count_AW_A_indp / valid_games_A_indp)
    prob_HW_A_indp = 1 - prob_AW_A_indp

    if prob_HW_A_indp == 1.0:
        prob_HW_A_indp -= 0.01
    if prob_AW_A_indp == 1.0:
        prob_AW_A_indp -= 0.01
    if prob_GG_A_indp == 1.0:
        prob_GG_A_indp -= 0.01
    if prob_1_5_A_indp == 1.0:
        prob_1_5_A_indp -= 0.01
    if prob_2_5_A_indp == 1.0:
        prob_2_5_A_indp -= 0.01
    if prob_12_A_indp == 1.0:
        prob_12_A_indp -= 0.01

    if prob_GG_A_indp == 0.0:
        prob_GG_A_indp += 0.01
    if prob_1_5_A_indp == 0.0:
        prob_1_5_A_indp += 0.01
    if prob_2_5_A_indp == 0.0:
        prob_2_5_A_indp += 0.01
    if prob_12_A_indp == 0.0:
        prob_12_A_indp += 0.01
    if prob_HW_A_indp == 0.0:
        prob_HW_A_indp += 0.01
    if prob_AW_A_indp == 0.0:
        prob_AW_A_indp += 0.01
    return [prob_HW_A_indp, prob_AW_A_indp, prob_GG_A_indp, prob_1_5_A_indp, prob_2_5_A_indp, prob_12_A_indp]


def at_indp_appender(prb_HW_A_indp, prb_AW_A_indp, prb_GG_A_indp, prb_1_5_A_indp, prb_2_5_A_indp, prb_12_A_indp):
    prob_HW_A_indps.append(prb_HW_A_indp)
    prob_AW_A_indps.append(prb_AW_A_indp)
    prob_GG_A_indps.append(prb_GG_A_indp)
    prob_1_5_A_indps.append(prb_1_5_A_indp)
    prob_2_5_A_indps.append(prb_2_5_A_indp)
    prob_12_A_indps.append(prb_12_A_indp)


def show_more_matches():
    try:
        shows = driver.find_elements(By.CSS_SELECTOR, '[class="h2h__showMore showMore"]')
        if len(shows) == 3:
            shows[0].click()
            sleep(0.1)
            shows[1].click()
            sleep(0.1)
            shows[2].click()
        elif len(shows) == 2:
            shows[0].click()
            sleep(0.1)
            shows[1].click()
        else:
            show = driver.find_element(By.CSS_SELECTOR, '[class="h2h__showMore showMore"]')
            show.click()
    except ElementClickInterceptedException:
        try:
            driver.refresh()
            sleep(0.1)
            show = driver.find_element(By.CSS_SELECTOR, '[class="h2h__showMore showMore"]')
            show.click()
            sleep(0.1)
        except ElementClickInterceptedException:
            pass
    except NoSuchElementException:
        pass


def home_form_checker(home_teamk, away_teamk):
    global valid_games_H_form
    global count_HW_form
    global count_HD_form
    global count_HL_form
    global H_form_L
    global H_form_W
    global H_form_D
    try:
        subx1 = driver.find_elements(By.CSS_SELECTOR, '.section:first-child .h2h__row')
        if len(subx1) >= 5:
            dssc = 0
            for k in range(5):
                datte = driver.find_elements(By.CSS_SELECTOR, '.section:first-child .h2h__row .h2h__date')
                homme_x = driver.find_elements(By.CSS_SELECTOR, '.section:first-child .h2h__row .h2h__homeParticipant .h2h__participantInner')
                awway_x = driver.find_elements(By.CSS_SELECTOR, '.section:first-child .h2h__row .h2h__awayParticipant .h2h__participantInner')
                homme_score = driver.find_elements(By.CSS_SELECTOR, '.section:first-child .h2h__row .h2h__result span:first-child')
                awway_score = driver.find_elements(By.CSS_SELECTOR, '.section:first-child .h2h__row .h2h__result span:last-child')
                teamm_vetter = [str(homme_x[k].text), str(awway_x[k].text)]
                try:
                    if str(home_teamk) in teamm_vetter and (str(away_teamk) not in teamm_vetter):
                        valid_games_H_form += 1
                        if (int(homme_score[k].text) > int(awway_score[k].text)) and (str(homme_x[k].text) == str(home_teamk)):
                            count_HW_form += 1
                        if (int(awway_score[k].text) > int(homme_score[k].text)) and (str(awway_x[k].text) == str(home_teamk)):
                            count_HW_form += 1
                        if int(homme_score[k].text) == int(awway_score[k].text):
                            count_HD_form += 1
                        dssc += 1
                    else:
                        break
                except ValueError:
                    print(f"Value Error at FORM Home : {datte[k].text} | {homme_x[k].text} vs {awway_x[k].text}")
                    break
            if dssc >= 5:
                try:
                    H_form_W = float(count_HW_form / dssc)
                    H_form_D = float(count_HD_form / dssc)
                    H_form_L = float(1 - (H_form_W + H_form_D))
                    h_form_W.append(round(H_form_W, 1))
                    h_form_D.append(round(H_form_D, 1))
                    h_form_L.append(round(H_form_L, 1))
                except ZeroDivisionError:
                    h_form_W.append(0)
                    h_form_D.append(0)
                    h_form_L.append(0)
            else:
                h_form_W.append(0)
                h_form_D.append(0)
                h_form_L.append(0)
        else:
            h_form_W.append(0)
            h_form_D.append(0)
            h_form_L.append(0)
    except ElementNotInteractableException:
        h_form_W.append(0)
        h_form_D.append(0)
        h_form_L.append(0)


def away_form_checker(home_teamk, away_teamk):
    global valid_games_A_form
    global count_AW_form
    global count_AD_form
    global count_AL_form
    global A_form_L
    global A_form_W
    global A_form_D
    try:
        subx2 = driver.find_elements(By.CSS_SELECTOR, '.section:nth-child(2) .h2h__row')
        if len(subx2) >= 5:
            dssc = 0
            for n in range(5):
                datte = driver.find_elements(By.CSS_SELECTOR, '.section:nth-child(2) .h2h__row .h2h__date')
                homme_x = driver.find_elements(By.CSS_SELECTOR, '.section:nth-child(2) .h2h__row .h2h__homeParticipant .h2h__participantInner')
                awway_x = driver.find_elements(By.CSS_SELECTOR, '.section:nth-child(2) .h2h__row .h2h__awayParticipant .h2h__participantInner')
                homme_score = driver.find_elements(By.CSS_SELECTOR, '.section:nth-child(2) .h2h__row .h2h__result span:first-child')
                awway_score = driver.find_elements(By.CSS_SELECTOR, '.section:nth-child(2) .h2h__row .h2h__result span:last-child')
                teamm_vetter = [str(homme_x[n].text), str(awway_x[n].text)]
                try:
                    if (str(home_teamk) not in teamm_vetter) and (str(away_teamk) in teamm_vetter):
                        valid_games_A_form += 1
                        if (int(homme_score[n].text) > int(awway_score[n].text)) and (str(homme_x[n].text) == str(away_teamk)):
                            count_AW_form += 1
                        if (int(awway_score[n].text) > int(homme_score[n].text)) and (str(awway_x[n].text) == str(away_teamk)):
                            count_AW_form += 1
                        if int(homme_score[n].text) == int(awway_score[n].text):
                            count_AD_form += 1
                        dssc += 1
                    else:
                        break
                except ValueError:
                    print(f"Error at FORM Away: {datte[n].text} | {homme_x[n].text} vs {awway_x[n].text}")
                    break
            if dssc >= 5:
                try:
                    A_form_W = float(count_AW_form / dssc)
                    A_form_D = float(count_AD_form / dssc)
                    A_form_L = float(1 - (A_form_W + A_form_D))
                    a_form_W.append(round(A_form_W, 1))
                    a_form_D.append(round(A_form_D, 1))
                    a_form_L.append(round(A_form_L, 1))
                except ZeroDivisionError:
                    a_form_W.append(0)
                    a_form_D.append(0)
                    a_form_L.append(0)
            else:
                a_form_W.append(0)
                a_form_D.append(0)
                a_form_L.append(0)
        else:
            a_form_W.append(0)
            a_form_D.append(0)
            a_form_L.append(0)
    except ElementNotInteractableException:
        a_form_W.append(0)
        a_form_D.append(0)
        a_form_L.append(0)


def print_all_data():
    print(f"Countries: {countries}")
    print(f"Leagues: {leagues}")
    print(f"Home Teams: {home_teams}")
    print(f"Home Positions: {home_positions}")
    print(f"Home Points: {home_points}")
    print(f"Home No Matches Played: {home_nums_matches_played}")
    print(f"Away Teams: {away_teams}")
    print(f"Away Positions: {away_positions}")
    print(f"Away Points: {away_points}")
    print(f"Away No Matches Played: {away_nums_matches_played}")
    print(f"Match Times: {match_times}")
    print(f"Home W Form: {h_form_W}")
    print(f"Home D Form: {h_form_D}")
    print(f"Home L Form: {h_form_L}")
    print(f"Away W Form: {a_form_W}")
    print(f"Away D Form: {a_form_D}")
    print(f"Away L Form: {a_form_L}")
    print(f"Prob GGs: {prob_GGs}")
    print(f"Prob 1_5s: {prob_1_5s}")
    print(f"Prob 2_5s: {prob_2_5s}")
    print(f"Prob 12s: {prob_12s}")
    print(f"Prob HWs: {prob_HWs}")
    print(f"Prob AWs: {prob_AWs}")
    print(f"Prob GG_H_indps: {prob_GG_H_indps}")
    print(f"Prob 1_5_H_indps: {prob_1_5_H_indps}")
    print(f"Prob 2_5_H_indps: {prob_2_5_H_indps}")
    print(f"Prob 12_H_indps: {prob_12_H_indps}")
    print(f"Prob HW_H_indps: {prob_HW_H_indps}")
    print(f"Prob AW_H_indps: {prob_AW_H_indps}")
    print(f"Prob GG_A_indps: {prob_GG_A_indps}")
    print(f"Prob 1_5_A_indps: {prob_1_5_A_indps}")
    print(f"Prob 2_5_A_indps: {prob_2_5_A_indps}")
    print(f"Prob 12_A_indps: {prob_12_A_indps}")
    print(f"Prob HW_A_indps: {prob_HW_A_indps}")
    print(f"Prob AW_A_indps: {prob_AW_A_indps}")
    print(f"Bayesian Home Win: {bayesian_home_Win_d}")
    print(f"Bayesian Away Win: {bayesian_away_Win_d}")
    print(f"Bayesian GG: {bayesian_GG_d}")
    print(f"Bayesian 1.5: {bayesian_1_5_d}")
    print(f"Bayesian 2.5: {bayesian_2_5_d}")
    print(f"Bayesian 12: {bayesian_12_d}")
    print(f"Countries: {len(countries)}, Leagues: {len(leagues)}, Home Teams: {len(home_teams)}, "
          f"Home Positions: {len(home_positions)}, Home Points: {len(home_points)}, "
          f"Home No Matches Played: {len(home_nums_matches_played)}, Away Teams: {len(away_teams)}, "
          f"Away Positions: {len(away_positions)}, Away Points: {len(away_points)}, "
          f"Away No Matches Played: {len(away_nums_matches_played)}, Match Times: {len(match_times)} "
          f"Home W Form: {len(h_form_W)}, Home D Form: {len(h_form_D)}, Home L Form: {len(h_form_L)}, "
          f"Away W Form: {len(a_form_W)}, Away D Form: {len(a_form_D)}, Away L Form: {len(a_form_L)}"
          f"Prob GGs: {len(prob_GGs)}, Prob 1_5s: {len(prob_1_5s)},Prob 2_5s: {len(prob_2_5s)},"
          f"Prob 12s: {len(prob_12s)}, Prob HWs: {len(prob_HWs)}, Prob AWs: {len(prob_AWs)}, "
          f"Prob GG_H_indps: {len(prob_GG_H_indps)}, Prob 1_5_H_indps: {len(prob_1_5_H_indps)}, "
          f"Prob 2_5_H_indps: {len(prob_2_5_H_indps)}, Prob 12_H_indps: {len(prob_12_H_indps)},"
          f"Prob HW_H_indps: {len(prob_HW_H_indps)}, Prob AW_H_indps: {len(prob_AW_H_indps)}, "
          f"Prob GG_A_indps: {len(prob_GG_A_indps)}, Prob 1_5_A_indps: {len(prob_1_5_A_indps)}, "
          f"Prob 2_5_A_indps: {len(prob_2_5_A_indps)}, Prob 12_A_indps: {len(prob_12_A_indps)}, "
          f"Prob HW_A_indps: {len(prob_HW_A_indps)}, Prob AW_A_indps: {len(prob_AW_A_indps)}, "
          f"Bayesian Home Win: {len(bayesian_home_Win_d)}, Bayesian Away Win: {len(bayesian_away_Win_d)}, "
          f"Bayesian GG: {len(bayesian_GG_d)}, Bayesian 1.5: {len(bayesian_1_5_d)}, Bayesian 2.5: {len(bayesian_2_5_d)}, "
          f"Bayesian 12: {len(bayesian_12_d) }")


countries = []
home_teams = []
away_teams = []
leagues = []
home_positions = []
away_positions = []
home_points = []
away_points = []
match_times = []
home_nums_matches_played = []
away_nums_matches_played = []
h_form_W = []
h_form_L = []
h_form_D = []
a_form_W = []
a_form_D = []
a_form_L = []
prob_GGs = []
prob_1_5s = []
prob_2_5s = []
prob_12s = []
prob_HWs = []
prob_AWs = []
prob_GG_H_indps = []
prob_1_5_H_indps = []
prob_2_5_H_indps = []
prob_12_H_indps = []
prob_HW_H_indps = []
prob_AW_H_indps = []
prob_GG_A_indps = []
prob_1_5_A_indps = []
prob_2_5_A_indps = []
prob_12_A_indps = []
prob_HW_A_indps = []
prob_AW_A_indps = []
home_z_prob = []
away_z_prob = []
diff_z_prob = []

divs = driver.find_elements(By.CSS_SELECTOR, '.soccer .event__match--scheduled')
print(len(divs))
match_timez = driver.find_elements(By.CLASS_NAME, 'event__time')
print(len(match_timez))

for i in range(len(match_timez)):
    try:
        divs[i].click()
    except StaleElementReferenceException:
        driver.refresh()
        sleep(4)
        driver.find_element(By.CSS_SELECTOR, ".filters__group .filters__tab:last-child").click()
        sleep(2)
        divs = driver.find_elements(By.CSS_SELECTOR, '.soccer .event__match--scheduled')
        divs[i].click()

    print(i)
    sleep(0.1)
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)

    try:
        home_teamx = driver.find_element(By.CSS_SELECTOR, '.duelParticipant__home  .participant__participantName a').text
        away_teamx = driver.find_element(By.CSS_SELECTOR, '.duelParticipant__away  .participant__participantName a').text
    except NoSuchElementException:
        try:
            driver.refresh()
            sleep(0.1)
            home_teamx = driver.find_element(By.CSS_SELECTOR, '.duelParticipant__home  .participant__participantName a').text
            away_teamx = driver.find_element(By.CSS_SELECTOR, '.duelParticipant__away  .participant__participantName a').text
        except NoSuchElementException:
            break
    try:
        driver.find_element(By.LINK_TEXT, "STANDINGS").click()
        form_l = len(driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--form .wld'))
        sleep(0.1)
        selected_teams_names = driver.find_elements(By.CSS_SELECTOR, ".table__row--selected  .tableCellParticipant__name")
        H_form_D = 0
        H_form_L = 0
        H_form_W = 0
        A_form_D = 0
        A_form_L = 0
        A_form_W = 0
        try:
            pts_pos_mp()
            teams_form_checker()
            current_ht_pts = home_points[i]
            current_at_pts = away_points[i]
            z_scorer(htpts=current_ht_pts, atpts=current_at_pts)
        except IndexError:
            print("IYYY")
            try:
                driver.close()
                driver.switch_to.window(window_before)
                divs[i].click()
                window_after = driver.window_handles[1]
                driver.switch_to.window(window_after)
                driver.find_element(By.LINK_TEXT, "STANDINGS").click()
                form_l = len(driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--form .wld'))
                sleep(0.2)
                selected_teams_names = driver.find_elements(By.CSS_SELECTOR, ".table__row--selected  .tableCellParticipant__name")
                H_form_D = 0
                H_form_L = 0
                H_form_W = 0
                A_form_D = 0
                A_form_L = 0
                A_form_W = 0
                pts_pos_mp()
                teams_form_checker()
                current_ht_pts = home_points[i]
                current_at_pts = away_points[i]
                z_scorer(htpts=current_ht_pts, atpts=current_at_pts)
            except IndexError:
                print("000")
                try:
                    driver.refresh()
                    sleep(1.5)
                    pts_pos_mp()
                    teams_form_checker()
                    current_ht_pts = home_points[i]
                    current_at_pts = away_points[i]
                    z_scorer(htpts=current_ht_pts, atpts=current_at_pts)
                except IndexError:
                    print("111")
                    driver.close()
                    driver.switch_to.window(window_before)
                    driver.get(FLASH_SCORE)
                    sleep(0.1)
                    driver.find_element(By.CSS_SELECTOR, '[title="Next day"]').click()
                    sleep(0.1)
                    driver.find_element(By.CSS_SELECTOR, ".filters__group .filters__tab:last-child").click()
                    sleep(0.1)
                    divs = driver.find_elements(By.CSS_SELECTOR, '.soccer .event__match--scheduled')
                    try:
                        divs[i].click()
                    except StaleElementReferenceException:
                        driver.refresh()
                        sleep(4)
                        driver.find_element(By.CSS_SELECTOR, ".filters__group .filters__tab:last-child").click()
                        sleep(2)
                        divs = driver.find_elements(By.CSS_SELECTOR, '.soccer .event__match--scheduled')
                        divs[i].click()
                    print(i)
                    sleep(0.1)
                    window_after = driver.window_handles[1]
                    driver.switch_to.window(window_after)
                    try:
                        home_teamx = driver.find_element(By.CSS_SELECTOR, '.duelParticipant__home  .participant__participantName a').text
                        away_teamx = driver.find_element(By.CSS_SELECTOR, '.duelParticipant__away  .participant__participantName a').text
                    except NoSuchElementException:
                        try:
                            driver.refresh()
                            sleep(0.1)
                            home_teamx = driver.find_element(By.CSS_SELECTOR, '.duelParticipant__home  .participant__participantName a').text
                            away_teamx = driver.find_element(By.CSS_SELECTOR, '.duelParticipant__away  .participant__participantName a').text
                        except NoSuchElementException:
                            break
                    driver.find_element(By.LINK_TEXT, "STANDINGS").click()
                    form_l = len(driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--form .wld'))
                    selected_teams_names = driver.find_elements(By.CSS_SELECTOR, ".table__row--selected  .tableCellParticipant__name")
                    H_form_D = 0
                    H_form_L = 0
                    H_form_W = 0
                    A_form_D = 0
                    A_form_L = 0
                    A_form_W = 0
                    pts_pos_mp()
                    teams_form_checker()
                    current_ht_pts = home_points[i]
                    current_at_pts = away_points[i]
                    z_scorer(htpts=current_ht_pts, atpts=current_at_pts)
        except StaleElementReferenceException:
            print("IZZZ")
            try:
                driver.close()
                driver.switch_to.window(window_before)
                divs[i].click()
                window_after = driver.window_handles[1]
                driver.switch_to.window(window_after)
                driver.find_element(By.LINK_TEXT, "STANDINGS").click()
                form_l = len(driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--form .wld'))
                sleep(0.2)
                selected_teams_names = driver.find_elements(By.CSS_SELECTOR, ".table__row--selected  .tableCellParticipant__name")
                H_form_D = 0
                H_form_L = 0
                H_form_W = 0
                A_form_D = 0
                A_form_L = 0
                A_form_W = 0
                pts_pos_mp()
                teams_form_checker()
                current_ht_pts = home_points[i]
                current_at_pts = away_points[i]
                z_scorer(htpts=current_ht_pts, atpts=current_at_pts)
            except StaleElementReferenceException:
                print("222")
                try:
                    driver.refresh()
                    sleep(1.5)
                    pts_pos_mp()
                    teams_form_checker()
                    current_ht_pts = home_points[i]
                    current_at_pts = away_points[i]
                    z_scorer(htpts=current_ht_pts, atpts=current_at_pts)
                except IndexError:
                    print("333")
                    driver.close()
                    driver.switch_to.window(window_before)
                    driver.get(FLASH_SCORE)
                    sleep(0.1)
                    driver.find_element(By.CSS_SELECTOR, '[title="Next day"]').click()
                    sleep(0.1)
                    driver.find_element(By.CSS_SELECTOR, ".filters__group .filters__tab:last-child").click()
                    sleep(0.1)
                    divs = driver.find_elements(By.CSS_SELECTOR, '.soccer .event__match--scheduled')
                    try:
                        divs[i].click()
                    except StaleElementReferenceException:
                        driver.refresh()
                        sleep(4)
                        driver.find_element(By.CSS_SELECTOR, ".filters__group .filters__tab:last-child").click()
                        sleep(2)
                        divs = driver.find_elements(By.CSS_SELECTOR, '.soccer .event__match--scheduled')
                        divs[i].click()
                    print(i)
                    sleep(0.1)
                    window_after = driver.window_handles[1]
                    driver.switch_to.window(window_after)
                    try:
                        home_teamx = driver.find_element(By.CSS_SELECTOR, '.duelParticipant__home  .participant__participantName a').text
                        away_teamx = driver.find_element(By.CSS_SELECTOR, '.duelParticipant__away  .participant__participantName a').text
                    except NoSuchElementException:
                        try:
                            driver.refresh()
                            sleep(0.1)
                            home_teamx = driver.find_element(By.CSS_SELECTOR, '.duelParticipant__home  .participant__participantName a').text
                            away_teamx = driver.find_element(By.CSS_SELECTOR, '.duelParticipant__away  .participant__participantName a').text
                        except NoSuchElementException:
                            break
                    driver.find_element(By.LINK_TEXT, "STANDINGS").click()
                    form_l = len(driver.find_elements(By.CSS_SELECTOR, '.table__row--selected  .table__cell--form .wld'))
                    selected_teams_names = driver.find_elements(By.CSS_SELECTOR, ".table__row--selected  .tableCellParticipant__name")
                    H_form_D = 0
                    H_form_L = 0
                    H_form_W = 0
                    A_form_D = 0
                    A_form_L = 0
                    A_form_W = 0
                    pts_pos_mp()
                    teams_form_checker()
                    current_ht_pts = home_points[i]
                    current_at_pts = away_points[i]
                    z_scorer(htpts=current_ht_pts, atpts=current_at_pts)
        sleep(0.1)
        team_data()
        driver.find_element(By.LINK_TEXT, "H2H").click()
        sleep(0.1)
        valid_games = 0
        count_GG = 0
        count_1_5 = 0
        count_2_5 = 0
        count_12 = 0
        count_HW = 0
        count_AW = 0
        valid_games_H_indp = 0
        count_GG_H_indp = 0
        count_1_5_H_indp = 0
        count_2_5_H_indp = 0
        count_12_H_indp = 0
        count_HW_H_indp = 0
        valid_games_A_indp = 0
        count_GG_A_indp = 0
        count_1_5_A_indp = 0
        count_2_5_A_indp = 0
        count_12_A_indp = 0
        count_AW_A_indp = 0
        show_more_matches()
        if form_l < 12:
            valid_games_H_form = 0
            valid_games_A_form = 0
            count_HW_form = 0
            count_HD_form = 0
            count_HL_form = 0
            count_AW_form = 0
            count_AD_form = 0
            count_AL_form = 0
            H_form_D = 0
            H_form_L = 0
            H_form_W = 0
            A_form_D = 0
            A_form_L = 0
            A_form_W = 0
            home_form_checker(home_teamk=home_teamx, away_teamk=away_teamx)
            away_form_checker(home_teamk=home_teamx, away_teamk=away_teamx)
        try:
            sub1 = driver.find_elements(By.CSS_SELECTOR, '.section:first-child .h2h__row')
            if len(sub1) > 9:
                dsc = 0
                for a in range(len(sub1)):
                    date = driver.find_elements(By.CSS_SELECTOR, '.section:first-child .h2h__row .h2h__date')
                    home_x = driver.find_elements(By.CSS_SELECTOR, '.section:first-child .h2h__row .h2h__homeParticipant .h2h__participantInner')
                    away_x = driver.find_elements(By.CSS_SELECTOR, '.section:first-child .h2h__row .h2h__awayParticipant .h2h__participantInner')
                    home_score = driver.find_elements(By.CSS_SELECTOR, '.section:first-child .h2h__row .h2h__result span:first-child')
                    away_score = driver.find_elements(By.CSS_SELECTOR, '.section:first-child .h2h__row .h2h__result span:last-child')
                    team_vetter = [home_x[a].text, away_x[a].text]
                    try:
                        if int(date[a].text.split('.')[-1].strip()) >= YEAR and (home_teamx in team_vetter) and (away_teamx not in team_vetter):
                            ht_indp_aggregator(a)
                            dsc += 1

                        else:
                            break
                    except ValueError:
                        print(f"Value Error at Home2 : {date[a].text} | {home_x[a].text} vs {away_x[a].text}")
                        break
                if dsc >= DSCRM_H_A:
                    try:
                        ht_indp_values = ht_indp_prob_calc()
                        ht_indp_appender(prb_HW_H_indp=ht_indp_values[0], prb_AW_H_indp=ht_indp_values[1], prb_GG_H_indp=ht_indp_values[2], prb_1_5_H_indp=ht_indp_values[3],
                                         prb_2_5_H_indp=ht_indp_values[4], prb_12_H_indp=ht_indp_values[5])
                    except ZeroDivisionError:
                        ht_indp_appender(prb_HW_H_indp=0.01, prb_AW_H_indp=0.01, prb_GG_H_indp=0.01, prb_1_5_H_indp=0.01, prb_2_5_H_indp=0.01, prb_12_H_indp=0.01)
                else:
                    ht_indp_appender(prb_HW_H_indp=0.01, prb_AW_H_indp=0.01, prb_GG_H_indp=0.01, prb_1_5_H_indp=0.01, prb_2_5_H_indp=0.01, prb_12_H_indp=0.01)
            else:
                ht_indp_appender(prb_HW_H_indp=0.01, prb_AW_H_indp=0.01, prb_GG_H_indp=0.01, prb_1_5_H_indp=0.01, prb_2_5_H_indp=0.01, prb_12_H_indp=0.01)
        except ElementNotInteractableException:
            ht_indp_appender(prb_HW_H_indp=0.01, prb_AW_H_indp=0.01, prb_GG_H_indp=0.01, prb_1_5_H_indp=0.01, prb_2_5_H_indp=0.01, prb_12_H_indp=0.01)
        sleep(0.1)
        try:
            sub2 = driver.find_elements(By.CSS_SELECTOR, '.section:nth-child(2) .h2h__row')
            if len(sub2) > 9:
                dsc = 0
                for b in range(len(sub2)):
                    date = driver.find_elements(By.CSS_SELECTOR, '.section:nth-child(2) .h2h__row .h2h__date')
                    home_x = driver.find_elements(By.CSS_SELECTOR, '.section:nth-child(2) .h2h__row .h2h__homeParticipant .h2h__participantInner')
                    away_x = driver.find_elements(By.CSS_SELECTOR, '.section:nth-child(2) .h2h__row .h2h__awayParticipant .h2h__participantInner')
                    home_score = driver.find_elements(By.CSS_SELECTOR, '.section:nth-child(2) .h2h__row .h2h__result span:first-child')
                    away_score = driver.find_elements(By.CSS_SELECTOR, '.section:nth-child(2) .h2h__row .h2h__result span:last-child')
                    team_vetter = [home_x[b].text, away_x[b].text]
                    try:
                        if int(date[b].text.split('.')[-1].strip()) >= YEAR and (home_teamx not in team_vetter) and (away_teamx in team_vetter):
                            at_indp_aggregator(b)
                            dsc += 1
                        else:
                            break
                    except ValueError:
                        print(f"Error at Away: {date[b].text} | {home_x[b].text} vs {away_x[b].text}")
                        break
                if dsc >= DSCRM_H_A:
                    try:
                        at_indp_values = at_indp_prob_calc()
                        at_indp_appender(prb_HW_A_indp=at_indp_values[0], prb_AW_A_indp=at_indp_values[1], prb_GG_A_indp=at_indp_values[2], prb_1_5_A_indp=at_indp_values[3],
                                         prb_2_5_A_indp=at_indp_values[4], prb_12_A_indp=at_indp_values[5])
                    except ZeroDivisionError:
                        at_indp_appender(prb_HW_A_indp=0.01, prb_AW_A_indp=0.01, prb_GG_A_indp=0.01, prb_1_5_A_indp=0.01, prb_2_5_A_indp=0.01, prb_12_A_indp=0.01)
                else:
                    at_indp_appender(prb_HW_A_indp=0.01, prb_AW_A_indp=0.01, prb_GG_A_indp=0.01, prb_1_5_A_indp=0.01, prb_2_5_A_indp=0.01, prb_12_A_indp=0.01)
            else:
                at_indp_appender(prb_HW_A_indp=0.01, prb_AW_A_indp=0.01, prb_GG_A_indp=0.01, prb_1_5_A_indp=0.01, prb_2_5_A_indp=0.01, prb_12_A_indp=0.01)
        except ElementNotInteractableException:
            pass
            at_indp_appender(prb_HW_A_indp=0.01, prb_AW_A_indp=0.01, prb_GG_A_indp=0.01, prb_1_5_A_indp=0.01, prb_2_5_A_indp=0.01, prb_12_A_indp=0.01)
        sleep(0.1)
        try:
            sub3 = driver.find_elements(By.CSS_SELECTOR, '.section:last-child .h2h__row')
            if len(sub3) > 2:
                dsc = 0
                for c in range(len(sub3)):
                    date = driver.find_elements(By.CSS_SELECTOR, '.section:last-child .h2h__row .h2h__date')
                    home_x = driver.find_elements(By.CSS_SELECTOR, '.section:last-child .h2h__row .h2h__homeParticipant .h2h__participantInner')
                    away_x = driver.find_elements(By.CSS_SELECTOR, '.section:last-child .h2h__row .h2h__awayParticipant .h2h__participantInner')
                    home_score = driver.find_elements(By.CSS_SELECTOR, '.section:last-child .h2h__row .h2h__result span:first-child')
                    away_score = driver.find_elements(By.CSS_SELECTOR, '.section:last-child .h2h__row .h2h__result span:last-child')
                    try:
                        if int(date[c].text.split('.')[-1].strip()) >= YEAR:
                            h2h_aggregator(c)
                            dsc += 1
                        else:
                            break
                    except ValueError:
                        pass
                        print(f"Value Error at H2H: {date[c].text} | {home_x[c].text} vs {away_x[c].text}")
                        break
                if dsc >= DSCRM_BT:
                    try:
                        h2h_values = h2h_prob_calc()
                        h2h_appender(prb_HW=h2h_values[0], prb_AW=h2h_values[1], prb_GG=h2h_values[2], prb_1_5=h2h_values[3],
                                     prb_2_5=h2h_values[4], prb_12=h2h_values[5])
                    except ZeroDivisionError:
                        pass
                        h2h_appender(prb_HW=0.01, prb_AW=0.1, prb_GG=0.01, prb_1_5=0.01, prb_2_5=0.01, prb_12=0.01)
                else:
                    h2h_appender(prb_HW=0.01, prb_AW=0.1, prb_GG=0.01, prb_1_5=0.01, prb_2_5=0.01, prb_12=0.01)
            else:
                h2h_appender(prb_HW=0.01, prb_AW=0.1, prb_GG=0.01, prb_1_5=0.01, prb_2_5=0.01, prb_12=0.01)
        except ElementNotInteractableException:
            pass
            h2h_appender(prb_HW=0.01, prb_AW=0.1, prb_GG=0.01, prb_1_5=0.01, prb_2_5=0.01, prb_12=0.01)
        sleep(0.1)
        driver.close()
        driver.switch_to.window(window_before)
        match_times.append(match_timez[i].text)
        sleep(0.1)

    except NoSuchElementException:
        try:
            sleep(1)
            print(f"No Pts Pos or Form Data for {home_teamx} vs {away_teamx}")
            team_data()
            driver.find_element(By.LINK_TEXT, "H2H").click()
            sleep(0.1)
            valid_games = 0
            count_GG = 0
            count_1_5 = 0
            count_2_5 = 0
            count_12 = 0
            count_HW = 0
            count_AW = 0
            valid_games_H_indp = 0
            count_GG_H_indp = 0
            count_1_5_H_indp = 0
            count_2_5_H_indp = 0
            count_12_H_indp = 0
            count_HW_H_indp = 0
            valid_games_A_indp = 0
            count_GG_A_indp = 0
            count_1_5_A_indp = 0
            count_2_5_A_indp = 0
            count_12_A_indp = 0
            count_AW_A_indp = 0
            show_more_matches()
            valid_games_H_form = 0
            valid_games_A_form = 0
            count_HW_form = 0
            count_HD_form = 0
            count_HL_form = 0
            count_AW_form = 0
            count_AD_form = 0
            count_AL_form = 0
            H_form_D = 0
            H_form_L = 0
            H_form_W = 0
            A_form_D = 0
            A_form_L = 0
            A_form_W = 0
            home_form_checker(home_teamk=home_teamx, away_teamk=away_teamx)
            away_form_checker(home_teamk=home_teamx, away_teamk=away_teamx)
            try:
                sub1 = driver.find_elements(By.CSS_SELECTOR, '.section:first-child .h2h__row')
                if len(sub1) > 9:
                    dsc = 0
                    for a in range(len(sub1)):
                        date = driver.find_elements(By.CSS_SELECTOR, '.section:first-child .h2h__row .h2h__date')
                        home_x = driver.find_elements(By.CSS_SELECTOR, '.section:first-child .h2h__row .h2h__homeParticipant .h2h__participantInner')
                        away_x = driver.find_elements(By.CSS_SELECTOR, '.section:first-child .h2h__row .h2h__awayParticipant .h2h__participantInner')
                        home_score = driver.find_elements(By.CSS_SELECTOR, '.section:first-child .h2h__row .h2h__result span:first-child')
                        away_score = driver.find_elements(By.CSS_SELECTOR, '.section:first-child .h2h__row .h2h__result span:last-child')
                        team_vetter = [home_x[a].text, away_x[a].text]
                        try:
                            if int(date[a].text.split('.')[-1].strip()) >= YEAR and (home_teamx in team_vetter) and (away_teamx not in team_vetter):
                                ht_indp_aggregator(a)
                                dsc += 1
                            else:
                                break
                        except ValueError:
                            print(f"Value Error at Home2 : {date[a].text} | {home_x[a].text} vs {away_x[a].text}")
                            break
                    if dsc >= DSCRM_H_A:
                        try:
                            ht_indp_values = ht_indp_prob_calc()
                            ht_indp_appender(prb_HW_H_indp=ht_indp_values[0], prb_AW_H_indp=ht_indp_values[1], prb_GG_H_indp=ht_indp_values[2], prb_1_5_H_indp=ht_indp_values[3],
                                             prb_2_5_H_indp=ht_indp_values[4], prb_12_H_indp=ht_indp_values[5])
                        except ZeroDivisionError:
                            ht_indp_appender(prb_HW_H_indp=0.01, prb_AW_H_indp=0.01, prb_GG_H_indp=0.01, prb_1_5_H_indp=0.01, prb_2_5_H_indp=0.01, prb_12_H_indp=0.01)
                    else:
                        ht_indp_appender(prb_HW_H_indp=0.01, prb_AW_H_indp=0.01, prb_GG_H_indp=0.01, prb_1_5_H_indp=0.01, prb_2_5_H_indp=0.01, prb_12_H_indp=0.01)
                else:
                    ht_indp_appender(prb_HW_H_indp=0.01, prb_AW_H_indp=0.01, prb_GG_H_indp=0.01, prb_1_5_H_indp=0.01, prb_2_5_H_indp=0.01, prb_12_H_indp=0.01)
            except ElementNotInteractableException:
                pass
                ht_indp_appender(prb_HW_H_indp=0.01, prb_AW_H_indp=0.01, prb_GG_H_indp=0.01, prb_1_5_H_indp=0.01, prb_2_5_H_indp=0.01, prb_12_H_indp=0.01)
            sleep(0.1)
            try:
                sub2 = driver.find_elements(By.CSS_SELECTOR, '.section:nth-child(2) .h2h__row')
                if len(sub2) > 9:
                    dsc = 0
                    for b in range(len(sub2)):
                        date = driver.find_elements(By.CSS_SELECTOR, '.section:nth-child(2) .h2h__row .h2h__date')
                        home_x = driver.find_elements(By.CSS_SELECTOR, '.section:nth-child(2) .h2h__row .h2h__homeParticipant .h2h__participantInner')
                        away_x = driver.find_elements(By.CSS_SELECTOR, '.section:nth-child(2) .h2h__row .h2h__awayParticipant .h2h__participantInner')
                        home_score = driver.find_elements(By.CSS_SELECTOR, '.section:nth-child(2) .h2h__row .h2h__result span:first-child')
                        away_score = driver.find_elements(By.CSS_SELECTOR, '.section:nth-child(2) .h2h__row .h2h__result span:last-child')
                        team_vetter = [home_x[b].text, away_x[b].text]
                        try:
                            if int(date[b].text.split('.')[-1].strip()) >= YEAR and (home_teamx not in team_vetter) and (away_teamx in team_vetter):
                                at_indp_aggregator(b)
                                dsc += 1
                            else:
                                break
                        except ValueError:
                            print(f"Error at Away: {date[b].text} | {home_x[b].text} vs {away_x[b].text}")
                            break
                    if dsc >= DSCRM_H_A:
                        try:
                            at_indp_values = at_indp_prob_calc()
                            at_indp_appender(prb_HW_A_indp=at_indp_values[0], prb_AW_A_indp=at_indp_values[1], prb_GG_A_indp=at_indp_values[2], prb_1_5_A_indp=at_indp_values[3],
                                             prb_2_5_A_indp=at_indp_values[4], prb_12_A_indp=at_indp_values[5])
                        except ZeroDivisionError:
                            at_indp_appender(prb_HW_A_indp=0.01, prb_AW_A_indp=0.01, prb_GG_A_indp=0.01, prb_1_5_A_indp=0.01, prb_2_5_A_indp=0.01, prb_12_A_indp=0.01)
                    else:
                        at_indp_appender(prb_HW_A_indp=0.01, prb_AW_A_indp=0.01, prb_GG_A_indp=0.01, prb_1_5_A_indp=0.01, prb_2_5_A_indp=0.01, prb_12_A_indp=0.01)
                else:
                    at_indp_appender(prb_HW_A_indp=0.01, prb_AW_A_indp=0.01, prb_GG_A_indp=0.01, prb_1_5_A_indp=0.01, prb_2_5_A_indp=0.01, prb_12_A_indp=0.01)
            except ElementNotInteractableException:
                at_indp_appender(prb_HW_A_indp=0.01, prb_AW_A_indp=0.01, prb_GG_A_indp=0.01, prb_1_5_A_indp=0.01, prb_2_5_A_indp=0.01, prb_12_A_indp=0.01)
            sleep(0.1)
            try:
                sub3 = driver.find_elements(By.CSS_SELECTOR, '.section:last-child .h2h__row')
                if len(sub3) > 2:
                    dsc = 0
                    for c in range(len(sub3)):
                        date = driver.find_elements(By.CSS_SELECTOR, '.section:last-child .h2h__row .h2h__date')
                        home_x = driver.find_elements(By.CSS_SELECTOR, '.section:last-child .h2h__row .h2h__homeParticipant .h2h__participantInner')
                        away_x = driver.find_elements(By.CSS_SELECTOR, '.section:last-child .h2h__row .h2h__awayParticipant .h2h__participantInner')
                        home_score = driver.find_elements(By.CSS_SELECTOR, '.section:last-child .h2h__row .h2h__result span:first-child')
                        away_score = driver.find_elements(By.CSS_SELECTOR, '.section:last-child .h2h__row .h2h__result span:last-child')
                        try:
                            if int(date[c].text.split('.')[-1].strip()) >= YEAR:
                                h2h_aggregator(c)
                                dsc += 1
                            else:
                                break
                        except ValueError:
                            print(f"Value Error at H2H: {date[c].text} | {home_x[c].text} vs {away_x[c].text}")
                            break
                    if dsc >= DSCRM_BT:
                        try:
                            h2h_values = h2h_prob_calc()
                            h2h_appender(prb_HW=h2h_values[0], prb_AW=h2h_values[1], prb_GG=h2h_values[2], prb_1_5=h2h_values[3],
                                         prb_2_5=h2h_values[4], prb_12=h2h_values[5])
                        except ZeroDivisionError:
                            h2h_appender(prb_HW=0.01, prb_AW=0.01, prb_GG=0.01, prb_1_5=0.01, prb_2_5=0.01, prb_12=0.01)
                    else:
                        h2h_appender(prb_HW=0.01, prb_AW=0.01, prb_GG=0.01, prb_1_5=0.01, prb_2_5=0.01, prb_12=0.01)
                else:
                    h2h_appender(prb_HW=0.01, prb_AW=0.01, prb_GG=0.01, prb_1_5=0.01, prb_2_5=0.01, prb_12=0.01)
            except ElementNotInteractableException:
                h2h_appender(prb_HW=0.01, prb_AW=0.01, prb_GG=0.01, prb_1_5=0.01, prb_2_5=0.01, prb_12=0.01)
            driver.close()
            driver.switch_to.window(window_before)
            try:
                match_times.append(match_timez[i].text)
            except NoSuchElementException:
                pass
            append_zeroes()
        except NoSuchElementException:
            print("No Internet")
            break
        except IndexError:
            print("IXX")
            break
        except StaleElementReferenceException:
            print("stale")
            break
        except UnexpectedAlertPresentException:
            print("UEAPE")
            break
        except WebDriverException:
            print("Webb")
            break
        except NoSuchWindowException:
            print("NoWind")
            break
    except IndexError:
        pass
        print("IXX")
        break
    except StaleElementReferenceException:
        print("stale")
        break
    except UnexpectedAlertPresentException:
        print("UEAPE")
        break
    except WebDriverException:
        print("Webb")
        break
    except NoSuchWindowException:
        print("NoWind")
        break

for CONFINTVL in CONFINTVLS:
    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = 0.5 * (rdm.random() + ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO)))))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = 0.5 * (rdm.random() + ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO)))))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = 0.5 * (rdm.random() + ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG)))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = 0.5 * (rdm.random() + ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5)))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = 0.5 * (rdm.random() + ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5)))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = 0.5 * (rdm.random() + ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12)))))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(9):
                with open(f"../RESULTS - AVERAGE RANDOMIZED/FLASHAVRAND_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")

        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                                with open("../RESULTS - AVERAGE RANDOMIZED/FLASHAVRAND_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                    with open("../RESULTS - AVERAGE RANDOMIZED/FLASHAVRAND_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                            with open("../RESULTS - AVERAGE RANDOMIZED/FLASHAVRAND_BAYESIAN2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                    with open("../RESULTS - AVERAGE RANDOMIZED/FLASHAVRAND_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 and a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                with open("../RESULTS - AVERAGE RANDOMIZED/FLASHAVRAND_BAYESIAN4.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if 0 <= int(match_times[q].split(':')[0].strip()) <= 6:
                                with open("../RESULTS - AVERAGE RANDOMIZED/FLASHAVRAND_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if 6 < int(match_times[q].split(':')[0].strip()) <= 12:
                                with open("../RESULTS - AVERAGE RANDOMIZED/FLASHAVRAND_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if 12 < int(match_times[q].split(':')[0].strip()) <= 18:
                                with open("../RESULTS - AVERAGE RANDOMIZED/FLASHAVRAND_BAYESIAN7.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if 18 < int(match_times[q].split(':')[0].strip()) <= 23:
                                with open("../RESULTS - AVERAGE RANDOMIZED/FLASHAVRAND_BAYESIAN8.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(9):
        with open(f"../RESULTS - AVERAGE RANDOMIZED/FLASHAVRAND_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = (prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO)))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = (prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO)))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = (prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG)))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = (prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5)))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = (prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5)))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = (prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12)))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(12):
                with open(f"../RESULTS - NORMAL ANALYSIS/FLASHSCORE_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            with open("../RESULTS - NORMAL ANALYSIS/FLASHSCORE_BAYESIAN0.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                with open("../RESULTS - NORMAL ANALYSIS/FLASHSCORE_BAYESIAN1.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        with open("../RESULTS - NORMAL ANALYSIS/FLASHSCORE_BAYESIAN2.txt", mode="a") as file:
                            file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                       f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                       f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                       f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                       f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                with open("../RESULTS - NORMAL ANALYSIS/FLASHSCORE_BAYESIAN3.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                            with open("../RESULTS - NORMAL ANALYSIS/FLASHSCORE_BAYESIAN4.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    with open("../RESULTS - NORMAL ANALYSIS/FLASHSCORE_BAYESIAN5.txt", mode="a") as file:
                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            with open("../RESULTS - NORMAL ANALYSIS/FLASHSCORE_BAYESIAN6.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 0 <= int(match_times[q].split(':')[0].strip()) <= 6:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            with open("../RESULTS - NORMAL ANALYSIS/FLASHSCORE_BAYESIAN7.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 6 < int(match_times[q].split(':')[0].strip()) <= 12:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            with open("../RESULTS - NORMAL ANALYSIS/FLASHSCORE_BAYESIAN8.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 12 < int(match_times[q].split(':')[0].strip()) <= 18:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            with open("../RESULTS - NORMAL ANALYSIS/FLASHSCORE_BAYESIAN9.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 18 < int(match_times[q].split(':')[0].strip()) <= 23:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            with open("../RESULTS - NORMAL ANALYSIS/FLASHSCORE_BAYESIAN10.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            with open("../RESULTS - NORMAL ANALYSIS/FLASHSCORE_BAYESIAN11.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")

        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(12):
        with open(f"../RESULTS - NORMAL ANALYSIS/FLASHSCORE_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    with open("../LISTS - NORMAL ANALYSIS/FLASHSCORE_LISTS.txt", mode="a") as file:
        try:
            file.write(f"Countries = {countries}\nLeagues = {leagues}\nHome_Teams = {home_teams}\n"
                       f"Home_Positions = {home_positions}\nHome Points = {home_points}\n"
                       f"Home_No_Matches_Played = {home_nums_matches_played}\nAway_Teams = {away_teams}\n"
                       f"Away_Positions = {away_positions}\nAway_Points = {away_points}\n"
                       f"Away_No_Matches Played = {away_nums_matches_played}\nMatch_Times = {match_times}\n"
                       f"Home_W_Form = {h_form_W}\nHome_D_Form = {h_form_D}\nHome_L_Form = {h_form_L}\n"
                       f"Away_W_Form = {a_form_W}\nAway_D_Form = {a_form_D}\nAway_L_Form = {a_form_L}\n"
                       f"Prob_GGs = {prob_GGs}\nProb_1_5s = {prob_1_5s}\nProb_2_5s = {prob_2_5s}\n"
                       f"Prob_12s = {prob_12s}\nProb_HWs = {prob_HWs}\nProb_AWs = {prob_AWs}\n"
                       f"Prob_GG_H_indps = {prob_GG_H_indps}\nProb_1_5_H_indps = {prob_1_5_H_indps}\n"
                       f"Prob_2_5_H_indps = {prob_2_5_H_indps}\nProb_12_H_indps = {prob_12_H_indps}\n"
                       f"Prob_HW_H_indps = {prob_HW_H_indps}\nProb_AW_H_indps = {prob_AW_H_indps}\n"
                       f"Prob_GG_A_indps = {prob_GG_A_indps}\nProb_1_5_A_indps = {prob_1_5_A_indps}\n"
                       f"Prob_2_5_A_indps = {prob_2_5_A_indps}\nProb_12_A_indps = {prob_12_A_indps}\n"
                       f"Prob_HW_A_indps = {prob_HW_A_indps}\nProb_AW_A_indps = {prob_AW_A_indps}\n"
                       f"Bayesian_Home_Win = {bayesian_home_Win_d}\nBayesian_Away_Win = {bayesian_away_Win_d}\n"
                       f"Bayesian_GG = {bayesian_GG_d}\nBayesian_1_5 = {bayesian_1_5_d}\nBayesian_2_5 = {bayesian_2_5_d}\n"
                       f"Bayesian_12 = {bayesian_12_d }\n")
        except UnicodeError:
            pass
    print_all_data()

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = rdm.random() * ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO))))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = rdm.random() * ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO))))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = rdm.random() * ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = rdm.random() * ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = rdm.random() * ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = rdm.random() * ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12))))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(9):
                with open(f"../RESULTS - PRODUCT RANDOMIZED/FLASHPRAND_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                with open("../RESULTS - PRODUCT RANDOMIZED/FLASHPRAND_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                    with open("../RESULTS - PRODUCT RANDOMIZED/FLASHPRAND_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        with open("../RESULTS - PRODUCT RANDOMIZED/FLASHPRAND_BAYESIAN2.txt", mode="a") as file:
                            file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                       f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                       f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                       f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                       f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                    with open("../RESULTS - PRODUCT RANDOMIZED/FLASHPRAND_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                        if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                            with open("../RESULTS - PRODUCT RANDOMIZED/FLASHPRAND_BAYESIAN4.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if 0 <= int(match_times[q].split(':')[0].strip()) <= 6:
                            with open("../RESULTS - PRODUCT RANDOMIZED/FLASHPRAND_BAYESIAN5.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if 6 < int(match_times[q].split(':')[0].strip()) <= 12:
                            with open("../RESULTS - PRODUCT RANDOMIZED/FLASHPRAND_BAYESIAN6.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if 12 < int(match_times[q].split(':')[0].strip()) <= 18:
                            with open("../RESULTS - PRODUCT RANDOMIZED/FLASHPRAND_BAYESIAN7.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if 18 < int(match_times[q].split(':')[0].strip()) <= 23:
                            with open("../RESULTS - PRODUCT RANDOMIZED/FLASHPRAND_BAYESIAN8.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(9):
        with open(f"../RESULTS - PRODUCT RANDOMIZED/FLASHPRAND_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = math.sqrt(0.5 * (rdm.random() + ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO))))))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = math.sqrt(0.5 * (rdm.random() + ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO))))))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = math.sqrt(0.5 * (rdm.random() + ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG))))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = math.sqrt(0.5 * (rdm.random() + ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5))))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = math.sqrt(0.5 * (rdm.random() + ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5))))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = math.sqrt(0.5 * (rdm.random() + ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12))))))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(9):
                with open(f"../RESULTS - SQRT AVERAGE RANDOMIZED/FLASHSQAVRAND_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")

        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                with open("../RESULTS - SQRT AVERAGE RANDOMIZED/FLASHSQAVRAND_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                    with open("../RESULTS - SQRT AVERAGE RANDOMIZED/FLASHSQAVRAND_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        with open("../RESULTS - SQRT AVERAGE RANDOMIZED/FLASHSQAVRAND_BAYESIAN2.txt", mode="a") as file:
                            file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                       f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                       f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                       f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                       f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                    with open("../RESULTS - SQRT AVERAGE RANDOMIZED/FLASHSQAVRAND_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                                with open("../RESULTS - SQRT AVERAGE RANDOMIZED/FLASHSQAVRAND_BAYESIAN4.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if 0 <= int(match_times[q].split(':')[0].strip()) <= 6:
                                with open("../RESULTS - SQRT AVERAGE RANDOMIZED/FLASHSQAVRAND_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if 6 < int(match_times[q].split(':')[0].strip()) <= 12:
                                with open("../RESULTS - SQRT AVERAGE RANDOMIZED/FLASHSQAVRAND_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if 12 < int(match_times[q].split(':')[0].strip()) <= 18:
                            if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                                with open("../RESULTS - SQRT AVERAGE RANDOMIZED/FLASHSQAVRAND_BAYESIAN7.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if 18 < int(match_times[q].split(':')[0].strip()) <= 23:
                            if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                                with open("../RESULTS - SQRT AVERAGE RANDOMIZED/FLASHSQAVRAND_BAYESIAN8.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")

        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(9):
        with open(f"../RESULTS - SQRT AVERAGE RANDOMIZED/FLASHSQAVRAND_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    print_all_data()

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = math.sqrt(rdm.random() * ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO)))))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = math.sqrt(rdm.random() * ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO)))))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = math.sqrt(rdm.random() * ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG)))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = math.sqrt(rdm.random() * ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5)))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = math.sqrt(rdm.random() * ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5)))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = math.sqrt(rdm.random() * ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12)))))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(9):
                with open(f"../RESULTS - SQRT PRODUCT RANDOMIZED/FLASHSQRAND_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                with open("../RESULTS - SQRT PRODUCT RANDOMIZED/FLASHSQRAND_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                    with open("../RESULTS - SQRT PRODUCT RANDOMIZED/FLASHSQRAND_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        with open("../RESULTS - SQRT PRODUCT RANDOMIZED/FLASHSQRAND_BAYESIAN2.txt", mode="a") as file:
                            file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                       f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                       f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                       f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                       f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                    with open("../RESULTS - SQRT PRODUCT RANDOMIZED/FLASHSQRAND_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                                with open("../RESULTS - SQRT PRODUCT RANDOMIZED/FLASHSQRAND_BAYESIAN4.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if 0 <= int(match_times[q].split(':')[0].strip()) <= 6:
                            if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                                with open("../RESULTS - SQRT PRODUCT RANDOMIZED/FLASHSQRAND_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if 6 < int(match_times[q].split(':')[0].strip()) <= 12:
                            if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                                with open("../RESULTS - SQRT PRODUCT RANDOMIZED/FLASHSQRAND_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if 12 < int(match_times[q].split(':')[0].strip()) <= 18:
                            if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                                with open("../RESULTS - SQRT PRODUCT RANDOMIZED/FLASHSQRAND_BAYESIAN7.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if 18 < int(match_times[q].split(':')[0].strip()) <= 23:
                            if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                                with open("../RESULTS - SQRT PRODUCT RANDOMIZED/FLASHSQRAND_BAYESIAN8.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(9):
        with open(f"../RESULTS - SQRT PRODUCT RANDOMIZED/FLASHSQRAND_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    ########################################################################################################################

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = 0.5 * (home_z_prob[q] + ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO)))))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = 0.5 * (away_z_prob[q] + ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO)))))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = 0.5 * (diff_z_prob[q] + ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG)))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = 0.5 * (diff_z_prob[q] + ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5)))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = 0.5 * (diff_z_prob[q] + ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5)))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = 0.5 * (diff_z_prob[q] + ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12)))))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(10):
                with open(f"../RESULTS - AVERAGE ZSCORED/ZFLASHAVRG_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - AVERAGE ZSCORED/ZFLASHAVRG_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - AVERAGE ZSCORED/ZFLASHAVRG_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - AVERAGE ZSCORED/ZFLASHAVRG_BAYESIAN2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - AVERAGE ZSCORED/ZFLASHAVRG_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - AVERAGE ZSCORED/ZFLASHAVRG_BAYESIAN4.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if 0 <= int(match_times[q].split(':')[0].strip()) <= 6:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - AVERAGE ZSCORED/ZFLASHAVRG_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if 6 < int(match_times[q].split(':')[0].strip()) <= 12:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - AVERAGE ZSCORED/ZFLASHAVRG_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if 12 < int(match_times[q].split(':')[0].strip()) <= 18:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - AVERAGE ZSCORED/ZFLASHAVRG_BAYESIAN7.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if 18 < int(match_times[q].split(':')[0].strip()) <= 23:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - AVERAGE ZSCORED/ZFLASHAVRG_BAYESIAN8.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - AVERAGE ZSCORED/ZFLASHAVRG_BAYESIAN9.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(10):
        with open(f"../RESULTS - AVERAGE ZSCORED/ZFLASHAVRG_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = home_z_prob[q] * ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO))))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = away_z_prob[q] * ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO))))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = diff_z_prob[q] * ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = diff_z_prob[q] * ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = diff_z_prob[q] * ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = diff_z_prob[q] * ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12))))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(10):
                with open(f"../RESULTS - PRODUCT ZSCORED/ZFLASHPROD_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")

        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - PRODUCT ZSCORED/ZFLASHPROD_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - PRODUCT ZSCORED/ZFLASHPROD_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - PRODUCT ZSCORED/ZFLASHPROD_BAYESIAN2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - PRODUCT ZSCORED/ZFLASHPROD_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - PRODUCT ZSCORED/ZFLASHPROD_BAYESIAN4.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 0 <= int(match_times[q].split(':')[0].strip()) <= 6:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - PRODUCT ZSCORED/ZFLASHPROD_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 6 < int(match_times[q].split(':')[0].strip()) <= 12:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - PRODUCT ZSCORED/ZFLASHPROD_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 12 < int(match_times[q].split(':')[0].strip()) <= 18:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - PRODUCT ZSCORED/ZFLASHPROD_BAYESIAN7.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 18 < int(match_times[q].split(':')[0].strip()) <= 23:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - PRODUCT ZSCORED/ZFLASHPROD_BAYESIAN8.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                        with open("../RESULTS - PRODUCT ZSCORED/ZFLASHPROD_BAYESIAN9.txt", mode="a") as file:
                            file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                       f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                       f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                       f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                       f"{bayesian_12_d[q]}|{match_times[q]}\n")
        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(10):
        with open(f"../RESULTS - PRODUCT ZSCORED/ZFLASHPROD_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = math.sqrt(0.5 * (home_z_prob[q] + ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO))))))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = math.sqrt(0.5 * (away_z_prob[q] + ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO))))))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = math.sqrt(0.5 * (diff_z_prob[q] + ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG))))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = math.sqrt(0.5 * (diff_z_prob[q] + ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5))))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = math.sqrt(0.5 * (diff_z_prob[q] + ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5))))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = math.sqrt(0.5 * (diff_z_prob[q] + ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12))))))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(10):
                with open(f"../RESULTS - SQRT AVERAGE ZSCORED/ZFLASHSQAVRG_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT AVERAGE ZSCORED/ZFLASHSQAVRG_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - SQRT AVERAGE ZSCORED/ZFLASHSQAVRG_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - SQRT AVERAGE ZSCORED/ZFLASHSQAVRG_BAYESIAN2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - SQRT AVERAGE ZSCORED/ZFLASHSQAVRG_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT AVERAGE ZSCORED/ZFLASHSQAVRG_BAYESIAN4.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if 0 <= int(match_times[q].split(':')[0].strip()) <= 6:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT AVERAGE ZSCORED/ZFLASHSQAVRG_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if 6 < int(match_times[q].split(':')[0].strip()) <= 12:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT AVERAGE ZSCORED/ZFLASHSQAVRG_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if 12 < int(match_times[q].split(':')[0].strip()) <= 18:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT AVERAGE ZSCORED/ZFLASHSQAVRG_BAYESIAN7.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 18 < int(match_times[q].split(':')[0].strip()) <= 23:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT AVERAGE ZSCORED/ZFLASHSQAVRG_BAYESIAN8.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                        with open("../RESULTS - SQRT AVERAGE ZSCORED/ZFLASHSQAVRG_BAYESIAN9.txt", mode="a") as file:
                            file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                       f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                       f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                       f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                       f"{bayesian_12_d[q]}|{match_times[q]}\n")

        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(10):
        with open(f"../RESULTS - SQRT AVERAGE ZSCORED/ZFLASHSQAVRG_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = math.sqrt(home_z_prob[q] * ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO)))))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = math.sqrt(away_z_prob[q] * ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO)))))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = math.sqrt(diff_z_prob[q] * ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG)))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = math.sqrt(diff_z_prob[q] * ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5)))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = math.sqrt(diff_z_prob[q] * ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5)))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = math.sqrt(diff_z_prob[q] * ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12)))))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(10):
                with open(f"../RESULTS - SQRT PRODUCT ZSCORED/ZFLASHSQPROD_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT PRODUCT ZSCORED/ZFLASHSQPROD_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - SQRT PRODUCT ZSCORED/ZFLASHSQPROD_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - SQRT PRODUCT ZSCORED/ZFLASHSQPROD_BAYESIAN2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - SQRT PRODUCT ZSCORED/ZFLASHSQPROD_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - SQRT PRODUCT ZSCORED/ZFLASHSQPROD_BAYESIAN4.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 0 <= int(match_times[q].split(':')[0].strip()) <= 6:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT PRODUCT ZSCORED/ZFLASHSQPROD_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 6 < int(match_times[q].split(':')[0].strip()) <= 12:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT PRODUCT ZSCORED/ZFLASHSQPROD_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 12 < int(match_times[q].split(':')[0].strip()) <= 18:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT PRODUCT ZSCORED/ZFLASHSQPROD_BAYESIAN7.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 18 < int(match_times[q].split(':')[0].strip()) <= 23:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT PRODUCT ZSCORED/ZFLASHSQPROD_BAYESIAN8.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                        with open("../RESULTS - SQRT PRODUCT ZSCORED/ZFLASHSQPROD_BAYESIAN9.txt", mode="a") as file:
                            file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                       f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                       f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                       f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                       f"{bayesian_12_d[q]}|{match_times[q]}\n")
        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(10):
        with open(f"../RESULTS - SQRT PRODUCT ZSCORED/ZFLASHSQPROD_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        bayesian_home_Win = home_z_prob[q]
        bayesian_away_Win = away_z_prob[q]
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = diff_z_prob[q] * ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = diff_z_prob[q] * ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = diff_z_prob[q] * ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = diff_z_prob[q] * ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12))))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(22):
                with open(f"../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN0.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN4.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN5.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 0 <= int(match_times[q].split(':')[0].strip()) <= 3:
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN7.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 3 < int(match_times[q].split(':')[0].strip()) <= 6:
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN8.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 6 < int(match_times[q].split(':')[0].strip()) <= 9:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN9.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 9 < int(match_times[q].split(':')[0].strip()) <= 12:
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN10.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if bayesian_home_Win_d[q] > bayesian_away_Win_d[q] and home_positions[q] < away_positions[q] and abs(home_positions[q] - away_positions[q]) >= POS_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN11.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 12 < int(match_times[q].split(':')[0].strip()) <= 15:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN12.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 15 < int(match_times[q].split(':')[0].strip()) <= 18:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN13.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 18 < int(match_times[q].split(':')[0].strip()) <= 21:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN14.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 21 < int(match_times[q].split(':')[0].strip()) <= 23:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN15.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN16.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF and abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                        if h_form_W[q] == 1 or a_form_W[q] == 1:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN17.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if bayesian_home_Win_d[q] < bayesian_away_Win_d[q] and home_positions[q] > away_positions[q] and abs(home_positions[q] - away_positions[q]) >= POS_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN18.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF and abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN19.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF and abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if h_form_L[q] == 0 or a_form_L[q] == 0:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN20.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF and abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN21.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")

        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(22):
        with open(f"../RESULTS - NORMAL ZSCORED/ZFLASHSCORE_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    ###################################################################################################################
    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = (1 / 3) * (home_z_prob[q] + rdm.random() + ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO)))))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = (1 / 3) * (away_z_prob[q] + rdm.random() + ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO)))))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = (1 / 3) * (diff_z_prob[q] + rdm.random() + ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG)))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = (1 / 3) * (diff_z_prob[q] + rdm.random() + ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5)))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = (1 / 3) * (diff_z_prob[q] + rdm.random() + ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5)))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = (1 / 3) * (diff_z_prob[q] + rdm.random() + ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12)))))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(10):
                with open(f"../RESULTS - AVERAGE ZRANDSCORED/ZRANDFLASHAVRAND_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - AVERAGE ZRANDSCORED/ZRANDFLASHAVRAND_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - AVERAGE ZRANDSCORED/ZRANDFLASHAVRAND_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - AVERAGE ZRANDSCORED/ZRANDFLASHAVRAND_BAYESIAN2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - AVERAGE ZRANDSCORED/ZRANDFLASHAVRAND_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - AVERAGE ZRANDSCORED/ZRANDFLASHAVRAND_BAYESIAN4.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if 0 <= int(match_times[q].split(':')[0].strip()) <= 6:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - AVERAGE ZRANDSCORED/ZRANDFLASHAVRAND_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if 6 < int(match_times[q].split(':')[0].strip()) <= 12:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - AVERAGE ZRANDSCORED/ZRANDFLASHAVRAND_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 12 < int(match_times[q].split(':')[0].strip()) <= 18:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - AVERAGE ZRANDSCORED/ZRANDFLASHAVRAND_BAYESIAN7.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if 18 < int(match_times[q].split(':')[0].strip()) <= 23:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - AVERAGE ZRANDSCORED/ZRANDFLASHAVRAND_BAYESIAN8.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            with open("../RESULTS - AVERAGE ZRANDSCORED/ZRANDFLASHAVRAND_BAYESIAN9.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(10):
        with open(f"../RESULTS - AVERAGE ZRANDSCORED/ZRANDFLASHAVRAND_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = home_z_prob[q] * rdm.random() * ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO))))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = away_z_prob[q] * rdm.random() * ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO))))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = diff_z_prob[q] * rdm.random() * ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = diff_z_prob[q] * rdm.random() * ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = diff_z_prob[q] * rdm.random() * ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = diff_z_prob[q] * rdm.random() * ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12))))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(10):
                with open(f"../RESULTS - PRODUCT ZRANDSCORED/ZRANDFLASHPRAND_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - PRODUCT ZRANDSCORED/ZRANDFLASHPRAND_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - PRODUCT ZRANDSCORED/ZRANDFLASHPRAND_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - PRODUCT ZRANDSCORED/ZRANDFLASHPRAND_BAYESIAN2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - PRODUCT ZRANDSCORED/ZRANDFLASHPRAND_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - PRODUCT ZRANDSCORED/ZRANDFLASHPRAND_BAYESIAN4.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if 0 <= int(match_times[q].split(':')[0].strip()) <= 6:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - PRODUCT ZRANDSCORED/ZRANDFLASHPRAND_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if 6 < int(match_times[q].split(':')[0].strip()) <= 12:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - PRODUCT ZRANDSCORED/ZRANDFLASHPRAND_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 12 < int(match_times[q].split(':')[0].strip()) <= 18:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - PRODUCT ZRANDSCORED/ZRANDFLASHPRAND_BAYESIAN7.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if 18 < int(match_times[q].split(':')[0].strip()) <= 23:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - PRODUCT ZRANDSCORED/ZRANDFLASHPRAND_BAYESIAN8.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            with open("../RESULTS - PRODUCT ZRANDSCORED/ZRANDFLASHPRAND_BAYESIAN9.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(10):
        with open(f"../RESULTS - PRODUCT ZRANDSCORED/ZRANDFLASHPRAND_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = np.cbrt((1 / 3) * (home_z_prob[q] + rdm.random() + ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO))))))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = np.cbrt((1 / 3) * (away_z_prob[q] + rdm.random() + ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO))))))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = np.cbrt((1 / 3) * (diff_z_prob[q] + rdm.random() + ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG))))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = np.cbrt((1 / 3) * (diff_z_prob[q] + rdm.random() + ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5))))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = np.cbrt((1 / 3) * (diff_z_prob[q] + rdm.random() + ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5))))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = np.cbrt((1 / 3) * (diff_z_prob[q] + rdm.random() + ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12))))))

        bayesian_home_Win_d.append(round((float(bayesian_home_Win)), 4))
        bayesian_away_Win_d.append(round((float(bayesian_away_Win)), 4))
        bayesian_GG_d.append(round((float(bayesian_GG)), 4))
        bayesian_1_5_d.append(round((float(bayesian_1_5)), 4))
        bayesian_2_5_d.append(round((float(bayesian_2_5)), 4))
        bayesian_12_d.append(round((float(bayesian_12)), 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(10):
                with open(f"../RESULTS - CBRT AVERAGE ZRANDSCORED/ZRANDFLASHCBRAVRAND_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT AVERAGE ZRANDSCORED/ZRANDFLASHCBRAVRAND_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - CBRT AVERAGE ZRANDSCORED/ZRANDFLASHCBRAVRAND_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - CBRT AVERAGE ZRANDSCORED/ZRANDFLASHCBRAVRAND_BAYESIAN2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - CBRT AVERAGE ZRANDSCORED/ZRANDFLASHCBRAVRAND_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - CBRT AVERAGE ZRANDSCORED/ZRANDFLASHCBRAVRAND_BAYESIAN4.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 0 <= int(match_times[q].split(':')[0].strip()) <= 6:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT AVERAGE ZRANDSCORED/ZRANDFLASHCBRAVRAND_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 6 < int(match_times[q].split(':')[0].strip()) <= 12:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT AVERAGE ZRANDSCORED/ZRANDFLASHCBRAVRAND_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 12 < int(match_times[q].split(':')[0].strip()) <= 18:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT AVERAGE ZRANDSCORED/ZRANDFLASHCBRAVRAND_BAYESIAN7.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 18 < int(match_times[q].split(':')[0].strip()) <= 23:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT AVERAGE ZRANDSCORED/ZRANDFLASHCBRAVRAND_BAYESIAN8.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            with open("../RESULTS - CBRT AVERAGE ZRANDSCORED/ZRANDFLASHCBRAVRAND_BAYESIAN9.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")

        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(10):
        with open(f"../RESULTS - CBRT AVERAGE ZRANDSCORED/ZRANDFLASHCBRAVRAND_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = np.cbrt(home_z_prob[q] * rdm.random() * ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO)))))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = np.cbrt(away_z_prob[q] * rdm.random() * ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO)))))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = np.cbrt(diff_z_prob[q] * rdm.random() * ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG)))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = np.cbrt(diff_z_prob[q] * rdm.random() * ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5)))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = np.cbrt(diff_z_prob[q] * rdm.random() * ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5)))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = np.cbrt(diff_z_prob[q] * rdm.random() * ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12)))))

        bayesian_home_Win_d.append(round((float(bayesian_home_Win)), 4))
        bayesian_away_Win_d.append(round((float(bayesian_away_Win)), 4))
        bayesian_GG_d.append(round((float(bayesian_GG)), 4))
        bayesian_1_5_d.append(round((float(bayesian_1_5)), 4))
        bayesian_2_5_d.append(round((float(bayesian_2_5)), 4))
        bayesian_12_d.append(round((float(bayesian_12)), 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(10):
                with open(f"../RESULTS - CBRT PRODUCT ZRANDSCORED/ZRANDFLASHCBRAND_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT PRODUCT ZRANDSCORED/ZRANDFLASHCBRAND_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - CBRT PRODUCT ZRANDSCORED/ZRANDFLASHCBRAND_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - CBRT PRODUCT ZRANDSCORED/ZRANDFLASHCBRAND_BAYESIAN2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - CBRT PRODUCT ZRANDSCORED/ZRANDFLASHCBRAND_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - CBRT PRODUCT ZRANDSCORED/ZRANDFLASHCBRAND_BAYESIAN4.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 0 <= int(match_times[q].split(':')[0].strip()) <= 6:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT PRODUCT ZRANDSCORED/ZRANDFLASHCBRAND_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 6 < int(match_times[q].split(':')[0].strip()) <= 12:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT PRODUCT ZRANDSCORED/ZRANDFLASHCBRAND_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 12 < int(match_times[q].split(':')[0].strip()) <= 18:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT PRODUCT ZRANDSCORED/ZRANDFLASHCBRAND_BAYESIAN7.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 18 < int(match_times[q].split(':')[0].strip()) <= 23:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT PRODUCT ZRANDSCORED/ZRANDFLASHCBRAND_BAYESIAN8.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            with open("../RESULTS - CBRT PRODUCT ZRANDSCORED/ZRANDFLASHCBRAND_BAYESIAN9.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(10):
        with open(f"../RESULTS - CBRT PRODUCT ZRANDSCORED/ZRANDFLASHCBRAND_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    print_all_data()

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = home_z_prob[q] * rdm.random()
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = away_z_prob[q] * rdm.random()
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = diff_z_prob[q] * rdm.random()
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = diff_z_prob[q] * rdm.random()
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = diff_z_prob[q] * rdm.random()
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = diff_z_prob[q] * rdm.random()

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(7):
                with open(f"../RESULTS - NORMAL ZRANDSCORED/ZRANDFLASHSCORE_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - NORMAL ZRANDSCORED/ZRANDFLASHSCORE_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if (h_form_D[q] == 0 or a_form_D[q] == 0) and (h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE):
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - NORMAL ZRANDSCORED/ZRANDFLASHSCORE_BAYESIAN1.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            with open("../RESULTS - NORMAL ZRANDSCORED/ZRANDFLASHSCORE_BAYESIAN2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - NORMAL ZRANDSCORED/ZRANDFLASHSCORE_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if 0 <= int(match_times[q].split(':')[0].strip()) <= 12:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - NORMAL ZRANDSCORED/ZRANDFLASHSCORE_BAYESIAN4.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if 12 < int(match_times[q].split(':')[0].strip()) <= 23:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - NORMAL ZRANDSCORED/ZRANDFLASHSCORE_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            with open("../RESULTS - NORMAL ZRANDSCORED/ZRANDFLASHSCORE_BAYESIAN6.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")

        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(7):
        with open(f"../RESULTS - NORMAL ZRANDSCORED/ZRANDFLASHSCORE_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    ########################################################################################################################

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = 0.5 * ((home_z_prob[q] * diff_z_prob[q]) + ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO)))))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = 0.5 * ((away_z_prob[q] * diff_z_prob[q]) + ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO)))))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = 0.5 * (diff_z_prob[q] + ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG)))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = 0.5 * (diff_z_prob[q] + ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5)))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = 0.5 * (diff_z_prob[q] + ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5)))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = 0.5 * (diff_z_prob[q] + ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12)))))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(10):
                with open(f"../RESULTS - AVERAGE DZSCORED/DZFLASHAVG_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - AVERAGE DZSCORED/DZFLASHAVG_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - AVERAGE DZSCORED/DZFLASHAVG_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - AVERAGE DZSCORED/DZFLASHAVG_BAYESIAN2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - AVERAGE DZSCORED/DZFLASHAVG_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - AVERAGE DZSCORED/DZFLASHAVG_BAYESIAN4.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 0 <= int(match_times[q].split(':')[0].strip()) <= 6:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - AVERAGE DZSCORED/DZFLASHAVG_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 6 < int(match_times[q].split(':')[0].strip()) <= 12:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - AVERAGE DZSCORED/DZFLASHAVG_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 12 < int(match_times[q].split(':')[0].strip()) <= 18:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - AVERAGE DZSCORED/DZFLASHAVG_BAYESIAN7.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 18 < int(match_times[q].split(':')[0].strip()) <= 23:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - AVERAGE DZSCORED/DZFLASHAVG_BAYESIAN8.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            with open("../RESULTS - AVERAGE DZSCORED/DZFLASHAVG_BAYESIAN9.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(10):
        with open(f"../RESULTS - AVERAGE DZSCORED/DZFLASHAVG_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = (home_z_prob[q] * diff_z_prob[q]) * ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO))))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = (away_z_prob[q] * diff_z_prob[q]) * ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO))))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = diff_z_prob[q] * ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = diff_z_prob[q] * ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = diff_z_prob[q] * ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = diff_z_prob[q] * ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12))))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(10):
                with open(f"../RESULTS - PRODUCT DZSCORED/DZFLASHPROD_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - PRODUCT DZSCORED/DZFLASHPROD_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - PRODUCT DZSCORED/DZFLASHPROD_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - PRODUCT DZSCORED/DZFLASHPROD_BAYESIAN2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - PRODUCT DZSCORED/DZFLASHPROD_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - PRODUCT DZSCORED/DZFLASHPROD_BAYESIAN4.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 0 <= int(match_times[q].split(':')[0].strip()) <= 6:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - PRODUCT DZSCORED/DZFLASHPROD_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 6 < int(match_times[q].split(':')[0].strip()) <= 12:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - PRODUCT DZSCORED/DZFLASHPROD_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 12 < int(match_times[q].split(':')[0].strip()) <= 18:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - PRODUCT DZSCORED/DZFLASHPROD_BAYESIAN7.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 18 < int(match_times[q].split(':')[0].strip()) <= 23:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - PRODUCT DZSCORED/DZFLASHPROD_BAYESIAN8.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - PRODUCT DZSCORED/DZFLASHPROD_BAYESIAN9.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(10):
        with open(f"../RESULTS - PRODUCT DZSCORED/DZFLASHPROD_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = math.sqrt(0.5 * ((home_z_prob[q] * diff_z_prob[q]) + ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO))))))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = math.sqrt(0.5 * ((away_z_prob[q] * diff_z_prob[q]) + ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO))))))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = math.sqrt(0.5 * (diff_z_prob[q] + ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG))))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = math.sqrt(0.5 * (diff_z_prob[q] + ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5))))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = math.sqrt(0.5 * (diff_z_prob[q] + ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5))))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = math.sqrt(0.5 * (diff_z_prob[q] + ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12))))))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(10):
                with open(f"../RESULTS - SQRT AVERAGE DZSCORED/DZFLASHSQAVG_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT AVERAGE DZSCORED/DZFLASHSQAVG_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - SQRT AVERAGE DZSCORED/DZFLASHSQAVG_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - SQRT AVERAGE DZSCORED/DZFLASHSQAVG_BAYESIAN2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - SQRT AVERAGE DZSCORED/DZFLASHSQAVG_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - SQRT AVERAGE DZSCORED/DZFLASHSQAVG_BAYESIAN4.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 0 <= int(match_times[q].split(':')[0].strip()) <= 6:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT AVERAGE DZSCORED/DZFLASHSQAVG_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 6 < int(match_times[q].split(':')[0].strip()) <= 12:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT AVERAGE DZSCORED/DZFLASHSQAVG_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 12 < int(match_times[q].split(':')[0].strip()) <= 18:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT AVERAGE DZSCORED/DZFLASHSQAVG_BAYESIAN7.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 18 < int(match_times[q].split(':')[0].strip()) <= 23:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT AVERAGE DZSCORED/DZFLASHSQAVG_BAYESIAN8.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT AVERAGE DZSCORED/DZFLASHSQAVG_BAYESIAN9.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(10):
        with open(f"../RESULTS - SQRT AVERAGE DZSCORED/DZFLASHSQAVG_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = math.sqrt((home_z_prob[q] * diff_z_prob[q]) * ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO)))))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = math.sqrt((away_z_prob[q] * diff_z_prob[q]) * ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO)))))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = math.sqrt(diff_z_prob[q] * ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG)))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = math.sqrt(diff_z_prob[q] * ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5)))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = math.sqrt(diff_z_prob[q] * ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5)))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = math.sqrt(diff_z_prob[q] * ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12)))))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(10):
                with open(f"../RESULTS - SQRT PRODUCT DZSCORED/DZFLASHSQPROD_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT PRODUCT DZSCORED/DZFLASHSQPROD_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - SQRT PRODUCT DZSCORED/DZFLASHSQPROD_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - SQRT PRODUCT DZSCORED/DZFLASHSQPROD_BAYESIAN2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - SQRT PRODUCT DZSCORED/DZFLASHSQPROD_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - SQRT PRODUCT DZSCORED/DZFLASHSQPROD_BAYESIAN4.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 0 <= int(match_times[q].split(':')[0].strip()) <= 6:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT PRODUCT DZSCORED/DZFLASHSQPROD_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 6 < int(match_times[q].split(':')[0].strip()) <= 12:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT PRODUCT DZSCORED/DZFLASHSQPROD_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 12 < int(match_times[q].split(':')[0].strip()) <= 18:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT PRODUCT DZSCORED/DZFLASHSQPROD_BAYESIAN7.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 18 < int(match_times[q].split(':')[0].strip()) <= 23:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - SQRT PRODUCT DZSCORED/DZFLASHSQPROD_BAYESIAN8.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            with open("../RESULTS - SQRT PRODUCT DZSCORED/DZFLASHSQPROD_BAYESIAN9.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(10):
        with open(f"../RESULTS - SQRT PRODUCT DZSCORED/DZFLASHSQPROD_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        bayesian_home_Win = (home_z_prob[q] * diff_z_prob[q])
        bayesian_away_Win = (away_z_prob[q] * diff_z_prob[q])
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = diff_z_prob[q] * ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = diff_z_prob[q] * ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = diff_z_prob[q] * ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = diff_z_prob[q] * ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12))))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(8):
                with open(f"../RESULTS - NORMAL DZSCORED/DZFLASHSCORE_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - NORMAL DZSCORED/DZFLASHSCORE_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - NORMAL DZSCORED/DZFLASHSCORE_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - NORMAL DZSCORED/DZFLASHSCORE_BAYESIAN2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - NORMAL DZSCORED/DZFLASHSCORE_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if 0 <= int(match_times[q].split(':')[0].strip()) <= 12:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - NORMAL DZSCORED/DZFLASHSCORE_BAYESIAN4.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 12 < int(match_times[q].split(':')[0].strip()) <= 23:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - NORMAL DZSCORED/DZFLASHSCORE_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - NORMAL DZSCORED/DZFLASHSCORE_BAYESIAN6.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            with open("../RESULTS - NORMAL DZSCORED/DZFLASHSCORE_BAYESIAN7.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")

        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(8):
        with open(f"../RESULTS - NORMAL DZSCORED/DZFLASHSCORE_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    ########################################################################################################################

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = (1 / 3) * ((home_z_prob[q] * diff_z_prob[q]) + rdm.random() + ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO)))))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = (1 / 3) * ((away_z_prob[q] * diff_z_prob[q]) + rdm.random() + ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO)))))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = (1 / 3) * (diff_z_prob[q] + rdm.random() + ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG)))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = (1 / 3) * (diff_z_prob[q] + rdm.random() + ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5)))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = (1 / 3) * (diff_z_prob[q] + rdm.random() + ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5)))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = (1 / 3) * (diff_z_prob[q] + rdm.random() + ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12)))))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(10):
                with open(f"../RESULTS - AVERAGE DZRANDSCORED/DZRANDFLASHAVRAND_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - AVERAGE DZRANDSCORED/DZRANDFLASHAVRAND_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - AVERAGE DZRANDSCORED/DZRANDFLASHAVRAND_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - AVERAGE DZRANDSCORED/DZRANDFLASHAVRAND_BAYESIAN2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - AVERAGE DZRANDSCORED/DZRANDFLASHAVRAND_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - AVERAGE DZRANDSCORED/DZRANDFLASHAVRAND_BAYESIAN4.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if 0 <= int(match_times[q].split(':')[0].strip()) <= 6:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - AVERAGE DZRANDSCORED/DZRANDFLASHAVRAND_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if 6 < int(match_times[q].split(':')[0].strip()) <= 12:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - AVERAGE DZRANDSCORED/DZRANDFLASHAVRAND_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 12 < int(match_times[q].split(':')[0].strip()) <= 18:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - AVERAGE DZRANDSCORED/DZRANDFLASHAVRAND_BAYESIAN7.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if 18 < int(match_times[q].split(':')[0].strip()) <= 23:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - AVERAGE DZRANDSCORED/DZRANDFLASHAVRAND_BAYESIAN8.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            with open("../RESULTS - AVERAGE DZRANDSCORED/DZRANDFLASHAVRAND_BAYESIAN9.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(10):
        with open(f"../RESULTS - AVERAGE DZRANDSCORED/DZRANDFLASHAVRAND_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = (home_z_prob[q] * diff_z_prob[q]) * rdm.random() * ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO))))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = (away_z_prob[q] * diff_z_prob[q]) * rdm.random() * ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO))))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = diff_z_prob[q] * rdm.random() * ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = diff_z_prob[q] * rdm.random() * ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = diff_z_prob[q] * rdm.random() * ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = diff_z_prob[q] * rdm.random() * ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12))))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(9):
                with open(f"../RESULTS - PRODUCT DZRANDSCORED/DZRANDFLASHPRAND_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - PRODUCT DZRANDSCORED/DZRANDFLASHPRAND_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                    with open("../RESULTS - PRODUCT DZRANDSCORED/DZRANDFLASHPRAND_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            with open("../RESULTS - PRODUCT DZRANDSCORED/DZRANDFLASHPRAND_BAYESIAN2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                    with open("../RESULTS - PRODUCT DZRANDSCORED/DZRANDFLASHPRAND_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            with open("../RESULTS - PRODUCT DZRANDSCORED/DZRANDFLASHPRAND_BAYESIAN4.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if 0 <= int(match_times[q].split(':')[0].strip()) <= 8:
                            if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                                with open("../RESULTS - PRODUCT DZRANDSCORED/DZRANDFLASHPRAND_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if 8 < int(match_times[q].split(':')[0].strip()) <= 16:
                            if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                                with open("../RESULTS - PRODUCT DZRANDSCORED/DZRANDFLASHPRAND_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if 16 < int(match_times[q].split(':')[0].strip()) <= 23:
                            if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                                with open("../RESULTS - PRODUCT DZRANDSCORED/DZRANDFLASHPRAND_BAYESIAN7.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            with open("../RESULTS - PRODUCT DZRANDSCORED/DZRANDFLASHPRAND_BAYESIAN8.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(9):
        with open(f"../RESULTS - PRODUCT DZRANDSCORED/DZRANDFLASHPRAND_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = np.cbrt((1 / 3) * ((home_z_prob[q] * diff_z_prob[q]) + rdm.random() + ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO))))))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = np.cbrt((1 / 3) * ((away_z_prob[q] * diff_z_prob[q]) + rdm.random() + ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO))))))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = np.cbrt((1 / 3) * (diff_z_prob[q] + rdm.random() + ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG))))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = np.cbrt((1 / 3) * (diff_z_prob[q] + rdm.random() + ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5))))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = np.cbrt((1 / 3) * (diff_z_prob[q] + rdm.random() + ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5))))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = np.cbrt((1 / 3) * (diff_z_prob[q] + rdm.random() + ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12))))))

        bayesian_home_Win_d.append(round((float(bayesian_home_Win)), 4))
        bayesian_away_Win_d.append(round((float(bayesian_away_Win)), 4))
        bayesian_GG_d.append(round((float(bayesian_GG)), 4))
        bayesian_1_5_d.append(round((float(bayesian_1_5)), 4))
        bayesian_2_5_d.append(round((float(bayesian_2_5)), 4))
        bayesian_12_d.append(round((float(bayesian_12)), 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(9):
                with open(f"../RESULTS - CBRT AVERAGE DZRANDSCORED/DZRANDFLASHAVCBRAND_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT AVERAGE DZRANDSCORED/DZRANDFLASHAVCBRAND_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - CBRT AVERAGE DZRANDSCORED/DZRANDFLASHAVCBRAND_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT AVERAGE DZRANDSCORED/DZRANDFLASHAVCBRAND_BAYESIAN2.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - CBRT AVERAGE DZRANDSCORED/DZRANDFLASHAVCBRAND_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - CBRT AVERAGE DZRANDSCORED/DZRANDFLASHAVCBRAND_BAYESIAN4.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 0 <= int(match_times[q].split(':')[0].strip()) <= 6:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT AVERAGE DZRANDSCORED/DZRANDFLASHAVCBRAND_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 6 < int(match_times[q].split(':')[0].strip()) <= 12:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT AVERAGE DZRANDSCORED/DZRANDFLASHAVCBRAND_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 12 < int(match_times[q].split(':')[0].strip()) <= 18:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT AVERAGE DZRANDSCORED/DZRANDFLASHAVCBRAND_BAYESIAN7.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 18 < int(match_times[q].split(':')[0].strip()) <= 23:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT AVERAGE DZRANDSCORED/DZRANDFLASHAVCBRAND_BAYESIAN8.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            with open("../RESULTS - CBRT AVERAGE DZRANDSCORED/DZRANDFLASHAVCBRAND_BAYESIAN9.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")

        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(9):
        with open(f"../RESULTS - CBRT AVERAGE DZRANDSCORED/DZRANDFLASHAVCBRAND_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = np.cbrt((home_z_prob[q] * diff_z_prob[q]) * rdm.random() * ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO)))))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = np.cbrt((away_z_prob[q] * diff_z_prob[q]) * rdm.random() * ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO)))))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = np.cbrt(diff_z_prob[q] * rdm.random() * ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG)))))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = np.cbrt(diff_z_prob[q] * rdm.random() * ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5)))))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = np.cbrt(diff_z_prob[q] * rdm.random() * ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5)))))
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = np.cbrt(diff_z_prob[q] * rdm.random() * ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12)))))

        bayesian_home_Win_d.append(round((float(bayesian_home_Win)), 4))
        bayesian_away_Win_d.append(round((float(bayesian_away_Win)), 4))
        bayesian_GG_d.append(round((float(bayesian_GG)), 4))
        bayesian_1_5_d.append(round((float(bayesian_1_5)), 4))
        bayesian_2_5_d.append(round((float(bayesian_2_5)), 4))
        bayesian_12_d.append(round((float(bayesian_12)), 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(10):
                with open(f"../RESULTS - CBRT PRODUCT DZRANDSCORED/DZRANDFLASHCBRAND_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT PRODUCT DZRANDSCORED/DZRANDFLASHCBRAND_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - CBRT PRODUCT DZRANDSCORED/DZRANDFLASHCBRAND_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT PRODUCT DZRANDSCORED/DZRANDFLASHCBRAND_BAYESIAN2.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                    with open("../RESULTS - CBRT PRODUCT DZRANDSCORED/DZRANDFLASHCBRAND_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                            with open("../RESULTS - CBRT PRODUCT DZRANDSCORED/DZRANDFLASHCBRAND_BAYESIAN4.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 0 <= int(match_times[q].split(':')[0].strip()) <= 6:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT PRODUCT DZRANDSCORED/DZRANDFLASHCBRAND_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 6 < int(match_times[q].split(':')[0].strip()) <= 12:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT PRODUCT DZRANDSCORED/DZRANDFLASHCBRAND_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 12 < int(match_times[q].split(':')[0].strip()) <= 18:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT PRODUCT DZRANDSCORED/DZRANDFLASHCBRAND_BAYESIAN7.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if 18 < int(match_times[q].split(':')[0].strip()) <= 23:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q]:
                                with open("../RESULTS - CBRT PRODUCT DZRANDSCORED/DZRANDFLASHCBRAND_BAYESIAN8.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                            with open("../RESULTS - CBRT PRODUCT DZRANDSCORED/DZRANDFLASHCBRAND_BAYESIAN9.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")

        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(10):
        with open(f"../RESULTS - CBRT PRODUCT DZRANDSCORED/DZRANDFLASHCBRAND_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        bayesian_home_Win = (home_z_prob[q] * diff_z_prob[q]) * rdm.random()
        bayesian_away_Win = (away_z_prob[q] * diff_z_prob[q]) * rdm.random()
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = diff_z_prob[q] * rdm.random()
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = diff_z_prob[q] * rdm.random()
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = diff_z_prob[q] * rdm.random()
        prob_12 = prob_12s[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = diff_z_prob[q] * rdm.random()

        bayesian_home_Win_d.append(round((float(bayesian_home_Win)), 4))
        bayesian_away_Win_d.append(round((float(bayesian_away_Win)), 4))
        bayesian_GG_d.append(round((float(bayesian_GG)), 4))
        bayesian_1_5_d.append(round((float(bayesian_1_5)), 4))
        bayesian_2_5_d.append(round((float(bayesian_2_5)), 4))
        bayesian_12_d.append(round((float(bayesian_12)), 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(7):
                with open(f"../RESULTS - NORMAL DZRANDSCORED/DZRANDFLASHSCORE_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - NORMAL DZRANDSCORED/DZRANDFLASHSCORE_BAYESIAN0.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if (h_form_D[q] == 0 or a_form_D[q] == 0) and (h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE):
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - NORMAL DZRANDSCORED/DZRANDFLASHSCORE_BAYESIAN1.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            with open("../RESULTS - NORMAL DZRANDSCORED/DZRANDFLASHSCORE_BAYESIAN2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - NORMAL DZRANDSCORED/DZRANDFLASHSCORE_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if 0 <= int(match_times[q].split(':')[0].strip()) <= 12:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - NORMAL DZRANDSCORED/DZRANDFLASHSCORE_BAYESIAN4.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if 12 < int(match_times[q].split(':')[0].strip()) <= 23:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - NORMAL DZRANDSCORED/DZRANDFLASHSCORE_BAYESIAN5.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            with open("../RESULTS - NORMAL DZRANDSCORED/DZRANDFLASHSCORE_BAYESIAN6.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")

        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(7):
        with open(f"../RESULTS - NORMAL DZRANDSCORED/DZRANDFLASHSCORE_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")
    ###################################################################################################################
    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = rdm.random()
        prob_matches_W_indp_home1 = rdm.random()
        prob_matches_W_indp_away1 = rdm.random()
        bayesian_home_Win = (prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO)))
        prob_matches_away_W_against_EO = rdm.random()
        prob_matches_W_indp_home2 = rdm.random()
        prob_matches_W_indp_away2 = rdm.random()
        bayesian_away_Win = (prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO)))
        prob_GG = rdm.random()
        prob_GG_indp_home = rdm.random()
        prob_GG_indp_away = rdm.random()
        bayesian_GG = (prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG)))
        prob_1_5 = rdm.random()
        prob_1_5_indp_home = rdm.random()
        prob_1_5_indp_away = rdm.random()
        bayesian_1_5 = (prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5)))
        prob_2_5 = rdm.random()
        prob_2_5_indp_home = rdm.random()
        prob_2_5_indp_away = rdm.random()
        bayesian_2_5 = (prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5)))
        prob_12 = rdm.random()
        prob_12_indp_home = rdm.random()
        prob_12_indp_away = rdm.random()
        bayesian_12 = (prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12)))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(22):
                with open(f"../RESULTS - PURE CHAOS/CHAOS_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN0.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN4.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN5.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 0 <= int(match_times[q].split(':')[0].strip()) <= 3:
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN7.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 3 < int(match_times[q].split(':')[0].strip()) <= 6:
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN8.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 6 < int(match_times[q].split(':')[0].strip()) <= 9:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN9.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 9 < int(match_times[q].split(':')[0].strip()) <= 12:
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN10.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if bayesian_home_Win_d[q] > bayesian_away_Win_d[q] and home_positions[q] < away_positions[q] and abs(home_positions[q] - away_positions[q]) >= POS_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN11.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 12 < int(match_times[q].split(':')[0].strip()) <= 15:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN12.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 15 < int(match_times[q].split(':')[0].strip()) <= 18:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN13.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 18 < int(match_times[q].split(':')[0].strip()) <= 21:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN14.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 21 < int(match_times[q].split(':')[0].strip()) <= 23:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN15.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN16.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF and abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                        if h_form_W[q] == 1 or a_form_W[q] == 1:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN17.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if bayesian_home_Win_d[q] < bayesian_away_Win_d[q] and home_positions[q] > away_positions[q] and abs(home_positions[q] - away_positions[q]) >= POS_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN18.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF and abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN19.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF and abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if h_form_L[q] == 0 or a_form_L[q] == 0:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN20.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF and abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - PURE CHAOS/CHAOS_BAYESIAN21.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")

        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(22):
        with open(f"../RESULTS - PURE CHAOS/CHAOS_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    print_all_data()

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = prob_HWs[q]
        prob_matches_W_indp_home1 = rdm.random()
        prob_matches_W_indp_away1 = rdm.random()
        bayesian_home_Win = (prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO)))
        prob_matches_away_W_against_EO = prob_AWs[q]
        prob_matches_W_indp_home2 = rdm.random()
        prob_matches_W_indp_away2 = rdm.random()
        bayesian_away_Win = (prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO)))
        prob_GG = prob_GGs[q]
        prob_GG_indp_home = rdm.random()
        prob_GG_indp_away = rdm.random()
        bayesian_GG = (prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG)))
        prob_1_5 = prob_1_5s[q]
        prob_1_5_indp_home = rdm.random()
        prob_1_5_indp_away = rdm.random()
        bayesian_1_5 = (prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5)))
        prob_2_5 = prob_2_5s[q]
        prob_2_5_indp_home = rdm.random()
        prob_2_5_indp_away = rdm.random()
        bayesian_2_5 = (prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5)))
        prob_12 = prob_12s[q]
        prob_12_indp_home = rdm.random()
        prob_12_indp_away = rdm.random()
        bayesian_12 = (prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12)))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(22):
                with open(f"../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC0.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC4.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC5.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 0 <= int(match_times[q].split(':')[0].strip()) <= 3:
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC7.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 3 < int(match_times[q].split(':')[0].strip()) <= 6:
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC8.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 6 < int(match_times[q].split(':')[0].strip()) <= 9:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC9.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 9 < int(match_times[q].split(':')[0].strip()) <= 12:
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC10.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if bayesian_home_Win_d[q] > bayesian_away_Win_d[q] and home_positions[q] < away_positions[q] and abs(home_positions[q] - away_positions[q]) >= POS_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC11.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 12 < int(match_times[q].split(':')[0].strip()) <= 15:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC12.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 15 < int(match_times[q].split(':')[0].strip()) <= 18:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC13.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 18 < int(match_times[q].split(':')[0].strip()) <= 21:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC14.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 21 < int(match_times[q].split(':')[0].strip()) <= 23:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC15.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC16.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF and abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                        if h_form_W[q] == 1 or a_form_W[q] == 1:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC17.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if bayesian_home_Win_d[q] < bayesian_away_Win_d[q] and home_positions[q] > away_positions[q] and abs(home_positions[q] - away_positions[q]) >= POS_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC18.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF and abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC19.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF and abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if h_form_L[q] == 0 or a_form_L[q] == 0:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC20.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF and abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC21.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")

        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(22):
        with open(f"../RESULTS - CHAOTIC BAYESIAN/BAYESIAN_CHAOTIC{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")

    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = home_z_prob[q]
        prob_matches_W_indp_home1 = rdm.random()
        prob_matches_W_indp_away1 = rdm.random()
        bayesian_home_Win = (prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO)))
        prob_matches_away_W_against_EO = away_z_prob[q]
        prob_matches_W_indp_home2 = rdm.random()
        prob_matches_W_indp_away2 = rdm.random()
        bayesian_away_Win = (prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO)))
        prob_GG = diff_z_prob[q]
        prob_GG_indp_home = rdm.random()
        prob_GG_indp_away = rdm.random()
        bayesian_GG = ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG))))
        prob_1_5 = diff_z_prob[q]
        prob_1_5_indp_home = rdm.random()
        prob_1_5_indp_away = rdm.random()
        bayesian_1_5 = diff_z_prob[q] * ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5))))
        prob_2_5 = diff_z_prob[q]
        prob_2_5_indp_home = rdm.random()
        prob_2_5_indp_away = rdm.random()
        bayesian_2_5 = ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5))))
        prob_12 = diff_z_prob[q]
        prob_12_indp_home = rdm.random()
        prob_12_indp_away = rdm.random()
        bayesian_12 = ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12))))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(22):
                with open(f"../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN0.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN4.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN5.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 0 <= int(match_times[q].split(':')[0].strip()) <= 3:
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN7.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 3 < int(match_times[q].split(':')[0].strip()) <= 6:
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN8.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 6 < int(match_times[q].split(':')[0].strip()) <= 9:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN9.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 9 < int(match_times[q].split(':')[0].strip()) <= 12:
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN10.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if bayesian_home_Win_d[q] > bayesian_away_Win_d[q] and home_positions[q] < away_positions[q] and abs(home_positions[q] - away_positions[q]) >= POS_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN11.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 12 < int(match_times[q].split(':')[0].strip()) <= 15:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN12.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 15 < int(match_times[q].split(':')[0].strip()) <= 18:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN13.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 18 < int(match_times[q].split(':')[0].strip()) <= 21:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN14.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 21 < int(match_times[q].split(':')[0].strip()) <= 23:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN15.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN16.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF and abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                        if h_form_W[q] == 1 or a_form_W[q] == 1:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN17.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if bayesian_home_Win_d[q] < bayesian_away_Win_d[q] and home_positions[q] > away_positions[q] and abs(home_positions[q] - away_positions[q]) >= POS_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN18.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF and abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN19.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF and abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if h_form_L[q] == 0 or a_form_L[q] == 0:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN20.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF and abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN21.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")

        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(22):
        with open(f"../RESULTS - ZCHAOTIC BAYESIAN/ZCHAOS_BAYESIAN{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")
    bayesian_home_Win_d = []
    bayesian_away_Win_d = []
    bayesian_GG_d = []
    bayesian_1_5_d = []
    bayesian_2_5_d = []
    bayesian_12_d = []

    for q in range(len(home_teams)):
        prob_matches_home_W_against_EO = home_z_prob[q]
        prob_matches_W_indp_home1 = prob_HW_H_indps[q]
        prob_matches_W_indp_away1 = prob_AW_H_indps[q]
        bayesian_home_Win = (prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) / ((prob_matches_home_W_against_EO * (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) + ((1 - (prob_matches_W_indp_home1 * prob_matches_W_indp_away1)) * (1 - prob_matches_home_W_against_EO)))
        prob_matches_away_W_against_EO = away_z_prob[q]
        prob_matches_W_indp_home2 = prob_HW_A_indps[q]
        prob_matches_W_indp_away2 = prob_AW_A_indps[q]
        bayesian_away_Win = (prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) / ((prob_matches_away_W_against_EO * (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) + ((1 - (prob_matches_W_indp_home2 * prob_matches_W_indp_away2)) * (1 - prob_matches_away_W_against_EO)))
        prob_GG = diff_z_prob[q]
        prob_GG_indp_home = prob_GG_H_indps[q]
        prob_GG_indp_away = prob_GG_A_indps[q]
        bayesian_GG = ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) / ((prob_GG * (prob_GG_indp_home * prob_GG_indp_away)) + ((1 - (prob_GG_indp_home * prob_GG_indp_away)) * (1 - prob_GG))))
        prob_1_5 = diff_z_prob[q]
        prob_1_5_indp_home = prob_1_5_H_indps[q]
        prob_1_5_indp_away = prob_1_5_A_indps[q]
        bayesian_1_5 = diff_z_prob[q] * ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) / ((prob_1_5 * (prob_1_5_indp_home * prob_1_5_indp_away)) + ((1 - (prob_1_5_indp_home * prob_1_5_indp_away)) * (1 - prob_1_5))))
        prob_2_5 = diff_z_prob[q]
        prob_2_5_indp_home = prob_2_5_H_indps[q]
        prob_2_5_indp_away = prob_2_5_A_indps[q]
        bayesian_2_5 = ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) / ((prob_2_5 * (prob_2_5_indp_home * prob_2_5_indp_away)) + ((1 - (prob_2_5_indp_home * prob_2_5_indp_away)) * (1 - prob_2_5))))
        prob_12 = diff_z_prob[q]
        prob_12_indp_home = prob_12_H_indps[q]
        prob_12_indp_away = prob_12_A_indps[q]
        bayesian_12 = ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) / ((prob_12 * (prob_12_indp_home * prob_12_indp_away)) + ((1 - (prob_12_indp_home * prob_12_indp_away)) * (1 - prob_12))))

        bayesian_home_Win_d.append(round(bayesian_home_Win, 4))
        bayesian_away_Win_d.append(round(bayesian_away_Win, 4))
        bayesian_GG_d.append(round(bayesian_GG, 4))
        bayesian_1_5_d.append(round(bayesian_1_5, 4))
        bayesian_2_5_d.append(round(bayesian_2_5, 4))
        bayesian_12_d.append(round(bayesian_12, 4))

    for q in range(len(home_teams)):
        if q == 0:
            for i in range(22):
                with open(f"../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED{i}.txt", mode="a") as file:
                    file.write(f"CONFIDENCE INTERVAL - {CONFINTVL}|COUNTRIES|LEAGUES|HOME TEAMS|AWAY TEAMS|HOME POSITIONS|AWAY POSITIONS|HOME NMP|AWAY NMP|"
                               f"HOME PTS|AWAY PTS|HW FORM|HD FORM|HL FORM|AW FORM|AD FORM|AL FORM|BAYESIAN HOME WIN|"
                               f"BAYESIAN AWAY WIN|BAYESIAN GG|BAYESIAN 1.5|BAYESIAN 2.5|BAYESIAN 12|MATCH TIME\n")
        try:
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_D[q] == 0 and a_form_D[q] == 0:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED0.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] <= POS_MARK or away_positions[q] <= POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED1.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED2.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_positions[q] > POS_MARK or away_positions[q] > POS_MARK:
                    if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                        if h_form_D[q] == 0 or a_form_D[q] == 0:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED3.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if (h_form_W != h_form_D != h_form_L) or (a_form_W != a_form_D != a_form_L):
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED4.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                    if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                        if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                            with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED5.txt", mode="a") as file:
                                file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                           f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                           f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                           f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                           f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if h_form_W[q] != a_form_W[q] and h_form_L[q] != a_form_L[q]:
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED6.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 0 <= int(match_times[q].split(':')[0].strip()) <= 3:
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED7.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 3 < int(match_times[q].split(':')[0].strip()) <= 6:
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED8.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 6 < int(match_times[q].split(':')[0].strip()) <= 9:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED9.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 9 < int(match_times[q].split(':')[0].strip()) <= 12:
                        if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                            if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED10.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if bayesian_home_Win_d[q] > bayesian_away_Win_d[q] and home_positions[q] < away_positions[q] and abs(home_positions[q] - away_positions[q]) >= POS_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED11.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 12 < int(match_times[q].split(':')[0].strip()) <= 15:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED12.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 15 < int(match_times[q].split(':')[0].strip()) <= 18:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED13.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 18 < int(match_times[q].split(':')[0].strip()) <= 21:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED14.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if 21 < int(match_times[q].split(':')[0].strip()) <= 23:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED15.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED16.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF and abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                        if h_form_W[q] == 1 or a_form_W[q] == 1:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED17.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if bayesian_home_Win_d[q] < bayesian_away_Win_d[q] and home_positions[q] > away_positions[q] and abs(home_positions[q] - away_positions[q]) >= POS_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED18.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF and abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED19.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF and abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if h_form_L[q] == 0 or a_form_L[q] == 0:
                                if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                    with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED20.txt", mode="a") as file:
                                        file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                                   f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                                   f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                                   f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                                   f"{bayesian_12_d[q]}|{match_times[q]}\n")
            if bayesian_home_Win_d[q] > CONFINTVL or bayesian_away_Win_d[q] > CONFINTVL or bayesian_GG_d[q] > CONFINTVL or bayesian_1_5_d[q] > CONFINTVL or bayesian_2_5_d[q] > CONFINTVL or bayesian_12_d[q] > CONFINTVL:
                if home_nums_matches_played[q] >= NMP and away_nums_matches_played[q] >= NMP:
                    if abs(home_positions[q] - away_positions[q]) >= POS_DIFF and abs(bayesian_home_Win_d[q] - bayesian_away_Win_d[q]) >= BAY_DIFF:
                        if h_form_W[q] >= FORM_VALUE or a_form_W[q] >= FORM_VALUE:
                            if bayesian_1_5_d[q] >= bayesian_2_5_d[q] and bayesian_1_5_d[q] >= bayesian_GG_d[q] and (bayesian_home_Win_d[q] + bayesian_away_Win_d[q]) <= 1:
                                with open("../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED21.txt", mode="a") as file:
                                    file.write(f"{countries[q]}|{leagues[q]}|{home_teams[q]}|{away_teams[q]}|{home_positions[q]}|"
                                               f"{away_positions[q]}|{home_nums_matches_played[q]}|{away_nums_matches_played[q]}|{home_points[q]}|"
                                               f"{away_points[q]}|{h_form_W[q]}|{h_form_D[q]}|{h_form_L[q]}|{a_form_W[q]}|{a_form_D[q]}|{a_form_L[q]}|"
                                               f"{bayesian_home_Win_d[q]}|{bayesian_away_Win_d[q]}|{bayesian_GG_d[q]}|{bayesian_1_5_d[q]}|{bayesian_2_5_d[q]}|"
                                               f"{bayesian_12_d[q]}|{match_times[q]}\n")

        except UnicodeError:
            pass
        except IndexError:
            pass
        except OSError:
            pass
    for i in range(22):
        with open(f"../RESULTS - BAYESIAN ZSCORED/BAYESIAN_ZSCORED{i}.txt", mode="a") as file:
            file.write("\n\n\n\n\n")
end_time = time.time()
print(f"run speed: {end_time - start_time}s")
# cleanse()
driver.quit()
