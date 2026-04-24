import pytest
import os
import sys
import tempfile
from pathlib import Path

# Agregar src al path para importar el módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from regulon_summary import (
    construir_regulon,
    obtener_efecto_TF,
    clasificacion_TF,
    lecture_validation,
    generar_salida,
    parse_arguments
)


# ===================================================================================================
# FIXTURES
# ===================================================================================================

@pytest.fixture
def temp_dir():
    """Crea un directorio temporal para pruebas."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def crear_archivo_tsv():
    """Factory fixture para crear archivos TSV temporales con contenido específico."""
    def _crear(contenido, directorio=None):
        if directorio is None:
            directorio = tempfile.gettempdir()
        
        archivo = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.tsv',
            dir=directorio,
            delete=False,
            encoding='utf-8'
        )
        archivo.write(contenido)
        archivo.close()
        return archivo.name
    
    yield _crear
    
    # Limpieza: eliminar archivos creados
    for archivo in []:
        if os.path.exists(archivo):
            os.remove(archivo)


# ===================================================================================================
# TESTS: construir_regulon()
# ===================================================================================================

class TestConstruirRegulon:
    """Tests para la función construir_regulon()"""

    def test_caso_1_lista_interacciones_normal(self):
        """Caso 1: Lista de interacciones normal."""
        interacciones = [
            ("AraC", "araA", "+"),
            ("AraC", "araB", "-"),
            ("LexA", "recA", "-"),
            ("CRP", "lacZ", "+"),
            ("CRP", "lacY", "+"),
        ]
        resultado = construir_regulon(interacciones)
        
        assert resultado["AraC"] == ["araA", "araB"]
        assert resultado["LexA"] == ["recA"]
        assert resultado["CRP"] == ["lacY", "lacZ"]
        assert len(resultado) == 3

    def test_caso_3_un_solo_tf(self):
        """Caso 3: Un solo factor de transcripción."""
        interacciones = [
            ("AraC", "araA", "+"),
            ("AraC", "araB", "-"),
            ("AraC", "araC", "+"),
        ]
        resultado = construir_regulon(interacciones)
        
        assert len(resultado) == 1
        assert "AraC" in resultado
        assert len(resultado["AraC"]) == 3

    def test_caso_4_target_duplicado_evitado(self):
        """Caso 4: Target duplicado en el mismo TF (se evita duplicado)."""
        interacciones = [
            ("AraC", "araA", "+"),
            ("AraC", "araA", "-"),
        ]
        resultado = construir_regulon(interacciones)
        
        assert resultado["AraC"] == ["araA"]
        assert len(resultado["AraC"]) == 1

    def test_caso_5_minimo_una_interaccion(self):
        """Caso 5: Un solo factor de transcripción con un solo target."""
        interacciones = [("LexA", "recA", "-")]
        resultado = construir_regulon(interacciones)
        
        assert resultado["LexA"] == ["recA"]
        assert len(resultado) == 1


# ===================================================================================================
# TESTS: obtener_efecto_TF()
# ===================================================================================================

class TestObtenerEfectoTF:
    """Tests para la función obtener_efecto_TF()"""

    def test_caso_1_clasificacion_correcta(self):
        """Caso 1: Clasificación correcta (Activador, Represor, Dual)."""
        interacciones = [
            ("AraC", "araA", "+"),
            ("AraC", "araB", "-"),
            ("CRP", "lacZ", "+"),
        ]
        regulon = construir_regulon(interacciones)
        resultado = obtener_efecto_TF(interacciones, regulon)
        
        assert resultado["AraC"] == "Dual"
        assert resultado["CRP"] == "Activador"

    def test_caso_5_minimo_represor(self):
        """Caso 5: Un solo TF Represor."""
        interacciones = [("LexA", "recA", "-")]
        regulon = construir_regulon(interacciones)
        resultado = obtener_efecto_TF(interacciones, regulon)
        
        assert resultado["LexA"] == "Represor"

    def test_caso_23_tf_efectos_mixtos_dual(self):
        """Caso 23: TF con efectos mixtos (clasificación Dual)."""
        interacciones = [
            ("AraC", "araA", "+"),
            ("AraC", "araB", "-"),
        ]
        regulon = construir_regulon(interacciones)
        resultado = obtener_efecto_TF(interacciones, regulon)
        
        assert resultado["AraC"] == "Dual"


# ===================================================================================================
# TESTS: clasificacion_TF()
# ===================================================================================================

class TestClasificacionTF:
    """Tests para la función clasificacion_TF()"""

    def test_caso_1_clasificacion_completa(self):
        """Caso 1: Clasificación completa."""
        interacciones = [
            ("AraC", "araA", "+"),
            ("AraC", "araB", "-"),
            ("LexA", "recA", "-"),
            ("CRP", "lacZ", "+"),
            ("CRP", "lacY", "+"),
        ]
        regulon, clas = clasificacion_TF(interacciones)
        
        assert isinstance(regulon, dict)
        assert isinstance(clas, dict)
        assert "AraC" in regulon and "AraC" in clas
        assert "LexA" in regulon and "LexA" in clas
        assert "CRP" in regulon and "CRP" in clas


# ===================================================================================================
# TESTS: lecture_validation()
# ===================================================================================================

class TestLectureValidation:
    """Tests para la función lecture_validation()"""

    def test_caso_13_archivo_no_encontrado(self, capsys):
        """Caso 13: Archivo no encontrado."""
        with pytest.raises(RuntimeError, match="No se pudo encontrar el archivo"):
            lecture_validation("ruta/inexistente/archivo.tsv")

    def test_caso_15_archivo_vacio(self, crear_archivo_tsv, temp_dir, capsys):
        """Caso 15: Archivo vacío."""
        archivo = crear_archivo_tsv("", temp_dir)
        
        with pytest.raises(RuntimeError, match="parece estar vacío"):
            lecture_validation(archivo)
        
        os.remove(archivo)

    def test_caso_16_archivo_solo_comentarios(self, crear_archivo_tsv, temp_dir, capsys):
        """Caso 16: Archivo solo con comentarios."""
        contenido = "# Comentario 1\n# Comentario 2\n"
        archivo = crear_archivo_tsv(contenido, temp_dir)
        
        with pytest.raises(RuntimeError, match="No hay interacciones registradas"):
            lecture_validation(archivo)
        
        os.remove(archivo)

    def test_caso_17_encabezado_columnas_faltantes(self, crear_archivo_tsv, temp_dir):
        """Caso 17: Encabezado con columnas faltantes."""
        contenido = "1)regulatorId\t2)regulatorName\t3)RegulatorGeneName\t4)regulatedId\t5)regulatedName\n"
        archivo = crear_archivo_tsv(contenido, temp_dir)
        
        with pytest.raises(RuntimeError, match="columnas faltantes"):
            lecture_validation(archivo)
        
        os.remove(archivo)

    def test_caso_18_fila_efecto_invalido(self, crear_archivo_tsv, temp_dir, capsys):
        """Caso 18: Fila con efecto inválido."""
        contenido = (
            "1)regulatorId\t2)regulatorName\t3)RegulatorGeneName\t4)regulatedId\t5)regulatedName\t6)function\n"
            "ID1\tAraC\tAraC\tID2\taraA\t?\n"
        )
        archivo = crear_archivo_tsv(contenido, temp_dir)
        
        with pytest.raises(RuntimeError, match="No hay interacciones registradas"):
            lecture_validation(archivo)
        
        os.remove(archivo)

    def test_caso_19_fila_campos_vacios(self, crear_archivo_tsv, temp_dir):
        """Caso 19: Fila con campos vacíos."""
        contenido = (
            "1)regulatorId\t2)regulatorName\t3)RegulatorGeneName\t4)regulatedId\t5)regulatedName\t6)function\n"
            "ID1\t\t\tID2\taraA\t+\n"
        )
        archivo = crear_archivo_tsv(contenido, temp_dir)
        
        with pytest.raises(RuntimeError, match="No hay interacciones registradas"):
            lecture_validation(archivo)
        
        os.remove(archivo)

    def test_caso_20_columnas_diferente_orden(self, crear_archivo_tsv, temp_dir):
        """Caso 20: Columnas en diferente orden."""
        contenido = (
            "6)function\t5)regulatedName\t3)RegulatorGeneName\t1)regulatorId\t2)regulatorName\t4)regulatedId\n"
            "+\taraA\tAraC\tID1\tAraC\tID2\n"
            "-\taraB\tAraC\tID1\tAraC\tID3\n"
        )
        archivo = crear_archivo_tsv(contenido, temp_dir)
        
        resultado = lecture_validation(archivo)
        
        assert len(resultado) == 2
        assert ("AraC", "araA", "+") in resultado
        assert ("AraC", "araB", "-") in resultado
        
        os.remove(archivo)

    def test_caso_21_interacciones_duplicadas(self, crear_archivo_tsv, temp_dir):
        """Caso 21: Interacciones duplicadas."""
        contenido = (
            "1)regulatorId\t2)regulatorName\t3)RegulatorGeneName\t4)regulatedId\t5)regulatedName\t6)function\n"
            "ID1\tAraC\tAraC\tID2\taraA\t+\n"
            "ID1\tAraC\tAraC\tID2\taraA\t+\n"
        )
        archivo = crear_archivo_tsv(contenido, temp_dir)
        
        resultado = lecture_validation(archivo)
        
        # Las interacciones duplicadas se mantienen en la tupla, pero construir_regulon evita duplicados
        assert len(resultado) == 2
        
        os.remove(archivo)

    def test_caso_27_encoding_incorrecto(self, temp_dir):
        """Caso 27: Archivo con encoding incorrecto."""
        archivo = os.path.join(temp_dir, "test_latin1.tsv")
        
        with open(archivo, 'w', encoding='latin-1') as f:
            f.write("1)regulatorId\t2)regulatorName\t3)RegulatorGeneName\t4)regulatedId\t5)regulatedName\t6)function\n")
            f.write("ID1\tÜmlaut\tAraC\tID2\taraA\t+\n")
        
        # Intentar leer con UTF-8 debería fallar
        with pytest.raises(RuntimeError, match="no es un archivo de texto UTF-8"):
            lecture_validation(archivo)
        
        os.remove(archivo)

    def test_caso_29_archivo_sin_encabezado_valido(self, crear_archivo_tsv, temp_dir):
        """Caso 29: Archivo sin encabezado válido (datos sin encabezado)."""
        contenido = "ID1\tAraC\tAraC\tID2\taraA\t+\n"
        archivo = crear_archivo_tsv(contenido, temp_dir)
        
        with pytest.raises(RuntimeError, match="parece estar vacío"):
            lecture_validation(archivo)
        
        os.remove(archivo)

    def test_caso_30_linea_menos_columnas(self, crear_archivo_tsv, temp_dir):
        """Caso 30: Línea con menos columnas que el índice máximo."""
        contenido = (
            "1)regulatorId\t2)regulatorName\t3)RegulatorGeneName\t4)regulatedId\t5)regulatedName\t6)function\n"
            "ID1\tAraC\tAraC\n"  # Solo 3 columnas, faltan columnas 5 y 6
        )
        archivo = crear_archivo_tsv(contenido, temp_dir)
        
        with pytest.raises(RuntimeError, match="No hay interacciones registradas"):
            lecture_validation(archivo)
        
        os.remove(archivo)


# ===================================================================================================
# TESTS: generar_salida()
# ===================================================================================================

class TestGenerarSalida:
    """Tests para la función generar_salida()"""

    def test_caso_22_archivo_generado_correctamente(self, temp_dir):
        """Caso 22: Archivo de salida generado correctamente."""
        regulon = {"AraC": ["araA", "araB"], "LexA": ["recA"]}
        clas = {"AraC": "Dual", "LexA": "Represor"}
        ruta_salida = os.path.join(temp_dir, "output.tsv")
        
        generar_salida(regulon, clas, ruta_salida)
        
        assert os.path.exists(ruta_salida)
        
        with open(ruta_salida, 'r') as f:
            contenido = f.read()
        
        assert "Gen\tNo. de genes que regula\tGenes regulados\tEfecto" in contenido
        assert "AraC\t2\taraA, araB\tDual" in contenido
        assert "LexA\t1\trecA\tRepresor" in contenido

    def test_caso_24_directorio_salida_no_existe(self, temp_dir):
        """Caso 24: Directorio de salida no existe (se crea automáticamente)."""
        ruta_salida = os.path.join(temp_dir, "subdir", "nuevo", "output.tsv")
        regulon = {"AraC": ["araA"]}
        clas = {"AraC": "Activador"}
        
        generar_salida(regulon, clas, ruta_salida)
        
        assert os.path.exists(ruta_salida)

    def test_caso_25_archivo_una_interaccion_valida(self, temp_dir):
        """Caso 25: Archivo con solo una interacción válida."""
        regulon = {"AraC": ["araA"]}
        clas = {"AraC": "Activador"}
        ruta_salida = os.path.join(temp_dir, "output.tsv")
        
        generar_salida(regulon, clas, ruta_salida)
        
        with open(ruta_salida, 'r') as f:
            lineas = f.readlines()
        
        assert len(lineas) == 2  # Encabezado + 1 TF
        assert "AraC\t1\taraA\tActivador" in lineas[1]

    def test_caso_generar_salida_con_filtro_min_genes(self, temp_dir):
        """Test adicional: generar_salida con filtro minimal_genes."""
        regulon = {"AraC": ["araA", "araB"], "LexA": ["recA"]}
        clas = {"AraC": "Dual", "LexA": "Represor"}
        ruta_salida = os.path.join(temp_dir, "output.tsv")
        
        # Filtrar TFs con menos de 2 genes (solo AraC)
        generar_salida(regulon, clas, ruta_salida, minimal_genes=2)
        
        with open(ruta_salida, 'r') as f:
            contenido = f.read()
        
        assert "AraC" in contenido
        assert "LexA" not in contenido  # Filtrado por tener solo 1 gen


# ===================================================================================================
# TESTS: parse_arguments() y CLI
# ===================================================================================================

class TestCLI:
    """Tests para la función parse_arguments() y comportamiento CLI"""

    def test_cli_argumentos_validos(self, monkeypatch):
        """CLI: Ejecutar con argumentos posicionales válidos."""
        monkeypatch.setattr(
            sys,
            "argv",
            ["regulon_summary.py", "input.tsv", "output.tsv"]
        )
        
        args = parse_arguments()
        
        assert args.input_file == "input.tsv"
        assert args.output_file == "output.tsv"
        assert args.min_genes == 0

    def test_cli_min_genes_argumento(self, monkeypatch):
        """CLI: Argumento --min_genes válido."""
        monkeypatch.setattr(
            sys,
            "argv",
            ["regulon_summary.py", "input.tsv", "output.tsv", "--min_genes", "5"]
        )
        
        args = parse_arguments()
        
        assert args.min_genes == 5

    def test_cli_min_genes_negativo(self, monkeypatch):
        """Caso 26: Argumento --min_genes negativo."""
        monkeypatch.setattr(
            sys,
            "argv",
            ["regulon_summary.py", "input.tsv", "output.tsv", "--min_genes", "-1"]
        )
        
        args = parse_arguments()
        
        # El error se valida en main(), aquí solo verificamos que se parsea
        assert args.min_genes == -1


# ===================================================================================================
# TESTS DE INTEGRACIÓN
# ===================================================================================================

class TestIntegracion:
    """Tests de integración completos"""

    def test_flujo_completo_datos_validos(self, crear_archivo_tsv, temp_dir):
        """Test de integración: flujo completo con datos válidos."""
        contenido = (
            "1)regulatorId\t2)regulatorName\t3)RegulatorGeneName\t4)regulatedId\t5)regulatedName\t6)function\n"
            "ID1\tAraC\tAraC\tID2\taraA\t+\n"
            "ID1\tAraC\tAraC\tID3\taraB\t-\n"
            "ID4\tLexA\tLexA\tID5\trecA\t-\n"
        )
        archivo_entrada = crear_archivo_tsv(contenido, temp_dir)
        archivo_salida = os.path.join(temp_dir, "output.tsv")
        
        # Simular el flujo
        interacciones = lecture_validation(archivo_entrada)
        regulon, clas = clasificacion_TF(interacciones)
        generar_salida(regulon, clas, archivo_salida)
        
        assert os.path.exists(archivo_salida)
        
        with open(archivo_salida, 'r') as f:
            contenido_salida = f.read()
        
        assert "AraC\t2\taraA, araB\tDual" in contenido_salida
        assert "LexA\t1\trecA\tRepresor" in contenido_salida
        
        os.remove(archivo_entrada)

    def test_flujo_completo_con_filtro(self, crear_archivo_tsv, temp_dir):
        """Test de integración: flujo completo con filtro --min_genes."""
        contenido = (
            "1)regulatorId\t2)regulatorName\t3)RegulatorGeneName\t4)regulatedId\t5)regulatedName\t6)function\n"
            "ID1\tAraC\tAraC\tID2\taraA\t+\n"
            "ID1\tAraC\tAraC\tID3\taraB\t+\n"
            "ID4\tLexA\tLexA\tID5\trecA\t-\n"
        )
        archivo_entrada = crear_archivo_tsv(contenido, temp_dir)
        archivo_salida = os.path.join(temp_dir, "output.tsv")
        
        interacciones = lecture_validation(archivo_entrada)
        regulon, clas = clasificacion_TF(interacciones)
        generar_salida(regulon, clas, archivo_salida, minimal_genes=2)
        
        with open(archivo_salida, 'r') as f:
            contenido_salida = f.read()
        
        # AraC tiene 2 genes (pasa filtro), LexA tiene 1 (no pasa)
        assert "AraC" in contenido_salida
        assert "LexA" not in contenido_salida
        
        os.remove(archivo_entrada)
