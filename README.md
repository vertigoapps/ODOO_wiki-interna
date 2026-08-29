# Wiki Interna para Odoo 18

Módulo Odoo 18 que añade una wiki interna con organización por **categorías** y **secciones**, control de acceso por **grupos de usuarios** y gestión de **adjuntos** con vista previa de imágenes.

## Funcionalidades

- **Artículos de la wiki**: título, contenido (HTML), categoría, sección, etiquetas y autor.
- **Organización por secciones**: la lista de artículos puede agruparse por sección y alternar entre vista de lista y kanban.
- **Grupos de usuarios** con distintos niveles de acceso:
  - `Administración`: acceso total (crear, editar, borrar).
  - `Socios`: acceso total.
  - `Oficina`, `Almacén`, `Trabajadores`: lectura/acceso a sus categorías.
  - `Clientes`: solo lectura.
- **Artículos públicos y bloqueados**: control de visibilidad global (`Visible para todos`) y edición restringida (`Solo lectura`).
- **Adjuntos por artículo**: subida de archivos con vista previa en miniatura de las imágenes directamente en el listado (campo calculado `preview_image`, solo decodifica cuando el adjunto es una imagen).
- **Menús y acciones creados automáticamente** al instalar: Artículos, Categorías, Etiquetas y Secciones.

## Cómo funciona

- Todo el scaffolding del módulo (categorías por defecto, vistas de lista/formulario/kanban/búsqueda, acciones y menús) se crea en el **`post_init_hook`** la primera vez que se instala.
- Los artículos (`wiki.article`) se enlazan a `ir.attachment` mediante un One2many con dominio `res_model = 'wiki.article'`; un override en `create`/`write` garantiza que `res_model` se rellene correctamente y los adjuntos no "desaparezcan" al recargar.
- La vista previa `preview_image` se añade a `ir.attachment` como campo calculado solo para adjuntos tipo imagen.

## Requisitos

- Odoo 18 (Community o Enterprise).
- Sin dependencias externas (depende de `base` y `mail`).

## Instalación

1. Copia la carpeta `wiki_interna` dentro del directorio de addons de tu Odoo (por ejemplo `/mnt/extra-addons` o `<odoo>/addons`).
2. Actualiza la lista de aplicaciones: **Aplicaciones → Actualizar lista de aplicaciones**.
3. Busca *Wiki Interna* en **Aplicaciones** e instálala.
4. Al instalarse se crean automáticamente categorías, secciones, vistas, acciones y menús.

A partir de ahí, asigna los usuarios a los grupos del módulo desde **Ajustes → Usuarios y Compañías** y empieza a crear artículos.

## Estructura

```
wiki_interna/
├── __manifest__.py
├── __init__.py
├── post_init_hook.py          # Crea categorías, vistas, acciones y menús
├── models/
│   ├── wiki_article.py        # Artículo y lógica de adjuntos
│   ├── wiki_category.py
│   ├── wiki_tag.py
│   ├── wiki_section.py
│   └── ir_attachment.py       # Campo calculado preview_image
├── security/
│   └── wiki_security.xml      # Grupos y reglas de acceso
└── views/
    └── wiki_attachment_views.xml
```

## ¿Necesitas un módulo personalizado de Odoo?

En **Vertigo Apps** desarrollamos módulos y personalizaciones de Odoo a medida. Si tu empresa necesita una funcionalidad específica, escríbenos a **hola@vertigoapps.com**.