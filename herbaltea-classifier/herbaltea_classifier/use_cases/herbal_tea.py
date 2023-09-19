import re
import urllib
from io import BytesIO
import logging

import requests
import pdftotext
from pydantic import AnyHttpUrl

from herbaltea_classifier.entities.herbal_tea import HerbalTeaCreateCreateOrUpdate
from herbaltea_classifier.use_cases.interfaces.crud import HerbalTeaResource
from .scrapers import (
    plant_latin_scraper,
    plant_url_scraper,
    pdf_scraper,
    EMA_HERBAL_MONOGRAPH_LIST_URL,
)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class HerbalTeaUseCase:
    def __init__(
        self,
        herbal_tea_resource: HerbalTeaResource,
    ):
        self.herbal_tea_resource = herbal_tea_resource

    def create_herbal_teas(self) -> None:
        for plant in get_plants_url():
            logger.warning(plant)
            logger.warning(get_pdf_url(plant))
            if pdf_url := get_pdf_url(plant):
                logger.warning(pdf_url)
                full_text = get_full_text(pdf_url)
                if "herbal tea" in full_text.lower():
                    self.create_herbal_tea(plant, pdf_url, full_text)

    def create_herbal_tea(
        self, plant: str, pdf_url: AnyHttpUrl, full_text: str
    ) -> None:
        name_botanical = plant_latin_scraper.get_result_exact(plant)[0]
        logger.info(name_botanical)
        herbal_tea = HerbalTeaCreateCreateOrUpdate(
            name_botanical=name_botanical, monograph_url=pdf_url
        )

        get_vernacular_name(herbal_tea)
        get_indication_raw(herbal_tea, full_text)

        if not self.herbal_tea_resource.read(name_botanical=name_botanical):
            self.herbal_tea_resource.create(herbal_tea)


def get_vernacular_name(herbal_tea: HerbalTeaCreateCreateOrUpdate) -> None:
    try:
        gbif_id = get_gbif_id(herbal_tea.name_botanical)
        herbal_tea.gbif_id = gbif_id
        name_fr = get_name_fr(gbif_id)
        herbal_tea.name_fr = name_fr
        logger.debug(name_fr)
    except Exception:
        logger.warning("unable to get vernacular name")


def get_indication_raw(
    herbal_tea: HerbalTeaCreateCreateOrUpdate, full_text: str
) -> None:
    try:
        indication_raw = get_indication(full_text)
        logger.debug(indication_raw)
        herbal_tea.indication_raw = indication_raw
    except Exception:
        logger.error("Error getting indication raw data")


def get_plants_url() -> list[str]:
    page = 0
    plants_url: list[str] = []
    result: list[str] = [""]
    while result:
        url = f"{EMA_HERBAL_MONOGRAPH_LIST_URL}&page={page}"
        result = plant_url_scraper.get_result_similar(url)
        plants_url.extend(result)
        page += 1
    return plants_url


def get_pdf_url(plant_url: str) -> AnyHttpUrl | None:
    pattern = r"final-(?:community|european-union)-herbal-monograph"
    result = pdf_scraper.get_result_similar(plant_url)
    filtered: list[AnyHttpUrl] = [
        pdf_link
        for pdf_link in result
        if re.search(pattern, pdf_link) and "supersed" not in pdf_link
    ]
    if len(filtered) == 1:
        return filtered[0]
    return None


def get_full_text(url: str) -> str:
    data = urllib.request.urlopen(url)
    pdf = pdftotext.PDF(BytesIO(data.read()))

    return "\n".join(remove_footer(page) for page in pdf)


def remove_footer(page: str) -> str:
    return "\n".join(page.split("\n")[:-3])


def get_indication(full_text: str) -> str:
    pattern = r"\n(4.\d+\. +.*)\n"

    split = re.split(pattern, full_text)[1:]

    return split[1]


def get_gbif_id(name: str) -> int:
    url = f'https://api.gbif.org/v1/species/match?name="{name}"'
    return int(requests.get(url).json()["speciesKey"])


def get_name_fr(gbif_id: int) -> str:
    url = f"https://api.gbif.org/v1/species/{gbif_id}"
    headers = {"Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3"}
    data = requests.get(url, headers=headers).json()
    logger.debug(url)
    logger.debug(data)
    return str(data["vernacularName"])
