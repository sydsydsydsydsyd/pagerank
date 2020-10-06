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

    # print(f"CORPUS: {corpus}")

    #initialize transition model dictionary with all values = 0
    tm = {}
    for p in corpus:
        tm[p] = 0

    # if page has no outgoing links
    if len(corpus[page]) == 0:
        #print(f"no outgoing links")
        # all items in the corpus have an equal chance
        random = 1 / len(corpus)
        for p in tm:
            tm[p] += random
    else:
        #print(f"has outgoing links")
        # chance for each page that is linked to page
        initial_val = damping_factor * len(list(corpus.get(page)))
        for p in corpus[page]:
            tm[p] += initial_val
        #print(f"initial tm: {tm}")

        # adjust for possibility of random choice
        adjust = (1 - damping_factor) / len(corpus)
        for p in tm:
            tm[p] += adjust

        #print(f"tm: {tm}")

    return tm


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # initialize empty pagerank dictionary with each val = 0
    pr = {}
    for page in corpus:
        pr[page] = 0
    # print(f"initial empty pr: {pr}")

    # choose initial random sample
    samp = random.choice(list(pr.keys())) # if error change pr.keys() to list(pr.keys())
    pr[samp] += (1 / n)
    # print(f"initial sample: {samp}, {pr[samp]}")

    #loop n times
    for s in range(n - 1):
        tm = transition_model(corpus, samp, damping_factor)
        nsamp = random.choices(list(tm.keys()), weights = tm.values(), k = 1) # if error then change tm.keys() to list(tm.keys())
        pr[nsamp[0]] += (1 / n)
        samp = nsamp[0]

        #print(f"annoyingly long list of samples taken: {samp}")

    """
    # check if add up to 1
    count = 0
    for i in pr.values():
        count += i
    print(f"count: {count}")
    """

    return pr


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    """

    # initialize pagrank dictionary with all values as 1/N
    N = len(corpus)
    pr = {}
    for page in corpus:
        pr[page] = 1 / N

    margins = [False, False]
    # keep looping until all margins are less than 0.001
    #CAUSES INFINITE LOOP
    while margins.count(True) != len(pr):

        # go through every page in dictionary
        for p in pr:
            opr = pr[p]

            # get list of pages that reference p
            all_i = []
            for page in corpus:
                # if page doesn't link to any others
                if len(corpus[page]) == 0:
                    all_i.append(page)
                if p in corpus[page]:
                    all_i.append(page)

            # calculate P if not chosen randomly
            for i in all_i:
                adjust = damping_factor * (pr[i] / len(all_i))

            # total P
            npr = ((1 - damping_factor) / N) + adjust

            pr[p] = npr

            # update list of margins
            margins.pop(0)
            margins.append(abs(opr - npr) < 0.001)

    # check if sum to 1
    count = 0
    for i in pr.values():
        count += i
    print(f"count: {count}")

    return pr
    """
    return NotImplementedError

if __name__ == "__main__":
    main()
