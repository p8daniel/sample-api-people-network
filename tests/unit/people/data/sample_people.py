from app.models.peoples import NameIdDataclass, PersonDataclass

SAMPLE_PERSON = PersonDataclass(
    ID="abcb029f-9562-46db-bfc9-b3fb00b60e2e",
    first_name="Anna",
    last_name="Smith",
    nickname="Annie",
    parent_of=[
        NameIdDataclass(ID="801225df-d5e1-4b01-adae-0cca392608da", name="Susan Smith"),
        NameIdDataclass(ID="4b3df73f-0174-4c20-b82c-89a1466689cb", name="John Smith"),
    ],
    child_of=[NameIdDataclass(ID="94c245b1-3be2-4eda-8737-e559f8cac2e5", name="Lisa Smith")],
    friend_of=[],
)

SAMPLE_PERSON_JSON = {
    "ID": "abcb029f-9562-46db-bfc9-b3fb00b60e2e",
    "childOf": [{"ID": "94c245b1-3be2-4eda-8737-e559f8cac2e5", "name": "Lisa Smith"}],
    "firstName": "Anna",
    "friendOf": [],
    "lastName": "Smith",
    "nickname": "Annie",
    "parentOf": [
        {"ID": "801225df-d5e1-4b01-adae-0cca392608da", "name": "Susan Smith"},
        {"ID": "4b3df73f-0174-4c20-b82c-89a1466689cb", "name": "John Smith"},
    ],
}

THREE_SAMPLE_PEOPLE = [
    PersonDataclass(
        ID="abcb029f-9562-46db-bfc9-b3fb00b60e2e",
        first_name="Anna",
        last_name="Smith",
        nickname="Annie",
        parent_of=[
            NameIdDataclass(ID="801225df-d5e1-4b01-adae-0cca392608da", name="Susan Smith"),
            NameIdDataclass(ID="4b3df73f-0174-4c20-b82c-89a1466689cb", name="John Smith"),
        ],
        child_of=[NameIdDataclass(ID="94c245b1-3be2-4eda-8737-e559f8cac2e5", name="Lisa Smith")],
        friend_of=[],
    ),
    PersonDataclass(
        ID="690d15ae-0f8c-4645-81b4-8a9eee2f2d4f",
        first_name="Bob",
        last_name="Smith",
        nickname="Bobby",
        parent_of=[],
        child_of=[NameIdDataclass(ID="4b3df73f-0174-4c20-b82c-89a1466689cb", name="John Smith")],
        friend_of=[],
    ),
    PersonDataclass(
        ID="f5ad3d6f-ea7b-4fb6-a5f3-40103fa2668f",
        first_name="Brian",
        last_name="Wilson",
        nickname="Bri",
        parent_of=[
            NameIdDataclass(ID="71823d62-0e66-47ca-a572-8349d8e21fe7", name="Liam Wilson"),
            NameIdDataclass(ID="d4b31401-9661-4f21-a751-f62acd745835", name="Emma Wilson"),
        ],
        child_of=[
            NameIdDataclass(ID="12d0869c-840a-4a2c-8ea2-c4bdd0b91592", name="Jessica Wilson")
        ],
        friend_of=[],
    ),
]

THREE_SAMPLE_PEOPLE_JSON = [
    {
        "ID": "abcb029f-9562-46db-bfc9-b3fb00b60e2e",
        "childOf": [{"ID": "94c245b1-3be2-4eda-8737-e559f8cac2e5", "name": "Lisa Smith"}],
        "firstName": "Anna",
        "friendOf": [],
        "lastName": "Smith",
        "nickname": "Annie",
        "parentOf": [
            {"ID": "801225df-d5e1-4b01-adae-0cca392608da", "name": "Susan Smith"},
            {"ID": "4b3df73f-0174-4c20-b82c-89a1466689cb", "name": "John Smith"},
        ],
    },
    {
        "ID": "690d15ae-0f8c-4645-81b4-8a9eee2f2d4f",
        "childOf": [{"ID": "4b3df73f-0174-4c20-b82c-89a1466689cb", "name": "John Smith"}],
        "firstName": "Bob",
        "friendOf": [],
        "lastName": "Smith",
        "nickname": "Bobby",
        "parentOf": [],
    },
    {
        "ID": "f5ad3d6f-ea7b-4fb6-a5f3-40103fa2668f",
        "childOf": [{"ID": "12d0869c-840a-4a2c-8ea2-c4bdd0b91592", "name": "Jessica Wilson"}],
        "firstName": "Brian",
        "friendOf": [],
        "lastName": "Wilson",
        "nickname": "Bri",
        "parentOf": [
            {"ID": "71823d62-0e66-47ca-a572-8349d8e21fe7", "name": "Liam Wilson"},
            {"ID": "d4b31401-9661-4f21-a751-f62acd745835", "name": "Emma Wilson"},
        ],
    },
]

