import MapReduce
import sys
mr = MapReduce.MapReduce()
def mapper(record):
    matrix = record[0]
    if matrix == 'a':
        i = record[1]
        for ka in range(0, 5):
            mr.emit_intermediate((i, ka), record)
    else:
        kb = record[2]
        for i in range(0, 5):
            mr.emit_intermediate((i,kb),  record)

def reducer(key, list_of_values):
    avalues = {}
    bvalues= {}
    for v in list_of_values:
        matrix = v[0]
        rowId = v[1]
        colId= v[2]
        val = v[3]
        if matrix == 'a':
            avalues[colId] = val
        else:
            bvalues[rowId] = val
    cellValue = 0 
    for j in avalues.keys():
        if bvalues.has_key(j):
            cellValue += avalues[j]*bvalues[j]
    if cellValue > 0:
        mr.emit( (key[0],key[1], cellValue) )

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
