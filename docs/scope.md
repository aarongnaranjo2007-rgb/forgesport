---
title: ForgeSport — Alcance del MVP
---
# ForgeSport — Alcance del MVP

## Funcionalidades incluidas

### Catálogo
- Página de inicio sencilla.
- Listado de productos activos.
- Búsqueda simple por nombre.
- Filtro básico por categoría.
- Acceso al detalle del producto.
- Indicador de disponibilidad (agotado vs disponible).

### Detalle de producto
- Nombre, descripción, precio, imagen principal, categoría y stock disponible.
- Selector de cantidad.
- Botón para añadir al carrito (desactivado si no hay stock).

### Usuarios
- Registro, inicio de sesión y cierre de sesión.
- Roles `customer` y `admin`.
- Protección de rutas privadas y rutas administrativas.

### Carrito
- Añadir productos (también antes de iniciar sesión).
- Consultar productos añadidos.
- Cambiar cantidades (mínimo 1).
- Eliminar productos y vaciar el carrito.
- Calcular subtotal.
- Validar que no se supere el stock disponible.
- Mantener el carrito mientras el usuario navega.
- Tras iniciar sesión, el carrito anónimo se asocia al usuario autenticado.

### Pedidos simulados
- Confirmar un pedido sin realizar un pago real.
- Asociar el pedido al usuario autenticado.
- Guardar productos, cantidades, precios y total.
- Volver a validar stock en el backend antes de crear el pedido.
- Reducir el stock al crear el pedido.
- Vaciar el carrito al crear correctamente el pedido.
- Mostrar pantalla de confirmación.
- Generar identificador o número de pedido.
- Estado inicial sencillo: `pending` o `confirmed`.

### Historial de pedidos
- Listar los pedidos del usuario autenticado.
- Ver el detalle de un pedido (fecha, productos, cantidades, precios, total, estado).
- Mostrar estado vacío cuando el usuario no tenga pedidos.

### Panel de administración
- Acceso exclusivo para usuarios con rol `admin`.
- Listar productos.
- Crear productos.
- Editar productos.
- Desactivar productos.
- Actualizar stock.

### UX y calidad visual
- Diseño responsive y vista móvil usable.
- Estados de carga, vacío, error, éxito, hover y focus.
- Validación de formularios.
- Navegación clara y componentes reutilizables.
- CSS puro organizado por componente o dominio.
- HTML semántico y accesibilidad básica.

## Funcionalidades fuera del MVP

- Pagos reales, Stripe, PayPal, tarjetas bancarias.
- Envíos reales, cálculo de gastos de envío, seguimiento de paquetes.
- Integración con proveedores, impuestos o facturación real.
- Emails transaccionales, recuperación de contraseña, verificación de email.
- Compra como invitado, direcciones guardadas.
- Variantes complejas de producto, favoritos, valoraciones y reseñas.
- Cupones, descuentos, devoluciones y reembolsos.
- Gestión avanzada de categorías, dashboard avanzado de ventas, analítica.
- Recomendaciones, IA, chatbot, integración con n8n, notificaciones push.
- Multiidioma, multi-tenant, aplicación móvil nativa, tiempo real, microservicios.

## Criterios de aceptación

### Cliente
- Puede ver el catálogo.
- Puede buscar productos.
- Puede abrir el detalle de un producto.
- Puede añadir productos con stock al carrito (antes y después de iniciar sesión).
- Puede cambiar cantidades.
- Puede eliminar productos.
- Puede registrarse.
- Puede iniciar sesión.
- Puede crear un pedido simulado.
- Puede ver la confirmación.
- Puede consultar sus pedidos.

### Administrador
- Puede iniciar sesión como admin.
- Puede crear productos.
- Puede editar productos.
- Puede desactivar productos.
- Puede actualizar stock.
- Un cliente no puede acceder al panel admin.

### Calidad
- Funciona en escritorio.
- Funciona en móvil.
- Hay estados de carga.
- Hay estados vacíos.
- Hay mensajes de error comprensibles.
- Las contraseñas no se guardan en texto plano.
- No hay secretos en el repositorio.
- El README explica cómo ejecutar el proyecto.
- El flujo principal se puede demostrar sin intervención manual en la base de datos.

## Decisiones pendientes registradas

- Estructura exacta del modelo Cart (pendiente de definir antes de implementar).
- Estado inicial del pedido (`pending` o `confirmed`).
- Desactivar productos frente a permitir también su eliminación en el panel.

## Reglas de negocio del MVP

- Solo se pueden mostrar productos activos en el catálogo.
- No se puede añadir una cantidad menor que uno.
- No se puede superar el stock disponible.
- No se puede crear un pedido con el carrito vacío.
- Solo un usuario autenticado puede crear un pedido.
- El stock se vuelve a validar en el backend.
- El pedido guarda el precio que existía en el momento de crearlo.
- Solo un administrador puede modificar productos.
- Un usuario solo puede ver sus propios pedidos.
- Un pedido creado correctamente reduce el stock.
- Si la creación del pedido falla, el carrito no debe perderse.