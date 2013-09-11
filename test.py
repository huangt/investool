import ystockquote
import csv

#print ystockquote.get_price('GOOG')

#print ystockquote.get_all('MSFT')

#print ystockquote.get_book_value('GOOG')

csvfile = open('nasdaqlist.csv', 'rb')
reader = csv.reader(csvfile)

rownum = 0
stocksymbols = []
for row in reader:
    # Save header row.
    if rownum == 0:
        header = row
    else:
        #print row
        stocksymbols.append(row[0])
        #colnum = 0
        #for col in row:
        #    print '%-8s: %s' % (header[colnum], col)
        #    colnum += 1
             
    rownum += 1
 
csvfile.close()

results = []
for symbol in stocksymbols:
    price = float(ystockquote.get_price(symbol))
    bookvalue = float(ystockquote.get_book_value(symbol)) * 0.8
    if (price < bookvalue):
        print symbol
        results.append(symbol)

print len(results)
