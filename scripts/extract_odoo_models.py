"""Read-only, dependency-free Odoo Python ORM field indexer.

Parses source AST only: does not execute Odoo or connect to PostgreSQL.
Output is a preliminary field-declaration inventory, not a database schema.
"""
import ast
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'models' / 'source'
OUTPUT = ROOT / 'models' / 'odoo19_field_inventory.csv'
FILES = ('account_move.py', 'account_move_line.py', 'purchase_order.py', 'stock_move.py')


def literal(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return ''


def field_call(node):
    if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
        return None
    if not isinstance(node.func.value, ast.Name) or node.func.value.id != 'fields':
        return None
    return node.func.attr


rows = []
for filename in FILES:
    path = SOURCE / filename
    tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        name = ''
        inherit = ''
        for statement in node.body:
            if isinstance(statement, ast.Assign):
                for target in statement.targets:
                    if isinstance(target, ast.Name) and target.id == '_name':
                        name = literal(statement.value)
                    if isinstance(target, ast.Name) and target.id == '_inherit':
                        try: inherit = ast.unparse(statement.value)
                        except Exception: pass
        model = name or ('inherits ' + inherit if inherit else '<unknown>')
        for statement in node.body:
            if not isinstance(statement, (ast.Assign, ast.AnnAssign)):
                continue
            value = statement.value
            kind = field_call(value)
            if not kind:
                continue
            targets = statement.targets if isinstance(statement, ast.Assign) else [statement.target]
            for target in targets:
                if not isinstance(target, ast.Name):
                    continue
                relation = literal(value.args[0]) if value.args else ''
                rows.append({
                    'source_file': filename, 'source_line': statement.lineno,
                    'python_class': node.name, 'model_declaration': model,
                    'field_name': target.id, 'field_type': kind,
                    'comodel_if_literal': relation if kind in ('Many2one','One2many','Many2many') else '',
                    'computed': str(any(k.arg == 'compute' for k in value.keywords)),
                    'store_explicit': next((ast.unparse(k.value) for k in value.keywords if k.arg == 'store'), ''),
                })

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
with OUTPUT.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['source_file','source_line','python_class','model_declaration','field_name','field_type','comodel_if_literal','computed','store_explicit'])
    writer.writeheader()
    writer.writerows(rows)
print(f'Extracted {len(rows)} declarations across {len(FILES)} files')
print(f'Wrote {OUTPUT}')
print('NOTE: AST-only extraction; inherited and runtime fields may not be included.')
