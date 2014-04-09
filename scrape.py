#########
# Notes #
#########
# 
# When scraping comments out of tex files, separate short comments
# (less than full line) from long comments (at least one full line)
# because the character of what is said is typically different in a
# few words vs. a full paragraph.
# 
# Comments: Backslash-percent (to get percent into the latex output)
# shows up in the python strings as "\\%" and a regexp for just '%'
# doesn't match them, which simplifies my life...

import os, re

import fetch

# long comment is 'optional whitepace % comment'
long_comment_regexp = "^\s*(%.*)$"

# Short comment is "string including at least one non-whitespace char
# and not including percent, percent, any string."  
# 
# Can't find a regexp that matches 'some % comment % and more' but not
# ' % comment $ and more' which is a long comment.  Therefore define a
# short comment to be "some string + longest string starting with
# percent, that doesn't also match long_comment_regexp"
short_comment_regexp = '.*?(%.*)$'

def long_comments(aid):
    "Scrape full-line and multi-line comments out of latex file"

    with open(fetch.latex_file_path(aid)) as ff:
        lines = ff.readlines()

    # State variable
    comment_started = False 
    # Contains current comment
    comment = []
    # Contains list of all comments -- overall output
    result = []

    for line in lines:
        line_is_comment = re.search(long_comment_regexp, line)
        if not comment_started and line_is_comment:
            # beginning of comment
            comment = [line]
            comment_started = True
        elif comment_started and line_is_comment:
            # continuation of comment
            comment.append(line_is_comment.group(1))
        elif comment_started and not line_is_comment:
            # end of comment
            result.append(comment)
            comment_started = False            
        elif not comment_started and not line_is_comment:
            # continuation of non-comment
            pass
        else:
            # This should never happen
            raise RuntimeError

    return result

def short_comments(aid):
    "Scrape partial-line comments out of latex file"
    with open(fetch.latex_file_path(aid)) as ff:
        lines = ff.readlines()

    result = []
    for line in lines:
        if not re.search(long_comment_regexp, line):
            match = re.search(short_comment_regexp, line)
            if match:
                result.append(match.group(1))
    return result

def write_output(aids, long_outfn, short_outfn):
    "Scrape long and short comments, write to output files."
    with open(long_outfn, 'w') as outf:
        for aid in aids:
            comments = long_comments(aid)
            for comment in comments:
                outf.writelines(comment)
                outf.write('\n')

    with open(short_outfn, 'w') as outf:
        for aid in aids:
            comments = short_comments(aid)
            for comment in comments:
                outf.write(comment)
                outf.write('\n')
    
