from __future__ import annotations

from dataclasses import dataclass
from flask_babel import lazy_gettext as _
from typing import List


@dataclass
class Profile:
    full_name: str
    role: str
    bio: str
    location: str
    email: str
    social_links: List[dict]


@dataclass
class Technology:
    name: str
    level: str  # e.g., Beginner / Intermediate / Advanced
    icon: str | None = None  # nombre de icono o ruta
    category: str | None = None  # categoría para agrupar en UI


@dataclass
class Project:
    title: str
    description: str
    tags: List[str]
    repo_url: str | None = None
    live_url: str | None = None
    image: str | None = None


def get_sample_profile() -> Profile:
    return Profile(
        full_name="Juan Felipe Rodriguez Valencia",
        role=_("Ingeniero electrónico y desarrollador de software"),
        bio=_(
            "Ingeniero Electrónico con formación especializada en análisis de datos e inteligencia artificial, "
            "enfocado en el desarrollo de software y en soluciones tecnológicas inteligentes. "
            "Cuento con experiencia en sistemas embebidos; modelado y análisis de datos con Python y SQL; "
            "administración de servidores Linux; y desarrollo de aplicaciones web. "
            "Combino una base técnica sólida con una visión práctica para crear soluciones escalables, "
            "confiables y listas para entornos de producción."
        ),
        location="Ibagué, Tolima",
        email="jrovez@outlook.com",
        social_links=[
            {"name": "GitHub", "url": "https://github.com/jrovz", "icon": "https://cdn.simpleicons.org/github/000000"},
            {"name": "LinkedIn", "url": "https://www.linkedin.com/in/jrovez/", "icon": "icons/linkedin.svg"},
            {"name": "X", "url": "https://x.com/Jrovez", "icon": "https://cdn.simpleicons.org/x/000000"},
            {"name": "Instagram", "url": "https://www.instagram.com/jorvaz_/", "icon": "https://cdn.simpleicons.org/instagram/E4405F"},
            {"name": "TikTok", "url": "https://www.tiktok.com/@jrovez_?is_from_webapp=1&sender_device=pc", "icon": "https://cdn.simpleicons.org/tiktok/000000"},
        ],
    )


def get_sample_stack() -> list[Technology]:
    return [
        # Lenguajes de programación
        Technology(name="Python", level="Avanzado", icon="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg", category="Lenguajes de programación"),
        Technology(name="C", level="Intermedio", icon="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/c/c-original.svg", category="Lenguajes de programación"),
        Technology(name="C++", level="Intermedio", icon="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/cplusplus/cplusplus-original.svg", category="Lenguajes de programación"),
        Technology(name="JavaScript", level="Intermedio", icon="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg", category="Lenguajes de programación"),
        Technology(name="PHP", level="Intermedio", icon="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/php/php-original.svg", category="Lenguajes de programación"),
        Technology(name="TypeScript", level="Intermedio", icon="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg", category="Lenguajes de programación"),

        # Bases de datos
        Technology(name="MySQL", level="Intermedio", icon="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg", category="Bases de datos"),
        Technology(name="PostgreSQL", level="Intermedio", icon="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg", category="Bases de datos"),

        # Desarrollo de software
        Technology(name="Next.js", level="Intermedio", icon="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nextjs/nextjs-original.svg", category="Desarrollo de software"),
        Technology(name="Node.js", level="Intermedio", icon="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg", category="Desarrollo de software"),
        Technology(name="Flask", level="Avanzado", icon="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg", category="Desarrollo de software"),
        Technology(name="Laravel", level="Intermedio", icon="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/laravel/laravel-original.svg", category="Desarrollo de software"),
        Technology(name="HTML5", level="Avanzado", icon="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg", category="Desarrollo de software"),
        Technology(name="CSS3", level="Avanzado", icon="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg", category="Desarrollo de software"),

        # Infraestructura y servidores
        Technology(name="Linux", level="Intermedio", icon="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linux/linux-original.svg", category="Infraestructura y servidores"),
        Technology(name="Ubuntu", level="Intermedio", icon="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/ubuntu/ubuntu-plain.svg", category="Infraestructura y servidores"),
        Technology(name="Docker", level="Intermedio", icon="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg", category="Infraestructura y servidores"),
        Technology(name="Azure", level="Intermedio", icon="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/azure/azure-original.svg", category="Infraestructura y servidores"),
        Technology(name="Google Cloud", level="Intermedio", icon="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/googlecloud/googlecloud-original.svg", category="Infraestructura y servidores"),
    ]


def get_sample_projects() -> list[Project]:
    return [
        Project(
            title="La Barber Brothers",
            description=_(
                "Aplicación web en producción para gestión de barbería: reservas online, catálogo de servicios y "
                "panel administrativo. En operación real, construida con Flask y PostgreSQL."
            ),
            tags=["Flask", "PostgreSQL", "Docker", "HTML/CSS/JS"],
            repo_url="https://github.com/jrovz/Barber-Brothers",
            live_url="https://www.labarberbrothers.com/",
            image="images/barber.png",
        ),
        Project(
            title="scholarESP32",
            description=_(
                "Tarjeta educativa y proyecto IoT con ESP32 para prototipos: sensores, monitoreo y conexión WiFi; "
                "incluye flujo de datos y scripts en Python para procesamiento/IA."
            ),
            tags=["ESP32", "Arduino", "C++", "Python", "IoT"],
            repo_url="https://github.com/jrovz/scholarESP32",
            live_url=None,
            image="images/image.png",
        ),
        Project(
            title="CryptoBot (Telegram)",
            description=_(
                "Chatbot para Telegram que consume la API de CoinMarketCap, almacena datos en SQLite, "
                "analiza mercado (tendencias, liquidez, volatilidad, dominancia) y envía reportes estructurados."
            ),
            tags=["Python", "Telegram", "CoinMarketCap", "SQLite", "Pandas"],
            repo_url="https://github.com/jrovz/Chatbot",
            live_url=None,
            image=None,
        ),
    ]


