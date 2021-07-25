# syncrohizing directories

I keep running into problems where I need to copy files between very similar folders.  Windows copy is too slow and prompts the user for what they want to do with collisions so I wanted to write my own version using Python that would allow user to choose useful defaults.  I also wanted the ability to detect if the file date had been changed by the content was exactly the same.  Occasionally copying file updates the mofidication date, which would make it look newer and potentially trigger an unnecessary copy back to the original location.  Yes, this very like syncToy and some other utilities.

I've been through several iterations of solutions for this problem and there are numerous viable approaches.  Originally I used the os package to recursively step through a folder tree and compare modification teimstamp and file sizes.  I subsequently swapped in os.walk to replace the recursion.  I even attempted to leverage watchdog package directory snapshot, but this did not yield the desired results.

Utlimately python has some useful solutions in the standard library. Comparing directories and file contents can be accomplished with difflib and filecmp.  If the files are exactly the same there is no point in checking for granular differences, to detect this condition I am using cryptography library to compare hashes of the two files.
