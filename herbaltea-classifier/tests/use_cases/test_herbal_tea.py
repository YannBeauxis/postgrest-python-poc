from herbaltea_classifier.use_cases.herbal_tea import HerbalTeaUseCase
from herbaltea_classifier.use_cases.interfaces.crud import HerbalTeaResource


def test_create_herbal_teas(herbal_tea_resource: HerbalTeaResource) -> None:
    use_case = HerbalTeaUseCase(herbal_tea_resource)
    use_case.create_herbal_teas()
    assert len(herbal_tea_resource.read()) == 1
