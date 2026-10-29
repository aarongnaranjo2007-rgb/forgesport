---
title: ForgeSport — Estrategia del carrito
---
# ForgeSport — Estrategia del carrito

## Comportamiento antes del login

El carrito está disponible para cualquier visitante, incluso sin iniciar sesión. Un usuario anónimo puede:

- Añadir productos al carrito desde el detalle del producto.
- Ver los productos añadidos.
- Cambiar cantidades.
- Eliminar productos.
- Vaciar el carrito.
- Ver el subtotal calculado.

El carrito anónimo se guarda en **cookies** del navegador, de forma que persiste mientras el usuario navega por la aplicación.

## Comportamiento tras el login

Cuando el usuario inicia sesión, el carrito anónimo se **fusiona** con el carrito previo del usuario autenticado (si existe).

Reglas de fusión:

- Si un producto ya estaba en el carrito del usuario, se suma la cantidad del carrito anónimo a la existente.
- Si un producto no estaba en el carrito del usuario, se añade como nuevo item.
- Después de fusionar, se valida que ninguna cantidad supere el stock disponible.
- El carrito resultante queda asociado al usuario autenticado.

## Estructura del carrito

```json
{
  "cartId": "uuid-o-id",
  "userId": "id-del-usuario-o-null-si-anónimo",
  "items": [
    {
      "productId": "id-del-producto",
      "nameSnapshot": "Nombre del producto",
      "priceSnapshot": 19.99,
      "quantity": 2
    }
  ],
  "subtotal": 39.98,
  "createdAt": "fecha",
  "updatedAt": "fecha"
}
```

- `productId`: referencia al producto en la base de datos.
- `nameSnapshot` y `priceSnapshot`: copia del nombre y precio en el momento de añadir, para que el carrito no cambie si el producto se edita después.
- `quantity`: cantidad de unidades.
- `subtotal`: calculado dinámicamente (suma de precio × cantidad).
- `userId`: `null` si es anónimo, id del usuario tras el login.

## Validación de stock

- **Frontend**: valida al añadir y al modificar cantidad que no se supere el stock disponible, mostrando mensajes claros al usuario.
- **Backend**: vuelve a validar siempre antes de crear el pedido y también al añadir/modificar si el carrito se guarda en backend.
- **Prioridad**: el backend es la fuente de verdad; el frontend solo ofrece una validación rápida para mejorar la UX.

## Reglas de negocio del carrito

- No se puede añadir una cantidad menor que 1.
- No se puede superar el stock disponible.
- El carrito puede estar vacío, pero no se puede crear un pedido con él vacío.
- Si la creación del pedido falla, el carrito no debe perderse.