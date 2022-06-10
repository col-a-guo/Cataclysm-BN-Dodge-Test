def dodge_roll(numer, add, excess, subtract, powernum, powerdenom):
    if excess-subtract < 0:
        return numer/(add+((-(excess-subtract))**powernum)**(1/powerdenom))
    else:
        return numer/(add+((excess-subtract)**powernum)**(1/powerdenom))

def plunge_bench_error_2_5_1(powernum, powerdenom):
    numer = 2
    add = 5
    subtract = 1
    old_roll = 0
    new_roll = dodge_roll(numer, add, 6, subtract, powernum, powerdenom)
    current_plunge = 1
    current_2_3_error = 1
    bench_error = 1
    for i in range(6,-1,-1):
        old_roll = new_roll
        new_roll = dodge_roll(numer, add, i, subtract, powernum, powerdenom)
        if abs(new_roll/old_roll) > current_plunge:
            current_plunge = abs(new_roll/old_roll)

    for i in range(1,11):
        old_roll = new_roll
        new_roll = dodge_roll(numer, add, i, subtract, powernum, powerdenom)
        if old_roll/(1-new_roll) > current_plunge:
            current_plunge = old_roll/(1-new_roll)
        if i == 2:
            if new_roll < .25:
                current_2_3_error = 1+abs(new_roll-0.25)
        elif i == 3:
            if new_roll > .25 and new_roll-0.25 < current_2_3_error:
                current_2_3_error = 1+abs(new_roll-0.25)
        elif i == 5:
            if .07 < new_roll < .13:
                bench_error *= 1
            else:
                bench_error*=1+min(abs(new_roll-.07)/.07, (abs(new_roll-.13))/.13)
        elif i == 10:
            if .02 < new_roll < .5:
                bench_error *= 1
            else:
                bench_error*=1+min(abs(new_roll-.05)/.05, (abs(new_roll-.02))/.02)
        if new_roll > 1:
            print(new_roll)
            print(numer, add, i, subtract, powernum, powerdenom)
            bench_error *= 10000
    return bench_error, current_2_3_error, current_plunge

best_list = [100,0,0]
for i in range(3, 11):
    for j in range (3, 11):
        bench, err2_3, plunge = plunge_bench_error_2_5_1(i*2+1, j*2+1)
        err =  bench*err2_3*plunge
        #print(err)
        if err < best_list[0]:
            best_list[0] = err
            best_list[1] = i
            best_list[2] = j
            print(f"Best so far: {best_list}, bench {bench}, 2/3 bench {err2_3}, plunge {plunge}")