from odoo import api, SUPERUSER_ID


def _init_wiki(env):
    """Crea TODO el modulo wiki desde Python."""

    # 1. Crear categorias
    categories_data = [
        ('category_oficina', 'Oficina', 'Documentos y procedimientos de la oficina', 1),
        ('category_almacen', 'Almacen', 'Documentos y procedimientos del almacen', 2),
        ('category_trabajadores', 'Trabajadores', 'Documentos y procedimientos de trabajadores', 3),
        ('category_clientes', 'Clientes', 'Documentos y procedimientos de clientes', 4),
        ('category_admin', 'Administracion', 'Documentos administrativos generales', 5),
        ('category_socios', 'Socios', 'Documentos reservados para socios', 6),
    ]

    for xml_id, name, description, color in categories_data:
        existing = env['wiki.category'].search([('name', '=', name)], limit=1)
        if not existing:
            existing = env['wiki.category'].create({
                'name': name,
                'description': description,
                'color': color,
            })
            env.cr.execute(
                "INSERT INTO ir_model_data (name, module, model, res_id, noupdate) "
                "VALUES (%s, %s, %s, %s, %s) "
                "ON CONFLICT (name, module) DO NOTHING",
                (xml_id, 'wiki_interna', 'wiki.category', existing.id, True)
            )

    # 2. Crear vistas
    views_to_create = [
        ('wiki.article.tree', 'wiki.article', '''<list decoration-info="is_public" decoration-warning="is_locked">
            <field name="name"/>
            <field name="category_id" optional="hide"/>
            <field name="tag_ids" widget="many2many_tags" optional="hide"/>
            <field name="author_id" optional="hide"/>
            <field name="write_date" string="Actualizado" optional="show"/>
            <field name="is_public" string="Publico" optional="hide"/>
            <field name="is_locked" string="Solo lectura" optional="hide"/>
        </list>''', 'list'),
        ('wiki.article.form', 'wiki.article', '''<form>
            <sheet>
                <div class="oe_title">
                    <label for="name"/>
                    <h1><field name="name" placeholder="Titulo del articulo"/></h1>
                </div>
                <group>
                    <field name="category_id"/>
                    <field name="section_id"/>
                    <field name="tag_ids" widget="many2many_tags"/>
                    <field name="author_id" readonly="1"/>
                    <field name="create_date" readonly="1"/>
                    <field name="write_date" readonly="1"/>
                    <field name="is_public"/>
                </group>
                <notebook>
                    <page string="Contenido">
                        <field name="body" placeholder="Escribe el contenido aqui..."/>
                    </page>
                    <page string="Adjuntos">
                        <field name="attachment_ids">
                            <list>
                                <field name="name"/>
                                <field name="create_date"/>
                                <field name="file_size"/>
                                <field name="preview_image" widget="image"/>
                            </list>
                        </field>
                    </page>
                </notebook>
            </sheet>
        </form>''', 'form'),
        ('wiki.article.search', 'wiki.article', '''<search>
            <field name="name"/>
            <field name="body"/>
            <field name="section_id"/>
            <field name="category_id"/>
            <field name="tag_ids"/>
            <filter name="filter_section" string="Seccion" context="{'group_by': 'section_id'}"/>
            <filter name="filter_category" string="Categoria" context="{'group_by': 'category_id'}"/>
            <filter name="filter_author" string="Autor" context="{'group_by': 'author_id'}"/>
            <separator/>
            <filter name="filter_sin_seccion" string="Sin seccion" domain="[('section_id', '=', False)]"/>
            <filter name="filter_public" string="Publicos" domain="[('is_public', '=', True)]"/>
            <filter name="filter_locked" string="Solo lectura" domain="[('is_locked', '=', True)]"/>
        </search>''', 'search'),
        ('wiki.article.kanban', 'wiki.article', '''<kanban class="o_kanban_mobile">
            <field name="name"/>
            <field name="category_id"/>
            <field name="tag_ids"/>
            <field name="author_id"/>
            <field name="is_locked"/>
            <field name="is_public"/>
            <field name="write_date"/>
            <templates>
                <t t-name="card">
                    <div t-attf-class="oe_kanban_card">
                        <div class="o_kanban_card_header">
                            <div class="o_kanban_record_title w-100">
                                <strong><field name="name"/></strong>
                            </div>
                            <div class="o_kanban_record_buttons">
                                <span t-if="record.is_locked.raw_value" class="text-warning me-1" title="Solo lectura"><i class="fa fa-lock"/></span>
                                <span t-if="record.is_public.raw_value" class="text-success" title="Visible para todos"><i class="fa fa-globe"/></span>
                            </div>
                        </div>
                        <div class="o_kanban_record_body">
                            <div><i class="fa fa-folder-o me-1 text-muted" title="Categoria"/><field name="category_id"/></div>
                            <field name="tag_ids" widget="many2many_tags"/>
                            <div class="mt-2 small text-muted d-flex justify-content-between">
                                <span><i class="fa fa-user me-1" title="Autor"/><field name="author_id"/></span>
                                <span><field name="write_date"/></span>
                            </div>
                        </div>
                    </div>
                </t>
            </templates>
        </kanban>''', 'kanban'),
        ('wiki.category.tree', 'wiki.category', '''<list>
            <field name="name"/>
            <field name="description"/>
            <field name="color"/>
        </list>''', 'list'),
        ('wiki.category.form', 'wiki.category', '''<form>
            <sheet>
                <div class="oe_title">
                    <label for="name"/>
                    <h1><field name="name" placeholder="Nombre de la categoria"/></h1>
                </div>
                <group>
                    <field name="parent_id"/>
                    <field name="description"/>
                    <field name="color"/>
                    <field name="user_ids" widget="many2many_tags"/>
                </group>
                <notebook>
                    <page string="Articulos">
                        <field name="article_ids">
                            <list>
                                <field name="name"/>
                                <field name="author_id"/>
                                <field name="create_date"/>
                            </list>
                        </field>
                    </page>
                </notebook>
            </sheet>
        </form>''', 'form'),
        ('wiki.tag.tree', 'wiki.tag', '''<list>
            <field name="name"/>
        </list>''', 'list'),
        ('wiki.section.tree', 'wiki.section', '''<list>
            <field name="sequence"/>
            <field name="name"/>
            <field name="description"/>
        </list>''', 'list'),
        ('wiki.section.form', 'wiki.section', '''<form>
            <sheet>
                <div class="oe_title">
                    <label for="name"/>
                    <h1><field name="name" placeholder="Nombre de la seccion"/></h1>
                </div>
                <group>
                    <field name="sequence"/>
                    <field name="description"/>
                </group>
                <notebook>
                    <page string="Articulos">
                        <group string="Añadir articulos existentes">
                            <field name="linked_article_ids" widget="many2many_tags" options="{'no_create': True}"/>
                        </group>
                        <field name="article_ids">
                            <list>
                                <field name="name"/>
                                <field name="category_id"/>
                                <field name="author_id"/>
                                <field name="create_date"/>
                                <field name="is_locked"/>
                            </list>
                        </field>
                    </page>
                </notebook>
            </sheet>
        </form>''', 'form'),
    ]

    view_ids = {}
    for xml_id, model, arch, view_type in views_to_create:
        existing = env['ir.ui.view'].search([('name', '=', xml_id)], limit=1)
        if not existing:
            existing = env['ir.ui.view'].create({
                'name': xml_id,
                'model': model,
                'arch': arch,
                'type': view_type,
            })
            env.cr.execute(
                "INSERT INTO ir_model_data (name, module, model, res_id, noupdate) "
                "VALUES (%s, %s, %s, %s, %s) "
                "ON CONFLICT (name, module) DO NOTHING",
                (xml_id, 'wiki_interna', 'ir.ui.view', existing.id, True)
            )
        view_ids[xml_id] = existing.id

    # 3. Crear acciones y sus vistas vinculadas
    def _create_act_window(xml_id, name, res_model, view_mode, linked_views, search_view_id=None, context=None):
        action = env['ir.actions.act_window'].search([('res_model', '=', res_model)], limit=1)
        if not action:
            action = env['ir.actions.act_window'].create({
                'name': name,
                'res_model': res_model,
                'view_mode': view_mode,
                'context': context or {},
            })
            env.cr.execute(
                "INSERT INTO ir_model_data (name, module, model, res_id, noupdate) "
                "VALUES (%s, %s, %s, %s, %s) "
                "ON CONFLICT (name, module) DO NOTHING",
                (xml_id, 'wiki_interna', 'ir.actions.act_window', action.id, True)
            )
        for view_mode_key, view_id in linked_views.items():
            if view_id:
                env['ir.actions.act_window.view'].create({
                    'act_window_id': action.id,
                    'view_id': view_id,
                    'view_mode': view_mode_key,
                })
        if search_view_id:
            action.write({'search_view_id': search_view_id})
        return action

    article_action = _create_act_window(
        'action_wiki_article', 'Articulos', 'wiki.article', 'list,kanban,form',
        {
            'list': view_ids.get('wiki.article.tree'),
            'kanban': view_ids.get('wiki.article.kanban'),
            'form': view_ids.get('wiki.article.form'),
        },
        search_view_id=view_ids.get('wiki.article.search'),
        context={'group_by': ['section_id']},
    )

    category_action = _create_act_window(
        'action_wiki_category', 'Categorias', 'wiki.category', 'list,form',
        {
            'list': view_ids.get('wiki.category.tree'),
            'form': view_ids.get('wiki.category.form'),
        },
    )

    tag_action = _create_act_window(
        'action_wiki_tag', 'Etiquetas', 'wiki.tag', 'list',
        {
            'list': view_ids.get('wiki.tag.tree'),
        },
    )

    section_action = _create_act_window(
        'action_wiki_section', 'Secciones', 'wiki.section', 'list,form',
        {
            'list': view_ids.get('wiki.section.tree'),
            'form': view_ids.get('wiki.section.form'),
        },
    )

    # 4. Crear menus
    menu_root = env['ir.ui.menu'].search([('name', '=', 'Wiki Interna')], limit=1)
    if not menu_root:
        menu_root = env['ir.ui.menu'].create({
            'name': 'Wiki Interna',
            'sequence': 100,
        })

    menu_items = [
        ('Articulos', 'wiki_interna.action_wiki_article', 10),
        ('Categorias', 'wiki_interna.action_wiki_category', 20),
        ('Etiquetas', 'wiki_interna.action_wiki_tag', 30),
        ('Secciones', 'wiki_interna.action_wiki_section', 40),
    ]
    for name, action_ref, sequence in menu_items:
        if env['ir.ui.menu'].search([('name', '=', name), ('parent_id', '=', menu_root.id)]):
            continue
        action_id = env.ref(action_ref).id
        env['ir.ui.menu'].create({
            'name': name,
            'parent_id': menu_root.id,
            'action': 'ir.actions.act_window,%i' % action_id,
            'sequence': sequence,
        })