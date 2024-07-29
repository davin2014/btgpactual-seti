# BTG Pactual

BTG Pactual es una aplicación web que permite a los usuarios gestionar sus suscripciones a fondos, ver el historial de transacciones y más.

## Descripción

Esta aplicación está construida con React y utiliza React Router para la navegación. Incluye componentes como un `Header`, `Sidebar`, y `Navbar` para una mejor experiencia de usuario.

## Instalación

Sigue estos pasos para instalar y configurar el proyecto en tu entorno local:

1. Clona el repositorio:
    ```bash
    git clone https://github.com/tu-usuario/btg-pactual.git
    ```

2. Navega al directorio del proyecto:
    ```bash
    cd btg-pactual
    ```

3. Instala las dependencias:
    ```bash
    npm install
    ```

4. Inicia la aplicación:
    ```bash
    npm start
    ```

La aplicación estará disponible en `http://localhost:3000`.

## Uso

Una vez que la aplicación esté en funcionamiento, puedes navegar a través de las diferentes secciones utilizando la barra de navegación o el sidebar.

- **Inicio**: Página principal de la aplicación.
- **Clientes**: Gestión de clientes.
- **Suscribirse a un fondo**: Página para suscribirse a un fondo.
- **Cancelar suscripción**: Página para cancelar una suscripción.
- **Historial de transacciones**: Página para ver el historial de transacciones.

## Estructura del Proyecto

```plaintext
btg-pactual/
├── public/
│   ├── index.html
│   └── ...
├── src/
│   ├── assets/
│   │   └── css/
│   │       └── Navbar.css
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   └── ...
│   ├── App.tsx
│   ├── index.tsx
│   └── ...
├── package.json
└── README.md

# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type aware lint rules:

- Configure the top-level `parserOptions` property like this:

```js
export default {
  // other rules...
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    project: ['./tsconfig.json', './tsconfig.node.json', './tsconfig.app.json'],
    tsconfigRootDir: __dirname,
  },
}
```

- Replace `plugin:@typescript-eslint/recommended` to `plugin:@typescript-eslint/recommended-type-checked` or `plugin:@typescript-eslint/strict-type-checked`
- Optionally add `plugin:@typescript-eslint/stylistic-type-checked`
- Install [eslint-plugin-react](https://github.com/jsx-eslint/eslint-plugin-react) and add `plugin:react/recommended` & `plugin:react/jsx-runtime` to the `extends` list
