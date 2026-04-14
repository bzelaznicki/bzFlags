import pytest
from model_bakery import baker
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_flag_rollout_percentage_over_100_should_fail():

    flag = baker.make("flags.Flag", rollout_percentage=200)
    with pytest.raises(ValidationError):
        flag.full_clean()

