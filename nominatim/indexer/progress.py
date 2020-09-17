# SPDX-License-Identifier: GPL-2.0-only
#
# This file is part of Nominatim.
# Copyright (C) 2020 Sarah Hoffmann

import logging
from datetime import datetime

log = logging.getLogger()

class ProgressLogger(object):
    """ Tracks and prints progress for the indexing process.
        `name` is the name of the indexing step being tracked.
        `total` sets up the total number of items that need processing.
        `log_interval` denotes the interval in seconds at which progres
        should be reported.
    """

    def __init__(self, name, total, log_interval=1):
        self.name = name
        self.total_places = total
        self.done_places = 0
        self.rank_start_time = datetime.now()
        self.next_info = 100 if log.isEnabledFor(logging.INFO) else total + 1

    def add(self, num=1):
        """ Mark `num` places as processed. Print a log message if the
            logging is at least info and the log interval has past.
        """
        self.done_places += num

        if self.done_places >= self.next_info:
            now = datetime.now()
            done_time = (now - self.rank_start_time).total_seconds()
            places_per_sec = self.done_places / done_time
            eta = (self.total_places - self.done_places)/places_per_sec

            log.info("Done {} in {} @ {:.3f} per second - {} ETA (seconds): {:.2f}"
                     .format(self.done_places, int(done_time),
                             places_per_sec, self.name, eta))

            self.next_info += int(places_per_sec)

    def done(self):
        """ Print final staticstics about the progress.
        """
        rank_end_time = datetime.now()
        diff_seconds = (rank_end_time-self.rank_start_time).total_seconds()

        log.warning("Done {}/{} in {} @ {:.3f} per second - FINISHED {}\n".format(
                    self.done_places, self.total_places, int(diff_seconds),
                    self.done_places/diff_seconds, self.name))