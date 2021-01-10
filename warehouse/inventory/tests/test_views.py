from django.urls import reverse
import pytest


@pytest.mark.django_db
class TestDocumentationViews:
    """
    Normally documentation requires additional authentication but in our case we will simply check their
    availability for the anonymous users
    """

    @pytest.mark.parametrize(
        "url",
        [
            reverse('schema-json', args=('.json', )),
            reverse('schema-swagger-ui'),
        ]
    )
    def test_availability(self, url, client):
        response = client.get(url)
        assert response.status_code == 200
