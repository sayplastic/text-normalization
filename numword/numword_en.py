# coding: utf-8
#This file is part of numword.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

"""numword for English language"""

from numword_base import NumWordBase

class NumWordEN(NumWordBase):
    """
    NumWord EN
    """

    def _set_high_numwords(self, high):
        """
        Set high num words
        """
        # short scale
        max_val = 3 + 3 * len(high)
        for word, i in zip(high, range(max_val, 3, -3)):
            self.cards[10**i] = word + u"illion"

    ''' # long scale
        max_val = 3 + 6 * len(high)

        for word, i in zip(high, range(max_val, 3, -6)):
            self.cards[10**i] = word + u"illiard"
            self.cards[10**(i-3)] = word + u"illion"
    '''

    def _base_setup(self):
        """
        Base setup
        """
        lows = [u"non", u"oct", u"sept", u"sext", u"quint", u"quadr", u"tr",
                u"b", u"m"]
        units = [u"", u"un", u"duo", u"tre", u"quattuor", u"quin", u"sex",
                u"sept", u"octo", u"novem"]
        tens = [u"dec", u"vigint", u"trigint", u"quadragint", u"quinquagint",
                u"sexagint", u"septuagint", u"octogint", u"nonagint"]
        self.high_numwords = [u"cent"] + self._gen_high_numwords(units, tens, lows)


    def _setup(self):
        """
        Setup
        """
        self.negword = u"minus "
        self.pointword = u"point"
        self.errmsg_nonnum = "Only numbers may be converted to words."
        self.exclude_title = [u"and", u"point", u"minus"]

        self.mid_numwords = [(1000, u"thousand"), (100, u"hundred"),
                (90, u"ninety"), (80, u"eighty"), (70, u"seventy"),
                (60, u"sixty"), (50, u"fifty"), (40, u"forty"), (30, u"thirty")]
        self.low_numwords = [u"twenty", u"nineteen", u"eighteen", u"seventeen",
                u"sixteen", u"fifteen", u"fourteen", u"thirteen", u"twelve",
                u"eleven", u"ten", u"nine", u"eight", u"seven", u"six", u"five",
                u"four", u"three", u"two", u"one", u"zero"]
        self.ords = {
                u"one": u"first",
                u"two": u"second",
                u"three": u"third",
                u"five": u"fifth",
                u"eight": u"eighth",
                u"nine": u"ninth",
                u"twelve": u"twelfth",
                }


    def _merge(self, curr, next):
        """
        Merge
        """
        curr_text, curr_num, next_text, next_num = curr + next
        if curr_num == 1 and next_num < 100:
            return next # everything less than 100 doesn't need a prefix 'one'
        elif 100 > curr_num > next_num :
            return u"%s-%s" % (curr_text, next_text), curr_num + next_num
        elif curr_num >= 100 > next_num:
            return u"%s and %s" % (curr_text, next_text), curr_num + next_num
        elif next_num > curr_num:
            return u"%s %s" % (curr_text, next_text), curr_num * next_num
        return u"%s, %s" % (curr_text, next_text), curr_num + next_num


    def ordinal(self, value):
        """
        Convert to ordinal
        """
        self._verify_ordinal(value)
        outwords = self.cardinal(value).split(" ")
        lastwords = outwords[-1].split("-")
        lastword = lastwords[-1].lower()
        try:
            lastword = self.ords[lastword]
        except KeyError:
            if lastword[-1] == u"y":
                lastword = lastword[:-1] + u"ie"
            lastword += u"th"
        lastwords[-1] = self._title(lastword)
        outwords[-1] = u"-".join(lastwords)
        return " ".join(outwords)


    def ordinal_number(self, value):
        """
        Convert to ordinal num
        """
        self._verify_ordinal(value)
        return u"%s%s" % (value, self.ordinal(value)[-2:])


    def year(self, value, longval=True):
        """Convert number into year"""
        self._verify_ordinal(value)
        century = value // 100
        decades = value % 100
        if 0 < value < 1000 or 2099 < value < 3000: # 2177 -> two thousand and twelve; 711 -> seven hundred eleven
            return self._split(value, hightxt=u"hundred", jointxt=u"and", longval=longval)
        if century < 20: # 1145 -> eleven forty-five
            if decades < 10: # years like 1406 or 2108 should be said as 'forteen o six'
                return self._split(value, hightxt=u"", jointxt=u"o", longval=longval)
            else:
                return self._split(value, hightxt=u"", jointxt=u"", longval=longval)
        else:
            self.cardinal(value)
        if 0 < value < 10000:
            return self._split(value, hightxt=u"", jointxt=u"", longval=longval)
        return self.cardinal(value)

    def currency(self, value, longval=True):
        temp_precision, self.precision = self.precision, 2
        return_var = self._split(value, hightxt=u"dollar/s", lowtxt=u"cent/s",
                                split_precision=0, jointxt=u"and", longval=longval)
        self.precision = temp_precision
        return return_var


_NW = NumWordEN()

def cardinal(value):
    """
    Convert to cardinal
    """
    return _NW.cardinal(value)

def ordinal(value):
    """
    Convert to ordinal
    """
    return _NW.ordinal(value)

def ordinal_number(value):
    """
    Convert to ordinal num
    """
    return _NW.ordinal_number(value)

def currency(value, longval=True):
    """
    Convert to currency
    """
    return _NW.currency(value, longval=longval)

def year(value, longval=True):
    """
    Convert to year
    """
    return _NW.year(value, longval=longval)

def main():
    """Main program"""
    for val in [ 400, 5, 2.4, 3.60,
            -19.98, -100, -2.128212, 2.40, 1.2345678,
            #11, 12, 21, 31, 33, 71, 80, 81, 91, 99, 100, 101, 102, 120, 155,
            #180, 300, 308, 832, 1000, 1001, 1061, 1100, 1120, 1500, 1701, 1800,
            #2000, 2010, 2099, 2171, 3000, 8280, 8291, 150000, 500000, 1000000,
            #2000000, 2000001, -21212121211221211111, -2.121212, -1.0000100,
            #1325325436067876801768700107601001012212132143210473207540327057320957032975032975093275093275093270957329057320975093272950730
    ]:
        _NW.test(val)

if __name__ == "__main__":
    main()
