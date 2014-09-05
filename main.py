__author__ = 'qqy'

import os
import ast
import sys
import matplotlib.pyplot as plt

def save_src(path, lst, ext='txt', verbose=True):
    # Extract the directory and filename from the given path
    directory = os.path.split(path)[0]
    filename = "%s.%s" % (os.path.split(path)[1], ext)
    if directory == '':
        directory = '.'

    # If the directory does not exist, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    # The final path to save to
    savepath = os.path.join(directory, filename)

    if verbose:
        print("Saving points to '%s'..." % savepath),

    with open(savepath, 'w') as fhand:
        for item in lst:
            fhand.write(str(item[0]) + ' ' + str(item[1]) + '\n')

    if verbose:
        print "Done"


def save_fig(path, ext='png', close=True, verbose=True):
    """Save a figure from pyplot.

    Parameters
    ----------
    path : string
        The path (and filename, without the extension) to save the
        figure to.

    ext : string (default='png')
        The file extension. This must be supported by the active
        matplotlib backend (see matplotlib.backends module).  Most
        backends support 'png', 'pdf', 'ps', 'eps', and 'svg'.

    close : boolean (default=True)
        Whether to close the figure after saving.  If you want to save
        the figure multiple times (e.g., to multiple formats), you
        should NOT close it in between saves or you will have to
        re-plot it.

    verbose : boolean (default=True)
        Whether to print information about when and where the image
        has been saved.

    """

    # Extract the directory and filename from the given path
    directory = os.path.split(path)[0]
    filename = "%s.%s" % (os.path.split(path)[1], ext)
    if directory == '':
        directory = '.'

    # If the directory does not exist, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    # The final path to save to
    savepath = os.path.join(directory, filename)

    if verbose:
        print("Saving figure to '%s'..." % savepath),

    # Actually save the figure
    plt.savefig(savepath)

    # Close it
    if close:
        plt.close()

    if verbose:
        print("Done")

def step1(econ_journal_ids, econ_only=True):
    print "Step1"
    files = os.listdir(os.getcwd())
    for file in files:
        if not file.endswith(".txt"): continue
        if not file.startswith("cite_ref"): continue
        year = file[-8:-4]
        print year
        counter = {}
        num_total_parent_paper = 0
        with open(file) as fhand:
            for line in fhand:
                if line.startswith("year"): continue
                cat = line.split()[1]
                if econ_only:
                    if cat not in econ_journal_ids: continue
                num_total_parent_paper += 1
                atpos = line.find("Counter")
                counter_start = atpos + len("Counter") + 1
                counter_end = line.find(")", counter_start)
                counter_cnt = line[counter_start:counter_end]
                counter_cnt = ast.literal_eval(counter_cnt)
                for key, val in counter_cnt.items():
                    counter[key] = counter.get(key, 0) + val

        #print len(counter)
        ratio = []
        for key, val in counter.items():
            try:
                ratio.append((int(key), float(val) / num_total_parent_paper))
            except:
                continue
        ratio.sort()

        x = list()
        y = list()
        for item in ratio:
            #ignore illegal points
            if key == "NULL": continue
            x.append(item[0])
            y.append(item[1])
        plt.plot(x, y, 'o')
        plt.axis([int(year) - 50,int(year) + 10, 0, max(y) + 0.5 ])
        if econ_only:
            save_fig("results/step1/econ/img/" + file[0:(len(file) - 4)])
            save_src("results/step1/econ/src/" + file[0:(len(file) - 4)], ratio)
        else:
            save_fig("results/step1/all/img/" + file[0:(len(file) - 4)])
            save_src("results/step1/all/src/" + file[0:(len(file) - 4)], ratio)

def step2(econ_journal_ids):
    #Find the ratio of econ papers
    print "Step2"
    files = os.listdir(os.getcwd())

    ratio_of_econ_paper = []
    for file in files:
        if not file.endswith(".txt"): continue
        if not file.startswith("cite_ref"): continue
        year = file[-8:-4]

        num_total_econ_paper = 0
        num_total_parent_paper = 0
        with open(file) as fhand:
            for line in fhand:
                if line.startswith("year"): continue
                cat = line.split()[1]
                if cat in econ_journal_ids:
                    num_total_econ_paper += 1
                num_total_parent_paper += 1

        try:
            ratio_of_econ_paper.append((int(year), float(num_total_econ_paper) / num_total_parent_paper))
        except:
            continue

    ratio_of_econ_paper.sort()
    x = list()
    y = list()
    for item in ratio_of_econ_paper:
        x.append(int(item[0]))
        y.append(item[1])
    plt.plot(x, y, 'o')
    save_fig("results/step2/econ/img/ratio")
    save_src("results/step2/econ/src/ratio", ratio_of_econ_paper)

