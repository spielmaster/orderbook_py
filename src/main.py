import orderbook_init
import visuals

if __name__ == '__main__':

    book = orderbook_init.triangular_symmetrical(100, .01, .05, 
                                               1000, 10000, 20)

    visuals.depth_chart(book)

    print('done')
