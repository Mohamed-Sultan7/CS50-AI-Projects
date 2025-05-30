import os
import random
import re

DAMPING = 0.85
SAMPLES = 10000


def main():
    corpus = crawl("corpus0")
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print("PageRank Results from Sampling (n = {})".format(SAMPLES))
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print("PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    pages = dict()

    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = set(re.findall(r'<a\s+href="([^"]+)"', contents))
            pages[filename] = set(
                link for link in links
                if link in os.listdir(directory) and link != filename
            )

    return dict(pages)


def transition_model(corpus, page, damping_factor):
    distribution = dict()
    N = len(corpus)

    if corpus[page]:
        for p in corpus:
            distribution[p] = (1 - damping_factor) / N
        linked = corpus[page]
        for p in linked:
            distribution[p] += damping_factor / len(linked)
    else:
        for p in corpus:
            distribution[p] = 1 / N

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    pagerank = {page: 0 for page in corpus}
    page = random.choice(list(corpus.keys()))

    for _ in range(n):
        pagerank[page] += 1
        model = transition_model(corpus, page, damping_factor)
        page = random.choices(list(model.keys()), weights=model.values(), k=1)[0]

    for p in pagerank:
        pagerank[p] /= n

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    N = len(corpus)
    pagerank = {page: 1 / N for page in corpus}
    converged = False

    while not converged:
        new_ranks = {}
        for page in corpus:
            total = 0
            for potential_linker in corpus:
                links = corpus[potential_linker]
                if not links:
                    total += pagerank[potential_linker] / N
                elif page in links:
                    total += pagerank[potential_linker] / len(links)
            new_ranks[page] = (1 - damping_factor) / N + damping_factor * total

        converged = all(abs(new_ranks[p] - pagerank[p]) < 0.001 for p in pagerank)
        pagerank = new_ranks

    return pagerank
