from models import session, Formula


def insert_into(name: str, schema_name: str, formula_name: str, text_formula: str):
    with open(f"formulas/{formula_name}", mode="rb") as formula, open(f"schemas/{schema_name}", mode="rb") as schema:
        session.add(
            Formula(
                name=name,
                schema=schema.read(),
                formula=formula.read(),
                text_formula=text_formula
            )
        )
    session.commit()
    session.close()


schemas = ["formula_1.png", ""]
formulas = [""]
name = []
text_formulas = []

for s, f, n, t in zip(schemas, formulas, name, text_formulas):
    insert_into(
        name=n,
        formula_name=f,
        schema_name=s,
        text_formula=t
    )
