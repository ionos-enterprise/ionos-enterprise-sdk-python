# Copyright 2015-2017 IONOS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re


def ask(question, options, default):
    """
    Ask the user a question with a list of allowed answers (like yes or no).

    The user is presented with a question and asked to select an answer from
    the given options list. The default will be returned if the user enters
    nothing. The user is asked to repeat his answer if his answer does not
    match any of the allowed anwsers.

    :param    question: Question to present to the user (without question mark)
    :type     question: ``str``

    :param    options: List of allowed anwsers
    :type     options: ``list``

    :param    default: Default answer (if the user enters no text)
    :type     default: ``str``

    """
    assert default in options

    question += " ({})? ".format("/".join(o.upper() if o == default else o for o in options))
    selected = None
    while selected not in options:
        selected = input(question).strip().lower()
        if selected == "":
            selected = default
        else:
            if selected not in options:
                question = "Please type '{}'{comma} or '{}': ".format(
                    "', '".join(options[:-1]), options[-1],
                    comma=',' if len(options) > 2 else '',
                )
    return selected


def find_item_by_name(list_, namegetter, name):
    """
    Find a item a given list by a matching name.

    The search for the name is done in this relaxing way:

    - exact name match
    - case-insentive name match
    - attribute starts with the name
    - attribute starts with the name (case insensitive)
    - name appears in the attribute
    - name appears in the attribute (case insensitive)

    :param    list_: A list of elements
    :type     list_: ``list``

    :param    namegetter: Function that returns the name for a given
                          element in the list
    :type     namegetter: ``function``

    :param    name: Name to search for
    :type     name: ``str``

    """
    matching_items = [i for i in list_ if namegetter(i) == name]
    if not matching_items:
        prog = re.compile(re.escape(name) + '$', re.IGNORECASE)
        matching_items = [i for i in list_ if prog.match(namegetter(i))]
    if not matching_items:
        prog = re.compile(re.escape(name))
        matching_items = [i for i in list_ if prog.match(namegetter(i))]
    if not matching_items:
        prog = re.compile(re.escape(name), re.IGNORECASE)
        matching_items = [i for i in list_ if prog.match(namegetter(i))]
    if not matching_items:
        prog = re.compile(re.escape(name))
        matching_items = [i for i in list_ if prog.search(namegetter(i))]
    if not matching_items:
        prog = re.compile(re.escape(name), re.IGNORECASE)
        matching_items = [i for i in list_ if prog.search(namegetter(i))]
    return matching_items
