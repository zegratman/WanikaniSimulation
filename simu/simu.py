from model.item import ReviewEngine, ReviewItem, ReviewStats

if __name__ == '__main__':

    n_iter = 1000
    prob_array = [0.9534] * 8
    review_engine = ReviewEngine(prob_array)

    items = []

    for i in range(n_iter):
        items.append(review_engine.process(ReviewItem()))

    stats = ReviewStats(items)

    print("<A> = {0}".format(stats.mean_a()))
    print("<G> = {0}".format(stats.mean_g()))
    print("<M> = {0}".format(stats.mean_m()))
    print("<E> = {0}".format(stats.mean_e()))

    print("Corr_A = {0}".format(stats.corr_a()))
    print("Corr_G = {0}".format(stats.corr_g()))
    print("Corr_M = {0}".format(stats.corr_m()))
    print("Corr_E = {0}".format(stats.corr_e()))
