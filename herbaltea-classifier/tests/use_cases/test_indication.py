from herbaltea_classifier.use_cases.indication import (
    IndicationUseCase,
    indication_keywords,
)
from herbaltea_classifier.use_cases.interfaces.crud import (
    IndicationResource,
    HerbalTeaResource,
)


def test_fill_indications(
    indication_resource: IndicationResource,
    herbal_tea_resource: HerbalTeaResource,
) -> None:
    use_case = IndicationUseCase(
        indication_resource=indication_resource, herbal_tea_resource=herbal_tea_resource
    )
    use_case.fill_indications()
    assert len(indication_resource.read()) == len(indication_keywords)
