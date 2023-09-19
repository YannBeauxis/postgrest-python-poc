from autoscraper import AutoScraper


EMA_URL_BASE = "https://www.ema.europa.eu"
EMA_URL_MEDECINES = f"{EMA_URL_BASE}/en/medicines"
EMA_HERBAL_MONOGRAPH_LIST_URL = (
    f"{EMA_URL_MEDECINES}"
    "/field_ema_web_categories%253Aname_field"
    "/Herbal/field_ema_herb_outcome"
    "/european-union-herbal-monograph-254?search_api_views_fulltext="
)
EMA_HERBAL_URL = f"{EMA_URL_MEDECINES}/herbal"
EMA_MONOGRAPH_PDF_BASE_URL = f"{EMA_URL_BASE}/documents/herbal-monograph"
EMA_THYME_MONOGRAPH_URL = f"{EMA_HERBAL_URL}/thymi-herba"

plant_url_scraper = AutoScraper()
plant_url_scraper.build(
    EMA_HERBAL_MONOGRAPH_LIST_URL, [f"{EMA_HERBAL_URL}/fragariae-folium"]
)

plant_latin_scraper = AutoScraper()
plant_latin_scraper.build(
    EMA_THYME_MONOGRAPH_URL, ["Thymus vulgaris L.; Thymus zygis L. "]
)


pdf_scraper = AutoScraper()
pdf_scraper.build(
    EMA_THYME_MONOGRAPH_URL,
    [
        f"{EMA_MONOGRAPH_PDF_BASE_URL}/final-community-herbal-monograph-thymus-vulgaris-l-thymus-zygis-l-herba_en.pdf"
    ],
)
