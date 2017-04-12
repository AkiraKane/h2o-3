from __future__ import print_function
import sys
sys.path.insert(1,"../../")
import h2o
import time
from tests import pyunit_utils
import numpy
#----------------------------------------------------------------------
# This test is carried out to find out how the speed of parsing changes with
# code from Vlad.
#----------------------------------------------------------------------


def hdfs_orc_parser():

    # Check if we are running inside the H2O network by seeing if we can touch
    # the namenode.
    hadoop_namenode_is_accessible = pyunit_utils.hadoop_namenode_is_accessible()

    if hadoop_namenode_is_accessible:
        numTimes = 10
        hdfs_name_node = pyunit_utils.hadoop_namenode()
        allFiles = ["/datasets/bigCatFiles/tenThousandCat.csv", "/datasets/bigCatFiles/hundredThousandCat.csv",
                    "/datasets/bigCatFiles/oneMillionCat.csv"]

        for ind in range(0,len(allFiles)):  # run tests for 3 different sizes per Tomas request
            print("*******  Parsing file {0} ********".format(allFiles[ind]))
            runPerformance("hdfs://{0}{1}".format(hdfs_name_node, allFiles[ind]), numTimes)

    else:
        raise EnvironmentError


def runPerformance(url_csv, numTimes):
    columntypes = ["enum"]*10
    runtimes = []

    for ind in range(0, numTimes):
        startcsv = time.time()
        multi_file_csv = h2o.import_file(url_csv, na_strings=['\\N'], col_types=columntypes)
        endcsv = time.time()

        runtimes.append(endcsv-startcsv)
        h2o.remove(multi_file_csv)  # remove file to save space

    # write out summary run results
    print("*******************************")
    print("All run times {0}".format(runtimes))
    arr = numpy.array(runtimes)
    print(" Maximum run time is {0}, minimum run time is {1}".format(max(runtimes), min(runtimes)))
    print("Mean run time is {0}, std is {1}".format(numpy.mean(arr, axis=0), numpy.std(arr, axis=0)))
    print("*******************************")

if __name__ == "__main__":
    pyunit_utils.standalone_test(hdfs_orc_parser)
else:
    hdfs_orc_parser()