import csv
import itertools
import sys
from pomegranate import *


PROBS = {
    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },
    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait

    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    # construct bayesian network from dictionary
    # construct bayesian network from dictionary
    # Now for parents make discrete distribution nodes
    left_parent = Node(DiscreteDistribution({
        "2": 0.01,
        "1": 0.03,
        "0": 0.96,
    }), "left_parent")

    right_parent = Node(DiscreteDistribution({
        "2": 0.01,
        "1": 0.03,
        "0": 0.96,
    }), "right_parent")

    # Make Has traits for left_parent and right_parent
    left_trait = Node(ConditionalProbabilityTable([

        # Probability of trait given copies of gene

        ["0", "True", 0.01],
        ["0", "False", 0.99],

        ["1", "True", 0.56],
        ["1", "False", 0.44],

        ["2", "True", 0.65],
        ["2", "False", 0.35],

    ], [left_parent.distribution]), "left_trait")

    right_trait = Node(ConditionalProbabilityTable([

        ["0", "True", 0.01],
        ["0", "False", 0.99],

        ["1", "True", 0.56],
        ["1", "False", 0.44],

        ["2", "True", 0.65],
        ["2", "False", 0.35]

    ], [right_parent.distribution]), "right_trait")

    # make childGene node which is conditional on MotherGene and FatherGene
    child_gene = Node(ConditionalProbabilityTable([

        # probability both parents give neither gene
        ['0', '0', '0', 0.98],
        ["0", "0", "1", 0.01],
        ["0", "0", "2", 0.01],

        ["0", "1", "0", 0.495],
        ["0", "1", "1", 0.495],
        ["0", "1", "2", 0.01],

        ["0", "2", "0", 0.495],
        ["0", "2", "1", 0.01],
        ["0", "2", "2", 0.495],

        ["1", "0", "0", 0.495],
        ["1", "0", "1", 0.495],
        ["1", "0", "2", 0.01],

        ["1", "1", "0", 0.01],
        ['1', '1', '1', 0.48],
        ["1", "1", "2", 0.01],

        ["1", "2", "0", 0.01],
        ["1", "2", "1", 0.495],
        ["1", "2", "2", 0.495],

        ["2", "0", "0", 0.495],
        ["2", "0", "1", 0.01],
        ["2", "0", "2", 0.495],

        ["2", "1", "0", 0.01],
        ["2", "1", "1", 0.495],
        ["2", "1", "2", 0.495],

        ['2', '2', "0", 0.01],
        ["2", "2", "1", 0.01],
        ["2", "2", "2", 0.98],

    ], [left_parent.distribution, right_parent.distribution]), "child_gene")

    # make child has trait
    child_trait = Node(ConditionalProbabilityTable([

        ["0", "True", 0.01],
        ["0", "False", 0.99],

        ["1", "True", 0.56],
        ["1", "False", 0.44],

        ["2", "True", 0.65],
        ["2", "False", 0.35],

    ], [child_gene.distribution]), "child_trait")

    model = BayesianNetwork()
    model.add_states(left_parent, right_parent, left_trait, right_trait, child_gene, child_trait)
    model.add_edge(left_parent, left_trait)
    model.add_edge(right_parent, right_trait)
    model.add_edge(left_parent, child_gene)
    model.add_edge(right_parent, child_gene)
    model.add_edge(child_gene, child_trait)
    model.bake()

    final = 1
    # separate children in people
    children_list = []
    for n in people:
        # print(people[n]["mother"])
        if people[n]["mother"] != None and people[n]["father"] != None:
            children_list.append(people[n])

    # loop through children list
    for child in children_list:
        # check if it has_trait and set trait,
        if child["name"] in have_trait:
            child_tra = "True"
        else:
            child_tra = "False"

        # check if in one_gene or two_gene , else gene is 0
        if child["name"] in one_gene:
            child_g = "1"
        elif child["name"] in two_genes:
            child_g = "2"
        else:
            child_g = "0"

        # for every parent of that child check , check if in has_trait and set trait, check if in one_gene or two_gene , else gene is 0
        if child["mother"] in have_trait:
            left_tra = "True"
        else:
            left_tra = "False"

            # check if in one_gene or two_gene , else gene is 0
        if child["mother"] in one_gene and child["mother"] is not None:
            left_par = "1"
        elif child["mother"] in two_genes and child["mother"] is not None:
            left_par = "2"
        else:
            left_par = "0"

        if child["father"] in have_trait:
            right_tra = "True"
        else:
            right_tra = "False"

        # check if in one_gene or two_gene , else gene is 0

        if child["father"] in one_gene:
            right_par = "1"
        elif child["father"] in two_genes:
            right_par = "2"
        else:
            right_par = "0"

        # find probability by child

        # evidence = {
        #     "left_parent": left_par,
        #     "right_parent": right_par,
        #     "left_trait": left_tra,
        #     "right_trait": right_tra,
        #     "child_gene": child_g,
        #     "child_trait": child_tra
        # }

        evidence = [
            [
                left_par, right_par, left_tra, right_tra, child_g, child_tra
            ]
        ]

        pr = model.probability(evidence)

        final = final * pr

    return final


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities:

        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p

        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        total_genes = probabilities[person]["gene"][0]+probabilities[person]["gene"][1]+probabilities[person]["gene"][2]
        total_traits = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        print("****")
        probabilities[person]["gene"][1] = probabilities[person]["gene"][1] / total_genes
        probabilities[person]["gene"][2] = probabilities[person]["gene"][2] / total_genes
        probabilities[person]["gene"][0] = probabilities[person]["gene"][0] / total_genes

        probabilities[person]["trait"][True] = probabilities[person]["trait"][True] / total_traits
        probabilities[person]["trait"][False] = probabilities[person]["trait"][False] / total_traits


if __name__ == "__main__":

    main()

