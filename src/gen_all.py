from pathlib import Path

root_dir = Path(__file__).parent.parent
template_dir = root_dir / "templates"

Html = str
Option = str

def indent(html: Html, n: int):
    html_lines = html.split('\n')
    space = ' ' * n
    html_lines = [space + line for line in html_lines]
    return '\n'.join(html_lines)

def replace_elem(name, line, html):
    elem = f'<{name}></{name}>'
    n_space = line.index(elem)  # will throw error if not found
    return indent(html, n_space)

def base_html(option_on_page: Option, sub_page_body: Html):
    html = open(template_dir / "base.tplt.html").read()
    html_lines = html.split('\n')
    for i in range(len(html_lines)):
        line = html_lines[i]
        on_page = option_on_page + '.html'
        if option_on_page + '.html' in line:
            line = line.replace(f'<a href="{on_page}">', '').replace('</a>', '')
            html_lines[i] = line
        elif 'page-body' in line:
            text = replace_elem('page-body', line, sub_page_body)
            html_lines[i] = text
    html = '\n'.join(html_lines)
    return html

def index_html():
    html = open(template_dir / "index.tplt.html").read()
    return html

def publications_html():
    html = open(template_dir / "publications.tplt.html").read()
    return html

def random_things_html():
    return '<h3>Random Things</h3> <p>To be filled :)</p>'

def fragments_html():
    html = open(template_dir / "fragments.tplt.html").read()
    return html

if __name__ == '__main__':
    with open(root_dir / "index.html", 'w') as f:
        f.write(base_html('index', index_html()))
    with open(root_dir / "publications.html", 'w') as f:
        f.write(base_html('publications', publications_html()))
    with open(root_dir / "random_things.html", 'w') as f:
        f.write(base_html('random_things', random_things_html()))
    with open(root_dir / "fragments.html", 'w') as f:
        f.write(base_html('fragments', fragments_html()))
        
