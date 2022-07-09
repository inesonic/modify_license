#!/usr/bin/env python3
#-*-python-*-##################################################################
# Copyright 2022 Inesonic, LLC
#
# GNU Public License, Version 3:
#   This program is free software: you can redistribute it and/or modify it
#   under the terms of the GNU General Public License as published by the Free
#   Software Foundation, either version 3 of the License, or (at your option)
#   any later version.
#
#   This program is distributed in the hope that it will be useful, but WITHOUT
#   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#   FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#   more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program.  If not, see <https://www.gnu.org/licenses/>.
###############################################################################

"""
Command line tool you can use to update source file licensing terms.

"""

###############################################################################
# Import:
#

import os
import shutil
import sys
import datetime
import re
import textwrap3
import argparse

###############################################################################
# Globals:
#

VERSION = "1.0"
"""
The script version number.

"""

DESCRIPTION = """
Command line tool you can use to modify source file license terms.

"""
"""
The comamnd description.

"""

DEFAULT_COLUMN_WIDTH = 79
"""
The default column width.

"""

LICENSE_TEXT = {
    "commercial" : {
        "header" : "Inesonic Commercial License",
        "text" : "All rights reserved."
    },
    "aion" : {
        "header" : "Aion End User License Agreement",
        "text" : "Use under the terms of the Aion End User License Agreement."
    },
    "mit" : {
        "header" : "MIT License",
        "text" : """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    },
    "gplv2" : {
        "header" : "GNU Public License, Version 2",
        "text" : """
This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 51 Franklin
Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
    },
    "lgplv2" : {
        "header" : "GNU Lesser Public License, Version 2",
        "text" : """
This library is free software; you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation; either version 2.1 of the License, or (at your option)
any later version.

This library is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
details.

You should have received a copy of the GNU Lesser General Public License along
with this library; if not, write to the Free Software Foundation, Inc., 51
Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""
    },
    "gplv3" : {
        "header" : "GNU Public License, Version 3",
        "text" : """
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <https://www.gnu.org/licenses/>.
"""
    },
    "lgplv3" : {
        "header" : "GNU Lesser Public License, Version 3",
        "text" : """
This library is free software; you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation; either version 3 of the License, or (at your option) any
later version.

This library is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
details.

You should have received a copy of the GNU Lesser General Public License along
with this library; if not, write to the Free Software Foundation, Inc., 51
Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""
    }
}

BACKUP_DIRECTORY = "backup_license"
"""
The backup directory name.

"""

COPYRIGHT_DATE_RE = re.compile(
    r'(.*)Copyright(\s+)(2[0-9]{3})(\s*-\s*(2[0-9]{3}))?([, ].*)?'
)
"""
Regular expression used to update copyright dates.

"""

COPYRIGHT_DATE_HEADER = re.compile(r'\s*[#*]?\s+Copyright\s+[0-9]{4}.*')
"""
Regular expression used to identify copyright dates.  The first of these lines
are preserved and placed at the top of the copyright region.

"""

LINE_START_RE = re.compile(r'(\s*[*#]*[^*#]).*')
"""
Regular expression used to identify how each line should be started.

"""

###############################################################################
# Functions
#

