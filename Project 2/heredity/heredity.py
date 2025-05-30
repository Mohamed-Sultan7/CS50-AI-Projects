from typing import Dict, Set, List
import itertools

# Constants used in the heredity problem
PROBS = {
    "gene": {2: 0.01, 1: 0.03, 0: 0.96},
    "trait": {
        2: {True: 0.65, False: 0.35},
        1: {True: 0.56, False: 0.44},
        0: {True: 0.01, False: 0.99}
    },
    "mutation": 0.01
}


def joint_probability(people: Dict[str, dict], one_gene: Set[str], two_genes: Set[str], have_trait: Set[str]) -> float:
    prob = 1.0
    for person, data in people.items():
        mother = data['mother']
        father = data['father']
        genes = (2 if person in two_genes else 1 if person in one_gene else 0)
        has_trait = person in have_trait

        # If no parental info
        if not mother and not father:
            prob *= PROBS["gene"][genes] * PROBS["trait"][genes][has_trait]
        else:
            def pass_prob(parent):
                if parent in two_genes:
                    return 1 - PROBS["mutation"]
                elif parent in one_gene:
                    return 0.5
                else:
                    return PROBS["mutation"]

            mom_pass = pass_prob(mother)
            dad_pass = pass_prob(father)

            if genes == 2:
                prob *= mom_pass * dad_pass
            elif genes == 1:
                prob *= mom_pass * (1 - dad_pass) + (1 - mom_pass) * dad_pass
            else:
                prob *= (1 - mom_pass) * (1 - dad_pass)

            prob *= PROBS["trait"][genes][has_trait]
    return prob


def update(probabilities: Dict[str, dict], one_gene: Set[str], two_genes: Set[str],
           have_trait: Set[str], p: float) -> None:
    for person in probabilities:
        genes = (2 if person in two_genes else 1 if person in one_gene else 0)
        probabilities[person]["gene"][genes] += p
        probabilities[person]["trait"][person in have_trait] += p


def normalize(probabilities: Dict[str, dict]) -> None:
    for person in probabilities:
        for key in ["gene", "trait"]:
            total = sum(probabilities[person][key].values())
            for value in probabilities[person][key]:
                probabilities[person][key][value] /= total
