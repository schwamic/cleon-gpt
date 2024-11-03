from uuid import UUID

from conversations.models import AIModel, Chat
from conversations.schemas import Temperature
from users.models import User


"""Utility Script 

Seed the database with initial data, to be used in development and testing.
"""


def run():
    AIModel.objects.get_or_create(
        provider="Azure OpenAI",
        slug_provider=AIModel.Provider.AZURE_OPEN_AI,
        name="GPT-4o",
        slug_name=AIModel.Name.GPT_4O
    )

    model, isCreated = AIModel.objects.get_or_create(
        provider="Azure OpenAI",
        slug_provider=AIModel.Provider.AZURE_OPEN_AI,
        name="GPT-4o mini",
        slug_name=AIModel.Name.GPT_4O_MINI
    )

    User.objects.get_or_create(
        id=UUID("088948cc-e508-4ead-afde-7b9dd013a940"),
        nickname="Tester",
    )

    Chat.objects.get_or_create(
        id=UUID("579d6fb7-fa62-42bd-80bb-7f4870cbd810"),
        model=model,
        configuration={"temperature": Temperature.MEDIUM}
    )

    print('Database Seeds successfully created')
