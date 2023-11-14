from itertools import groupby
from typing import Dict, List

from app.models.peoples import NameIdDataclass, PersonDataclass


def construct_people_list_from_query_result(query_result: List[Dict]) -> List[PersonDataclass]:
    """Construct a list of Person with relevant information from the query result"""

    def extract_common_part(one_line: Dict) -> Dict:
        return {"ID": one_line["person"]["uuid"], "person": one_line["person"]}

    people = []
    for common, group in groupby(query_result, extract_common_part):
        parents = set()
        children = set()
        friends = set()
        for component in group:
            if "child" in component and component["child"] is not None:
                children.add(
                    (
                        ("ID", component["child"]["uuid"]),
                        (
                            "name",
                            f"{component['child']['firstname']} {component['child']['lastname']}",
                        ),
                    )
                )
            if "parent" in component and component["parent"] is not None:
                parents.add(
                    (
                        ("ID", component["parent"]["uuid"]),
                        (
                            "name",
                            f"{component['parent']['firstname']} "
                            f"{component['parent']['lastname']}",
                        ),
                    )
                )
            if "friend" in component and component["friend"] is not None:
                friends.add(
                    (
                        ("ID", component["friend"]["uuid"]),
                        (
                            "name",
                            f"{component['friend']['firstname']} "
                            f"{component['friend']['lastname']}",
                        ),
                    )
                )

        people.append(
            PersonDataclass(
                ID=common["ID"],
                first_name=common["person"]["firstname"],
                last_name=common["person"]["lastname"],
                nickname=common["person"]["nickname"] if "nickname" in common["person"] else None,
                parent_of=[
                    NameIdDataclass(ID=child[0][1], name=child[1][1]) for child in children
                ],
                child_of=[
                    NameIdDataclass(ID=parent[0][1], name=parent[1][1]) for parent in parents
                ],
                friend_of=[
                    NameIdDataclass(ID=friend[0][1], name=friend[1][1]) for friend in friends
                ],
            )
        )
    return people