def modify_copyright_dates(file_content, wrap_column):
    """
    Function that scans a file for copyright strings, modifying them as needed.

    :param file_content:
        An array of file lines to be modified.

    :param wrap_column:
        The maximum allowed line width in characters.

    :return:
        Returns True on success.  Returns false on error.

    :type file_content: list
    :type wrap_count: int
    :rtype: bool

    """

    current_year = str(datetime.date.today().year)

    number_lines = len(file_content)
    i = 0;
    while i < number_lines:
        l = file_content[i]
        match = COPYRIGHT_DATE_RE.fullmatch(l)
        if match:
            change_made = True
            actual_change_made = False
            while change_made:
                change_made = False

                groups = match.groups();
                start_year = groups[2]
                if start_year != current_year:
                    end_year = groups[4]
                    if end_year is None or end_year != current_year:
                        pre_string = groups[0]
                        post_string = groups[5]
                        space_between = groups[1]

                        if post_string is None:
                            post_string = ''

                        l = (
                              pre_string
                            + 'Copyright'
                            + space_between
                            + start_year
                            + ' - '
                            + current_year
                            + post_string
                        )

                        actual_change_made = True
                        change_made = True

                        match = COPYRIGHT_DATE_RE.fullmatch(l)

            if actual_change_made:
                file_content[i] = l
                if len(l) > wrap_column:
                    sys.stderr.write(
                        "*** Warning: Line %d exceeds maximum line length.\n"
                        "    %s"%(
                            i + 1,
                            l
                        )
                    )

        i += 1

    return True


def interesting_line(l, wrap_column):
    """
    Method that determines if a line is interesting as a copyright start or end.

    :param l:
        The line to be tested.

    :param wrap_column:
        The maximum line length.  Interesting lines must be at least 90% of this
        value.

    :return:
        Returns True if this line marks the start/end of a copyright header.
        Returns False otherwise.

    :type l:           str
    :type wrap_column: int
    :rtype:            bool

    """

    result = (
            (len(l) >= 0.5 * wrap_column)
        and (   (l.count('*') >= 0.7 * len(l))
             or (l.count('#') >= 0.7 * len(l))
            )
    )

    return result


def update_license_header(
    file_content,
    wrap_column,
    license_list
    ):
    """
    Function that updates the license header data.

    :param file_content:
        List of file lines.

    :param wrap_column:
        The maximum line length in characters.

    :param license_list:
        A list of licenses to include in the file header.

    :return:
        Returns the updated file content or None on error.

    :type file_content: list
    :type wrap_column:  int
    :type license_list: list
    :rtype:             list or None

    """

    i = 0;
    number_lines = len(file_content)
    while i < number_lines                                   and \
          not interesting_line(file_content[i], wrap_column)     :
        i += 1

    start_line = file_content[i]

    i += 1
    copyright_region_start = i;

    copyright_date_line = None
    line_start = None
    while i < number_lines                                   and \
          not interesting_line(file_content[i], wrap_column)     :
        l = file_content[i]
        if not copyright_date_line and COPYRIGHT_DATE_HEADER.match(l):
            copyright_date_line = l

        if not line_start:
            match = LINE_START_RE.match(l)
            if match:
                line_start = match.group(1)

        i += 1

    copyright_region_end = i - 1

    file_pre = file_content[:copyright_region_start]
    file_post = file_content[i:]

    if copyright_date_line is not None:
        copyright_content = [ copyright_date_line ]
    else:
        copyright_content = []

    indented_line_start = line_start + '  '
    maximum_text_width = wrap_column - len(indented_line_start)

    for license in license_list:
        copyright_content.append(line_start.rstrip())
        header = LICENSE_TEXT[license]['header']
        text = LICENSE_TEXT[license]['text']

        copyright_content.append(line_start + header + ':')

        text_lines = [ l.strip() for l in text.split("\n") ]
        while text_lines[0] == '':
            text_lines = text_lines[1:]

        while text_lines[-1] == '':
            text_lines = text_lines[:-1]

        paragraph = ''
        for l in text_lines:
            if l != "":
                if paragraph == '':
                    paragraph = l
                else:
                    paragraph += ' ' + l
            else:
                if paragraph != '':
                    wrapped = textwrap3.wrap(paragraph, maximum_text_width)
                    for l in wrapped:
                        copyright_content.append(
                            indented_line_start + l.strip()
                        )

                    copyright_content.append(indented_line_start)

                    paragraph = ''

        if paragraph != '':
            wrapped = textwrap3.wrap(paragraph, maximum_text_width)
            for l in wrapped:
                copyright_content.append(indented_line_start + l.strip())

    file_content = (
          file_pre
        + copyright_content
        + file_post
    )

    return file_content


