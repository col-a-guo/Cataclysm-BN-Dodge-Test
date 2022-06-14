from numpy import arange

def dodge_roll(numer, add, excess, subtract, powernum, powerdenom):
    fail_chance = 0.5
    if excess-subtract < 0:
        fail_d = (add-((-(excess-subtract))**powernum)**(1/powerdenom))
        if fail_d <= 0:
            fail_chance = 0.9999
        else:
            fail_chance = numer/fail_d
    else:
        fail_d = (add+((excess-subtract)**powernum)**(1/powerdenom))
        if fail_d <= 0:
            fail_chance = 0.9999
        else:
            fail_chance = numer/fail_d
    if fail_chance >= 1:
        fail_chance = 0.9999
    if fail_chance <= 0:
        fail_chance = 0.0001

    return fail_chance

def plunge_bench_error_2_5_1(numer, add, subtract, powernum, powerdenom):

    old_roll = 0
    new_roll = dodge_roll(numer, add, 6, subtract, powernum, powerdenom)
    current_plunge = 1
    current_2_3_error = 1
    bench_error = 1
    for i in arange(6,-1,-1):
        old_roll = new_roll
        new_roll = dodge_roll(numer, add, i, subtract, powernum, powerdenom)
        if abs(new_roll/old_roll) > current_plunge:
            current_plunge = abs(new_roll/old_roll)
        if i == 0:
            bench_error *= max(new_roll/.5, .5/new_roll)**10

    for i in arange(1,11):
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
            if .06 < new_roll < .14:
                bench_error *= 1
            else:
                # print("new best 5")
                # print(new_roll)
                # print(1+min((abs(new_roll-.06))/.06, (abs(new_roll-.14))/.14))
                bench_error*=1+min((abs(new_roll-.06))/.06, (abs(new_roll-.14))/.14)
        elif i == 10:
            if .02 < new_roll < .05:
                bench_error*=1
            else:
                # print("new best 10")
                # print(new_roll)
                # print(1+min((abs(new_roll-.05))/.05, (abs(new_roll-.02))/.02))
                bench_error*=1+min((abs(new_roll-.05))/.05, (abs(new_roll-.02))/.02)
    return bench_error, current_2_3_error, current_plunge

best_list = [100,0,0,0]
for numer_i in arange (1,5,0.1):
    for add_i in arange(1,10,0.02):
        for sub in arange(1,2,0.2):
            for i in arange(1, 11):
                for j in arange (1, 11):
                    bench, err2_3, plunge = plunge_bench_error_2_5_1(numer_i, add_i, sub, i*2+1, j*2+1)
                    err =  (bench*err2_3)*plunge**3
                    #print(err)
                    if err < best_list[0]:
                        best_list[0] = err
                        best_list[1] = i
                        best_list[2] = j
                        best_list[3] = f"plunge {plunge}, numer {numer_i}, add {add_i}, sub {sub}"
                        print(f"Best so far: {best_list}, bench {bench}, 2/3 bench {err2_3}, plunge {plunge}, numer {numer_i}, add {add_i}, sub {sub}")
print(f"Best so far: {best_list}, bench {bench}, 2/3 bench {err2_3}, plunge {plunge}, numer {numer_i}, add {add_i}, sub {sub}")
