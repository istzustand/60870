#! /usr/bin/env python3
"""
    Class to reformat IEC-60870-5-101/4 Adresses from the RWE-communications-profile to the standard ASDU and IOA
    structured and unstructured annotation is supported
    the other way around works perfectly fine too
    setting one value will calculate all depending values with accordingly
    depends on bitstring
    sorry for the shitty implementation, it's my first time...
"""
import bitstring as bs


class InformationObject:
    """
        Represents an Information-object
    """

    def __init__(self, *args):
        self._meldetext = ''
        self._asdu = bs.BitArray('uint:16=0')
        self._asdu_1 = bs.BitArray('uint:8=0')
        self._asdu_2 = bs.BitArray('uint:8=0')
        self._ioa = bs.BitArray('uint:24=0')
        self._ioa_1 = bs.BitArray('uint:8=0')
        self._ioa_2 = bs.BitArray(
            'uint:8=0')  # kann man zwar setzen, sollte man aber nur zusammen mit ioa 3 machen, da img sich überschneidet
        self._ioa_3 = bs.BitArray(
            'uint:8=0')  # kann man zwar setzen, sollte man aber nur zusammen mit ioa 2 machen, da img sich überschneidet
        self._anl = bs.BitArray('uint:12=0')
        self._spg = bs.BitArray('uint:4=0')
        self._feld = bs.BitArray('uint:6=2')
        self._img = bs.BitArray('uint:4=0')  # Informationsgruppe
        self._bmg = bs.BitArray('uint:3=0')  # Betriebsmittelgruppe
        self._beg = bs.BitArray('uint:3=0')  # Basiselementgruppe
        self._bel = bs.BitArray('uint:8=0')  # Basiselement(liste)
        self._tk = 0

        if len(args) == 9:
            self.meldetext = args[0]
            self.anl = args[1]
            self.spg = args[2]
            self.feld = args[3]
            self.img = args[4]
            self.bmg = args[5]
            self.beg = args[6]
            self.bel = args[7]
            self.tk = args[8]

    # region properties
    @property
    def meldetext(self):
        return self._meldetext

    @property
    def asdu(self):
        return self._asdu

    @property
    def asdu_1(self):
        return self._asdu_1

    @property
    def asdu_2(self):
        return self._asdu_2

    @property
    def ioa(self):
        return self._ioa

    @property
    def ioa_1(self):
        return self._ioa_1

    @property
    def ioa_2(self):
        return self._ioa_2

    @property
    def ioa_3(self):
        return self._ioa_3

    @property
    def anl(self):
        return self._anl

    @property
    def spg(self):
        return self._spg

    @property
    def feld(self):
        return self._feld

    @property
    def img(self):
        return self._img

    @property
    def bmg(self):
        return self._bmg

    @property
    def beg(self):
        return self._beg

    @property
    def bel(self):
        return self._bel

    @property
    def tk(self):
        return self._tk

    # endregion

    # region setters
    @meldetext.setter
    def meldetext(self, value):
        self._meldetext = value

    @asdu.setter
    def asdu(self, value):
        self._asdu = bs.BitArray('uint:16=' + str(value))
        self._asdu_1 = bs.BitArray('0b' + self._asdu[0:8].bin)
        self._asdu_2 = bs.BitArray('0b' + self._asdu[8:16].bin)
        self._anl = bs.BitArray('0b' + self._asdu[0:12].bin)
        self._spg = bs.BitArray('0b' + self._asdu[12:16].bin)

    @asdu_1.setter
    def asdu_1(self, value):
        self._asdu_1 = bs.BitArray('uint:8=' + str(value))
        self.asdu = bs.BitArray('0b' + self._asdu_1.bin + self._asdu[8:16].bin).uint

    @asdu_2.setter
    def asdu_2(self, value):
        self._asdu_2 = bs.BitArray('uint:8=' + str(value))
        self.asdu = bs.BitArray('0b' + self._asdu[0:8].bin + self._asdu_2.bin).uint

    @ioa.setter
    def ioa(self, value):
        self._ioa = bs.BitArray('uint:24=' + str(value))
        self.ioa_1 = bs.BitArray('0b' + self._ioa[16:24].bin).uint
        self.ioa_2 = bs.BitArray('0b' + self._ioa[8:16].bin).uint
        self.ioa_3 = bs.BitArray('0b' + self._ioa[0:8].bin).uint

    @ioa_1.setter
    def ioa_1(self, value):
        self._ioa_1 = bs.BitArray('uint:8=' + str(value))
        self._ioa = bs.BitArray('0b' + self._ioa[0:16].bin + self._ioa_1.bin)
        self._bel = self._ioa_1

    @ioa_2.setter
    def ioa_2(self, value):
        self._ioa_2 = bs.BitArray('uint:8=' + str(value))
        self._ioa = bs.BitArray('0b' + self._ioa[0:8].bin + self._ioa_2.bin + self._ioa[16:24].bin)
        self._img = bs.BitArray('0b' + self._ioa_3[6:8].bin + self.ioa_2[0:2].bin)
        self._bmg = bs.BitArray('0b' + self._ioa_2[2:5].bin)
        self._beg = bs.BitArray('0b' + self._ioa_2[5:8].bin)

    @ioa_3.setter
    def ioa_3(self, value):
        self._ioa_3 = bs.BitArray('uint:8=' + str(value))
        self._ioa = bs.BitArray('0b' + self._ioa_3.bin + self._ioa[8:24].bin)
        self._feld = bs.BitArray('0b' + self._ioa_3[0:6].bin)
        self._img = bs.BitArray('0b' + self._ioa_3[6:8].bin + self.ioa_2[0:2].bin)

    @anl.setter
    def anl(self, value):
        self._anl = bs.BitArray('uint:12=' + str(value))
        self.asdu = bs.BitArray('0b' + self.anl.bin + self.asdu[12:16].bin).uint

    @spg.setter
    def spg(self, value):
        self._spg = bs.BitArray('uint:4=' + str(value))
        self.asdu = bs.BitArray('0b' + self.asdu[0:12].bin + self.spg.bin).uint

    @feld.setter
    def feld(self, value):
        self._feld = bs.BitArray('uint:6=' + str(value))
        self.ioa = bs.BitArray('0b' + self._feld.bin + self._ioa[6:24].bin).uint

    @img.setter
    def img(self, value):
        self._img = bs.BitArray('uint:4=' + str(value))
        self.ioa = bs.BitArray('0b' + self._ioa[0:6].bin + self._img.bin + self._ioa[10:24].bin).uint

    @bmg.setter
    def bmg(self, value):
        self._bmg = bs.BitArray('uint:3=' + str(value))
        self.ioa = bs.BitArray('0b' + self._ioa[0:10].bin + self._bmg.bin + self._ioa[13:24].bin).uint

    @beg.setter
    def beg(self, value):
        self._beg = bs.BitArray('uint:3=' + str(value))
        self.ioa = bs.BitArray('0b' + self._ioa[0:13].bin + self._beg.bin + self._ioa[16:24].bin).uint

    @bel.setter
    def bel(self, value):
        self._bel = bs.BitArray('uint:8=' + str(value))
        self.ioa = bs.BitArray('0b' + self._ioa[0:16].bin + self._bel.bin).uint

    @tk.setter
    def tk(self, value):
        self._tk = value

    # endregion
