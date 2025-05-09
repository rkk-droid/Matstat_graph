import networkx as nx
from pyvis.network import Network
import pandas as pd
import json

# Чтение графа
edges = pd.read_csv("graph.csv")
G = nx.DiGraph()
G.add_edges_from(edges.values)

# Чтение описаний (включая LaTeX)
with open("descriptions.json", "r", encoding="utf-8") as f:
    descriptions = json.load(f)

# Создаем визуализацию
net = Network(notebook=False, directed=True)
net.repulsion(node_distance=250, central_gravity=0.1, spring_length=200, spring_strength=0.05)

# Добавляем узлы и ребра
for node in G.nodes():
    net.add_node(node, label=str(node))
for src, dst in G.edges():
    net.add_edge(src, dst)

# Рендерим в HTML
out_html = "graph.html"
net.write_html(out_html, notebook=False)

# Загружаем сгенерированный файл
with open(out_html, "r", encoding="utf-8") as f:
    html = f.read()

# 1) Конфигурация MathJax для inline-$ и \(...\)
mathjax_config = """
<script>
window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$','$$'], ['\\\\[','\\\\]']]
  },
  svg: { fontCache: 'global' }
};
</script>
"""

# 2) Подключение MathJax v3
mathjax_script = """
<script id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
</script>
"""

# 3) Скрипт для клика и вставки описания
click_script = f"""
<script>
  const descriptions = {json.dumps(descriptions, ensure_ascii=False)};
  function showDescription(nodeId) {{
    const desc = descriptions[nodeId] || "Описание недоступно.";
    document.getElementById("description").innerHTML = desc;
    if (window.MathJax) {{
      MathJax.typesetPromise();
    }}
  }}
  // Ждем, пока network станет глобальным
  setTimeout(() => {{
    if (typeof network !== 'undefined') {{
      network.on("click", function(params) {{
        if (params.nodes.length > 0) {{
          showDescription(params.nodes[0]);
        }}
      }});
    }}
  }}, 500);
</script>
<div id="description" style="margin-top:20px;padding:10px;border:1px solid #ccc;">
  Кликните на узел, чтобы увидеть описание.
</div>
"""

# Вставляем всё перед закрывающим </body>
injection = mathjax_config + mathjax_script + click_script
html = html.replace("</body>", injection + "</body>")

# Сохраняем результат
with open(out_html, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Готово! Откройте {out_html} в браузере.")
