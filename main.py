import httpx
import sqlite3
from bs4 import BeautifulSoup
from tqdm import tqdm

def main() -> None:

    conn = sqlite3.connect("bestmovies.db")
    cur = conn.cursor()
    try:
        cur.execute("CREATE TABLE bestmovieslist(authors, name, year)")
    except sqlite3.OperationalError:
        print('Database exists, skipping database creation...')

    request = httpx.get("https://www.imdb.com/chart/top/")

    data = request.content
    soup = BeautifulSoup(data, "lxml")
    columns = soup.find_all('td', class_ ="titleColumn")

    for title in tqdm(columns):
        authors = title.find('a')
        year = title.find('span')
        query = "INSERT INTO bestmovieslist VALUES(?, ?, ?)"
        cur.execute(query, (authors['title'], authors.string, str(year.string).strip("()")))
    print("Finished!")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
