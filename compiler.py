import re

class SimpleCompiler:

    def __init__(self, source):
        self.source = source
        self.tokens = []

        # Simulasi Symbol Table
        self.symbol_table = {
            "x": "int",
            "y": "int"
        }

    # =====================================
    # ANALISIS LEKSIKAL
    # =====================================
    def lexical_analysis(self):

        pattern = r'if|else|>=|<=|==|!=|>|<|=|\{|\}|\(|\)|;|[A-Za-z_]\w*|\d+'

        self.tokens = re.findall(pattern, self.source)

        return self.tokens

    # =====================================
    # ANALISIS SINTAKSIS
    # Membentuk AST sederhana
    # =====================================
    def syntax_analysis(self):

        t = self.tokens

        # kondisi
        condition = {
            "left": t[2],
            "operator": t[3],
            "right": t[4]
        }

        # assignment THEN
        then_assign = {
            "var": t[7],
            "value": t[9]
        }

        # assignment ELSE
        else_assign = {
            "var": t[14],
            "value": t[16]
        }

        ast = {
            "type": "IF",
            "condition": condition,
            "then": then_assign,
            "else": else_assign
        }

        return ast

    # =====================================
    # ANALISIS SEMANTIK
    # =====================================
    def semantic_analysis(self, ast):

        cond = ast["condition"]

        # cek variabel kondisi
        if cond["left"] not in self.symbol_table:
            raise Exception(
                f"Error Semantik: Variabel '{cond['left']}' belum dideklarasikan."
            )

        # cek variabel assignment THEN
        if ast["then"]["var"] not in self.symbol_table:
            raise Exception(
                f"Error Semantik: Variabel '{ast['then']['var']}' belum dideklarasikan."
            )

        # cek variabel assignment ELSE
        if ast["else"]["var"] not in self.symbol_table:
            raise Exception(
                f"Error Semantik: Variabel '{ast['else']['var']}' belum dideklarasikan."
            )

        return "Analisis semantik berhasil."

    # =====================================
    # GENERASI THREE ADDRESS CODE
    # =====================================
    def generate_TAC(self, ast):

        cond = ast["condition"]

        tac = []

        tac.append(
            f"ifFalse {cond['left']} {cond['operator']} {cond['right']} goto L1"
        )

        tac.append(
            f"{ast['then']['var']} = {ast['then']['value']}"
        )

        tac.append("goto L2")

        tac.append("L1:")

        tac.append(
            f"{ast['else']['var']} = {ast['else']['value']}"
        )

        tac.append("L2:")

        return tac


# =====================================
# PROGRAM UTAMA
# =====================================

source = """
if ( x > 5 ) {
    y = 1 ;
}
else {
    y = 0 ;
}
"""

compiler = SimpleCompiler(source)

# 1. Analisis Leksikal
tokens = compiler.lexical_analysis()

print("========== ANALISIS LEKSIKAL ==========")
print(tokens)

# 2. Analisis Sintaksis
ast = compiler.syntax_analysis()

print("\n========== ABSTRACT SYNTAX TREE ==========")
print(ast)

# 3. Analisis Semantik
print("\n========== ANALISIS SEMANTIK ==========")
print(compiler.semantic_analysis(ast))

# 4. Three Address Code
print("\n========== THREE ADDRESS CODE ==========")

for code in compiler.generate_TAC(ast):
    print(code)