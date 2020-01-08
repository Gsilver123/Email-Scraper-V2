import requests
import bs4


def grab_email_from_site(url):

    try:
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text, 'lxml')

        allowed_characters_list = ['!', '#', '$', '%&', '*', '+', '-', '/', '=', '?', '^', '_', '`', '{', '|', '}', '~', '.']

        href = ''
        for i in soup.find_all('a', href=True):
            if i['href'].find('@') != -1:
                if i['href'].find('map') != -1:
                    return None
                href = i['href']
                break

        split_href = href.split('@')

        if len(split_href) > 1 and split_href[1].isdigit():
            return None

        split_counter = 1
        for i in split_href[0]:
            if not i.isalpha() and not i.isdigit() and i not in allowed_characters_list:
                split_href[0] = split_href[0][split_counter:]
                split_counter = 1

            split_counter += 1

        if len(split_href) != 1:
            split_domain_index = split_href[1].find('.com')
            if split_domain_index != -1:
                split_href[1] = split_href[1][:split_domain_index + 4]

            href = split_href[0] + '@' + split_href[1]

        return href

    except Exception as e:
        print('Could not request ' + url + ', error message: ' + str(e))
        return None
