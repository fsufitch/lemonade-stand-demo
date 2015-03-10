from lemonade_stand import LemonadeStand, NotEnoughLemonsException

num_lemons = input("Number of starting lemons? ")
price = input("Lemonade price? ")

num_lemons = int(num_lemons)
price = float(price)

stand = LemonadeStand(num_lemons, price)

while True:
    print("----------\n")
    try:
        num_sell = int(input("Number of lemonades to sell? "))
    except EOFError:
        # Input is done
        break
    except ValueError as e:
        # Invalid input
        print("Invalid input:", e)
        continue

    total_price = stand.get_total(num_sell)
    confirmation = input("Selling %s lemonades for $%.2f. Confirm? (y/N) " % (num_sell, total_price))
    if confirmation.lower()=='y':
        try:
            sale = stand.sell(num_sell)
        except NotEnoughLemonsException:
            print("Not enough lemons for that sale. Sale canceled!")
        else:
            print("[%.2f] Sold %s lemonades for $%.2f" % (sale['time'], sale['amount'], sale['income']))
            print("Lemons remaining:", stand.supply)
    else:
        print("Sale canceled")

print("\n\nDone!")
print("Lemonades sold:", stand.total_lemonades_sold())
print("Total income:", stand.total_income())
print("Sale window:", stand.sale_window())

        
