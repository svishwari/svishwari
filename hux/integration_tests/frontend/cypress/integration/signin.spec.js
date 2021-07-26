import ROUTES from "../support/routes.js";

describe("Tests user sign in", () => {
  before(() => {
    // visit the application
    cy.visit(ROUTES.index);
    cy.get("button").click();

    cy.location("pathname")
      .should("not.eq", ROUTES.index)
      .then((pathname) => {
        if (pathname === "/login/callback") {
          // User has authenticated with okta successfully, so it redirects to
          // this URI and we can just continue on to our test cases...
        } else {
          cy.get("input[id=okta-signin-username]")
          .type(Cypress.env("USER_EMAIL"), { log: false });

          cy.get("input[id=okta-signin-password]")
            .type(Cypress.env("USER_PASSWORD"), { log: false });

          cy.get("input[id=okta-signin-submit]").click();

          // TODO: add MFA related authentication if needed
        }
      });
  });

  it("should be able to view overview page", () => {
    cy.location("pathname").should("eq", ROUTES.overview);
  });
});
