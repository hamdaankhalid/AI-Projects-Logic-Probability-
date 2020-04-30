import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    """transition model idea:
    an n by n matrix of (n is num of pages)
    rows: will be the page you are on
    columns: page that can be chosen for next and the probability
    """

    """
    For example, if the corpus were {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}, 
    the page was "1.html", and the damping_factor was 0.85, then the output of transition_model should be 
    {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}. 
    This is because with probability 0.85, we choose randomly to go from page 1 to either page 2 or page 3
     (so each of page 2 or page 3 has probability 0.425 to start), but every page gets an additional 0.05 because with 
     probability 0.15 we choose randomly among all three of the pages.
    """

    model = {}
    all_damped = (1-damping_factor)/ len(corpus)

    model[page] = all_damped
    #print(model)

    # if the page has links
    if len(corpus[page]) >= 1:
        for i in corpus[page]:

            model[i] = all_damped
            #print(model[i])

        for i in corpus[page]:
            model[i] += damping_factor/len(corpus[page])

    # if page has no links!
    else:
        for i in corpus[page]:
            model[i] = all_damped

        for i in corpus[page]:
            model[i] += damping_factor / len(corpus)

    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample_pr = {}
    for i in corpus.keys():
        sample_pr[i] = 0

    count = 0
    # create first sample:
    prev_page = random.choice(list(corpus.keys()))
    for i in corpus.keys():
        if i == prev_page:
            sample_pr[i] += 1/n

    while count <= n:
        #print(list(transition_model(corpus, prev_page, damping_factor)))
        # create n samples that transition from previous ones
        new_page = random.choices(list(transition_model(corpus, prev_page, damping_factor).keys()), list(transition_model(corpus,prev_page, damping_factor).values()))

        #unpack above
        for i in new_page:
            new_page = i
        for i in corpus.keys():
            if i == new_page:
                sample_pr[i] += 1/n

        prev_page = new_page
        count += 1

    return sample_pr


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n=1
    while True:
        pr = sample_pagerank(corpus, damping_factor, n)
        n += 1

        if round(sum(list(sample_pagerank(corpus, damping_factor, n).values())), 2) == 1:
            return pr


if __name__ == "__main__":
    main()

    #test transition model
    #print(transition_model({"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}} , "1.html", 0.85))