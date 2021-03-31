const getenv = (name) => process.env[name];

const oktaAuthConfig = {
  // Note: If your app is configured to use the Implicit Flow
  // instead of the Authorization Code with Proof of Code Key Exchange (PKCE)
  // you will need to add pkce: false
  issuer: `${getenv("REACT_APP_OKTA_ISSUER")}/oauth2/default`,
  clientId: getenv("REACT_APP_OKTA_CLIENT_ID"),
  redirectUri: `${window.location.origin}/login/callback`,
};

const oktaSignInConfig = {
  baseUrl: getenv("REACT_APP_OKTA_ISSUER"),
  clientId: getenv("REACT_APP_OKTA_CLIENT_ID"),
  redirectUri: `${window.location.origin}/login/callback`,
  authParams: {
    // If your app is configured to use the Implicit Flow
    // instead of the Authorization Code with Proof of Code Key Exchange (PKCE)
    // you will need to uncomment the below line
    pkce: false,
  },
};

export { oktaAuthConfig, oktaSignInConfig };
