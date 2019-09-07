import requests
from bs4 import BeautifulSoup
import threading 
import time
# import pdb
# print(dir(threading))
help(threading.Timer)

def get_page_data(start_url):
    lock.acquire()
    response = requests.get(start_url)

    soup = BeautifulSoup(response.content,"html.parser")

    detail_links =  soup.find_all("a",attrs = {"class":"_31qSD5"})

    for detail_link in detail_links:

        details_page_res = requests.get(HOME+detail_link.get("href"))

        details_soup = BeautifulSoup(details_page_res.content,"html.parser")
        all_review_text = details_soup.find("div",attrs={"class":"swINJg"})

        if all_review_text:
            all_review_link = all_review_text.findParent("a")

            review_page_resp = requests.get(HOME + all_review_link.get("href"))
            review_soup = BeautifulSoup(review_page_resp.content,"html.parser")

            review_cards = review_soup.find_all("div",attrs = {"class":"_1gY8H-"})

            for review_card in review_cards:
                rating = review_card.find("div",attrs = {"class":"E_uFuv"})

                review_text = review_card.find("div",attrs = {"class":"qwjRop"})

                likes_count = review_card.find("span",attrs = {"class":"_1_BQL8"})


                print("{} {} {}".format(rating.text,review_text.text,likes_count.text))

    lock.release()
def main():
    
    count = 0

    start_url = "https://www.flipkart.com/search?q=mobiles&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_0_7_na_na_pr&otracker1=AS_QueryStore_OrganicAutoSuggest_0_7_na_na_pr&as-pos=0&as-type=RECENT&suggestionId=mobiles&requestId=e0714d09-557d-4631-ba66-88a10e2b7f42&as-backfill=on"

    while(True):
        print("************************PAGE NO IS",count+1)
        response = requests.get(start_url)
        soup = BeautifulSoup(response.content,"html.parser")
        if count ==0 :
            t = threading.Thread(target= get_page_data,args = (start_url,),daemon = True)
            # t.start()
    
        elif count > 3:
            break
        else:
            next_link = soup.find("a",attrs ={"class":"_3fVaIS"})
            start_url = HOME+next_link.get("href")

            t = threading.Thread(target= get_page_data,args = (start_url,))
            # t.start()
        
        count+=1


if __name__ == '__main__':

    lock = threading.RLock()
    HOME = "https://www.flipkart.com"
    # pdb.set_trace()
    main()



# def a
#         acquire
#                 acquire
#                 release
#         release
# def b
#     release 
#     acquire
#     release

# .py => Process 
#         t1
#         t2
#         t3
