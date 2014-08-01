import MapReduce
import sys
mr = MapReduce.MapReduce()
def mapper(record):
    friendOf = record[0]
    friend = record[1]
    mr.emit_intermediate(friendOf, friend)
    mr.emit_intermediate(friend, friendOf)

def reducer(key, list_of_values):
    for v in list_of_values:
        if list_of_values.count(v) == 1:
            mr.emit( (key, v) )

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
