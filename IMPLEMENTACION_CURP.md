# Implementación del Campo CURP - Instrucciones de Despliegue

## 📋 Resumen de Cambios Implementados

### Backend (FastAPI) ✅
- ✅ Actualizado modelo `UserCreate` para incluir campo `curp: str`
- ✅ Agregada validación de CURP en endpoint `/usuarios`:
  - Campo obligatorio
  - Exactamente 18 caracteres
  - Conversión automática a mayúsculas
  - Validación de unicidad (no duplicados)
- ✅ Actualizados endpoints de consulta para incluir CURP:
  - `GET /usuarios` (listar todos)
  - `GET /usuarios/{user_id}` (obtener uno)
- ✅ Agregado endpoint de debugging: `GET /debug/usuarios-estructura`

### Frontend (Vue.js) ✅
- ✅ Agregado campo CURP en formulario de registro
- ✅ Validación en tiempo real:
  - Conversión automática a mayúsculas
  - Validación de 18 caracteres
  - Validación de formato (solo letras y números)
  - Mensajes de error descriptivos
- ✅ Incluye CURP en petición de registro al backend
- ✅ URL de API configurada a producción: `https://apipwa.sembrandodatos.com`

## 🗃️ Base de Datos - IMPORTANTE

**DEBES EJECUTAR ESTE SCRIPT SQL ANTES DE USAR EL SISTEMA:**

```sql
-- Ejecutar en PostgreSQL
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'usuarios' 
        AND column_name = 'curp'
    ) THEN
        ALTER TABLE usuarios ADD COLUMN curp VARCHAR(18) UNIQUE;
        COMMENT ON COLUMN usuarios.curp IS 'Clave Única de Registro de Población - 18 caracteres obligatorios';
        RAISE NOTICE 'Columna CURP agregada exitosamente a la tabla usuarios';
    ELSE
        RAISE NOTICE 'La columna CURP ya existe en la tabla usuarios';
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_usuarios_curp ON usuarios(curp);
```

## 🚀 Pasos de Despliegue

### 1. Base de Datos
```bash
# Conectar a PostgreSQL y ejecutar:
psql -h 31.97.8.51 -d app_registros -U jesus
# Ejecutar el script SQL de arriba
```

### 2. Backend
```bash
# El código ya está actualizado en main.py
# Solo reiniciar el servidor:
cd backend
python main.py
```

### 3. Frontend
```bash
# El código ya está actualizado
# Compilar y desplegar:
cd pwasuper
npm run build
# Subir dist/ al servidor web
```

## 🧪 Pruebas

### Probar Backend
```bash
cd backend
python test_registro_curp.py
```

### Probar Frontend
1. Abrir el formulario de registro
2. Intentar registrar sin CURP (debe fallar)
3. Intentar con CURP de 17 caracteres (debe fallar)
4. Intentar con CURP de 19 caracteres (debe fallar)
5. Registrar con CURP válida de 18 caracteres (debe funcionar)

### Verificar Base de Datos
```sql
-- Ver estructura actualizada
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'usuarios' 
ORDER BY ordinal_position;

-- Ver registros con CURP
SELECT id, correo, nombre_completo, curp 
FROM usuarios 
WHERE curp IS NOT NULL;
```

## 📱 Estructura Esperada del Usuario

```json
{
  "correo": "usuario@ejemplo.com",
  "nombre_completo": "Juan Pérez García",
  "cargo": "Desarrollador",
  "supervisor": "María González",
  "contrasena": "mi_password_seguro",
  "curp": "PEGJ901201HDFRLN08"
}
```

## ⚠️ Validaciones Implementadas

### Frontend
- ✅ CURP obligatoria
- ✅ Exactamente 18 caracteres
- ✅ Solo letras mayúsculas y números
- ✅ Conversión automática a mayúsculas
- ✅ Mensajes de error en tiempo real

### Backend
- ✅ CURP obligatoria (HTTP 400 si falta)
- ✅ Exactamente 18 caracteres (HTTP 400 si no)
- ✅ Conversión automática a mayúsculas
- ✅ Unicidad (HTTP 400 si ya existe)
- ✅ Validación de formato

## 🔧 Endpoints Actualizados

| Método | Endpoint | Cambios |
|--------|----------|---------|
| POST | `/usuarios` | Requiere campo `curp`, validaciones agregadas |
| GET | `/usuarios` | Incluye `curp` en respuesta |
| GET | `/usuarios/{id}` | Incluye `curp` en respuesta |
| GET | `/debug/usuarios-estructura` | **NUEVO** - Para verificar tabla |

## 📞 Contacto y Soporte

Si hay problemas:
1. Verificar que la columna CURP exista en la base de datos
2. Verificar que el backend esté corriendo
3. Verificar logs del servidor para errores
4. Usar endpoint de debug para verificar estructura

## ✅ Checklist de Verificación

- [ ] Script SQL ejecutado en base de datos
- [ ] Backend reiniciado
- [ ] Frontend compilado y desplegado
- [ ] Prueba de registro exitosa con CURP
- [ ] Verificación en base de datos que CURP se guarda
- [ ] Validaciones funcionando (campos obligatorios, longitud, formato)
- [ ] URL de API apuntando a producción
