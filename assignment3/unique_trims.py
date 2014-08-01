import MapReduce
import sys
mr = MapReduce.MapReduce()
def mapper(record):
    nucleotides = record[1]
    mr.emit_intermediate(nucleotides[:len(nucleotides)-10], record[0])

def reducer(key, list_of_values):
    mr.emit( key )

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
