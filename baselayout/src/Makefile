# Copyleft Pisi Linux Community
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.
#
# Original work belongs Gentoo Linux

CC = gcc
LD = gcc

CFLAGS = -Wall -O2
DESTDIR =

SBIN_TARGETS = start-stop-daemon

TARGET = $(BIN_TARGETS) $(SBIN_TARGETS)

all: $(TARGET)

start-stop-daemon: start-stop-daemon.c
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^

install: $(TARGET)
	install -m 0755 -d $(DESTDIR)/sbin
	install -m 0755 $(SBIN_TARGETS) $(DESTDIR)/sbin

clean:
	rm -f $(TARGET)
	rm -f *.o *~ core
