import ROUTES from "../support/routes.js";

describe("Tests user sign in", () => {
  before(() => {
    // visit the application sign-on page
    cy.visit(ROUTES.index);
    cy.get("button").click();

    cy.location("pathname")
      .should("not.eq", ROUTES.index)
      .then((pathname) => {
        // redirects to sign-on (Okta)
        if (pathname !== "/auth") {
          cy.get("input[id=okta-signin-username]").type(
            Cypress.env("USER_EMAIL")
          );

          cy.get("input[id=okta-signin-password]").type(
            Cypress.env("USER_PASSWORD")
          );
          cy.get("input[id=okta-signin-submit]").click();

          //TODO: MFA related authentication
        }
      });
  });

  it("should be able to view overview page", () => {
    //TODO: need to find an alternate solution to wait
    cy.wait(10000);
    cy.location("pathname").should("eq", ROUTES.overview);
  });
});
