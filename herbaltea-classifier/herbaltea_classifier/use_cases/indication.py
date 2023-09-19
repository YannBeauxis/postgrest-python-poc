from herbaltea_classifier.entities.herbal_tea import HerbalTea
from herbaltea_classifier.entities.indication import (
    IndicationCreateOrUpdate,
    IndicationCreated,
)
from herbaltea_classifier.use_cases.interfaces.crud import (
    HerbalTeaResource,
    IndicationResource,
)

indication_keywords = {
    "cold": ["cold"],
    "digestive": ["digestive", "gastrointestinal", "gastro-intestinal"],
    "diuretic": ["urinary"],
    "mental stress": ["mental stress"],
    "menstrual": ["menstrual"],
}


class IndicationUseCase:
    def __init__(
        self,
        indication_resource: IndicationResource,
        herbal_tea_resource: HerbalTeaResource,
    ):
        self.indication_resource = indication_resource
        self.herbal_tea_resource = herbal_tea_resource

    def fill_indications(self) -> None:
        for name, keywords in indication_keywords.items():
            indication = self.create_indication_if_not_exists(name)
            for keyword in keywords:
                for herbal_tea in self.find_herbal_teas_containing_keyword(keyword):
                    herbal_tea.indication_ids = list(
                        set(herbal_tea.indication_ids) | {indication.id}
                    )
                    self.herbal_tea_resource.update(herbal_tea, id=herbal_tea.id)

    def create_indication_if_not_exists(self, name: str) -> IndicationCreated:
        if not (indication := self.indication_resource.read(name=name)):
            return self.indication_resource.create(IndicationCreateOrUpdate(name=name))[
                0
            ]
        return indication[0]

    def find_herbal_teas_containing_keyword(self, keyword: str) -> list[HerbalTea]:
        return self.herbal_tea_resource.read(indication_raw=f"plfts.{keyword}")
