import urllib.request
import json
import logging as log
from bs4 import BeautifulSoup

def main():
    # Number of rows on the logged-out world selector
    MAX_ROWS = 24
    URL = "https://oldschool.runescape.com/a=13/slu?order=WMLPA"

    worlds_data = dict()

    # Open page and setup parser
    page = urllib.request.urlopen(URL)
    soup = BeautifulSoup(page, features="html.parser")

    # Find the table rows
    tbody = soup.find("tbody", class_="server-list__body")
    trs = tbody.find_all("tr")

    log.info("Scraping " + URL + "...")

    row = 1
    col = 1

    # Iterate each <tr> element
    for tr in trs:
        # Get all <td> elements in the row
        tds = tr.find_all("td")

        # Parse out relevant data
        world = tds[0].find("a").get("id").replace("slu-world-", "")
        world_members_only = True if "Members" == tds[3].get_text() else False
        world_description = tds[4].get_text()

        # False and "None" by default
        world_pvp = False
        world_skill_requirement = "None"

        # Check world description
        if "PvP" in world_description:
            world_pvp = True
        elif "skill total" in world_description:
            world_skill_requirement = tds[4].get_text().replace(" skill total", "")

        worlds_data[world] = {
            "members_only": world_members_only,
            "pvp": world_pvp,
            "total_level_requirement": world_skill_requirement,
            "row": row,
            "column": col,
        }

        row += 1

        if row > MAX_ROWS:
            row = 1
            col += 1

    # Write to json file
    with open("worlds.json", "w") as f:
        json.dump(worlds_data, f, indent=4)

    log.info('Wrote worlds to "worlds.json"')

if __name__ == "__main__":
    main()