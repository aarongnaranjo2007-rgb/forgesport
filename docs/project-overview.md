---
title: ForgeSport — Visión general del proyecto
---
# ForgeSport — Visión general del proyecto

## Propósito

ForgeSport es un e-commerce ficticio de material deportivo para gimnasio y vóley. Es un proyecto personal de aprendizaje y portfolio, no un proyecto de clase ni una tienda activa. El objetivo es construir una aplicación full-stack completa con un alcance que pueda terminarse.

## Usuarios

- **Visitante**: puede explorar el catálogo, buscar productos y ver el detalle sin iniciar sesión.
- **Cliente autenticado**: puede registrarse, iniciar sesión, añadir productos al carrito (también antes de iniciar sesión), crear pedidos simulados y consultar su historial de pedidos.
- **Administrador**: puede gestionar el catálogo y el stock (crear, editar, desactivar productos y actualizar inventario).

## Restricciones principales

- No se venden productos reales durante el MVP. Los productos, precios, imágenes y pedidos son datos de demostración.
- No hay pagos reales, ni Stripe, ni PayPal, ni tarjetas bancarias.
- No hay envíos reales, ni cálculo de gastos de envío, ni seguimiento de paquetes.
- No hay emails transaccionales, ni recuperación de contraseña, ni verificación de email.
- No hay compra como invitado, ni direcciones guardadas, ni variantes complejas de producto.
- No hay favoritos, reseñas, cupones, descuentos, devoluciones ni reembolsos.
- No hay dashboard avanzado de ventas, ni analítica, ni recomendaciones, ni IA, ni chatbot.
- No hay integración con n8n, ni notificaciones push, ni multiidioma, ni multi-tenant, ni aplicación móvil nativa.
- No hay tiempo real, ni microservicios.

## Stack tecnológico

- **Frontend**: React, Vite, JavaScript/JSX, CSS puro (sin Tailwind), React Router, Context API o solución sencilla para carrito y sesión.
- **Backend**: Node.js, Express, API REST, middleware de autenticación y autorización por rol, validación de entradas, manejo centralizado de errores.
- **Base de datos**: MongoDB (Mongoose opcional).
- **Autenticación**: JWT, preferiblemente en cookies HTTP-only.
- **Roles**: `customer` y `admin`.

## Decisiones cerradas

- El carrito funciona antes del inicio de sesión (sesión anónima). Tras hacer login, el carrito se asocia al usuario autenticado.
- El repositorio es público para el portfolio, pero no se añade una licencia open source por ahora.
- El estilo es CSS puro con diseño mobile-first, variables CSS, Grid y Flexbox.

## Alcance del MVP

Ver `docs/scope.md`.

## Criterios de cierre del MVP

El MVP estará terminado cuando se cumplan los criterios de aceptación definidos en `docs/scope.md` para cliente, administrador y calidad.