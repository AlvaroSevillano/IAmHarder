from profiles import get_profiles
import datetime
import logging as logger
import pytz
import time
from selenium import webdriver
import random

class IAmHarder:

    def __init__(self, user, is_dev):
        self.user = user
        self.is_dev = is_dev

        self.today = datetime.datetime.today()

        profiles, assigned_profiles = get_profiles()
        self.time_class = profiles[assigned_profiles[user][0]][0]
        self.type_class = profiles[assigned_profiles[user][0]][1]
        self.email = assigned_profiles[user][1]
        self.password = assigned_profiles[user][2]
        self.waiting_time = assigned_profiles[user][3]

        self.driver = self.init_browser()

        self.list_months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        self.list_days = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo',
                          'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']

        # URLs
        self.url_login = "https://aimharder.com/login"
        self.url_book = "https://komcrossfit.aimharder.com/schedule"
        self.url_out = "https://aimharder.com/Util/logout.php"

        self.complete_task()

    def complete_task(self):

        if not self.is_dev:
            self.wait_until(wait_time='23:58', timezone='Europe/Madrid')

        logger.info('Its time to start')
        time.sleep(random.uniform(0, 2))
        self.log_in()
        self.book_CF()
        self.end_browser()

    def get_string_check_date(self, today):
        str_template = 'Clases disponibles el {day} de {month} de {year}'
        list_strings = []
        for i in range(7):
            date = today + datetime.timedelta(days=i)
            list_strings.append(str_template.format(day=date.day,
                                                    month=self.list_months[date.month - 1],
                                                    year=date.year))
        return list_strings

    def log_in(self):
        logger.info('Visiting logging web aimharder')
        self.driver.get(self.url_login)

        self.manage_waiting_elements(self.wait_until_text(self.driver, 'Keep me logged in', max_time=40))
        self.manage_waiting_elements(self.wait_until_text(self.driver, 'Forgot my password', max_time=10))

        time.sleep(5)
        logger.info('Filling email and password')
        input_element = self.driver.find_element_by_id("mail")
        input_element.send_keys(self.email)
        input_element = self.driver.find_element_by_id("pw")
        input_element.send_keys(self.password)
        logger.info('Logging in')
        self.driver.find_element_by_id('loginSubmit').click()

        self.manage_waiting_elements(self.wait_until_text(self.driver, 'Reservas', max_time=40))

    def book_CF(self):
        self.driver.get(self.url_book)
        if self.is_dev:
            n_days = 5
        else:
            n_days = 6
        self.go_to_desire_day(n_days)
        self.book_class(n_days)

    def go_to_desire_day(self, n_days):

        strings_check_date = self.get_string_check_date(self.today)
        for i in range(0, n_days):
            time.sleep(0.3)
            logger.info('Waiting for {}'.format(strings_check_date[i]))
            self.manage_waiting_elements(self.wait_until_text(self.driver, strings_check_date[i],
                                                              max_time=20))
            self.driver.find_element_by_id("nextDay").click()

        logger.info('Waiting for {}'.format(strings_check_date[n_days]))
        self.manage_waiting_elements(self.wait_until_text(self.driver, strings_check_date[n_days],
                                                          max_time=20))

        logger.info('Correct Day Selected')

    def find_button(self, type_class, time_class):
        for prefix in type_class:
            button = self.driver.find_elements_by_xpath("//div[span[contains(text(), \'{prefix}\')] and "
                                                       "span[contains(text(), \'{int_time}\')]]"
                                                       "//a[contains(text(), 'Reservar')]".
                                                       format(prefix=prefix, int_time=time_class))
            if len(button) > 0:
                return button[0]
        logger.error('Configuracion no encontrada')
        self.end_browser()
        raise

    def book_class(self, n_days):
        if not self.is_dev:
            logger.info('Waiting until midnight')
            self.wait_until(wait_time='00:00', timezone='Europe/Madrid')

        if self.list_days[self.today.weekday() + n_days] != 'Sabado':
            logger.info('The reservation day is not Saturday')
            button = self.find_button(self.type_class, self.time_class)
            logger.info('Waiting a few seconds')
            time.sleep(self.waiting_time + 3)
            logger.info('Pushing button to make reservation')
            button.click()
            self.manage_waiting_elements(self.wait_until_text(self.driver, 'Cancelar reserva', max_time=20))
            logger.info('Reservation is ok')

        else:
            logger.info('The reservation day is not Saturday')
            button = self.find_button(['Team'], '12:00 - 13:00')
            logger.info('Waiting a few seconds')
            time.sleep(self.waiting_time + 3)
            logger.info('Pushing button to make reservation')
            button.click()
            time.sleep(10)
            logger.info('Pushing button to make reservation')
            self.find_button(['Open'], '11:00 - 12:00').click()
            self.manage_waiting_elements(self.wait_until_text(self.driver, 'Cancelar reserva', max_time=20))
            logger.info('Reservation is ok')
            time.sleep(5)

    @staticmethod
    def init_browser():
        logger.info('Trying Browser')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
        init_cont = 0
        while init_cont < 5:
            try:
                driver.get('https://www.google.com')
                break
            except:
                time.sleep(1)
                init_cont += 1
        return driver

    def end_browser(self):
        logger.info('Ending Browser')
        self.driver.close()

    @staticmethod
    def wait_until(wait_time, timezone):
        logger.info('Waiting until {}'.format(wait_time))
        [hour, minute] = [int(i) for i in wait_time.split(':')]
        while True:
            actual_time = datetime.datetime.now(pytz.timezone(timezone))
            if ((actual_time.hour == hour and actual_time.minute >= minute) or
                    (hour != 23 and actual_time.hour == hour + 1 and actual_time.minute < minute) or
                    (hour == 23 and actual_time.hour == 0 and actual_time.minute < minute)):
                return
            else:
                time.sleep(3)

    @staticmethod
    def wait_until_text(driver, txt, max_time=120):
        cont = 0
        while cont <= max_time:
            if driver.find_elements_by_xpath("//*[contains(text(), \'{text}\')]".format(text=txt)):
                return 0
            else:
                cont += 1
                time.sleep(1)
        return 1

    def manage_waiting_elements(self, is_fail):
        if is_fail:
            logger.error('Element not found')
            self.end_browser()
            raise






