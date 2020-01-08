from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import ScrapeSite
import time


def start_search(location, search_list, file_location, is_email_scrape):
    in_list = location_search(append_location_to_searches(search_list, location), is_email_scrape)

    if is_email_scrape:
        search_sites_from_list(in_list)
    else:
        write_file(file_location, in_list)


def create_browser():
    return webdriver.Chrome('C:\\Users\Garre\Downloads\chromedriver_win32\chromedriver')


def search_sites_from_list(search_list):
    email_list = []

    print('------------------ \nScraping emails:\n')
    for search in search_list:
        # Appending the cities will hbe done in the calling function, not this one
        # site_list = location_search(append_cities_to_searches(search))
        email_list.append(scrape_email(email_list, search))

    file_name = ('%sEmailList.txt' % search)
    print('Writing to ' + file_name + '\n------------------')
    write_file(file_name, email_list)


def scrape_email(email_list, search):
    email = ScrapeSite.grab_email_from_site(str(search))
    if email and email not in email_list:
        return email
    return None


def write_file(file_name, list_to_write):
    with open(file_name, 'w+') as file:
        for i in list_to_write:
            file.write(i + ',')


def location_search(search_list, is_email_scrape):
    out_list = []
    browser = create_browser()

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
                    if j.get_attribute('href').find('maps') == -1 and j.get_attribute('href').find(
                            'google') == -1 and j.get_attribute('href') not in out_list:
                        out_list.append(j.get_attribute('href'))
                        print(str(counter) + ' : ' + str(len(elems)))
                    counter += 1

                browser.get(browser.find_element_by_id('pnnext').get_attribute('href'))
                time.sleep(2)
                elems = browser.find_elements_by_class_name('yYlJEf')

        except Exception:
            continue

    browser.close()

    return out_list


def append_location_to_searches(search_list, location):
    # city_list = CityScraper.read_and_parse_city_file()

    appended_search_list = []
    for search in search_list:
        search_city_string = search + ' in ' + location
        appended_search_list.append(search_city_string)

    return appended_search_list


# if __name__ == '__main__':
# search_sites_from_list(['Massage Therapy'])
