
import ast


class NotebookCellParser:

    def __init__(self, code):
        self.parsed = None

        self.symbols = set()
        self.classFunctionCalls = set() # <- eg the object is already defined and we do a myDF.filter(...), we want myDF to show up

        self.parse(code)

    def parse(self, code):

        self.parsed = ast.parse(code)
        self._parseSymbols()

    def _parseSymbols(self):

        for n, item in enumerate(self.parsed.body):

            if isinstance(item, ast.Assign):
                for target in item.targets:
                    self.symbols.add(target.id)

            elif isinstance(item, ast.Expr):
                if item.value.__dict__.get('id', None) is not None:
                    self.symbols.add(item.value.id)

                elif item.value.__dict__.get('func', None) is not None:
                    if item.value.func.__dict__.get('value', None) is not None:
                        self.classFunctionCalls.add(item.value.func.value.id)





if __name__ == '__main__':
    code = "a=5\n5+2\nimport numpy as np\nc = np.random.rand(5,5)\ndff9\nmyDF.filter(5)\n" \
           "plt.plot()\nmyFunction()"

    ncp = NotebookCellParser(code)
    #ncp.parse(code)

    ncp.getSymbols()

    print()