LIST_PEOPLE = [
    PersonDataclass(
        ID="abcb029f-9562-46db-bfc9-b3fb00b60e2e",
        first_name="Anna",
        last_name="Smith",
        nickname="Annie",
        parent_of=[
            NameIdDataclass(ID="4b3df73f-0174-4c20-b82c-89a1466689cb", name="John Smith"),
            NameIdDataclass(ID="801225df-d5e1-4b01-adae-0cca392608da", name="Susan Smith"),
        ],
        child_of=[NameIdDataclass(ID="94c245b1-3be2-4eda-8737-e559f8cac2e5", name="Lisa Smith")],
        friend_of=[],
    ),
    PersonDataclass(
        ID="690d15ae-0f8c-4645-81b4-8a9eee2f2d4f",
        first_name="Bob",
        last_name="Smith",
        nickname="Bobby",
        parent_of=[],
        child_of=[NameIdDataclass(ID="4b3df73f-0174-4c20-b82c-89a1466689cb", name="John Smith")],
        friend_of=[],
    ),
    PersonDataclass(
        ID="f5ad3d6f-ea7b-4fb6-a5f3-40103fa2668f",
        first_name="Brian",
        last_name="Wilson",
        nickname="Bri",
        parent_of=[
            NameIdDataclass(ID="d4b31401-9661-4f21-a751-f62acd745835", name="Emma Wilson"),
            NameIdDataclass(ID="71823d62-0e66-47ca-a572-8349d8e21fe7", name="Liam Wilson"),
        ],
        child_of=[
            NameIdDataclass(ID="12d0869c-840a-4a2c-8ea2-c4bdd0b91592", name="Jessica Wilson")
        ],
        friend_of=[],
    ),
    PersonDataclass(
        ID="b3d0dfce-af08-4633-8ed8-5cae89dd8a1b",
        first_name="Clara",
        last_name="Duvall",
        nickname="Clary",
        parent_of=[
            NameIdDataclass(ID="3d660778-d473-4042-8670-95d7451fa32c", name="Peter Smith"),
            NameIdDataclass(ID="3d4320e2-83e2-4fde-8776-862d1fc07680", name="Mary Smith"),
        ],
        child_of=[NameIdDataclass(ID="4b3df73f-0174-4c20-b82c-89a1466689cb", name="John Smith")],
        friend_of=[],
    ),
    PersonDataclass(
        ID="f03b9fcc-e708-482a-9344-4f8e2da2930b",
        first_name="David",
        last_name="White",
        nickname="Dave",
        parent_of=[
            NameIdDataclass(ID="13b7c938-8f3b-4c2f-a6fb-3470dddca42b", name="Jake White"),
            NameIdDataclass(ID="245d82c1-b1b8-4a65-8ad4-0bd60f8bba8e", name="Mia White"),
        ],
        child_of=[
            NameIdDataclass(ID="fffd93c7-0042-4605-b1cb-a68a23074ee1", name="Rebecca White")
        ],
        friend_of=[],
    ),
    PersonDataclass(
        ID="223bae59-f829-401b-a985-08b37d6eb1c7",
        first_name="Ella",
        last_name="Brown",
        nickname="Ellie",
        parent_of=[
            NameIdDataclass(ID="d74ca3da-4d30-4142-9257-24af0fab7f31", name="Ian Brown"),
            NameIdDataclass(ID="f5337bc9-2a8b-42bf-b481-d50774acbc15", name="Sara Brown"),
        ],
        child_of=[NameIdDataclass(ID="e708394e-935c-405d-b2a2-6d68a1470d41", name="James Brown")],
        friend_of=[],
    ),
    PersonDataclass(
        ID="141574ad-be93-449d-9730-469d997d8562",
        first_name="Emily",
        last_name="Stevens",
        nickname="Emmy",
        parent_of=[
            NameIdDataclass(ID="1b4326e5-1853-48d1-ad69-ecee0259f2c4", name="Rachel Brown"),
            NameIdDataclass(ID="e708394e-935c-405d-b2a2-6d68a1470d41", name="James Brown"),
        ],
        child_of=[NameIdDataclass(ID="c3e9bab7-afa5-4cc9-a453-3985d992eb0a", name="Kate Brown")],
        friend_of=[],
    ),
    PersonDataclass(
        ID="d4b31401-9661-4f21-a751-f62acd745835",
        first_name="Emma",
        last_name="Wilson",
        nickname="Emmy",
        parent_of=[
            NameIdDataclass(ID="ddd9d0c1-36c6-4700-8086-ffdf6f1b0130", name="Sophie Wilson")
        ],
        child_of=[NameIdDataclass(ID="f5ad3d6f-ea7b-4fb6-a5f3-40103fa2668f", name="Brian Wilson")],
        friend_of=[],
    ),
    PersonDataclass(
        ID="d89e937b-f903-49f1-afdc-5ffa93b15d15",
        first_name="Eve",
        last_name="Brown",
        nickname="Evie",
        parent_of=[],
        child_of=[NameIdDataclass(ID="3dbb7473-347a-4f4c-9d6e-07c5cc00324f", name="Olivia Brown")],
        friend_of=[],
    ),
    PersonDataclass(
        ID="de3eba75-df67-4a4c-8d74-2dc194c21993",
        first_name="Frank",
        last_name="Smith",
        nickname="Frankie",
        parent_of=[],
        child_of=[NameIdDataclass(ID="801225df-d5e1-4b01-adae-0cca392608da", name="Susan Smith")],
        friend_of=[],
    ),
]


SAMPLE_ANCESTORS = [
    NameIdDataclass(ID="10d11ded-8550-44ac-9a30-1c5b453fe801", name="Zoe Taylor"),
    NameIdDataclass(ID="a2e47d96-2a7c-4132-a9e6-fbc5ddd2c05f", name="Richard Taylor"),
    NameIdDataclass(ID="034d840e-7d35-4c0e-9bc5-a82b9d2f7fa7", name="Grace Taylor"),
]
