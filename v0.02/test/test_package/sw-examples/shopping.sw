-- learn the prices for some items:
the-price-for |apple> => 0.6|dollar>
the-price-for |orange> => 0.8|dollar>
the-price-for |milk> => 2.3|dollar>
the-price-for |coffee> => 5.5|dollar>
the-price-for |steak> => 9|dollar>

-- learn our shopping list:
the |shopping list> => |orange> + 4|apple> + |milk> + |coffee> + |steak>


price-is-defined |*> #=> do-you-know the-price-for |_self>
the-list-of |available items> #=> such-that[price-is-defined] the |shopping list>

buy (*,*) #=> consume-reaction( |_self2>, the-price-for |_self1>, |_self1>)


-- what is the price for the available items?
the-price-for the-list-of |available items>

-- now go shopping:
buy(the-list-of |available items>, 30 |dollar>)