def process_file(
    file_handle,
    verbose,
    license_list,
    modify_dates,
    create_backups,
    wrap_column
    ):
    """
    Function you can use to parse a single file.

    :param file_handle:
        The file handle to the file to be processed.

    :param verbose:
        If True, then verbose reporting will be generated.

    :param license_list:
        An ordered list of licenses to be inserted into the source file header.

    :param modify_dates:
        If True, then copyright dates in the file should be updated.

    :param create_backups:
        If True, then a backup of the file should be created.

    :param wrap_column:
        The maximum column width for the file.

    :return:
        Returns True if the operation was successful.  Returns False on error.

    :type file_handle:    file
    :type verbose:        bool
    :type license_list:   list
    :type modify_dates:   bool
    :type create_backups: bool
    :type wrap_column:    int
    :rtype:               bool

    """

    success = True

    filename = os.path.abspath(file_handle.name)
    if verbose:
        sys.stdout.write("Processing %s:\n"%filename)

    if create_backups:
        ( filepath, basename ) = os.path.split(filename)

        backup_path = os.path.join(filepath, BACKUP_DIRECTORY)

        if not os.path.exists(backup_path):
            if verbose:
                sys.stdout.write(
                    "    Creating backup directory %s\n"%backup_path
                )

            try:
                os.mkdir(backup_path)
            except:
                success = False

            if not success:
                sys.stderr.write(
                    "*** Could not create backup directory %s\n"
                    "    exiting...\n"%backup_path
                )
        elif not os.path.isdir(backup_path):
            sys.stderr.write(
                "*** Could not create backup directory %s, already exists "
                "as file\n"
                "    exiting...\n"%backup_path
            )
            success = False

        if success:
            backup_file = os.path.join(backup_path, basename)
            if verbose:
                sys.stdout.write("    Copying to %s\n"%backup_file)

            try:
                shutil.copyfile(filename, backup_file)
            except:
                success = False

            if not success:
                sys.stderr.write(
                    "*** Could not copy file %s to %s\n"%(
                        filename,
                        backup_file
                    )
                )

    if success:
        if verbose:
            sys.stdout.write("    Reading.\n")
        try:
            file_lines = file_handle.readlines()
        except:
            success = False

        if success:
            file_content = [ l.rstrip() for l in file_lines ]
        else:
            sys.stderr.write("*** Could not read file %s\n"%filename)

    if success and modify_dates:
        if verbose:
            sys.stdout.write("    Updating copyright dates.\n")

        success = modify_copyright_dates(file_content, wrap_column)

    if success and license_list:
        if verbose:
            sys.stdout.write("    Updating licenses.\n")

        new_file_content = update_license_header(
            file_content,
            wrap_column,
            license_list
        )

        if new_file_content is None:
            success = False
        else:
            file_content = new_file_content

    if success:
        file_handle.close()

        if verbose:
            sys.stdout.write("    Writing updates.\n")

        try:
            with open(filename, "w+") as file_handle:
                for l in file_content:
                    file_handle.write(l + "\n")
        except Exception as e:
            sys.stderr.write(
                "*** Failed to write updates to %s: %s\n"%(
                    filename,
                    str(e)
                )
            )
            success = False

    return success

###############################################################################
# Main:
#

success = True;

command_line_parser = argparse.ArgumentParser(description = DESCRIPTION)
command_line_parser.add_argument(
    "-V",
    "--version",
    help = "You can use this switch to obtain the software release "
           "version.",
    action = "version",
    version = VERSION
)

command_line_parser.add_argument(
    "-v",
    "--verbose",
    help = "You can use this switch to request verbose status updates.",
    action = "store_true",
    default = False,
    dest = "verbose"
)

