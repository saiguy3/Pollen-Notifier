from bs4 import BeautifulSoup
import requests
import re

from typing import Dict, Optional

# from datetime import datetime, timedelta

WEATHER_BASE_URL = "https://weather.com/forecast/allergy/l/"

LEVEL_EMOJI_DICT: Dict[str, str] = {
    "High": "⏶",
    "Moderate": "‒",
    "Low": "⏷",
}


def _get_city(soup: BeautifulSoup) -> str:
    """
    Return the city.
    e.g. 'Fremont, CA'
    """
    city = soup.find("span", class_="styles--locationName--1R6PN").text.strip()
    return city


def _get_pollen_count(soup: BeautifulSoup) -> str:
    """
    Return the pollen count.
    e.g. '154 grains per cubic meter of air'
    """
    pollen_count_amt = soup.find(
        "strong", class_="PollenCount--count--3KgvF"
    ).text.strip()
    pollen_count_units = soup.find(
        "span", class_="PollenCount--unit--pXLTi"
    ).text.strip()
    pollen_count = " ".join([pollen_count_amt, pollen_count_units])
    return pollen_count


def _get_today(soup: BeautifulSoup) -> Optional[str]:
    """
    Return the date for today.
    e.g. '10/11/2023'
    """
    day_regex = r"Last updated: (\d+/\d+/\d+)"
    explanation_content = soup.find_all("p", class_="PollenCard--explanation--1o20G")
    for explanation in explanation_content:
        match = re.search(day_regex, explanation.text)
        if match:
            today = match.group(1)
            return today


# # e.g. '10/11/2023', '10/12/2023', '10/13/2023'
# date_repr = "%m/%d/%Y"
# today_datetime = datetime.strptime(today, date_repr)
# tomorrow = (today_datetime + timedelta(days=1)).strftime(date_repr)
# day_after_tomorrow = (today_datetime + timedelta(days=2)).strftime(date_repr)


def _get_pollen_types(soup: BeautifulSoup) -> Optional[str]:
    """
    Return the pollen types.
    e.g. ['Tree Pollen', 'Grass Pollen', 'Ragweed Pollen']
    """
    pollen_type_content = soup.find_all(
        "h3", class_="PollenBreakdown--pollenType--y4gFi"
    )
    pollen_types = [pt.text.strip() for pt in pollen_type_content]
    return pollen_types


def _get_pollen_levels(soup: BeautifulSoup) -> Optional[str]:
    """
    Return the pollen levels breakdown for today.
    e.g. ['High', 'Low', 'Low']
    """
    level_content = soup.find_all("li", class_="PollenBreakdown--outlookLevel--2rf6z")
    levels = [l.text for l in level_content]
    today_levels = [outlook.split(": ")[1] for outlook in levels[::3]]
    # tomorrow_levels = [outlook.split(': ')[1] for outlook in levels[1::3]]
    # day_after_tomorrow_levels = [outlook.split(': ')[1] for outlook in levels[2::3]]
    return today_levels


def extract_pollen_info(area_code: str) -> str:
    """
    Given a long area code for a location, return the pollen info.
    e.g.
    10/11/2023 -- Fremont, CA
    154 grains per cubic meter of air
    - Tree Pollen: High
    - Grass Pollen: Low
    - Ragweed Pollen: Low
    """

    page = requests.get(WEATHER_BASE_URL + area_code)
    soup = BeautifulSoup(page.content, "html.parser")

    city = _get_city(soup)
    pollen_count = _get_pollen_count(soup)
    today = _get_today(soup)
    pollen_types = _get_pollen_types(soup)
    today_levels = _get_pollen_levels(soup)

    output = f"{today} — {city}"
    output += f"\n{pollen_count}"
    for pt, l in zip(pollen_types, today_levels):
        if l in LEVEL_EMOJI_DICT:
            emoji = LEVEL_EMOJI_DICT[l]
        else:
            emoji = "-"
        output += f"\n{emoji} {pt}: {l}"
    return output
