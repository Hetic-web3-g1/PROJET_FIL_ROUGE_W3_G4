import React from "react";
import "./index.css";

// React Router
import ReactDOM from "react-dom/client";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

//Pages
import App from "./App";
import Home from "./pages/home/Home";
import Masterclass from "./pages/masterclass/Masterclass";
import Login from "./pages/login/Login";
import ErrorPage from "./pages/errorPage";
import ResetPasswordEmail from "./pages/auth/reset/ResetPasswordEmail";
import ResetPassword from "./pages/auth/reset/ResetPassword";
import Profile from "./pages/profile/profile";


//Store
import { Provider } from 'react-redux'

import configureStore from './features/store/store';

import { persistStore } from 'redux-persist';
import { PersistGate } from 'redux-persist/integration/react';

//i18n
import i18n from './i18n';
import { I18nextProvider } from 'react-i18next';

const store = configureStore;
let persistor = persistStore(store);

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/Home",
    element: <Home />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/Login",
    element: <Login />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/reset-password",
    element: <ResetPasswordEmail />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/reset-password/:token",
    element: <ResetPassword />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/Masterclass/:id",
    element: <Masterclass />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/Profile",
    element: <Profile />,
    errorElement: <ErrorPage />,
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Provider store={store}>
      <PersistGate persistor={persistor}>
        <I18nextProvider i18n={i18n} defaultNS={'translation'}>
          <RouterProvider router={router} />
        </I18nextProvider>
      </PersistGate>
    </Provider>
  </React.StrictMode>
);