def step3(econ_journal_ids):
    #Find the total number of papers of each kind
    print "Step3"
    files = os.listdir(os.getcwd())

    num_total_econ_paper_lst= []
    num_total_parent_paper_lst = []
    for file in files:
        if not file.endswith(".txt"): continue
        if not file.startswith("cite_ref"): continue
        year = file[-8:-4]

        num_total_econ_paper = 0
        num_total_parent_paper = 0
        with open(file) as fhand:
            for line in fhand:
                if line.startswith("year"): continue
                cat = line.split()[1]
                if cat in econ_journal_ids:
                    num_total_econ_paper += 1
                num_total_parent_paper += 1

        try:
            num_total_parent_paper_lst.append((int(year), num_total_parent_paper))
            num_total_econ_paper_lst.append((int(year), num_total_econ_paper))
        except:
            continue

    num_total_parent_paper_lst.sort()
    num_total_econ_paper_lst.sort()

    x = list()
    y = list()
    for item in num_total_parent_paper_lst:
        x.append(int(item[0]))
        y.append(item[1])
    plt.plot(x, y, 'o')
    plt.axis([int(year) - 50,int(year) + 10, 0, max(y) + 0.1 * max(y) ])
    save_fig("results/step3/econ/img/econ_number" )
    save_src("results/step3/econ/src/econ_number", num_total_econ_paper_lst)

    x = list()
    y = list()
    for item in num_total_parent_paper_lst:
        x.append(int(item[0]))
        y.append(item[1])
    plt.plot(x, y, 'o')
    save_fig("results/step3/all/img/all_number")
    save_src("results/step3/all/src/all_number", num_total_parent_paper_lst)


def step5(econ_journal_ids, econ_only=True):
    print "Step5"
    files = os.listdir(os.getcwd())

    sum_list = {}
    for file in files:
        if not file.endswith(".txt"): continue
        if not file.startswith("cite_ref"): continue
        year = file[-8:-4]

        with open(file) as fhand:
            for line in fhand:
                if line.startswith("year"): continue

                cat = line.split()[1]
                if econ_only:
                    if cat not in econ_journal_ids: continue

                atpos = line.find("Counter")
                counter_start = atpos + len("Counter") + 1
                counter_end = line.find(")", counter_start)
                counter_cnt = line[counter_start:counter_end]
                counter_cnt = ast.literal_eval(counter_cnt)
                try:
                    sum_list[year] = sum_list.get(year, 0) + sum(counter_cnt.values())
                except:
                    continue

    t = []

    for key, val in sum_list.items():
        try:
            t.append((int(key), val))
        except:
            continue
    t.sort()

    sum_list = t

    x = list()
    y = list()
    for item in sum_list:
        try:
            x.append(int(item[0]))
            y.append(item[1])
        except:
            continue
    plt.plot(x, y, 'o')
    if econ_only:
        save_fig("results/step5/econ/img/number")
        save_src("results/step5/econ/src/number", sum_list)
    else:
        save_fig("results/step5/all/img/number")
        save_src("results/step5/all/src/number", sum_list)


def parse_inputfile(input_filename):
    path = os.path.join(os.getcwd(), input_filename)
    fhand = open(path)
    t = list()
    for line in fhand:
        line = line.split()
        if len(line) == 0: continue
        t = t + line

    journal_ids = t

    if len(t) <= 0:
        print "Input Error: too few eco paper ids"
        sys.exit()
    for i, journal_id in enumerate(journal_ids):
        try:
            int(journal_id)
        except:
            print "Input Error:", i + 1, " th element must be a number instead of :", journal_ids[i]
            sys.exit()
    return journal_ids

def main():
    econ_journal_ids = parse_inputfile("econ_journal_ids.txt")

    step2(econ_journal_ids)
    step3(econ_journal_ids)
    for flag in [True, False]:
        step1(econ_journal_ids, econ_only=flag)
        step5(econ_journal_ids, econ_only=flag)


if __name__ == "__main__":
    main()