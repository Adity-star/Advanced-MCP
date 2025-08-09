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
      loginRedirectURL: "https://www.stytch.com/login",
      resetPasswordRedirectURL: "https://www.stytch.com/reset-password"
    }
  };

  return (
    <div>
        {!user ? <StytchLogin config={config}/> : <IdentityProvider mcp_api_url="http://127.0.0.1:8000" />}
    </div>
  )
}

export default App
