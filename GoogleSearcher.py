from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import ScrapeSite
import time


def start_search(location, search_list, file_location, is_email_scrape):
    in_list = location_search(append_location_to_searches(search_list, location), is_email_scrape)

    if is_email_scrape:
        search_sites_from_list(in_list, file_location)
    else:
        write_file(file_location, in_list)


def create_browser():
    return webdriver.Chrome('chromedriver_win32\chromedriver')


def search_sites_from_list(search_list, file_location):
    email_list = []

    counter = 1
    print('------------------ \nScraping emails:\n\nSite:\n')
    for search in search_list:
        # Appending the cities will hbe done in the calling function, not this one
        # site_list = location_search(append_cities_to_searches(search))
        print('\t' + str(counter) + ' : ' + str(len(search_list)))
        counter += 1
        email_list.append(scrape_email(email_list, search))

    print('Writing to ' + file_location + '\n------------------')
    write_file(file_location, email_list)


def scrape_email(email_list, search):
    email = ScrapeSite.grab_email_from_site(str(search))
    if email and email not in email_list:
        return email
    return None


def write_file(file_name, list_to_write):
    with open(file_name, 'w+') as file:
        for i in list_to_write:
            if i:
                file.write(i + '\n')


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
        except Exception as ex:
            print(str(ex))
            continue

        if is_email_scrape:
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

            except Exception as e:
                print(str(e))
                continue
        else:
            try:
                elems = browser.find_elements_by_class_name('cXedhc')

                print('Elems: ')
                for x in range(5):
                    counter = 1
                    for j in elems:
                        try:
                            title = str(j.find_element_by_xpath('div/div').text)
                            title = title.replace('\n', ' ')
                            title = title.replace(',', '')
                            number = str(j.find_element_by_xpath('span/div[3]/span[2]').text)
                            entry = title + ", " + number
                            if entry not in out_list:
                                out_list.append(entry)

                        except Exception as exc:
                            print('Could not retrieve name or phone number: error: ' + str(exc))

                        print(str(counter) + ' : ' + str(len(elems)))
                        counter += 1

                    browser.get(browser.find_element_by_id('pnnext').get_attribute('href'))
                    time.sleep(2)
                    elems = browser.find_elements_by_class_name('cXedhc')

            except Exception as e:
                print(str(e))
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
