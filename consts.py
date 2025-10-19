PADRAO = (
    r"^SELECT\s+(?P<select>[\w\.\s,\*]+)\s+"       # permite . nos nomes e *
    r"FROM\s+(?P<from>\w+)"                        # nome da tabela após FROM
    r"(?P<joins>(?:\s+INNER\s+JOIN\s+\w+\s+ON\s+\w+\.\w+\s*=\s*\w+\.\w+)*)"  # zero ou mais INNER JOINs
    r"(?:\s+WHERE\s+(?P<where>.+?))?"              # cláusula WHERE opcional
    r";?$"                                         # final opcional com ;
)

PALAVRAS_RESERVADAS = {
    "SELECT", "FROM", "WHERE", "JOIN", "INNER", "LEFT", "RIGHT", "ON",
    "AS", "AND", "OR", "NOT", "INSERT", "UPDATE", "DELETE", "CREATE",
    "DROP", "TABLE", "VALUES", "INTO", "GROUP", "BY", "HAVING", "ORDER"
}