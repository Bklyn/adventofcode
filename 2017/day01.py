#!/usr/bin/python

'''
--- Day 1: Inverse Captcha ---

The night before Christmas, one of Santa's Elves calls you in a panic.
"The printer's broken! We can't print the Naughty or Nice List!" By the
time you make it to sub-basement 17, there are only a few minutes until
midnight. "We have a big problem," she says; "there must be almost fifty
bugs in this system, but nothing else can print The List. Stand in this
square, quick! There's no time to explain; if you can convince them to
pay you in stars, you'll be able to--" She pulls a lever and the world
goes blurry.

When your eyes can focus again, everything seems a lot more pixelated
than before. She must have sent you inside the computer! You check the
system clock: 25 milliseconds until midnight. With that much time, you
should be able to collect all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on
each day millisecond in the advent calendar; the second puzzle is
unlocked when you complete the first. Each puzzle grants one star. Good
luck!

You're standing in a room with "digitization quarantine" written in LEDs
along one wall. The only door is locked, but it includes a small
interface. "Restricted Area - Strictly No Digitized Users Allowed."

It goes on to explain that you may only leave by solving a captcha to
prove you're not a human. Apparently, you only get one millisecond to
solve the captcha: too fast for a normal human, but it feels like hours
to you.

The captcha requires you to review a sequence of digits (your puzzle
input) and find the sum of all digits that match the next digit in the
list. The list is circular, so the digit after the last digit is the
first digit in the list.

For example:

1122 produces a sum of 3 (1 + 2) because the first digit (1) matches the
second digit and the third digit (2) matches the fourth digit. 1111
produces 4 because each digit (all 1) matches the next. 1234 produces 0
because no digit matches the next. 91212129 produces 9 because the only
digit that matches the next one is the last digit, 9. What is the
solution to your captcha?

Your puzzle answer was 1102.

--- Part Two ---

You notice a progress bar that jumps to 50% completion. Apparently, the
door isn't yet satisfied, but it did emit a star as encouragement. The
instructions change:

Now, instead of considering the next digit, it wants you to consider the
digit halfway around the circular list. That is, if your list contains
10 items, only include a digit in your sum if the digit 10/2 = 5 steps
forward matches it. Fortunately, your list has an even number of
elements.

For example:

1212 produces 6: the list contains 4 items, and all four digits match the digit 2 items ahead.
1221 produces 0, because every comparison is between a 1 and a 2.
123425 produces 4, because both 2s match each other, but no other digit has a match.
123123 produces 12.
12131415 produces 4.
What is the solution to your new captcha?

Your puzzle answer was 1076.

Both parts of this puzzle are complete! They provide two gold stars: **

At this point, you should return to your advent calendar and try another puzzle.

If you still want to see it, you can get your puzzle input.

You can also [Share] this puzzle.
'''

import string

INPUT = '''3499774489291465329682787161338855299363493517373359747499739
343132412171894248467449213373648661951524682924847783654445194393883284
815719922411656371564612643149356377211271474154663576466558645285834932
665834552457368122482922182977272853127889335714663877229178279674481247
959517257855593196828532674119155873549192368258684418547658412467785685
661258226326312471591649825465976131222529594732867187372959418269542585
255971892281683281634125969576632235756525233585126493347155535153636394
457276362176148994421778778556435513175694833141365264681162674216885763
485623434743269893137175745415639643299342179567514727322964244188877651
716537596528892351537887177344971418931116784978851947927417261733437841
266157488515698817153248338552834285135859979215433188934298516852818656
287373611711324227186331887391735542839317315278322372736228216998259712
352567189545293711868719128138294933593717332386261817228425474193586596
387735947712618887948191114882745378154678943731758156893144525991254127
335334525417125258834461238664913456263875891533697634729121884874454875
546249398187154394969733173557724365872211137155236317958454352114994424
784817679357185516432941514375347929787992695914159769517467438646785477
648168931461232453472918733536847169773892527161824331286465644229993888
675567999656829749896565165233796183787646859674943345463397572256197193
545955497971334431329251144728893937936927948729955732613779821964639543
624174275158136375289683389271354362796663378845538412934763769355971317
447726291491659899182398368622637839634155421954468343953693333818572383
274396425833516399332419158924639953584543416781913541391644376493166838
681728227987726429626282399922494397497448989277879965672345384913919494
836899899553126122466947855935968916793462468162283493122372831824783213
475858188273641533418756234237514469339877122312713256269252562939288972
324237474691193631313638235485876716945265622451912828789926483146359766
346185711913231257864889481541734836453237283662164417629577697894278371
477895486471954183217663389214784569375224856514779435786485996146291884
7471158244516279178346514129117328285132341339595664283'''


def captcha(msg, halfway_around=False):
    prev = None
    answer = 0
    digits = map(int, filter (lambda x: x in string.digits, msg))
    if halfway_around:
        offset = len(digits)/2
    else:
        offset = 1
    for i in xrange (len (digits)):
        j = (i + offset) % len (digits)
        if digits[i] == digits[j]:
            answer += digits[i]
    return answer

assert captcha('1122') == 3
assert captcha('1111') == 4

print captcha(INPUT)

def captcha2(msg):
    return captcha(msg, True)

assert captcha2('1212') == 6
assert captcha2('1221') == 0
assert captcha2('123425') == 4
assert captcha2('123123') == 12
assert captcha2('12131415') == 4

print captcha2(INPUT)
