class exercise:
    def __init__(self, name:str, difficulty:str, switch:bool) -> None:
        self.name: str = name
        self.difficulty: str = difficulty
        self.switch: bool = switch
    
    def __str__(self) -> str:
        return f'{self.name}'

