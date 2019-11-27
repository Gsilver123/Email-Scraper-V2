from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import ScrapeSite
import time
import CityScraper

def search_sites_from_list(search_list):
	email_list = []
	browser = webdriver.Chrome('/Users/garrettsilver/Documents/chromedriver')

	for search in search_list:
		site_list = location_search(browser, append_cities_to_searches(search))

		print('------------------ \nEmails for %s:' %search)
		for i in range(len(site_list)):
			email = ScrapeSite.grab_email_from_site(str(site_list[i]))
			if email and email not in email_list:
				email_list.append(email)
			print(str(i + 1) + ' : ' + str(len(site_list)))

		file_name = ('%sEmailList.txt' %search)
		print('Writing to ' + file_name + '\n------------------')

		with open(file_name, 'w+') as email_file:
			for i in email_list:
				email_file.write(i + ',')



def location_search(browser, search_list):
	out_url_list = []

	for i in search_list:
		browser.get('https://www.Google.com')
		search_bar = browser.find_element_by_name('q')
		search_bar.send_keys(i)
		search_bar.send_keys(Keys.ENTER)

		try:
			button = browser.find_element_by_class_name('cMjHbjVt9AZ__button')
			button.send_keys(Keys.ENTER)
		except Exception:
			continue

		try:
			elems = browser.find_elements_by_class_name('yYlJEf')

			print('Elems: ')
			for x in range(5):
				counter = 1
				for j in elems:
					if j.get_attribute('href').find('maps') == -1 and j.get_attribute('href').find('google') == -1 and j.get_attribute('href') not in out_url_list:
						out_url_list.append(j.get_attribute('href'))
						print(str(counter) + ' : ' + str(len(elems)))
					counter += 1

				browser.get(browser.find_element_by_id('pnnext').get_attribute('href'))
				time.sleep(2)
				elems = browser.find_elements_by_class_name('yYlJEf')

		except Exception:
			continue

	browser.close()

	return out_url_list

def append_cities_to_searches(search):
	city_list = CityScraper.read_and_parse_city_file()

	appended_search_list = []
	for city in city_list:
		search_city_string = search + ' in ' + city[0] + ', ' + city[1]
		appended_search_list.append(search_city_string)

	return appended_search_list


search_sites_from_list(['Massage Therapy', 'Physical Therapy Clinic', 'Sports Rehab Clinic', 'Rehab Center', 'Floation Therapy Spa', 'Wellness Center'])
