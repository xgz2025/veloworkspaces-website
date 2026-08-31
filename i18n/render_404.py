# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from gen_locales import ALL_LOCALES, nav_prefix

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

NOTFOUND = {
    "en": dict(title="Page not found — Velo Workspaces", eyebrow="404", h1="That page doesn't exist.",
               p="The link may be out of date. Try the homepage, or head straight to support.",
               home="Go home", support="Visit support", brand="Velo Workspaces",
               footer="© 2026 Velo Workspaces."),
    "de": dict(title="Seite nicht gefunden — Velo Workspaces", eyebrow="404", h1="Diese Seite gibt es nicht.",
               p="Der Link ist möglicherweise veraltet. Versuchen Sie es mit der Startseite oder gehen Sie direkt zum Support.",
               home="Zur Startseite", support="Support besuchen", brand="Velo Workspaces",
               footer="© 2026 Velo Workspaces."),
    "fr": dict(title="Page introuvable — Velo Workspaces", eyebrow="404", h1="Cette page n'existe pas.",
               p="Le lien est peut-être obsolète. Essayez la page d'accueil, ou allez directement au support.",
               home="Retour à l'accueil", support="Voir le support", brand="Velo Workspaces",
               footer="© 2026 Velo Workspaces."),
    "it": dict(title="Pagina non trovata — Velo Workspaces", eyebrow="404", h1="Questa pagina non esiste.",
               p="Il link potrebbe non essere aggiornato. Prova la home page, oppure vai direttamente al supporto.",
               home="Vai alla home", support="Vai al supporto", brand="Velo Workspaces",
               footer="© 2026 Velo Workspaces."),
    "es": dict(title="Página no encontrada — Velo Workspaces", eyebrow="404", h1="Esa página no existe.",
               p="Puede que el enlace esté desactualizado. Prueba la página de inicio, o ve directamente al soporte.",
               home="Ir al inicio", support="Ir a soporte", brand="Velo Workspaces",
               footer="© 2026 Velo Workspaces."),
    "ja": dict(title="ページが見つかりません — Velo Workspaces", eyebrow="404", h1="このページは存在しません。",
               p="リンクが古くなっている可能性があります。ホームページをお試しいただくか、サポートへ直接お進みください。",
               home="ホームへ戻る", support="サポートを見る", brand="Velo Workspaces",
               footer="© 2026 Velo Workspaces."),
    "ko": dict(title="페이지를 찾을 수 없습니다 — Velo Workspaces", eyebrow="404", h1="해당 페이지가 존재하지 않습니다.",
               p="링크가 오래되었을 수 있습니다. 홈페이지를 이용하시거나 지원 페이지로 바로 이동해 보세요.",
               home="홈으로 이동", support="지원 방문", brand="Velo Workspaces",
               footer="© 2026 Velo Workspaces."),
    "pt-BR": dict(title="Página não encontrada — Velo Workspaces", eyebrow="404", h1="Essa página não existe.",
               p="O link pode estar desatualizado. Tente a página inicial, ou vá direto para o suporte.",
               home="Ir para o início", support="Visitar suporte", brand="Velo Workspaces",
               footer="© 2026 Velo Workspaces."),
    "zh-Hans": dict(title="页面未找到 — Velo Workspaces", eyebrow="404", h1="该页面不存在。",
               p="链接可能已失效。请尝试访问首页，或直接前往支持页面。",
               home="返回首页", support="访问支持", brand="Velo Workspaces",
               footer="© 2026 Velo Workspaces。"),
    "zh-Hant": dict(title="頁面未找到 — Velo Workspaces", eyebrow="404", h1="該頁面不存在。",
               p="連結可能已失效。請嘗試造訪首頁，或直接前往支援頁面。",
               home="返回首頁", support="造訪支援", brand="Velo Workspaces",
               footer="© 2026 Velo Workspaces。"),
}

def render(code, seg):
    t = NOTFOUND[code]
    p = nav_prefix(seg)
    return f'''<!doctype html>
<html lang="{code}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="robots" content="noindex">
<link rel="icon" type="image/png" href="/assets/icon.png">
<link rel="stylesheet" href="/assets/style.css?v=2">
</head>
<body>
<header class="site-header">
  <div class="container">
    <a class="brand" href="{p}/">
      <img class="mark" src="/assets/icon.png" width="28" height="28" alt="Velo Workspaces">
      {t['brand']}
    </a>
  </div>
</header>
<main>
  <section class="section" style="text-align:center;">
    <div class="container">
      <span class="eyebrow">{t['eyebrow']}</span>
      <h1>{t['h1']}</h1>
      <p style="max-width:48ch; margin:0 auto 24px;">{t['p']}</p>
      <div class="hero-actions" style="justify-content:center;">
        <a class="btn btn-primary" href="{p}/">{t['home']}</a>
        <a class="btn btn-outline" href="{p}/support/">{t['support']}</a>
      </div>
    </div>
  </section>
</main>
<footer class="site-footer">
  <div class="container">
    <p class="footer-fine">{t['footer']}</p>
  </div>
</footer>
</body>
</html>
'''

def write_all():
    for code, seg, label in ALL_LOCALES:
        d = os.path.join(REPO, seg) if seg else REPO
        os.makedirs(d, exist_ok=True)
        out_path = os.path.join(d, "404.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(render(code, seg))
        print("wrote", out_path)

if __name__ == "__main__":
    write_all()
