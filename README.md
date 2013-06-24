stb-tester 0.14's new implementation of `wait_for_match`
(https://github.com/drothlis/stb-tester/commit/ca4201df) occasionally gives
incorrect results because OpenCV's `matchTemplate` gives the wrong output, but
only when using `decklinksrc` (the GStreamer element for Blackmagic
video-capture cards).

`*.png` are debug images from a real stbt script that show the problem. See
the missing areas in `source_matchtemplate.png`.
`source_matchtemplate_CORRECT.png` is what the result *should* look like.

In real-world usage, the problem is usually hidden because when `matchTemplate`
falsely reports a match, it is discarded by `wait_for_match`'s second pass. And
when `matchTemplate` falsely reports "no match", `wait_for_match` goes on to
process the next frame (`matchTemplate` only fails intermittently, so the next
frame is likely to be processed correctly). However this problem still causes
relatively frequent --and mysterious-- test-script failures.

`test.py` is a script that reproduces the problem. By loading the source images
from disk using OpenCV's standard `imread` function, it proves that the problem
isn't due to a bug in how `stbt.py` gets frames from GStreamer and converts
them to OpenCV images (aka numpy arrays).

`test.py` *only* reproduces the problem when run via `stbt run` with
`decklinksrc`, or when `decklinksrc` is running (even in a separate process):

                                                    slave1  slave2
--------------------------------------------------  ------  ------
stbt run (decklinksrc) test.py                      x 1-50  x 2.1k
stbt run (v4l2src) test.py                          ✓ 650k
nohup python test.py &                              ✓ 12k   ✓ 26k
stbt tv (decklinksrc) & python test.py              ✓ 1k
                                                    x 2
                                                    x 1.3k
stbt run (decklinksrc) sleep.py & python test.py    x 1.6k
stbt run (decklinksrc) sleep.py & python test.py &  x 50


Note that `stbt run` runs the GStreamer pipeline, and listens for messages,
grabs frames, etc. all in a separate thread; but none of those frames are
actually *used* by `test.py`, which loads all the images it uses from disk.

Further things to try:

* Check bugzilla & recent commits to decklinksrc.
* Run stbt run under valgrind.
* Upgrade blackmagic driver.
