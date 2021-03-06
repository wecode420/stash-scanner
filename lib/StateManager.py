import os
from datetime import datetime, timedelta

from lib.Utility import config


def itemToString(id, item):
    return "{};{};{};{}".format(id, item[0].isoformat(), "" if item[1] is None else item[1], item[2])

def getDateTimeFromString(datestr):
    try:
        return datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        return datetime.utcnow()

class StateManager:
    STATE_ID_FNAME = "tmp\\stateid.dat"
    STATE_FNAME = "tmp\\state.dat"

    def __init__(self):
        self.items = {}
        self.delta = {}
        self.changeid = ""
        self.fState = None
        self.fStateId = None

        # self.loadState()

    def itemExists(self, id):
        item = self.items.get(id)
        return item and \
               ((config.history_retention > 0 and datetime.utcnow() - item[0] <= timedelta(days=config.history_retention))
                or not config.history_retention)

    def addItem(self, id, price, acc):
        if id not in self.items:
            b_update = True
        else:
            timestamp, curprice, curacc = self.items[id]

            b_update = curprice != price or curacc != acc or \
                       (config.history_retention > 0 and datetime.utcnow() - timestamp > timedelta(days=config.history_retention))

        if b_update:
            self.items[id] = (datetime.utcnow(), price, acc)
            self.delta[id] = self.items[id]

        return b_update

    def __saveStateDelta(self):
        if self.fState is None or self.fState.closed:
            self.fState = open(StateManager.STATE_FNAME, mode="a+", encoding="utf-8", errors="replace")
        else:
            self.fState.seek(0, 2)

        for id in self.delta:
            self.fState.write(itemToString(id, self.delta[id]) + "\n")

        self.delta.clear()

    def saveStateItems(self):
        if self.fState is not None:
            self.fState.close()

        self.clearOldEntries()

        self.fState = open(StateManager.STATE_FNAME, mode="w", encoding="utf-8", errors="replace")

        for id in self.items:
            self.fState.write(itemToString(id, self.items[id]) + "\n")

        self.fState.flush()

    def saveState(self, id):
        if self.fStateId is None or self.fStateId.closed:
            self.fStateId = open(StateManager.STATE_ID_FNAME, "w")
        else:
            self.fStateId.seek(0)

        self.__saveStateDelta()
        self.fStateId.write(id)
        self.changeid = id

    def __loadStateItems(self):
        try:
            if self.fState is None or self.fState.closed:
                self.fState = open(StateManager.STATE_FNAME, encoding="utf-8", errors="replace")

            line = self.fState.readline()
            while line:
                fields = line.strip('\n').split(sep=";")
                try:
                    item_id, timestamp, price, acc = \
                        fields[0], getDateTimeFromString(fields[1]), None if fields[2] == "" else fields[2], fields[3]

                    self.items[item_id] = [timestamp, price, acc]
                except IndexError:
                    # 'ignoring entry {}'.format(line)
                    pass  # silently ignore invalid entries
                line = self.fState.readline()
        except FileNotFoundError:
            pass

        # This will remove unnecessary entries
        self.saveStateItems()

    def loadState(self):
        try:
            with open(StateManager.STATE_ID_FNAME, "r") as f:
                self.changeid = f.readline().strip('\n')
        except FileNotFoundError:
            self.changeid = ""

        self.__loadStateItems()

    def clearOldEntries(self):
        if config.history_retention > 0:
            last_date = datetime.utcnow() - timedelta(days=config.history_retention)
            for item_id, item in dict(self.items).items():
                timestamp = item[0]
                if timestamp < last_date:
                    self.items.pop(item_id, None)

    def getChangeId(self):
        return self.changeid

    def close(self):
        if self.fState:
            self.fState.close()
        if self.fStateId:
            self.fStateId.close()

    @classmethod
    def clearCache(cls):
        files = (cls.STATE_ID_FNAME, cls.STATE_FNAME)
        for fname in files:
            try:
                os.remove(fname)
            except FileNotFoundError:
                pass