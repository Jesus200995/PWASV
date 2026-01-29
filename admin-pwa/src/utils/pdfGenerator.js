/**
 * Utilidad para generar PDFs de reportes desde datos estructurados
 * Compatible con admin-pwa
 */
import jsPDF from 'jspdf'

// Imagen de encabezado superior (base64)
const superiorImageBase64 = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAB4AAAAJYCAYAAACp39LTAAAACXBIWXMAAAsSAAALEgHS3X78AAAgAElEQVR4nOzdd3hUVfrA8Xfqzck0eksgIaF3pIggSBFEEVBZ3VXWdW1rW3vvZRV/666ua1l7WdddXRUVUVARBKUjECC9t5lMvf8/xmCMlJCZ3Llzv5/nyYOQmXvfCWTO3O9973te' // Partial data for size

/**
 * Genera un PDF desde los datos estructurados del reporte
 * @param {Object} datos - Datos del reporte (datos_reporte)
 * @param {string} firmaUsuario - Firma del usuario en base64
 * @param {string} firmaSupervisor - Firma del supervisor en base64 (opcional)
 * @param {string} nombreSupervisor - Nombre del supervisor (opcional)
 * @returns {Promise<string>} - PDF en base64 (sin prefijo data:)
 */
export async function generarPDFDesdesDatos(datos, firmaUsuario, firmaSupervisor, nombreSupervisor) {
  console.log('📄 [PDFGenerator] Generando PDF desde datos estructurados...')
  console.log('   - Actividades:', datos.actividades?.length || 0)
  console.log('   - Firma usuario:', firmaUsuario ? 'Sí' : 'No')
  console.log('   - Firma supervisor:', firmaSupervisor ? 'Sí' : 'No')
  
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

  // ========== ENCABEZADO ==========
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
    day: '2-digit', month: '2-digit', year: 'numeric'
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
  const mesNombre = periodo.mesNombre || 'N/A'
  const anio = periodo.anio || 'N/A'
  doc.text(`${mesNombre} ${anio}`, margin + col1Width + 2, currentY + 4)
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
  const colWidths = [15, 32, 18, 22, 83]
  
  // Header
  doc.setFillColor(255, 255, 255)
  doc.rect(tableX, currentY, tableWidth, 8, 'FD')
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
  doc.setFontSize(7)
  doc.setFont(undefined, 'normal')
  const baseRowHeight = 8
  const lineHeight = 3

  actividades.forEach((actividad, index) => {
    const activDesc = actividad.descripcion || actividad.categoria_actividad || 'Actividad de campo'
    const maxTextWidth = colWidths[4] - 4
    const textLines = doc.splitTextToSize(activDesc, maxTextWidth)
    const rowHeight = Math.max(baseRowHeight, textLines.length * lineHeight + 3)
    
    if (currentY > pageHeight - 50) {
      doc.addPage()
      currentY = 20
    }

    doc.rect(tableX, currentY, tableWidth, rowHeight, 'S')

    const fecha = actividad.fecha_hora ? new Date(actividad.fecha_hora).toLocaleDateString('es-MX', { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' }) : '-'
    const hora = actividad.fecha_hora ? new Date(actividad.fecha_hora).toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit', hour12: false }) : '-'
    const tipo = (actividad.tipo_actividad || 'Campo').charAt(0).toUpperCase() + (actividad.tipo_actividad || 'campo').slice(1)

    colX = tableX + 2
    const textYCenter = currentY + (rowHeight / 2) + 1.5
    
    doc.text(String(index + 1), colX + colWidths[0]/2, textYCenter, { align: 'center' })
    doc.line(colX + colWidths[0], currentY, colX + colWidths[0], currentY + rowHeight)
    
    colX += colWidths[0]
    doc.text(fecha, colX + 2, textYCenter)
    doc.line(colX + colWidths[1], currentY, colX + colWidths[1], currentY + rowHeight)
    
    colX += colWidths[1]
    doc.text(tipo, colX + colWidths[2]/2, textYCenter, { align: 'center' })
    doc.line(colX + colWidths[2], currentY, colX + colWidths[2], currentY + rowHeight)
    
    colX += colWidths[2]
    doc.text(hora, colX + colWidths[3]/2, textYCenter, { align: 'center' })
    doc.line(colX + colWidths[3], currentY, colX + colWidths[3], currentY + rowHeight)
    
    colX += colWidths[3]
    textLines.forEach((line, lineIndex) => {
      doc.text(line, colX + 2, currentY + 4 + (lineIndex * lineHeight))
    })

    currentY += rowHeight
  })

  currentY += 15

  // ========== SECCIÓN DE FIRMAS ==========
  if (currentY > pageHeight - 70) {
    doc.addPage()
    currentY = 30
  }

  const firmaWidth = 70
  const firmaHeight = 30
  const firmaUsuarioX = margin + 5
  const firmaResponsableX = pageWidth - margin - firmaWidth - 5
  const firmaY = currentY
  
  // Etiquetas
  doc.setFillColor(255, 218, 185)
  doc.setLineWidth(0.3)
  
  doc.rect(firmaUsuarioX, firmaY - 8, firmaWidth, 7, 'FD')
  doc.setFontSize(9)
  doc.setFont(undefined, 'bold')
  doc.text('Elaboró', firmaUsuarioX + firmaWidth / 2, firmaY - 3.5, { align: 'center' })
  
  doc.setFillColor(255, 218, 185)
  doc.rect(firmaResponsableX, firmaY - 8, firmaWidth, 7, 'FD')
  doc.text('Autorizó', firmaResponsableX + firmaWidth / 2, firmaY - 3.5, { align: 'center' })
  
  // FIRMA DEL USUARIO (Izquierda)
  if (firmaUsuario) {
    try {
      doc.addImage(firmaUsuario, 'PNG', firmaUsuarioX, firmaY, firmaWidth, firmaHeight)
    } catch (e) {
      console.warn('No se pudo agregar firma del usuario')
    }
  }
  
  doc.setLineWidth(0.5)
  doc.line(firmaUsuarioX, firmaY + firmaHeight + 5, firmaUsuarioX + firmaWidth, firmaY + firmaHeight + 5)
  
  doc.setFontSize(8)
  doc.setFont(undefined, 'normal')
  doc.text(usuario.cargo || 'Facilitador Comunitario', firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' })
  doc.setFont(undefined, 'bold')
  doc.text(usuario.nombre || 'Sin nombre', firmaUsuarioX + firmaWidth / 2, firmaY + firmaHeight + 17, { align: 'center' })
  
  // FIRMA DEL SUPERVISOR (Derecha) - Solo si existe
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
  doc.text('Encargada de Despacho de la Coordinación', firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 11, { align: 'center' })
  doc.text('Territorial ' + (usuario.territorio || ''), firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 16, { align: 'center' })
  
  doc.setFontSize(8)
  doc.setFont(undefined, 'bold')
  doc.text(nombreSupervisor || usuario.supervisor || 'Sin asignar', firmaResponsableX + firmaWidth / 2, firmaY + firmaHeight + 22, { align: 'center' })

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
