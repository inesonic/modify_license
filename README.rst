==============
modify_license
==============
You can use this small Python script to modify licenses listed at the top of
source files as well as adjust copyright dates.

The script can operate on many files at once allowing you to modify the
licensing information across whole directories.

The script can optionally create backups of files, making it easy for you to
recover in the event of an error or bug in this script.

This script is used to manage copyright headers in products sold by
`Inesonic, LLC <https://inesonic.com>`.


Source File Format
==================
Source files are expected to meet a few requirements.


Copyright Header
----------------
The top of the source file is expected to have a copyright header that this
tool can modify.   Rules for the copyright header are as follows:

* The first line with more than 70% of the characters being "*" or more than
  50% of the characters being "#" marks the start of the copyright header.
  The line must be at least 50% of the expected maximum line width.

* The second line with more than 70% of the characters being "*" or more than
  50% of the characters being "#" marks the end of the copyright header.
  The line must be at least 50% of the expected maximum line width.

* Lines within the copyright header can start with the regular expression
  ``(\s*([*#]|//)*[^[*#]).*``.  The contents of the group with the first line
  in the copyright header region matching this regular expression will be used
  as the preamble for all the lines inserted into the header.

* The firsts line in the copyright region meeting the regular expression
  ``\s*([#*]|//)?\s+Copyright\s+[0-9]{4}.*`` will be kept.  All other lines
  will be replaced with the new copyright information.


Copyright Date Stamps
---------------------
This script can optionally adjust copyright dates throughout the entire source
file.   If enabled, any line matching the regular expression will be a
candidate for change:

.. code-block::
    (.*)Copyright(\s+)(2[0-9]{3})(\s*-\s*(2[0-9]{3}))?([, ].*)?

Example lines might be:

.. code-block::

   * Copyright 2020 Inesonic, LLC
   * Copyright 2020-2021, Inesonic, LLC
   * Copyright 2020 - 2021, Inesonic, LLC
   std::string copyright("Copyright 2020, Inesonic, LLC");
   copyright = 'Copyright 2020-2021 Inesonic, LLC'

Lines meeting this string will only be changed if:

* The starting date is not the current year, or
* The ending date is not the current year.

In these scenarios, the string will be modified to either append the current
year or adjust the second date to reflect the current year.

Assuming the year is 2022, the resulting lines above would become:

.. code-block::

   * Copyright 2020 - 2022 Inesonic, LLC
   * Copyright 2020 - 2022, Inesonic, LLC
   * Copyright 2020 - 2022, Inesonic, LLC
   std::string copyright("Copyright 2020 - 2022, Inesonic, LLC");
   copyright = 'Copyright 2020 - 2022 Inesonic, LLC'


Supported Licenses
==================
At this time the following copyright terms are supported:

* Generic Inesonic Commercial License
* Aion End User License Agreement
* MIT License
* GPLv2
* LGPLv2
* GPLv3
* LGPLv3

Command Line
============
The table below lists the supported command line options:

+------------+--------------+------------------------------------------------+
| Short Form | Long Form    | Function                                       |
+============+==============+================================================+
| -h         | --help       | Display a help message and exit.               |
+------------+--------------+------------------------------------------------+
| -V         | --version    | Display the current script version.            |
+------------+--------------+------------------------------------------------+
| -v         | --verbose    | Give verbose information about activity.       |
+------------+--------------+------------------------------------------------+
| -c         | --commercial | Include the Inesonic commercial license.       |
+------------+--------------+------------------------------------------------+
| -a         | --aion       | Include a reference to the Aion EULA.          |
+------------+--------------+------------------------------------------------+
| -m         | --mit        | Include the MIT license terms.                 |
+------------+--------------+------------------------------------------------+
| -g         | --gplv2      | Include the GPLv2 standard header.             |
+------------+--------------+------------------------------------------------+
| -l         | --lgplv2     | Include the LGPLv2 standard header.            |
+------------+--------------+------------------------------------------------+
| -G         | --gplv3      | Include the GPLv3 standard header.             |
+------------+--------------+------------------------------------------------+
| -L         | --lgplv3     | Include the LGPLv3 standard header.            |
+------------+--------------+------------------------------------------------+
| -d         | --date       | Identify and update copyright date strings to  |
|            |              | reflect the current year.                      |
+------------+--------------+------------------------------------------------+
| -b         | --backup     | Create backups of every file.  Backups will be |
|            |              | placed in a "backup_license" directory where   |
|            |              | each file is located.                          |
+------------+--------------+------------------------------------------------+
| -w <c>     | --wrap <c>   | Specify the maximum expected line width, in    |
|            |              | characters.  If not specified, then 79 columns |
|            |              | is assumed.  Note that this script does not    |
|            |              | treat tabs as special characters.              |
+------------+--------------+------------------------------------------------+

Note that licensing will not be changed if no licenses are specified on the
command line.  This allows you to use this script to update copyright dates
without also changing licensing terms.
