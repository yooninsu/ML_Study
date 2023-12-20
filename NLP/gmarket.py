from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from collections import Counter

url = "http://item.gmarket.co.kr/Item?goodsCode=1617800589"
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(10)
driver.get(url)


def goComment():
    comment = driver.find_element_by_partial_link_text("상품평")
    driver.execute_script("arguments[0].click();", comment)


def setPage(page_num):
    comment = driver.find_element_by_id("text-pagenation-wrap")
    page_list = comment.find_element_by_class_name("board_pagenation")
    page = page_list.find_element_by_link_text(str(page_num))
    driver.execute_script("arguments[0].click();", page)


def nextPage():
    comment = driver.find_element_by_id("text-pagenation-wrap")
    page_list = comment.find_element_by_class_name("board_pagenation")
    npage = page_list.find_element_by_class_name("next")
    driver.execute_script("arguments[0].click();", npage)


def crawlProduct(stats):
    table = driver.find_element_by_id("text-wrapper")

    products = table.find_elements_by_class_name("pd-tit")
    for p in products:
        p_ = p.text.split(" ")[-1].split("[")[0]
        stats.append(p_)
        print(p_)


def count(stats):
    return Counter(stats)


def main():
    goComment()
    stats = []

    for i in range(1, 105):
        time.sleep(5)
        setPage(i)
        crawlProduct(stats)

        if i % 10 == 0:
            nextPage()

    stats = count(stats)
    print(stats)


if __name__ == "__main__":
    main()
