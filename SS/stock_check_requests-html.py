from requests_html import HTMLSession
import csv

session = HTMLSession()

with HTMLSession() as session:

    r = session.request(
        url="https://www.lcbo.com/webapp/wcs/stores/servlet/PhysicalStoreInventoryView?langId=-1&storeId=10203&catalogId=10051&productId=203517"
    )

    # render html
    r.html.render()

    print(r.html)

entry = r.html.find("div.col-xs-4")

print(entry.html)

# match = html.find("#footer", first=True)
# print(match.html)

# article = html.find("div.article", first=True)
# articles = html.find("div.article")

# for article in articles:

#     headline = article.find("h2", first=True).text
#     summary = article.find("p", first=True).text

#     print(headline)
#     print(summary)
#     print()

# csv_file = open("cms_scrape.csv", "w")
# csv_writer = csv.writer(csv_file)
# csv_writer.writerow(["headline", "summary", "video"])

# session = HTMLSession()
# r = session.get("https://coreyms.com/")

# # replace links "with" "absolute_links" to return non-relative links
# for link in r.html.links:
#     print(link)


# articles = r.html.find("article")

# for article in articles:
#     headline = article.find(".entry-title-link", first=True).text
#     print(headline)

#     summary = article.find(".entry-content p", first=True).text
#     print(summary)

#     try:
#         vid_src = article.find("iframe", first=True).attrs["src"]
#         vid_id = vid_src.split("/")[4]
#         vid_id = vid_id.split("?")[0]
#         yt_link = f"https://youtube.com/watch?v={vid_id}"
#     except Exception as e:
#         yt_link = None

#     print(yt_link)

#     csv_writer.writerow([headline, summary, yt_link])

# csv_file.close()