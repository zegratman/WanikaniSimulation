from model.item import ReviewEngine, ReviewItem, ReviewStats
import multiprocessing as mp

global items


def launch_engine(x):
    prob_array = [0.9534] * 8
    review_engine = ReviewEngine(prob_array)
    return review_engine.process(ReviewItem())


def myerrorcallback(r):
    print("My errorcallback " + str(r))


if __name__ == '__main__':

    n_iter = 1000000

    pool = mp.Pool(processes=mp.cpu_count())
    items = pool.map_async(launch_engine, range(n_iter), error_callback=myerrorcallback)

    stats = ReviewStats(items.get())

    print("<A> = {0}".format(stats.mean_a))
    print("<G> = {0}".format(stats.mean_g))
    print("<M> = {0}".format(stats.mean_m))
    print("<E> = {0}".format(stats.mean_e))

    print("Corr_A = {0}".format(stats.corr_a()))
    print("Corr_G = {0}".format(stats.corr_g()))
    print("Corr_M = {0}".format(stats.corr_m()))
    print("Corr_E = {0}".format(stats.corr_e()))
