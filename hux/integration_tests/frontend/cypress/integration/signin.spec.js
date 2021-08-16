import route from "../support/routes.js";

const selector = {
  home: {
    signin: "[data-e2e='signin']",
  },
  login: {
    email: "[id=okta-signin-username]",
    password: "[id=okta-signin-password]",
    submit: "[id=okta-signin-submit]",
  }
}

describe("Tests user sign in", () => {
  before(() => {
    // opens the app
    cy.visit(route.home);

    // clicks the signin button
    cy.get(selector.home.signin).click();

    // we should now be on the login page
    cy.location("pathname").should("eq", route.login);

    // fill in the form
    cy.get(selector.login.email)
      .type(Cypress.env("USER_EMAIL"), { log: false });

    cy.get(selector.login.password)
      .type(Cypress.env("USER_PASSWORD"), { log: false });

    // submit the form
    cy.get(selector.login.submit).click();

    // TODO: add MFA related authentication if needed

    // we should no longer be on the login page
    cy.location("pathname", { timeout: 10000 })
      .should("not.eq", route.login)
      .then(() => {
        // okta does its authentication... 
        // once its done, we should be redirected back to the app
        cy.location("pathname")
          .should("eq", route.oktaSignInRedirectURI);
      })
  });

  it("should be able to view the overview", () => {
    cy.location("pathname").should("eq", route.overview);
  });
});
