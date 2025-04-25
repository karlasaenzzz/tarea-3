### En `components.py`
- `FunctionalDependency.is_trivial()`: Determina si una dependencia funcional es trivial. Una dependencia funcional X → Y es trivial si Y ⊆ X.
- `MultivaluedDependency.is_trivial()`: Determina si una dependencia multivaluada es trivial. Una MVD X ↠ Y es trivial si Y ⊆ X o X ∪ Y = R.

### En `algorithms.py`
- `closure(attributes, functional_dependencies)`: Calcula el cierre de un conjunto de atributos con respecto a un conjunto de dependencias funcionales.
- `is_superkey(attributes, header, functional_dependencies)`: Determina si un conjunto de atributos es superllave, es decir, si su cierre incluye todos los atributos del encabezado.
- `is_key(attributes, header, functional_dependencies)`: Determina si un conjunto de atributos es una llave, es decir, una superllave irreductible.
- `is_relvar_in_bcnf(relvar)`: Verifica si una relación está en forma normal de Boyce-Codd (BCNF).
- `is_relvar_in_4nf(relvar)`: Verifica si una relación está en cuarta forma normal (4NF).

## Suposiciones

- Las dependencias funcionales y multivaluadas están representadas como clases con atributos `lhs` y `rhs`, que son conjuntos de strings.
- El encabezado de una relación (`relvar`) es un conjunto de strings que representa los atributos de la relación.
- Se considera que una relvar está en BCNF si todas las dependencias funcionales no triviales tienen un antecedente que sea superllave.
- Se considera que una relvar está en 4NF si todas las dependencias (funcionales o multivaluadas) no triviales tienen un antecedente que sea superllave.

## Ejemplo de uso

```python
from normalization.components import FunctionalDependency
from normalization.algorithms import closure, is_superkey, is_key

fd1 = FunctionalDependency({'A'}, {'B'})
fd2 = FunctionalDependency({'B'}, {'C'})
fds = [fd1, fd2]

# Calcular el cierre de A
print(closure({'A'}, fds))  # Resultado esperado: {'A', 'B', 'C'}

# Verificar si A es superllave para encabezado ABC
print(is_superkey({'A'}, {'A', 'B', 'C'}, fds))  # True

# Verificar si A es llave
print(is_key({'A'}, {'A', 'B', 'C'}, fds))  # True

