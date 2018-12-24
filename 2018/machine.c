label_0: ++insns; e = 0;

	b = 123;
#ifdef DEBUG
	printf ("%ld 0 seti [123, 0, 1] [%d, %d, %d, %d, %d, %d]\n", insns, a, b, c, d, e, f);
#endif
label_1: ++insns; e = 1;

	b = b & 456;
#ifdef DEBUG
	printf ("%ld 1 bani [1, 456, 1] [%d, %d, %d, %d, %d, %d]\n", insns, a, b, c, d, e, f);
#endif
label_2: ++insns; e = 2;

	b = (b == 72);
#ifdef DEBUG
	printf ("%ld 2 eqri [1, 72, 1] [%d, %d, %d, %d, %d, %d]\n", insns, a, b, c, d, e, f);
#endif
label_3: ++insns; e = 3;

	if (b) goto label_5;
label_4: ++insns; e = 4;

	goto label_1;
label_5: ++insns; e = 5;

	b = 0;
#ifdef DEBUG
	printf ("%ld 5 seti [0, 6, 1] [%d, %d, %d, %d, %d, %d]\n", insns, a, b, c, d, e, f);
#endif
label_6: ++insns; e = 6;

	d = b | 65536;
#ifdef DEBUG
	printf ("%ld 6 bori [1, 65536, 3] [%d, %d, %d, %d, %d, %d]\n", insns, a, b, c, d, e, f);
#endif
label_7: ++insns; e = 7;

	b = 6780005;
#ifdef DEBUG
	printf ("%ld 7 seti [6780005, 8, 1] [%d, %d, %d, %d, %d, %d]\n", insns, a, b, c, d, e, f);
#endif
label_8: ++insns; e = 8;

	c = d & 255;
#ifdef DEBUG
	printf ("%ld 8 bani [3, 255, 2] [%d, %d, %d, %d, %d, %d]\n", insns, a, b, c, d, e, f);
#endif
label_9: ++insns; e = 9;

	b = b + c;
#ifdef DEBUG
	printf ("%ld 9 addr [1, 2, 1] [%d, %d, %d, %d, %d, %d]\n", insns, a, b, c, d, e, f);
#endif
label_10: ++insns; e = 10;

	b = b & 16777215;
#ifdef DEBUG
	printf ("%ld 10 bani [1, 16777215, 1] [%d, %d, %d, %d, %d, %d]\n", insns, a, b, c, d, e, f);
#endif
label_11: ++insns; e = 11;

	b = b * 65899;
#ifdef DEBUG
	printf ("%ld 11 muli [1, 65899, 1] [%d, %d, %d, %d, %d, %d]\n", insns, a, b, c, d, e, f);
#endif
label_12: ++insns; e = 12;

	b = b & 16777215;
#ifdef DEBUG
	printf ("%ld 12 bani [1, 16777215, 1] [%d, %d, %d, %d, %d, %d]\n", insns, a, b, c, d, e, f);
#endif
label_13: ++insns; e = 13;

	c = (256 > d);
#ifdef DEBUG
	printf ("%ld 13 gtir [256, 3, 2] [%d, %d, %d, %d, %d, %d]\n", insns, a, b, c, d, e, f);
#endif
label_14: ++insns; e = 14;

	if (c) goto label_16;
label_15: ++insns; e = 15;

	goto label_17;
label_16: ++insns; e = 16;

	goto label_28;
label_17: ++insns; e = 17;

	c = 0;
#ifdef DEBUG
	printf ("%ld 17 seti [0, 5, 2] [%d, %d, %d, %d, %d, %d]\n", insns, a, b, c, d, e, f);
#endif
label_18: ++insns; e = 18;

	f = c + 1;
#ifdef DEBUG
	printf ("%ld 18 addi [2, 1, 5] [%d, %d, %d, %d, %d, %d]\n", insns, a, b, c, d, e, f);
#endif
label_19: ++insns; e = 19;

	f = f * 256;
#ifdef DEBUG
	printf ("%ld 19 muli [5, 256, 5] [%d, %d, %d, %d, %d, %d]\n", insns, a, b, c, d, e, f);
#endif
label_20: ++insns; e = 20;

	f = (f > d);
#ifdef DEBUG
	printf ("%ld 20 gtrr [5, 3, 5] [%d, %d, %d, %d, %d, %d]\n", insns, a, b, c, d, e, f);
#endif
label_21: ++insns; e = 21;

	if (f) goto label_23;
label_22: ++insns; e = 22;

	goto label_24;
label_23: ++insns; e = 23;

	goto label_26;
label_24: ++insns; e = 24;

	c = c + 1;
#ifdef DEBUG
	printf ("%ld 24 addi [2, 1, 2] [%d, %d, %d, %d, %d, %d]\n", insns, a, b, c, d, e, f);
#endif
label_25: ++insns; e = 25;

	goto label_18;
label_26: ++insns; e = 26;

	d = c;
#ifdef DEBUG
	printf ("%ld 26 setr [2, 1, 3] [%d, %d, %d, %d, %d, %d]\n", insns, a, b, c, d, e, f);
#endif
label_27: ++insns; e = 27;

	goto label_8;
label_28: ++insns; e = 28;

	c = (b == a);
bool inserted = seen.insert(b).second;
#ifdef DEBUG2
printf ("%ld 28 eqrr [1, 0, 2] [%d, %d, %d, %d, %d, %d] size=%lu\n", insns, a, b, c, d, e, f, seen.size());
#endif
if (seen.size () == 1) {
    printf ("%d\n", b);
 } else if (!inserted) { // seen.size() == 1 || !inserted) {
    return;
 }
label_29: ++insns; e = 29;

	if (c) goto label_31;
label_30: ++insns; e = 30;

	goto label_6;
label_31:
