"""Rebuild index.html from prd.md.  Usage: python build.py  (needs Node for `npx marked`)."""
import re
import subprocess

body = subprocess.run("npx --yes marked -i prd.md --gfm", shell=True, check=True,
                      capture_output=True, encoding="utf-8").stdout
page = open("index.html", encoding="utf-8").read()

toc = []
def add_id(m):
    tag, inner = m.group(1), m.group(2)
    sid = "s%d" % (len(toc) + 1)
    toc.append('<a class="%s" href="#%s">%s</a>' % (tag, sid, re.sub("<[^>]+>", "", inner)))
    return '<%s id="%s">%s</%s>' % (tag, sid, inner, tag)

body = re.sub(r"<(h[23])>(.*?)</\1>", add_id, body)
body = body.replace("<table>", '<div class="table"><table>').replace("</table>", "</table></div>")

page = re.sub(r'<nav id="toc">.*?</nav>',
              lambda m: '<nav id="toc"><div class="title">Contents</div>\n' + "\n".join(toc) + "\n</nav>",
              page, flags=re.S)
page = re.sub(r'<main id="content">.*?</main>',
              lambda m: '<main id="content">\n' + body + "\n</main>", page, flags=re.S)
open("index.html", "w", encoding="utf-8", newline="\n").write(page)
print("index.html rebuilt: %d headings" % len(toc))
