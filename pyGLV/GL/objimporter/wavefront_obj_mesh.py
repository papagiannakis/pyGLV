class WavefrontObjectMesh:
    def __init__(self, name: str)-> None:
        self.name = name
        self.material = ""
        self.faces = []