command_line_parser.add_argument(
    "-c",
    "--commercial",
    help = "You can use this switch to specify that Inesonic commercial "
           "license should be included.",
    action = "store_true",
    default = False,
    dest = "commercial"
)

command_line_parser.add_argument(
    "-a",
    "--aion",
    help = "You can use this switch to specify that Inesonic Aion EULA should "
           "be included.",
    action = "store_true",
    default = False,
    dest = "aion"
)

command_line_parser.add_argument(
    "-m",
    "--mit",
    help = "You can use this switch to specify that the MIT license should be "
           "included.",
    action = "store_true",
    default = False,
    dest = "mit_license"
)

command_line_parser.add_argument(
    "-g",
    "--gplv2",
    help = "You can use this switch to specify that the GPLv2 license should "
           "be included.",
    action = "store_true",
    default = False,
    dest = "gplv2_license"
)

command_line_parser.add_argument(
    "-l",
    "--lgplv2",
    help = "You can use this switch to specify that the LGPLv2 license should "
           "be included.",
    action = "store_true",
    default = False,
    dest = "lgplv2_license"
)

command_line_parser.add_argument(
    "-G",
    "--gplv3",
    help = "You can use this switch to specify that the GPLv3 license should "
           "be included.",
    action = "store_true",
    default = False,
    dest = "gplv3_license"
)

command_line_parser.add_argument(
    "-L",
    "--lgplv3",
    help = "You can use this switch to specify that the LGPLv3 license should "
           "be included.",
    action = "store_true",
    default = False,
    dest = "lgplv3_license"
)

command_line_parser.add_argument(
    "-d",
    "--date",
    help = "You can use this switch to identify and adjust any copyright "
           "dates.  Date strings will be identified by the regular expression "
           "Copyright 2[0-9]{3}(-2[0-9]{3})?.",
    action = "store_true",
    default = False,
    dest = "modify_dates"
)

command_line_parser.add_argument(
    "-b",
    "--backup",
    help = "You can use this switch to indicate that a backup for each file "
           "should be created.  Backups will be placed in a \"%s\" "
           "directory under the same filename."%BACKUP_DIRECTORY,
    action = "store_true",
    default = True,
    dest = "create_backups"
)

command_line_parser.add_argument(
    "-w",
    "--wrap",
    help = "You can use this switch to specify the maximum column width for "
           "content.  This script will make a best attempt to meet this "
           "requirement, throwing an error if the requirement can not be "
           "met.  Note that this assumes the file uses spaces, not tabs.",
    type = int,
    default = DEFAULT_COLUMN_WIDTH,
    dest = "wrap"
)

command_line_parser.add_argument(
    "files",
    help = "One or more files to be modified.",
    type = argparse.FileType('r', encoding='utf-8'),
    nargs = '+',
)

arguments = command_line_parser.parse_args()

verbose = arguments.verbose
commercial = arguments.commercial
aion = arguments.aion
mit_license = arguments.mit_license
gplv2_license = arguments.gplv2_license
lgplv2_license = arguments.lgplv2_license
gplv3_license = arguments.gplv3_license
lgplv3_license = arguments.lgplv3_license
modify_dates = arguments.modify_dates
create_backups = arguments.create_backups
wrap_column = arguments.wrap
files = arguments.files

license_list = []
if commercial:
    license_list.append('commercial')

if aion:
    license_list.append('aion')

if mit_license:
    license_list.append('mit')

if gplv2_license:
    license_list.append('gplv2')

if lgplv2_license:
    license_list.append('lgplv2')

if gplv3_license:
    license_list.append('gplv3')

if lgplv3_license:
    license_list.append('lgplv3')

success = True
for fh in files:
    if success:
        success = process_file(
            file_handle = fh,
            verbose = verbose,
            license_list = license_list,
            modify_dates = modify_dates,
            create_backups = create_backups,
            wrap_column = wrap_column,
        )

if success:
    exit(0)
else:
    exit(1)
