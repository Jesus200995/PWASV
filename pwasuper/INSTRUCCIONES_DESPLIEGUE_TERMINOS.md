# 🚀 INSTRUCCIONES DE DESPLIEGUE - AVISO DE PRIVACIDAD
## Proyecto PWASuper - Sistema Sembrando Vida

### ❗ ESTADO ACTUAL
- ✅ **Frontend**: Completamente implementado en local
- ✅ **Base de datos**: Tabla `usuarios_terminos` existe y funciona
- ❌ **Backend producción**: **REQUIERE ACTUALIZACIÓN**
- ✅ **Usuarios existentes**: Términos corregidos automáticamente

---

### 📋 CHECKLIST DE DESPLIEGUE

#### 1. Backend (CRÍTICO - Debe hacerse primero)
- [ ] Subir archivo `main.py` modificado al servidor de producción
- [ ] Verificar que incluye los nuevos endpoints:
  - `POST /usuarios/aceptar_terminos`
  - `GET /usuarios/{user_id}/terminos`
- [ ] Reiniciar servicio backend en producción
- [ ] Probar endpoint: `GET https://apipwa.sembrandodatos.com/usuarios/1/terminos`

#### 2. Frontend
- [ ] Verificar que `Register.vue` tiene el aviso de privacidad
- [ ] Hacer build: `npm run build`
- [ ] Subir archivos de `dist/` al servidor web
- [ ] Probar registro completo en producción

#### 3. Base de Datos (Ya completado ✅)
- [x] Tabla `usuarios_terminos` existe
- [x] Usuarios existentes tienen términos registrados
- [x] Estructura correcta verificada

---

### 📁 ARCHIVOS A SUBIR A PRODUCCIÓN

#### Backend (`backend/main.py`):
```python
# CAMBIOS PRINCIPALES EN main.py:

# 1. Nuevo modelo
class TerminosAceptados(BaseModel):
    usuario_id: int

# 2. Modificación en crear_usuario() - líneas ~70-85
# Registra términos automáticamente al crear usuario

# 3. Nuevo endpoint
@app.post("/usuarios/aceptar_terminos")
async def aceptar_terminos(terminos: TerminosAceptados):
    # ... implementación completa

# 4. Nuevo endpoint  
@app.get("/usuarios/{user_id}/terminos")
async def verificar_terminos_usuario(user_id: int):
    # ... implementación completa
```

#### Frontend (`pwasuper/src/views/Register.vue`):
- Aviso de privacidad completo con scroll
- Checkbox obligatorio con validaciones
- Botón inteligente deshabilitado/habilitado
- Mensajes de error específicos

---

### 🧪 PRUEBAS POST-DESPLIEGUE

#### 1. Prueba de Registro Nuevo Usuario:
```bash
# Ejecutar en local después del despliegue:
python test_registro_completo.py
```

**Resultado esperado:**
```
✅ Usuario creado exitosamente 
✅ Términos se registraron automáticamente
```

#### 2. Prueba Manual Frontend:
1. Ir a: `https://app.sembrandodatos.com/register`
2. Llenar formulario **SIN** marcar checkbox
3. Verificar: Botón está deshabilitado y gris
4. Marcar checkbox
5. Verificar: Botón se habilita y cambia a azul
6. Completar registro
7. Verificar: Mensaje de éxito menciona términos aceptados

#### 3. Verificación Base de Datos:
```bash
python diagnostico_terminos.py
```

---

### 🚨 POSIBLES ERRORES Y SOLUCIONES

#### Error: "404 Not Found" en `/usuarios/{id}/terminos`
**Causa:** Backend de producción no actualizado  
**Solución:** Subir `main.py` y reiniciar servicio

#### Error: "Tabla usuarios_terminos no existe"
**Causa:** Script de creación de tabla faltante  
**Solución:** Ejecutar en base de datos:
```sql
CREATE TABLE IF NOT EXISTS usuarios_terminos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    aceptado BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_aceptado TIMESTAMP NOT NULL DEFAULT NOW(),
    ip_aceptado VARCHAR(50)
);
```

#### Error: Frontend no muestra aviso de privacidad
**Causa:** Archivos no subidos correctamente  
**Solución:** Verificar que `Register.vue` se subió completo

---

### 📞 CONTACTO DE SOPORTE

Si hay problemas durante el despliegue:
1. Ejecutar scripts de diagnóstico
2. Revisar logs del servidor backend
3. Verificar conectividad con base de datos
4. Comprobar permisos de archivos

---

### ✅ VALIDACIÓN FINAL

**Después del despliegue, verificar:**
- [ ] Página de registro muestra aviso de privacidad
- [ ] Checkbox es obligatorio y funciona
- [ ] Nuevos usuarios se crean con términos automáticamente
- [ ] Mensaje de éxito menciona términos aceptados
- [ ] No hay errores 404 en endpoints de términos
- [ ] Base de datos registra nuevas aceptaciones

**¡Una vez completado, el sistema estará 100% funcional!**
