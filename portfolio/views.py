from flask import render_template, request
from flask_babel import _

from . import bp
from collections import defaultdict
from pathlib import Path
from flask import url_for
from .models import Technology, get_sample_profile, get_sample_projects, get_sample_stack


@bp.get("/")
@bp.get("/en/")
def index():
    profile = get_sample_profile()
    stack = get_sample_stack()
    # Agrupar por categoría y mantener orden de aparición
    categorized: dict[str, list[Technology]] = defaultdict(list)
    for tech in stack:
        key = tech.category or "Otros"
        categorized[key].append(tech)

    # Orden deseado de categorías para el slider en una sola línea
    ordered_categories = [
        "Lenguajes de programación",
        "Bases de datos",
        "Desarrollo de software",
        "Infraestructura y servidores",
        "Otros",
    ]
    ordered_stack: list[Technology] = []
    for category in ordered_categories:
        ordered_stack.extend(categorized.get(category, []))
    projects = get_sample_projects()
    return render_template(
        "index.html",
        profile=profile,
        stack=stack,
        categorized_stack=categorized,
        ordered_stack=ordered_stack,
        projects=projects,
    )


@bp.get("/diplomas/")
@bp.get("/en/diplomas/")
def diplomas():
    """Página que muestra diplomas y certificaciones.

    Prioriza el diploma universitario cuyo archivo comienza por '1825-AA'.
    """
    base_dir = Path(bp.static_folder) / "Diplomas"
    pdf_files = []
    if base_dir.exists():
        for pdf_path in sorted(base_dir.glob("*.pdf")):
            filename = pdf_path.name
            pdf_url = url_for("portfolio.static", filename=f"Diplomas/{filename}")
            # Heurística de títulos amigables
            lower = filename.lower()
            if filename.startswith("1825-AA"):
                title = "Diploma universitario — Ingeniero Electrónico"
                priority = True
                group = "featured"
            elif "administracion-de-servidores-linux" in lower:
                title = "Ruta: Administración de servidores Linux (Platzi)"
                priority = False
                group = "primary"
            elif "diploma-datos-ai" in lower:
                title = "Ruta: Datos e Inteligencia Artificial (Platzi)"
                priority = False
                group = "primary"
            elif "diploma-backend" in lower:
                title = "Diploma: Backend con Python (Platzi)"
                priority = False
                group = "more"
            elif "diploma-flask" in lower:
                title = "Diploma: Flask (Platzi)"
                priority = False
                group = "more"
            elif "diploma-agentes-ai" in lower:
                title = "Diploma: Agentes de IA (Platzi)"
                priority = False
                group = "more"
            elif "diploma-dbsql" in lower:
                title = "Diploma: Bases de datos SQL (Platzi)"
                priority = False
                group = "more"
            elif "diploma-fundamentos-arquitectura-software" in lower:
                title = "Diploma: Fundamentos de Arquitectura de Software (Platzi)"
                priority = False
                group = "more"
            else:
                title = filename
                priority = False
                group = "more"

            pdf_files.append({
                "filename": filename,
                "url": pdf_url,
                "title": title,
                "priority": priority,
                "group": group,
            })

    featured = next((p for p in pdf_files if p["priority"]), None)
    primary_others = [p for p in pdf_files if p.get("group") == "primary"]
    more_others = [p for p in pdf_files if p.get("group") == "more"]

    return render_template(
        "diplomas.html",
        featured=featured,
        others=primary_others,
        more_others=more_others,
    )


@bp.get("/proyectos/")
@bp.get("/en/projects/")
def projects():
    projects = get_sample_projects()
    return render_template("projects.html", projects=projects)


@bp.get("/sobre-mi/")
@bp.get("/en/about/")
def about():
    profile = get_sample_profile()
    return render_template("about.html", profile=profile)


