from selenium import webdriver

from bs4 import BeautifulSoup

from lxml import etree

def get_info(page_src:str) -> dict[str, str]:
  output = {}
  soup = BeautifulSoup(page_src, 'lxml')
  hotel_name = soup.find(attrs={"data-selenium": "hotel-header-name"})
  
  if hotel_name is not None:
    output["hotel_name"] = hotel_name.text

  review_element = soup.select('[data-review-count-property-on-ssr]')
  if review_element is not None:
    output["number_of_reviews"] = review_element[0].attrs["data-review-count-property-on-ssr"]

  xpath_query_location = r'//*[@id="abouthotel-panel"]/div[3]/div/div[1]/div[1]/div/div/div[2]/span'
  dom_tree = etree.HTML(str(soup), parser=None)

  location_str = dom_tree.xpath(xpath_query_location)[0].text
  output["location"] = location_str

  return output


if __name__ == '__main__':
  driver = webdriver.Chrome()
  url = r"https://www.agoda.com/bally-s-las-vegas-hotel-casino/hotel/las-vegas-nv-us.html?finalPriceView=1&isShowMobileAppPrice=false&cid=-1&numberOfBedrooms=&familyMode=false&adults=2&children=0&rooms=1&maxRooms=0&checkIn=2024-04-25&isCalendarCallout=false&childAges=&numberOfGuest=0&missingChildAges=false&travellerType=1&showReviewSubmissionEntry=false&currencyCode=USD&isFreeOccSearch=false&isCityHaveAsq=false&tspTypes=8&los=1&searchrequestid=97f3fad4-bcfa-4462-b6ca-d49ab8bbeda6"
  driver.get(url)

  output = get_info(driver.page_source)
  print(output)

  driver.quit()