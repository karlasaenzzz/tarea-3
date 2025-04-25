from .components import FunctionalDependency, Attribute, Relvar


def closure(attributes: set[Attribute], functional_dependencies: set[FunctionalDependency]) -> set[Attribute]:
    # Iniciamos el cierre con los atributos dados
    closure_set = set(attributes)
    changed = True

    while changed:
        changed = False
        # Recorremos cada dependencia funcional
        for fd in functional_dependencies:
            # Si el determinante de la FD está dentro del cierre actual
            if fd.determinant.issubset(closure_set):
                # y si aún hay atributos del dependant que no están en el cierre
                if not fd.dependant.issubset(closure_set):
                    # los añadimos al cierre
                    closure_set |= fd.dependant
                    #Marcamos que cambiamos algo y habrá otra iteración
                    changed = True
     #Cuando no podamos añadir más devolvemos el cierre completo               
    return closure_set

def is_superkey(attributes: set[Attribute], heading: set[Attribute], functional_dependencies: set[FunctionalDependency]) -> bool:
    # TODO: Actividad 4
    #Calculamos el cierre de los atributos dados bajo las FDs
    cierre = closure(attributes, functional_dependencies)

    #Comparamos: si el cierre es superconjunto del encabezado, entonces attributes determina todo el esquema
    return cierre.issuperset(heading)


def is_key(attributes: set[Attribute], heading: set[Attribute], functional_dependencies: set[FunctionalDependency]) -> bool:

    # debe ser superllave
    if not is_superkey(attributes, heading, functional_dependencies):
        # Si no determina todo el encabezado
        return False

    #irreductibilidad: probar cada subconjunto (ningún subconjunto propio debe seguir siendo superllave)
    for a in set(attributes):
        #Creamos el subconjunto sin este atributo
        subset = attributes - {a}
        # si quitar a seguimos cubriendo todo el esquema, entonces 'attributes' tenía elementos de más y no es mínima
        if is_superkey(subset, heading, functional_dependencies):
            return False
    # Si supera ambas pruebas, es llave
    return True

def is_relvar_in_bcnf(relvar: Relvar):
   # Obtenemos el esquema completo como un set de atributos
    header = set(relvar.heading)
    for fd in relvar.functional_dependencies:
        # Ignoramos las FDs triviales
        if fd.is_trivial():
            continue
       
        #Preparamos el determinante como set de atributos
        ladoizquierdo = set(fd.determinant)

        #Si X no es superllave, rompe BCNF
        if not is_superkey(ladoizquierdo, header, relvar.functional_dependencies):
            return False

    # si ninguna FD rompe la condición, está en BCNF
    return True


def is_relvar_in_4nf(relvar: Relvar):
    #debe ser BCNF
    if not is_relvar_in_bcnf(relvar):
        #Si falla BCNF, no puede estar en 4NF
        return False

    header = set(relvar.heading)
    #dm=dependencia multivaluada
    for dm in relvar.multivalued_dependencies:
        # si es trivial, la ignoramos 
        if dm.is_trivial(header):
            continue
        # Extraemos el determinante como conjunto de atributos
        ladoizquierdo = set(dm.determinant)

        # Verificamos que X sea superllave según las FDs
        if not is_superkey(ladoizquierdo, header, relvar.functional_dependencies):
            # Si encontramos alguna dm no trivial cuyo X no sea superllave, la relvar NO está en 4NF
            return False

    # 4) Si ninguna MVD incumple la condición, está en 4NF
    return True

