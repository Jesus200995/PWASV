/**
 * Utilidad para comprimir imágenes antes de enviarlas al servidor
 * Reduce el tamaño manteniendo una calidad media
 */

/**
 * Comprime una imagen y la convierte a formato JPG con calidad media
 * @param {File|Blob} file - El archivo de imagen original
 * @param {Number} maxWidth - Ancho máximo de la imagen (por defecto 1280px)
 * @param {Number} quality - Calidad de la compresión (0-1, por defecto 0.6 = calidad media)
 * @returns {Promise<Blob>} - Blob de imagen comprimida en formato JPG
 */
export async function compressImage(file, maxWidth = 1280, quality = 0.6) {
  return new Promise((resolve, reject) => {
    try {
      // Crear un elemento Image para cargar el archivo
      const img = new Image();
      
      // Crear URL para el archivo
      const objectURL = URL.createObjectURL(file);
      
      img.onload = () => {
        // Liberar el URL del objeto para evitar fugas de memoria
        URL.revokeObjectURL(objectURL);
        
        // Calcular proporciones para mantener la relación de aspecto
        let width = img.width;
        let height = img.height;
        
        // Redimensionar solo si es más grande que el ancho máximo
        if (width > maxWidth) {
          height = Math.floor(height * (maxWidth / width));
          width = maxWidth;
        }
        
        // Crear canvas para manipular la imagen
        const canvas = document.createElement('canvas');
        canvas.width = width;
        canvas.height = height;
        
        // Dibujar la imagen redimensionada en el canvas
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, width, height);
        
        // Convertir a JPG con la calidad especificada
        canvas.toBlob(
          (blob) => {
            if (blob) {
              // Crear un nuevo archivo con extensión .jpg
              const compressedFile = new Blob([blob], { type: 'image/jpeg' });
              
              // Añadir propiedades de archivo útiles
              const compressedBlob = new Blob([compressedFile], { 
                type: 'image/jpeg',
              });
              
              console.log(`✅ Imagen comprimida: 
                Original: ${(file.size / 1024).toFixed(2)} KB
                Comprimida: ${(compressedBlob.size / 1024).toFixed(2)} KB
                Reducción: ${(100 - (compressedBlob.size * 100 / file.size)).toFixed(2)}%`);
              
              resolve(compressedBlob);
            } else {
              reject(new Error('Error al comprimir la imagen'));
            }
          },
          'image/jpeg',
          quality // Calidad media (0.6)
        );
      };
      
      img.onerror = () => {
        URL.revokeObjectURL(objectURL);
        reject(new Error('Error al cargar la imagen para compresión'));
      };
      
      // Establecer la fuente de la imagen
      img.src = objectURL;
    } catch (error) {
      reject(error);
    }
  });
}

/**
 * Convierte un Blob a un objeto File con un nombre personalizado
 * @param {Blob} blob - El Blob de la imagen
 * @param {String} fileName - Nombre para el archivo
 * @returns {File} - Objeto File
 */
export function blobToFile(blob, fileName) {
  // Crear un nuevo objeto File con el blob
  return new File([blob], fileName, { 
    type: 'image/jpeg',
    lastModified: new Date().getTime()
  });
}
