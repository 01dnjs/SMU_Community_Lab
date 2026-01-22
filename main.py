import bs4
import requests
import pandas as pd

base_url_for_download = "https://cs.smu.ac.kr/cs/community/lab_notice.do"
base_domain = "https://cs.smu.ac.kr"

url = "https://cs.smu.ac.kr/cs/community/lab_notice.do"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = bs4.BeautifulSoup(response.text, "html.parser")

data = []

for tag in soup.select("div.board-wrap ul > li"):
    try:
        title_elem = tag.select_one("div.board-thumb-content-title > a")
        if not title_elem: title_elem = tag.select_one("dl > dt > a")
        
        date_elem = tag.select_one("li.board-thumb-content-date")
        if not date_elem: date_elem = tag.select_one("dd span.hide")

        if not title_elem: continue

        title = title_elem.get_text(strip=True)
        date = date_elem.get_text(strip=True).replace("작성일", "").strip() if date_elem else "날짜없음"
        
        detail_path = title_elem["href"]
        detail_url = base_domain + detail_path


        data.append({
            "제목": title,
            "날짜": date,
            "본문주소": detail_url
        })
        

    except Exception as e:
        print(f"에러: {e}")
        continue

df = pd.DataFrame(data)
df.to_csv("docs/lab_notice.csv", index=False, encoding="utf-8-sig")

from feedgen. feed import FeedGenerator
fg = FeedGenerator()
fg.id('http://lernfunk.de/media/654321')
fg.title('Some Testfeed')
fg.author( {'name':'John Doe','email': 'john@example.de'} )
fg.link( href='http://example.com', rel='alternate' )
fg.logo('http://ex.com/logo.jpg')
fg.subtitle('This is a cool feed!')
fg.link( href='http://larskiesow.de/test.atom', rel='self' )
fg.language('en')
fg.rss_file('rss.xml')
