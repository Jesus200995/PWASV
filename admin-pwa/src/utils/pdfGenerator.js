/**
 * Utilidad para generar PDFs de reportes desde datos estructurados
 * Compatible con admin-pwa - Formato idéntico a pwasuper
 */
import jsPDF from 'jspdf'
import superiorImage from '../assets/images/superior2.png'

/**
 * Genera un PDF desde los datos estructurados del reporte
 * @param {Object} datos - Datos del reporte (datos_reporte)
 * @param {string} firmaUsuario - Firma del usuario en base64
 * @param {string} firmaSupervisor - Firma del supervisor en base64 (opcional)
 * @param {string} nombreSupervisor - Nombre del supervisor (opcional)
 * @param {string} facilitadorNombre - Nombre del facilitador asignado (si existe). Si se proporciona, el subtítulo del firmante será "Facilitador Comunitario" en lugar de "Encargada de Despacho...Territorial".
 * @returns {Promise<string>} - PDF en base64 (sin prefijo data:)
 */
export async function generarPDFDesdesDatos(datos, firmaUsuario, firmaSupervisor, nombreSupervisor, facilitadorNombre = null) {
  console.log('📄 [PDFGenerator] Generando PDF desde datos estructurados...')
  console.log('   - Actividades:', datos.actividades?.length || 0)
  console.log('   - Firma usuario:', firmaUsuario ? 'Sí' : 'No')
  console.log('   - Firma supervisor:', firmaSupervisor ? 'Sí' : 'No')
  console.log('   - Facilitador:', facilitadorNombre || 'No (supervisor territorial)')

  // Determinar si el firmante/responsable es un facilitador comunitario
  const esFacilitador = !!(facilitadorNombre && String(facilitadorNombre).trim())
  
  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a4'
  })

  const pageHeight = doc.internal.pageSize.getHeight()
  const pageWidth = doc.internal.pageSize.getWidth()
  const margin = 15
  const contentWidth = pageWidth - (margin * 2)
  let currentY = 10

  // ========== ENCABEZADO CON IMAGEN DE LOGOS ==========
  console.log('🖼️ Cargando imagen de encabezado...')
  
  let superiorImageBase64
  let imgDimensions
  try {
    const result = await cargarImagenComoBase64(superiorImage)
    superiorImageBase64 = result.data
    imgDimensions = result.dimensions
  } catch (error) {
    console.warn('⚠️ No se pudo cargar imagen de encabezado:', error)
    currentY = 10
  }
  
  if (superiorImageBase64 && imgDimensions) {
    const realAspectRatio = imgDimensions.height / imgDimensions.width
    const imgWidth = contentWidth * 0.95
    const imgHeight = imgWidth * realAspectRatio
    const imgX = margin + (contentWidth - imgWidth) / 2
    
    doc.addImage(superiorImageBase64, 'PNG', imgX, currentY, imgWidth, imgHeight)
    currentY += imgHeight + 5
    console.log('✅ Imagen de encabezado agregada')
  }

  // Recuadro principal con títulos
  doc.setDrawColor(0, 0, 0)
  doc.setLineWidth(0.5)
  doc.rect(margin, currentY, contentWidth, 25)
  
  doc.setFontSize(9)
  doc.setFont(undefined, 'bold')
  doc.setTextColor(0, 0, 0)
  doc.text('SECRETARÍA DE BIENESTAR', pageWidth / 2, currentY + 6, { align: 'center' })
  doc.text('SUBSECRETARÍA DE INCLUSIÓN PRODUCTIVA Y DESARROLLO RURAL', pageWidth / 2, currentY + 11, { align: 'center' })
  doc.text('FORMATO DE SEGUIMIENTO A ACTIVIDADES PROGRAMADAS', pageWidth / 2, currentY + 16, { align: 'center' })
  
  // Fecha en la esquina
  const fechaActual = new Date(datos.fechaGeneracion || new Date()).toLocaleDateString('es-MX', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
  doc.setFontSize(8)
  doc.setFont(undefined, 'normal')
  doc.text('Fecha:', pageWidth - margin - 35, currentY + 21)
  doc.rect(pageWidth - margin - 25, currentY + 18, 25, 5)
  doc.text(fechaActual, pageWidth - margin - 12.5, currentY + 21.5, { align: 'center' })
  
  currentY += 30
  
  // ========== TABLA DE INFORMACIÓN DEL PRESTADOR ==========
  const usuario = datos.usuario || {}
  const periodo = datos.periodo || {}
  const col1Width = contentWidth * 0.5
  const col2Width = contentWidth * 0.5
  
  // Fila 1: Nombre
  doc.setDrawColor(0, 0, 0)
  doc.setLineWidth(0.3)
  doc.rect(margin, currentY, col1Width, 6)
  doc.rect(margin + col1Width, currentY, col2Width, 6)
  doc.setFontSize(8)
  doc.setFont(undefined, 'bold')
  doc.text('Nombre del prestador de Servicios', margin + 2, currentY + 4)
  doc.setFont(undefined, 'normal')
  doc.text(usuario.nombre || 'Sin nombre', margin + col1Width + 2, currentY + 4)
  currentY += 6
  
  // Fila 2: CURP
  doc.rect(margin, currentY, col1Width, 6)
  doc.rect(margin + col1Width, currentY, col2Width, 6)
  doc.setFont(undefined, 'bold')
  doc.text('CURP', margin + 2, currentY + 4)
  doc.setFont(undefined, 'normal')
  doc.text(usuario.curp || 'No registrado', margin + col1Width + 2, currentY + 4)
  currentY += 6
  
  // Fila 3: Periodo
  doc.rect(margin, currentY, col1Width, 6)
  doc.rect(margin + col1Width, currentY, col2Width, 6)
  doc.setFont(undefined, 'bold')
  doc.text('Periodo', margin + 2, currentY + 4)
  doc.setFont(undefined, 'normal')
  
  // Formatear periodo con fechas completas
  const mes = periodo.mes !== undefined ? periodo.mes : 0
  const anio = periodo.anio || new Date().getFullYear()
  const inicioPeriodo = new Date(anio, mes, 1)
  const finPeriodo = new Date(anio, mes + 1, 0)
  const periodoTexto = `Del ${inicioPeriodo.toLocaleDateString('es-MX')} al ${finPeriodo.toLocaleDateString('es-MX')}`
  doc.text(periodoTexto, margin + col1Width + 2, currentY + 4)
  currentY += 8
  
  // Fila 4: Programa
  doc.rect(margin, currentY, col1Width, 6)
  doc.rect(margin + col1Width, currentY, col2Width, 6)
  doc.setFont(undefined, 'bold')
  doc.text('Programa Social del Apoyo', margin + 2, currentY + 4)
  doc.setFont(undefined, 'normal')
  doc.text('SEMBRANDO VIDA', margin + col1Width + 2, currentY + 4)
  currentY += 8
  
  // Fila 5: Territorio
  doc.rect(margin, currentY, col1Width, 6)
  doc.rect(margin + col1Width, currentY, col2Width, 6)
  doc.setFont(undefined, 'bold')
  doc.text('Territorio y entidad donde presta sus servicios', margin + 2, currentY + 4)
  doc.setFont(undefined, 'normal')
  doc.text(usuario.territorio || 'No asignado', margin + col1Width + 2, currentY + 4)
  currentY += 10
  
  // ========== TABLA DE ACTIVIDADES ==========
  const actividades = datos.actividades || []
  const tableWidth = contentWidth
  const tableX = margin
  const colWidths = [15, 32, 18, 22, 83] // No., Fecha, Tipo, Hora, Actividad
  
  // Header de la tabla
  doc.setDrawColor(0, 0, 0)
  doc.setLineWidth(0.3)
  doc.setFillColor(255, 255, 255)
  doc.rect(tableX, currentY, tableWidth, 8, 'FD')
  
  doc.setTextColor(0, 0, 0)
  doc.setFontSize(8)
  doc.setFont(undefined, 'bold')
  
  let colX = tableX + 2
  doc.text('No.', colX + colWidths[0]/2, currentY + 5.5, { align: 'center' })
  doc.line(colX + colWidths[0], currentY, colX + colWidths[0], currentY + 8)
  
  colX += colWidths[0]
  doc.text('Fecha', colX + colWidths[1]/2, currentY + 5.5, { align: 'center' })
  doc.line(colX + colWidths[1], currentY, colX + colWidths[1], currentY + 8)
  
  colX += colWidths[1]
  doc.text('Tipo', colX + colWidths[2]/2, currentY + 5.5, { align: 'center' })
  doc.line(colX + colWidths[2], currentY, colX + colWidths[2], currentY + 8)
  
  colX += colWidths[2]
  doc.text('Hora', colX + colWidths[3]/2, currentY + 5.5, { align: 'center' })
  doc.line(colX + colWidths[3], currentY, colX + colWidths[3], currentY + 8)
  
  colX += colWidths[3]
  doc.text('Actividad desarrollada', colX + colWidths[4]/2, currentY + 5.5, { align: 'center' })

  currentY += 8
  
  // Filas de datos
  doc.setTextColor(0, 0, 0)
  doc.setFontSize(7)
  doc.setFont(undefined, 'normal')
  
  const baseRowHeight = 8
  const lineHeight = 3

  actividades.forEach((actividad, index) => {
    const activDesc = actividad.descripcion || actividad.categoria_actividad || 'Actividad de ' + (actividad.tipo_actividad || 'campo')
    const maxTextWidth = colWidths[4] - 4
    const textLines = doc.splitTextToSize(activDesc, maxTextWidth)
    const numLines = textLines.length
    const rowHeight = Math.max(baseRowHeight, numLines * lineHeight + 3)
    
    // Verificar si necesitamos nueva página
    if (currentY > pageHeight - 50) {
      doc.addPage()
      currentY = 20
      
      // Re-dibujar header de tabla en nueva página
      doc.setDrawColor(0, 0, 0)
      doc.setLineWidth(0.3)
      doc.setFillColor(255, 255, 255)
      doc.rect(tableX, currentY, tableWidth, 8, 'FD')
      
      doc.setTextColor(0, 0, 0)
      doc.setFontSize(8)
      doc.setFont(undefined, 'bold')
      
      let headerX = tableX + 2
      doc.text('No.', headerX + colWidths[0]/2, currentY + 5.5, { align: 'center' })
      doc.line(headerX + colWidths[0], currentY, headerX + colWidths[0], currentY + 8)
      
      headerX += colWidths[0]
      doc.text('Fecha', headerX + colWidths[1]/2, currentY + 5.5, { align: 'center' })
      doc.line(headerX + colWidths[1], currentY, headerX + colWidths[1], currentY + 8)
      
      headerX += colWidths[1]
      doc.text('Tipo', headerX + colWidths[2]/2, currentY + 5.5, { align: 'center' })
      doc.line(headerX + colWidths[2], currentY, headerX + colWidths[2], currentY + 8)
      
      headerX += colWidths[2]
      doc.text('Hora', headerX + colWidths[3]/2, currentY + 5.5, { align: 'center' })
      doc.line(headerX + colWidths[3], currentY, headerX + colWidths[3], currentY + 8)
      
      headerX += colWidths[3]
      doc.text('Actividad desarrollada', headerX + colWidths[4]/2, currentY + 5.5, { align: 'center' })
      
      currentY += 8
      doc.setTextColor(0, 0, 0)
      doc.setFontSize(7)
      doc.setFont(undefined, 'normal')
    }

    // Bordes de la fila
    doc.setDrawColor(0, 0, 0)
    doc.setLineWidth(0.3)
    doc.rect(tableX, currentY, tableWidth, rowHeight, 'S')

    const fechaObj = actividad.fecha_hora ? new Date(actividad.fecha_hora) : new Date()
    const fecha = fechaObj.toLocaleDateString('es-MX', { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' })
    const hora = fechaObj.toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit', hour12: false })
    const tipo = (actividad.tipo_actividad || 'Campo').charAt(0).toUpperCase() + (actividad.tipo_actividad || 'campo').slice(1)

    colX = tableX + 2
    const textYCenter = currentY + (rowHeight / 2) + 1.5
    
    // No.
    doc.text(String(index + 1), colX + colWidths[0]/2, textYCenter, { align: 'center' })
    doc.line(colX + colWidths[0], currentY, colX + colWidths[0], currentY + rowHeight)
    
    // Fecha
    colX += colWidths[0]
    doc.text(fecha, colX + 2, textYCenter)
    doc.line(colX + colWidths[1], currentY, colX + colWidths[1], currentY + rowHeight)
    
    // Tipo
    colX += colWidths[1]
    doc.text(tipo, colX + colWidths[2]/2, textYCenter, { align: 'center' })
    doc.line(colX + colWidths[2], currentY, colX + colWidths[2], currentY + rowHeight)
    
    // Hora
    colX += colWidths[2]
    doc.text(hora, colX + colWidths[3]/2, textYCenter, { align: 'center' })
    doc.line(colX + colWidths[3], currentY, colX + colWidths[3], currentY + rowHeight)
    
    // Actividad - múltiples líneas
    colX += colWidths[3]
    textLines.forEach((line, lineIndex) => {
      doc.text(line, colX + 2, currentY + 4 + (lineIndex * lineHeight))
    })

    currentY += rowHeight
  })

  currentY += 15

  // ========== SECCIÓN DE FIRMAS (Formato oficial) ==========
  if (firmaUsuario) {
    // Verificar si necesitamos nueva página para las firmas
    if (currentY > pageHeight - 70) {
      doc.addPage()
      currentY = 30
    }

    const firmaWidth = 70
    const firmaHeight = 30
    const firmaUsuarioX = margin + 5
    const firmaResponsableX = pageWidth - margin - firmaWidth - 5
    const firmaY = currentY
    
    // Etiquetas "Elaboró" y "Autorizó"
    doc.setFillColor(255, 218, 185) // Color durazno/naranja claro
    doc.setDrawColor(0, 0, 0)
    doc.setLineWidth(0.3)
    
    // Etiqueta "Elaboró"
    doc.rect(firmaUsuarioX, firmaY - 8, firmaWidth, 7, 'FD')
    doc.setTextColor(0, 0, 0)
    doc.setFontSize(9)
    doc.setFont(undefined, 'bold')
    doc.text('Elaboró', firmaUsuarioX + firmaWidth / 2, firmaY - 3.5, { align: 'center' })
    
    // Etiqueta "Autorizó"
    doc.setFillColor(255, 218, 185)
    doc.rect(firmaResponsableX, firmaY - 8, firmaWidth, 7, 'FD')
    doc.text('Autorizó', firmaResponsableX + firmaWidth / 2, firmaY - 3.5, { align: 'center' })
    
    // FIRMA DEL PRESTADOR DE SERVICIOS (Izquierda)
    try {
      doc.addImage(firmaUsuario, 'PNG', firmaUsuarioX, firmaY, firmaWidth, firmaHeight)
      console.log('✅ Firma del usuario agregada al PDF')
    } catch (e) {
      console.warn('No se pudo agregar firma del usuario')
    }
    
    doc.setDrawColor(0, 0, 0)
    doc.setLineWidth(0.5)
    doc.line(firmaUsuarioX, firmaY + firmaHeight + 5, firmaUsuarioX + firmaWidth, firmaY + firmaHeight + 5)
    
    doc.setTextColor(0, 0, 0)
    doc.setFontSize(8)
    doc.setFont(undefined, 'normal')
    const cargoUsuario = usuario.cargo || 'Facilitador Comunitario'
    doc.text(cargoUsuario, firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' })
    
    doc.setFontSize(8)
    doc.setFont(undefined, 'bold')
    const nombreUsuario = usuario.nombre || 'Sin nombre'
    doc.text(nombreUsuario, firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 17, { align: 'center' })
    
    // FIRMA DEL RESPONSABLE (Derecha)
    if (firmaSupervisor) {
      try {
        doc.addImage(firmaSupervisor, 'PNG', firmaResponsableX, firmaY, firmaWidth, firmaHeight)
        console.log('✅ Firma del supervisor agregada al PDF')
      } catch (e) {
        console.warn('No se pudo agregar firma del supervisor')
      }
    }
    
    doc.setLineWidth(0.5)
    doc.line(firmaResponsableX, firmaY + firmaHeight + 5, firmaResponsableX + firmaWidth, firmaY + firmaHeight + 5)
    
    doc.setFontSize(7.5)
    doc.setFont(undefined, 'normal')
    if (esFacilitador) {
      // Firmante es Facilitador Comunitario
      doc.text('FACILITADOR COMUNITARIO', firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' })
    } else {
      // Firmante es supervisor territorial (Encargada de Despacho)
      doc.text('Encargada de Despacho de la Coordinación', firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' })
      doc.text('Territorial ' + (usuario.territorio || ''), firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 16, { align: 'center' })
    }

    doc.setFontSize(8)
    doc.setFont(undefined, 'bold')
    const nombreSupervisorFinal = nombreSupervisor || facilitadorNombre || usuario.supervisor || 'Sin asignar'
    // Si es facilitador, el nombre sube (solo una línea de cargo)
    const nombreY = esFacilitador ? firmaY + firmaHeight + 17 : firmaY + firmaHeight + 22
    doc.text(nombreSupervisorFinal, firmaResponsableX + firmaWidth / 2, nombreY, { align: 'center' })

    currentY = firmaY + firmaHeight + 30
  }

  // ========== SEGUNDA PÁGINA: EVIDENCIAS FOTOGRÁFICAS ==========
  try {
    console.log('🖼️ Generando página de evidencias fotográficas...')
    
    const actividadesConFoto = (datos.actividades || []).filter(act => act.foto_url || act.foto_base64)
    console.log(`📸 Actividades con foto: ${actividadesConFoto.length}`)
    
    // SIEMPRE crear la página de evidencias
    doc.addPage()
    currentY = 10
    
    // Cargar imagen de encabezado para segunda página
    if (superiorImageBase64 && imgDimensions) {
      const realAspectRatio = imgDimensions.height / imgDimensions.width
      const imgWidth = contentWidth * 0.95
      const imgHeight = imgWidth * realAspectRatio
      const imgX = margin + (contentWidth - imgWidth) / 2
      
      doc.addImage(superiorImageBase64, 'PNG', imgX, currentY, imgWidth, imgHeight)
      currentY += imgHeight + 5
    }
    
    // Título de la sección
    doc.setDrawColor(0, 0, 0)
    doc.setLineWidth(0.5)
    doc.rect(margin, currentY, contentWidth, 12)
    
    doc.setFontSize(11)
    doc.setFont(undefined, 'bold')
    doc.setTextColor(0, 0, 0)
    doc.text('EVIDENCIAS FOTOGRÁFICAS DE ACTIVIDADES', pageWidth / 2, currentY + 5, { align: 'center' })
    doc.setFontSize(9)
    doc.setFont(undefined, 'normal')
    doc.text(`${periodo.mesNombre || ''} ${periodo.anio || ''}`, pageWidth / 2, currentY + 10, { align: 'center' })
    
    currentY += 15

    // Datos del usuario
    doc.setFillColor(240, 240, 240)
    doc.setDrawColor(0, 0, 0)
    doc.setLineWidth(0.3)
    doc.rect(margin, currentY, contentWidth, 18, 'FD')
    
    doc.setFontSize(8)
    doc.setTextColor(0, 0, 0)
    
    doc.setFont(undefined, 'bold')
    doc.text('Nombre:', margin + 3, currentY + 5)
    doc.setFont(undefined, 'normal')
    doc.text(usuario.nombre || 'Sin nombre', margin + 20, currentY + 5)
    
    doc.setFont(undefined, 'bold')
    doc.text('CURP:', margin + 95, currentY + 5)
    doc.setFont(undefined, 'normal')
    doc.text(usuario.curp || 'No registrado', margin + 107, currentY + 5)
    
    doc.setFont(undefined, 'bold')
    doc.text('Cargo:', margin + 3, currentY + 11)
    doc.setFont(undefined, 'normal')
    doc.text(usuario.cargo || 'Facilitador Comunitario', margin + 17, currentY + 11)
    
    doc.setFont(undefined, 'bold')
    doc.text('Territorio:', margin + 95, currentY + 11)
    doc.setFont(undefined, 'normal')
    doc.text(usuario.territorio || 'No asignado', margin + 115, currentY + 11)
    
    doc.setFont(undefined, 'bold')
    doc.text('Período:', margin + 3, currentY + 17)
    doc.setFont(undefined, 'normal')
    doc.text(`${periodo.mesNombre || ''} ${periodo.anio || ''}`, margin + 18, currentY + 17)
    
    currentY += 22

    if (actividadesConFoto.length === 0) {
      // Mensaje cuando no hay fotos
      currentY += 20
      doc.setFillColor(255, 243, 205)
      doc.setDrawColor(200, 180, 100)
      doc.setLineWidth(0.5)
      doc.rect(margin, currentY, contentWidth, 40, 'FD')
      
      doc.setTextColor(120, 100, 50)
      doc.setFontSize(12)
      doc.setFont(undefined, 'bold')
      doc.text('Sin evidencias fotográficas disponibles', pageWidth / 2, currentY + 15, { align: 'center' })
      
      doc.setFontSize(9)
      doc.setFont(undefined, 'normal')
      doc.text('El reporte fotográfico solo está disponible para el mes en curso;', pageWidth / 2, currentY + 25, { align: 'center' })
      doc.text('al descargar información de meses anteriores, las fotografías no se mostrarán.', pageWidth / 2, currentY + 32, { align: 'center' })
      
      currentY += 50
    } else {
      // Función para seleccionar imágenes de diferentes días
      const seleccionarImagenesDiversas = (actividades, maxImagenes) => {
        const imagenesSeleccionadas = []
        const diasUsados = new Set()
        
        // Ordenar por fecha más reciente
        const actividadesOrdenadas = [...actividades].sort((a, b) => new Date(b.fecha_hora) - new Date(a.fecha_hora))
        
        // Primera pasada: una imagen por día
        for (const act of actividadesOrdenadas) {
          if (imagenesSeleccionadas.length >= maxImagenes) break
          const dia = new Date(act.fecha_hora).toISOString().split('T')[0]
          if (!diasUsados.has(dia)) {
            imagenesSeleccionadas.push(act)
            diasUsados.add(dia)
          }
        }
        
        // Segunda pasada: si no hay suficientes, agregar las restantes
        if (imagenesSeleccionadas.length < maxImagenes) {
          for (const act of actividadesOrdenadas) {
            if (imagenesSeleccionadas.length >= maxImagenes) break
            if (!imagenesSeleccionadas.includes(act)) {
              imagenesSeleccionadas.push(act)
            }
          }
        }
        
        return imagenesSeleccionadas
      }
      
      // Seleccionar hasta 6 imágenes (3 campo, 3 gabinete) priorizando diferentes días
      const actividadesCampoDisponibles = actividadesConFoto
        .filter(a => (a.tipo_actividad || 'campo').toLowerCase() === 'campo')
      const actividadesGabineteDisponibles = actividadesConFoto
        .filter(a => (a.tipo_actividad || '').toLowerCase() === 'gabinete')
      
      const actividadesCampo = seleccionarImagenesDiversas(actividadesCampoDisponibles, 3)
      const actividadesGabinete = seleccionarImagenesDiversas(actividadesGabineteDisponibles, 3)
      
      const imagenesSeleccionadas = [...actividadesCampo, ...actividadesGabinete].slice(0, 6)
      console.log(`📷 Procesando ${imagenesSeleccionadas.length} imágenes para el PDF`)
      
      // Grid de imágenes
      const imgGridWidth = 55
      const imgGridHeight = 45
      const imgsPerRow = 3
      const imgSpacing = 5
      const labelHeight = 14
      
      for (let i = 0; i < imagenesSeleccionadas.length; i++) {
        const actividad = imagenesSeleccionadas[i]
        const col = i % imgsPerRow
        const row = Math.floor(i / imgsPerRow)
        
        const imgX = margin + (col * (imgGridWidth + imgSpacing))
        const imgY = currentY + (row * (imgGridHeight + labelHeight + 5))
        
        // Verificar si necesitamos nueva página
        if (imgY + imgGridHeight + labelHeight + 15 > pageHeight - 40) {
          doc.addPage()
          currentY = 20
          
          doc.setFontSize(9)
          doc.setFont(undefined, 'bold')
          doc.setTextColor(0, 0, 0)
          doc.text('EVIDENCIAS FOTOGRÁFICAS (Continuación)', pageWidth / 2, currentY, { align: 'center' })
          currentY += 10
        }
        
        // Borde de la imagen
        doc.setDrawColor(0, 0, 0)
        doc.setLineWidth(0.3)
        doc.rect(imgX, imgY, imgGridWidth, imgGridHeight)
        
        // Intentar agregar imagen
        try {
          let imgData = null
          
          // Primero intentar con foto_base64
          if (actividad.foto_base64) {
            let imgBase64 = actividad.foto_base64
            if (!imgBase64.startsWith('data:')) {
              imgBase64 = 'data:image/jpeg;base64,' + imgBase64
            }
            imgData = imgBase64
            console.log(`✅ Usando foto_base64 para imagen ${i + 1}`)
          }
          // Si no tiene foto_base64, intentar cargar desde foto_url
          else if (actividad.foto_url) {
            console.log(`📥 Cargando imagen ${i + 1} desde URL: ${actividad.foto_url}`)
            try {
              const result = await cargarImagenComoBase64(actividad.foto_url)
              imgData = result.data
              console.log(`✅ Imagen ${i + 1} cargada desde URL`)
            } catch (loadError) {
              console.warn(`⚠️ No se pudo cargar imagen ${i + 1} desde URL:`, loadError)
            }
          }
          
          // Si tenemos imagen, agregarla
          if (imgData) {
            doc.addImage(imgData, 'JPEG', imgX + 1, imgY + 1, imgGridWidth - 2, imgGridHeight - 2)
            console.log(`✅ Imagen ${i + 1} agregada al PDF`)
          } else {
            // Placeholder gris
            doc.setFillColor(220, 220, 220)
            doc.rect(imgX + 1, imgY + 1, imgGridWidth - 2, imgGridHeight - 2, 'F')
            doc.setDrawColor(200, 200, 200)
            doc.rect(imgX, imgY, imgGridWidth, imgGridHeight, 'S')
            
            doc.setTextColor(150, 150, 150)
            doc.setFontSize(8)
            doc.text('Imagen no', imgX + imgGridWidth / 2, imgY + imgGridHeight / 2 - 3, { align: 'center' })
            doc.text('disponible', imgX + imgGridWidth / 2, imgY + imgGridHeight / 2 + 3, { align: 'center' })
            console.log(`⚠️ Imagen ${i + 1} sin datos`)
          }
        } catch (imgError) {
          console.warn(`❌ Error agregando imagen ${i + 1}:`, imgError)
          
          // Placeholder en caso de error
          doc.setFillColor(240, 240, 240)
          doc.rect(imgX, imgY, imgGridWidth, imgGridHeight, 'F')
          doc.setDrawColor(200, 200, 200)
          doc.rect(imgX, imgY, imgGridWidth, imgGridHeight, 'S')
          
          doc.setTextColor(150, 150, 150)
          doc.setFontSize(8)
          doc.text('Imagen no', imgX + imgGridWidth / 2, imgY + imgGridHeight / 2 - 3, { align: 'center' })
          doc.text('disponible', imgX + imgGridWidth / 2, imgY + imgGridHeight / 2 + 3, { align: 'center' })
        }
        
        // Etiqueta con tipo y fecha
        const tipoAct = actividad.tipo_actividad || actividad.tipo || 'campo'
        const tipoTexto = tipoAct.toLowerCase() === 'campo' ? 'CAMPO' : 'GABINETE'
        
        // Fondo según tipo
        if (tipoAct.toLowerCase() === 'campo') {
          doc.setFillColor(34, 197, 94) // Verde
        } else {
          doc.setFillColor(147, 51, 234) // Morado
        }
        doc.rect(imgX, imgY + imgGridHeight, imgGridWidth, labelHeight, 'F')
        doc.setDrawColor(0, 0, 0)
        doc.setLineWidth(0.2)
        doc.rect(imgX, imgY + imgGridHeight, imgGridWidth, labelHeight, 'S')
        
        // Texto tipo
        doc.setTextColor(255, 255, 255)
        doc.setFontSize(10)
        doc.setFont(undefined, 'bold')
        doc.text(tipoTexto, imgX + imgGridWidth / 2, imgY + imgGridHeight + 6, { align: 'center' })
        
        // Fecha compacta
        if (actividad.fecha_hora || actividad.fecha) {
          const fechaObj = new Date(actividad.fecha_hora || actividad.fecha)
          const dia = String(fechaObj.getDate()).padStart(2, '0')
          const mes = String(fechaObj.getMonth() + 1).padStart(2, '0')
          const anio = String(fechaObj.getFullYear()).slice(-2)
          const hora = String(fechaObj.getHours()).padStart(2, '0')
          const min = String(fechaObj.getMinutes()).padStart(2, '0')
          const fechaCompacta = `${dia}/${mes}/${anio} ${hora}:${min}`
          
          doc.setFont(undefined, 'normal')
          doc.setFontSize(6)
          doc.text(fechaCompacta, imgX + imgGridWidth / 2, imgY + imgGridHeight + 11, { align: 'center' })
        }
      }
      
      // Calcular currentY después del grid de imágenes
      const numRows = Math.ceil(imagenesSeleccionadas.length / imgsPerRow)
      currentY += (numRows * (imgGridHeight + labelHeight + 3)) + 20
    }
    
    // ========== FIRMAS EN PÁGINA DE EVIDENCIAS ==========
    if (firmaUsuario) {
      // Verificar si hay espacio para firmas
      if (currentY > pageHeight - 70) {
        doc.addPage()
        currentY = 30
      }

      const firmaWidth = 65
      const firmaHeight = 25
      const firmaUsuarioX = margin + 5
      const firmaResponsableX = pageWidth - margin - firmaWidth - 5
      const firmaY = currentY
      
      // Etiquetas "Elaboró" y "Autorizó"
      doc.setFillColor(255, 218, 185)
      doc.setDrawColor(0, 0, 0)
      doc.setLineWidth(0.3)
      
      doc.rect(firmaUsuarioX, firmaY - 8, firmaWidth, 7, 'FD')
      doc.setTextColor(0, 0, 0)
      doc.setFontSize(9)
      doc.setFont(undefined, 'bold')
      doc.text('Elaboró', firmaUsuarioX + firmaWidth / 2, firmaY - 3.5, { align: 'center' })
      
      doc.setFillColor(255, 218, 185)
      doc.rect(firmaResponsableX, firmaY - 8, firmaWidth, 7, 'FD')
      doc.text('Autorizó', firmaResponsableX + firmaWidth / 2, firmaY - 3.5, { align: 'center' })
      
      // FIRMA DEL USUARIO (Izquierda)
      try {
        doc.addImage(firmaUsuario, 'PNG', firmaUsuarioX, firmaY, firmaWidth, firmaHeight)
      } catch (e) {
        console.warn('No se pudo agregar firma del usuario en página de evidencias')
      }
      
      // Líneas de firma
      doc.setLineWidth(0.5)
      doc.line(firmaUsuarioX, firmaY + firmaHeight + 5, firmaUsuarioX + firmaWidth, firmaY + firmaHeight + 5)
      doc.line(firmaResponsableX, firmaY + firmaHeight + 5, firmaResponsableX + firmaWidth, firmaY + firmaHeight + 5)
      
      // Información del usuario
      doc.setTextColor(0, 0, 0)
      doc.setFontSize(8)
      doc.setFont(undefined, 'normal')
      const cargoUsuario = usuario.cargo || 'Facilitador Comunitario'
      doc.text(cargoUsuario, firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' })
      doc.setFont(undefined, 'bold')
      doc.text(usuario.nombre || 'Sin nombre', firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 17, { align: 'center' })
      
      // FIRMA DEL SUPERVISOR (Derecha) - Si existe
      if (firmaSupervisor) {
        try {
          doc.addImage(firmaSupervisor, 'PNG', firmaResponsableX, firmaY, firmaWidth, firmaHeight)
        } catch (e) {
          console.warn('No se pudo agregar firma del supervisor en página de evidencias')
        }
      }
      
      // Información del responsable
      doc.setFontSize(7.5)
      doc.setFont(undefined, 'normal')
      if (esFacilitador) {
        doc.text('FACILITADOR COMUNITARIO', firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' })
      } else {
        doc.text('Encargada de Despacho de la Coordinación', firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' })
        doc.text('Territorial ' + (usuario.territorio || ''), firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 16, { align: 'center' })
      }
      doc.setFontSize(8)
      doc.setFont(undefined, 'bold')
      const nombreSupervisorFinal = nombreSupervisor || facilitadorNombre || usuario.supervisor || 'Sin asignar'
      const nombreY = esFacilitador ? firmaY + firmaHeight + 17 : firmaY + firmaHeight + 22
      doc.text(nombreSupervisorFinal, firmaResponsableX + firmaWidth / 2, nombreY, { align: 'center' })
    }
    
  } catch (evidenciasError) {
    console.error('❌ Error generando página de evidencias:', evidenciasError)
  }

  // ========== PIE DE PÁGINA ==========
  const totalPages = doc.internal.getNumberOfPages()
  for (let i = 1; i <= totalPages; i++) {
    doc.setPage(i)
    doc.setTextColor(128, 0, 32)
    doc.setFontSize(7)
    doc.setFont(undefined, 'normal')
    const footerText = 'Paseo de la Reforma # 116, Piso 16, Col. Juárez, Alc. Cuauhtémoc, CDMX C.P. 06600 Tel.: (55) 5328 5000 www.gob.mx/bienestar'
    doc.text(footerText, pageWidth / 2, pageHeight - 10, { align: 'center' })
  }

  // Obtener PDF como base64 (sin prefijo data:)
  const pdfOutput = doc.output('datauristring')
  const base64 = pdfOutput.split(',')[1]
  
  console.log('✅ PDF generado desde datos estructurados')
  return base64
}

/**
 * Carga una imagen como base64 con dimensiones
 */
async function cargarImagenComoBase64(imageSrc) {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.crossOrigin = 'Anonymous'
    
    img.onload = function() {
      try {
        const canvas = document.createElement('canvas')
        canvas.width = img.width
        canvas.height = img.height
        
        const ctx = canvas.getContext('2d')
        ctx.drawImage(img, 0, 0)
        
        const dataURL = canvas.toDataURL('image/png')
        resolve({
          data: dataURL,
          dimensions: {
            width: img.width,
            height: img.height
          }
        })
      } catch (error) {
        reject(error)
      }
    }
    
    img.onerror = function(error) {
      reject(error)
    }
    
    img.src = imageSrc
  })
}
