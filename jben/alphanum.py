# -*- coding: utf-8 -*-

"""'Natural' alphanumeric sorting.

This code is from Chris Hulan's LGPLed example of the 'alphanum
algorithm'.  I have renamed the core function and removed all excess
content, except for the license statement which remains in this source
file.

"""

#
# The Alphanum Algorithm is an improved sorting algorithm for strings
# containing numbers.  Instead of sorting numbers in ASCII order like
# a standard sort, this algorithm sorts numbers in numeric order.
#
# The Alphanum Algorithm is discussed at http://www.DaveKoelle.com
#
#* Python implementation provided by Chris Hulan (chris.hulan@gmail.com)
#* Distributed under same license as original
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#

import re

def make_alphanum_list(str):
    chunks = re.findall("(\d+|\D+)", str)
    chunks = [re.match('\d',x) and int(x) or x for x in chunks]
    return chunks
