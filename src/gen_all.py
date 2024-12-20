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

def base_html_selected(option_on_page: Option, sub_page_body: Html):
    html = open(template_dir / "base.tplt.html").read()
    html_lines = html.split('\n')
    for i in range(len(html_lines)):
        line = html_lines[i]
        on_page = option_on_page + '.html'
        if option_on_page + '.html' in line:
            line = line.replace(f'<a href="/{on_page}">', '').replace('</a>', '')
            html_lines[i] = line
        elif 'page-body' in line:
            text = replace_elem('page-body', line, sub_page_body)
            html_lines[i] = text
    html = '\n'.join(html_lines)
    return html

def base_html(sub_page_body: Html):
    return base_html_selected('nosuchpagematch', sub_page_body)

def index_html():
    html = open(template_dir / "index.tplt.html").read()
    return html

def publications_html():
    html = open(template_dir / "publications.tplt.html").read()
    return html

def random_things_html():
    return '<h3>Random Things</h3> <p>To be filled :)</p>'

def fragment_names():
    return [f.name[:-len('.tplt.html')] for f in (template_dir / "fragments").iterdir()]

def fragments_html():
    html = open(template_dir / "fragments.tplt.html").read()
    return html

def single_fragment_html(fragment_name):
    inner_html = open(template_dir / "fragments" / (fragment_name + ".tplt.html")).read()
    return base_html(inner_html)

def gen_file_at(path_str: str, html: Html):
    path = Path(path_str)
    path.parent.mkdir(755, parents=True, exist_ok=True)
    with open(root_dir / path, 'w') as f:
        f.write(html)
        
if __name__ == '__main__':
    gen_file_at("index.html", base_html_selected('index', index_html()))
    gen_file_at("publications.html", base_html_selected('publications', publications_html()))
    gen_file_at("random_things.html", base_html_selected('random_things', random_things_html()))
    gen_file_at("fragments.html", base_html_selected('fragments', fragments_html()))
    for fragment_name in fragment_names():
        gen_file_at(root_dir / "fragments" / (fragment_name + ".html"),
                    single_fragment_html(fragment_name))
