{
    'name': 'Wiki Interna',
    'version': '18.0.1.0.0',
    'category': 'Productivity',
    'summary': 'Wiki interna con acceso por grupos de usuarios',
    'description': """Modulo de wiki interna para Odoo 18 Community.
        Permite crear y organizar articulos por categorias con acceso restringido por grupos de usuarios.
        
        Grupos:
        - Admin: acceso total
        - Socios: acceso total
        - Oficina: acceso a documentos de oficina
        - Almacen: acceso a documentos de almacen
        - Trabajadores: acceso a documentos de trabajadores
        - Clientes: acceso de lectura a documentos de clientes
    """,
    'author': 'Nacho Cabrero',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/wiki_security.xml',
        'views/wiki_attachment_views.xml',
    ],
    'installable': True,
    'application': True,
    'post_init_hook': '_init_wiki',
}