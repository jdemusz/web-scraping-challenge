import pandas as pd

from splinter import Browser
from bs4 import BeautifulSoup


def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path)

    results = {}

    # 1. mars.nasa.gov/news

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    browser.is_element_present_by_css('ul.item_list li.slide', wait_time=2)
    html = browser.html
    soup = BeautifulSoup(html)
    title_elm = soup.find('div', 'content_title')
    news_title = title_elm.get_text()
    news_p = soup.find('div', 'article_teaser_body').get_text()
    results['news_title'] = news_title
    results['news_paragraph'] = news_p

    # 2. jpl.nasa.gov/spaceimages
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    full_image_btn = browser.find_by_id('full_image')
    full_image_btn.click()
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_btn = browser.find_link_by_partial_text('more info')
    more_info_btn.click()
    soup = BeautifulSoup(browser.html)
    img_url_rel = soup.select_one('figure.lede a img').get('src')
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    results['featured_image'] = img_url

    # 3. table from space-facts.com/mars/
    df = pd.read_html('https://space-facts.com/mars/')[0]
    df.columns = ['description', 'value']
    df.set_index('description', inplace=True)
    results['facts'] = df.to_html(classes='table table-striped')

    # 4. hemispheres images from astrology.usgs.gov
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemispheres = []
    links = browser.find_by_css('a.product-item h3')

    for i in range(len(links)):
        hemi = {}
        browser.find_by_css('a.product-item h3')[i].click()
        sample_elm = browser.find_link_by_text('Sample').first
        img_url = sample_elm['href']
        title = browser.find_by_css('h2.title').text
        hemi['title'] = title
        hemi['img_url'] = img_url
        hemispheres.append(hemi)
        browser.back()
    results['hemispheres'] = hemispheres

    browser.quit()
    return results


# print(scrape())