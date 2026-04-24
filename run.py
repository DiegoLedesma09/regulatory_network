#!/usr/bin/env python3
"""
Script ejecutable para el programa de resumen de regulones.
"""
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from regulon_summary import main

if __name__ == "__main__":
    main()