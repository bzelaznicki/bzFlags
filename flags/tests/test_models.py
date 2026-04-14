import pytest
from model_bakery import baker
from django.core.exceptions import ValidationError
from django.db import IntegrityError

@pytest.mark.django_db
def test_flag_rollout_percentage_over_100_should_fail():

    flag = baker.make("flags.Flag", rollout_percentage=200)
    with pytest.raises(ValidationError):
        flag.full_clean()

@pytest.mark.django_db
def test_flag_rollout_negative_percentage_should_fail():
    flag = baker.make("flags.Flag", rollout_percentage=-10)

    with pytest.raises(ValidationError):
        flag.full_clean()


@pytest.mark.django_db
def test_flag_duplicate_key_on_project_should_fail():

    project = baker.make("flags.Project")

    baker.make("flags.Flag", key="same", project=project)
    with pytest.raises(IntegrityError):
        baker.make("flags.Flag", key="same", project=project)

@pytest.mark.django_db
def test_flag_override_duplicate_user_identifier_on_flag_should_fail():

    flag = baker.make("flags.Flag")

    baker.make("flags.FlagOverride", user_identifier="test_user", flag=flag)

    with pytest.raises(IntegrityError):
        baker.make("flags.FlagOverride", user_identifier="test_user", flag=flag)
