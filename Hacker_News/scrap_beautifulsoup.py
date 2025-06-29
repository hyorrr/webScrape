from bs4 import BeautifulSoup
import requests

def scrap():
    url = "https://news.ycombinator.com/"

    content = requests.get(url).text

    soup = BeautifulSoup(content, 'html.parser')

    articles = soup.find_all("tr", class_="athing")

    for idx, article in enumerate(articles, 1):
        title_tag = article.find("span", class_="titleline")
        #title = title_tag.get_text()
        title = title_tag.find("a").get_text(strip=True)
        link = title_tag.find("a")["href"]

        subtext = article.find_next_sibling("tr").find("td", class_="subtext")
        score_tag = subtext.find("span", class_="score")
        score = score_tag.get_text() if score_tag else "0 points"

        comment_links = subtext.find_all("a")
        if comment_links:
            comment_text = comment_links[-1].get_text()
            comments = comment_text if "comment" in comment_text else "0 comments"
        else:
            comments = "0 comments"

        print(f"{idx}. title: {title}")
        print(f"link: {link}")
        print(score)
        print(comments)


scrap()