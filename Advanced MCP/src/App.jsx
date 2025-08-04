import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import {StytchLogin, IdentityProvider, useStytchUser} from "@stytch/react";

function App() {
    const {user} = useStytchUser();

    const config = {
    products: ["passwords"],
    otpOptions: {
      methods: [],
      expirationMinutes: 5
    },
    passwordOptions: {
      loginRedirectURL: "http://localhost:5173/login",
      resetPasswordRedirectURL: "http://localhost:5173/reset-password"
    }
  };

  return (
    <div>
        {!user ? <StytchLogin config={config}/> : <IdentityProvider />}
    </div>
  )
}

export default App
