import csv
import itertools
import sys


# USED HELP USING ED FORUM https://us.edstem.org/courses/176/discussion/39305
# FOR FINDING GENE PROBABILITY WHEN DEALING WITH CHILD

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
    final = []
    for n in people:
        # parent
        if people[n]["mother"] == None and people[n]["father"] == None:
        # for parent figure out probability
            if n in one_gene:
                parent_gene_prob = PROBS["gene"][1]

            elif n in two_genes:
                parent_gene_prob = PROBS["gene"][2]

            else:
                parent_gene_prob = PROBS["gene"][0]

            if n in have_trait and parent_gene_prob == PROBS["gene"][0]:
                parent_trait_prob = PROBS["trait"][0][True]

            elif n not in have_trait and parent_gene_prob == PROBS["gene"][0]:
                parent_trait_prob = PROBS["trait"][0][False]

            elif n in have_trait and parent_gene_prob == PROBS["gene"][1]:
                parent_trait_prob = PROBS["trait"][1][True]

            elif n not in have_trait and parent_gene_prob == PROBS["gene"][1]:
                parent_trait_prob = PROBS["trait"][1][False]

            elif n in have_trait and parent_gene_prob == PROBS["gene"][2]:
                parent_trait_prob = PROBS["trait"][2][True]

            elif n not in have_trait and parent_gene_prob == PROBS["gene"][2]:
                parent_trait_prob = PROBS["trait"][2][False]

            final.append(parent_gene_prob*parent_trait_prob)

        #child
        else:
            # if child then see if child in one gene two gene or no gene
            # if in one gene, find probability of that
            if n in one_gene:
                # two ways for this to happen, either from mother or from father
                # from mother not father
                if people[n]["mother"] in one_gene:
                    gene_prob_from_mother = 0.5

                elif people[n]["mother"] in two_genes:
                    gene_prob_from_mother = 0.99

                else:
                    gene_prob_from_mother = PROBS["mutation"]

                if people[n]["father"] in one_gene:
                    gene_prob_from_mother_father = 0.5

                elif people[n]["father"] in two_genes:
                    gene_prob_from_mother_father = 0.01

                else:
                    gene_prob_from_mother_father = 0.99

                # from father not mother
                    # from mother not father
                if people[n]["father"] in one_gene:
                    gene_prob_from_father = 0.5

                elif people[n]["father"] in two_genes:
                    gene_prob_from_father = 0.99

                else:
                    gene_prob_from_father = PROBS["mutation"]

                if people[n]["mother"] in one_gene:
                    gene_prob_from_father_mother = 0.5

                elif people[n]["mother"] in two_genes:
                    gene_prob_from_father_mother = 0.01

                else:
                    gene_prob_from_father_mother = 0.99

                probability_gene = (gene_prob_from_mother * gene_prob_from_mother_father) + (gene_prob_from_father * gene_prob_from_father_mother)

            # if child in two gene find probability of that
            elif n in two_genes:
                # parents pass one gene individually
                if people[n]["mother"] in one_gene:
                    prob_gene_mother = 0.5

                elif people[n]["mother"] in two_genes:
                    prob_gene_mother = 0.99

                else:
                    prob_gene_mother = 0.01

                if people[n]["father"] in one_gene:
                    prob_gene_father = 0.5

                elif people[n]["father"] in two_genes:
                    prob_gene_father = 0.99

                else:
                    prob_gene_father = 0.01

                probability_gene = prob_gene_mother*prob_gene_father

            # if child in no gene find probability of that
            else:
                # all the ways a child could have no genes
                if people[n]["mother"] in one_gene:
                    prob_gene_mother = 0.5

                elif people[n]["mother"] in two_genes:
                    prob_gene_mother = 0.01

                else:
                    prob_gene_mother = 0.99

                if people[n]["father"] in one_gene:
                    prob_gene_father = 0.5

                elif people[n]["father"] in two_genes:
                    prob_gene_father = 0.01

                else:
                    prob_gene_father = 0.99

                probability_gene = prob_gene_father*prob_gene_mother

    #################By here we have found child_gene_prob##################

            # if child then for trait find probability
            if n in have_trait and n in one_gene:
                child_prob_trait = PROBS["trait"][1][True]
            elif n not in have_trait and n in one_gene:
                child_prob_trait = PROBS["trait"][1][False]

            elif n in have_trait and n in two_genes:
                child_prob_trait = PROBS["trait"][2][True]
            elif n not in have_trait and n in two_genes:
                child_prob_trait = PROBS["trait"][2][False]

            elif n in have_trait and n not in one_gene and n not in two_genes:
                child_prob_trait = PROBS["trait"][0][True]
            elif n not in have_trait and n not in one_gene and n not in two_genes:
                child_prob_trait = PROBS["trait"][0][False]

            final.append(probability_gene * child_prob_trait)
    result = 1
    for x in final:
        result = result * x

    return result


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
        total_genes = probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + \
                      probabilities[person]["gene"][2]
        total_traits = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]

        probabilities[person]["gene"][1] = probabilities[person]["gene"][1] / total_genes
        probabilities[person]["gene"][2] = probabilities[person]["gene"][2] / total_genes
        probabilities[person]["gene"][0] = probabilities[person]["gene"][0] / total_genes

        probabilities[person]["trait"][True] = probabilities[person]["trait"][True] / total_traits
        probabilities[person]["trait"][False] = probabilities[person]["trait"][False] / total_traits


if __name__ == "__main__":
    main()
