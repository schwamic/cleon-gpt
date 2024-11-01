from uuid import UUID

from conversations.models import AIModel, AIFunction
from users.models import User


'''
Utility script to seed the database with AIModels and AIFunctions
'''


def run():
    User.objects.get_or_create(
        id=UUID("088948cc-e508-4ead-afde-7b9dd013a940"),
        nickname="Tester",
    )
    AIModel.objects.get_or_create(
        name="GPT-4o",
        endpoint="https://zdp-x-cc-sdc-oai.openai.azure.com/",
        api_key_name="CGPT_OPENAI_API_KEY"
    )

    AIModel.objects.get_or_create(
        name="GPT-4o mini",
        endpoint="https://zdp-x-cc-sdc-oai.openai.azure.com/",
        api_key_name="CGPT_OPENAI_API_KEY"
    )

    AIFunction.objects.get_or_create(
        name="WeatherAPI",
        endpoint="http://api.weatherapi.com/v1/current.json",
        api_key_name="CGPT_WEATHER_API_KEY"
    )

    print('Users, AIModels and AIFunctions successfully created')
