"""Clase Cola (estructura FIFO: el primero en entrar es el primero en salir)."""


class Cola:
    def __init__(self):
        self.__items = []          # lista interna: índice 0 = frente de la cola

    def encolar(self, elemento):
        """Agrega un elemento al FINAL de la cola."""
        self.__items.append(elemento)

    def desencolar(self):
        """Saca y devuelve el elemento del FRENTE de la cola."""
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self.__items.pop(0)

    def frente(self):
        """Mira el primer elemento sin sacarlo."""
        if self.esta_vacia():
            raise IndexError("La cola está vacía")
        return self.__items[0]

    def esta_vacia(self):
        return len(self.__items) == 0

    def tamanio(self):
        return len(self.__items)

    def elementos(self):
        """Devuelve una copia (lista) para poder dibujar la cola sin alterarla."""
        return list(self.__items)

    def copiar(self):
        """Devuelve una nueva Cola con los mismos elementos."""
        nueva = Cola()
        for e in self.__items:
            nueva.encolar(e)
        return nueva

    def vaciar(self):
        self.__items.clear()
