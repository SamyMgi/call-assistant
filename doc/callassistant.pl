:- dynamic emergency/0, at_work/0, at_lunch/0, at_meeting/0, family/1, friend/1, phone_call/1.
rule(r1(Call), allow(Call), []):-phone_call(Call).
rule(r2(Call), deny(Call), []):-phone_call(Call).
rule(p1(Call), prefer(r2(Call), r1(Call)), []):-phone_call(Call).
rule(p2(Call), prefer(r1(Call), r2(Call)), []):-phone_call(Call), family(Call).
rule(p3(Call), prefer(r1(Call), r2(Call)), []):-phone_call(Call), friend(Call).
rule(c1(Call), prefer(p2(Call), p1(Call)), []):-phone_call(Call), family(Call).
rule(c2(Call), prefer(p3(Call), p1(Call)), []):-phone_call(Call), friend(Call).
rule(c3(Call), prefer(p1(Call), p2(Call)), []):-phone_call(Call), family(Call), at_meeting.
rule(c4(Call), prefer(c3(Call), c1(Call)), []):-phone_call(Call), family(Call), at_meeting.
rule(c5(Call), prefer(p1(Call), p3(Call)), []):-phone_call(Call), friend(Call), at_meeting.
rule(c6(Call), prefer(c5(Call), c2(Call)), []):-phone_call(Call), friend(Call), at_meeting.
rule(c7(Call), prefer(p2(Call), p1(Call)), []):-phone_call(Call), family(Call), at_work.
rule(c8(Call), prefer(c1(Call), c3(Call)), []):-phone_call(Call), family(Call), at_work.
rule(c9(Call), prefer(p1(Call), p3(Call)), []):-phone_call(Call), friend(Call), at_work.
rule(c10(Call), prefer(c9(Call), c2(Call)), []):-phone_call(Call), friend(Call), at_work.
rule(c11(Call), prefer(p2(Call), p1(Call)), []):-phone_call(Call), family(Call), at_lunch.
rule(c12(Call), prefer(c11(Call), c3(Call)), []):-phone_call(Call), family(Call), at_lunch.
rule(c13(Call), prefer(p3(Call), p1(Call)), []):-phone_call(Call), friend(Call), at_lunch.
rule(c14(Call), prefer(c13(Call), c2(Call)), []):-phone_call(Call), friend(Call), at_lunch.
rule(c15(Call), prefer(c1(Call), c3(Call)), []):-phone_call(Call), family(Call), at_meeting, emergency.
rule(c16(Call), prefer(c15(Call), c4(Call)), []):-phone_call(Call), family(Call), at_meeting, emergency.
complement(allow(Call), deny(Call)).
complement(deny(Call), allow(Call)).