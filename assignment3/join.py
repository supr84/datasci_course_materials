import MapReduce
import sys
mr = MapReduce.MapReduce()
def mapper(record):
    orderId = record[1]
    mr.emit_intermediate(orderId, record)

def reducer(key, list_of_values):
    def copy(orderItem):
        items = []
        for item in orderItem:
            items.append(item)
        return items
    orderItem = []
    lineItems = []
    isOrderItemFound = False
    for v in list_of_values:
        if isOrderItemFound:
            result = copy(orderItem)
            result.extend(v)
            mr.emit( result )
        else:
            itemType = v[0]
            if v[0] == 'order':
                orderItem = v
                isOrderItemFound = True
                for li in lineItems:
                    result = copy(orderItem)
                    result.extend(li)
                    mr.emit( result )

if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
