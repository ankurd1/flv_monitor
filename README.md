README
------

Monitors your system for flash videos that are being played with a browser.
Shows (EWMA) speed and the data downloaded. Periodically copies the video to a
folder in your home dir (by default, ~/Videos).

### Gotchas
+   Currently only keeps track of one video.
+   Should work on all linuxes (probably all *nixes!) and browsers like FF4 and
    chrome. But, I have tested this only on Ubuntu 10.10 using Firefox 4.

### TODO
+   Add support for monitoring multiple videos 	<---- done
+   Allow the user to specify a copy-dir at runtime
+   Add a daemon mode
+   Add a curses interface
